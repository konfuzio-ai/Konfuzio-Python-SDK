"""Test Splitting AI and the models' training, saving and prediction."""
import os
import pathlib
import pytest
import unittest

from copy import deepcopy

from konfuzio_sdk.data import Category, Document, Project
from konfuzio_sdk.samples import LocalTextProject
from konfuzio_sdk.tokenizer.regex import ConnectedTextTokenizer
from konfuzio_sdk.trainer.file_splitting import (
    ContextAwareFileSplittingModel,
    SplittingAI,
    MultimodalFileSplittingModel,
)

from konfuzio_sdk.trainer.document_categorization import FallbackCategorizationModel
from konfuzio_sdk.trainer.information_extraction import load_model


class TestContextAwareFileSplittingModel(unittest.TestCase):
    """Test Context Aware File Splitting Model."""

    @classmethod
    def setUpClass(cls) -> None:
        """Initialize the tested class."""
        cls.project = LocalTextProject()
        cls.file_splitting_model = ContextAwareFileSplittingModel(
            categories=[cls.project.get_category_by_id(3), cls.project.get_category_by_id(4)],
            tokenizer=ConnectedTextTokenizer(),
        )
        cls.file_splitting_model.test_documents = cls.file_splitting_model.test_documents[:-2]
        cls.test_document = cls.project.get_document_by_id(9)

    def test_fit_context_aware_splitting_model(self):
        """Test pseudotraining of the Context Aware File Splitting Model."""
        self.file_splitting_model.fit(allow_empty_categories=True)
        non_first_page_spans = {}
        for category in self.file_splitting_model.categories:
            cur_non_first_page_spans = []
            for doc in category.documents():
                for page in doc.pages():
                    if page.number > 1:
                        cur_non_first_page_spans.append({span.offset_string for span in page.spans()})
            if not cur_non_first_page_spans:
                cur_non_first_page_spans.append(set())
            true_non_first_page_spans = set.intersection(*cur_non_first_page_spans)
            non_first_page_spans[category.id_] = true_non_first_page_spans
        for category in self.file_splitting_model.categories:
            cur_exclusive_first_page_strings = category.exclusive_first_page_strings(tokenizer=ConnectedTextTokenizer())
            for span in cur_exclusive_first_page_strings:
                assert span not in non_first_page_spans[category.id_]

    def test_init_file_splitting_model_empty_list(self):
        """Test running Context Aware File Splitting Model with an empty Categories list."""
        with pytest.raises(ValueError, match="an empty list"):
            ContextAwareFileSplittingModel(categories=[], tokenizer=ConnectedTextTokenizer())

    def test_init_file_splitting_model_not_a_category(self):
        """Test passing a list with an element that is not a Category as an input."""
        with pytest.raises(ValueError, match="have to be Categories"):
            ContextAwareFileSplittingModel(
                categories=[self.project.get_category_by_id(3), ""], tokenizer=ConnectedTextTokenizer()
            )

    def test_init_file_splitting_model_category_no_documents(self):
        """Test passing a Category that does not have Documents."""
        _ = Category(project=self.project, id_=5, name="CategoryName 5")
        with pytest.raises(ValueError, match="does not have Documents"):
            ContextAwareFileSplittingModel(categories=[_], tokenizer=ConnectedTextTokenizer())

    def test_init_file_splitting_model_category_no_test_documents(self):
        """Test passing a Category that does not have test Documents."""
        _ = Category(project=self.project, id_=6, name="CategoryName 6")
        Document(project=self.project, category=_, text="Hi all, I like fish.", dataset_status=2)
        with pytest.raises(ValueError, match="does not have test Documents"):
            ContextAwareFileSplittingModel(categories=[_], tokenizer=ConnectedTextTokenizer())

    def test_load_incompatible_model(self):
        """Test initializing a model that does not pass has_compatible_interface check."""
        wrong_class = FallbackCategorizationModel(LocalTextProject())
        assert not self.file_splitting_model.has_compatible_interface(wrong_class)

    def test_load_model_from_different_class(self):
        """Test initializing Splitting AI with a model that does not inherit from AbstractFileSplittingModel class."""
        wrong_class = FallbackCategorizationModel(LocalTextProject())
        with pytest.raises(ValueError, match="model is not inheriting from AbstractFileSplittingModel"):
            SplittingAI(model=wrong_class)

    def test_predict_context_aware_splitting_model(self):
        """Test correct first Page prediction."""
        test_document = self.file_splitting_model.tokenizer.tokenize(
            deepcopy(self.project.get_category_by_id(3).test_documents()[0])
        )
        # deepcopying because we do not want changes in an original test Document.
        # typically this happens in one of the private methods, but since here we pass a Document Page by Page, we
        # need to tokenize it explicitly (compared to when we pass a full Document to the Splitting AI).
        for page in test_document.pages():
            page.is_first_page = False
            for category in self.file_splitting_model.categories:
                cur_first_page_strings = category.exclusive_first_page_strings(
                    tokenizer=self.file_splitting_model.tokenizer
                )
                intersection = {span.offset_string.strip('\f').strip('\n') for span in page.spans()}.intersection(
                    cur_first_page_strings
                )
                if len(intersection) > 0:
                    page.is_first_page = True
                    break
            if page.number == 1:
                assert intersection == {'I like bread.'}
                assert page.is_first_page
            if page.number in (2, 4):
                assert intersection == set()
            if page.number in (3, 5):
                assert intersection == {'Morning,'}
                assert page.is_first_page

    def test_predict_with_empty_categories(self):
        """Test predicting with all empty Categories."""
        model = ContextAwareFileSplittingModel(
            categories=[self.project.get_category_by_id(2)], tokenizer=self.file_splitting_model.tokenizer
        )
        model.fit(allow_empty_categories=True)
        with pytest.raises(ValueError, match="Cannot run prediction as none of the Categories in"):
            model.predict(self.test_document.pages()[0])

    def test_pickle_model_save_load(self):
        """Test saving Context Aware File Splitting Model to a pickle."""
        self.file_splitting_model.output_dir = self.project.model_folder
        self.file_splitting_model.path = self.file_splitting_model.save(keep_documents=True, max_ram='5MB')
        assert os.path.isfile(self.file_splitting_model.path)
        model = load_model(self.file_splitting_model.path)
        for category_gt, category_load in zip(self.file_splitting_model.categories, model.categories):
            gt_exclusive_first_page_strings = category_gt.exclusive_first_page_strings(
                tokenizer=ConnectedTextTokenizer()
            )
            load_exclusive_first_page_strings = category_load.exclusive_first_page_strings(
                tokenizer=ConnectedTextTokenizer()
            )
            assert gt_exclusive_first_page_strings == load_exclusive_first_page_strings

    def test_pickle_model_save_lose_weight(self):
        """Test saving Context Aware File Splitting Model with reduce_weight."""
        self.file_splitting_model.output_dir = self.project.model_folder
        self.file_splitting_model.path = self.file_splitting_model.save(
            reduce_weight=True, keep_documents=True, max_ram='5MB'
        )
        assert os.path.isfile(self.file_splitting_model.path)
        model = load_model(self.file_splitting_model.path)
        for category_gt, category_load in zip(self.file_splitting_model.categories, model.categories):
            gt_exclusive_first_page_strings = category_gt.exclusive_first_page_strings(
                tokenizer=ConnectedTextTokenizer()
            )
            load_exclusive_first_page_strings = category_load.exclusive_first_page_strings(
                tokenizer=ConnectedTextTokenizer()
            )
            assert gt_exclusive_first_page_strings == load_exclusive_first_page_strings

    def test_splitting_ai_predict(self):
        """Test Splitting AI's Document-splitting method."""
        splitting_ai = SplittingAI(self.file_splitting_model)
        pred = splitting_ai.propose_split_documents(self.test_document, return_pages=False)
        assert len(pred) == 3

    def test_splitting_ai_predict_one_file_document(self):
        """Test Splitting AI's Document-splitting method on a single-file Document."""
        splitting_ai = SplittingAI(self.file_splitting_model)
        test_document = self.project.get_document_by_id(17)
        pred = splitting_ai.propose_split_documents(test_document)
        assert len(pred) == 1
        assert len(pred[0].pages()) == 2

    def test_splitting_ai_evaluate_full_on_training(self):
        """Test Splitting AI's evaluate_full on training Documents."""
        splitting_ai = SplittingAI(self.file_splitting_model)
        splitting_ai.evaluate_full(use_training_docs=True)
        assert splitting_ai.full_evaluation.tp() == 3
        assert splitting_ai.full_evaluation.fp() == 0
        assert splitting_ai.full_evaluation.fn() == 0
        assert splitting_ai.full_evaluation.tn() == 3
        assert splitting_ai.full_evaluation.precision() == 1.0
        assert splitting_ai.full_evaluation.recall() == 1.0
        assert splitting_ai.full_evaluation.f1() == 1.0

    def test_splitting_ai_evaluate_full_on_testing(self):
        """Test Splitting AI's evaluate_full on testing Documents."""
        splitting_ai = SplittingAI(self.file_splitting_model)
        splitting_ai.evaluate_full()
        assert splitting_ai.full_evaluation.tp() == 9
        assert splitting_ai.full_evaluation.fp() == 0
        assert splitting_ai.full_evaluation.fn() == 0
        assert splitting_ai.full_evaluation.tn() == 7
        assert splitting_ai.full_evaluation.precision() == 1.0
        assert splitting_ai.full_evaluation.recall() == 1.0
        assert splitting_ai.full_evaluation.f1() == 1.0

    def test_splitting_no_category_document(self):
        """Test running Splitting AI on a Document with Category == NO_CATEGORY."""
        splitting_ai = SplittingAI(self.file_splitting_model)
        test_document = self.project.get_document_by_id(19)
        assert test_document._category == self.project.no_category
        pred = splitting_ai.propose_split_documents(test_document, return_pages=False)
        assert len(pred) == 1
        assert pred[0].text == test_document.text

    def test_splitting_with_inplace(self):
        """Test Context Aware File Splitting Model's predict method with inplace=True."""
        splitting_ai = SplittingAI(self.file_splitting_model)
        test_document = self.file_splitting_model.tokenizer.tokenize(self.test_document)
        pred = splitting_ai.propose_split_documents(test_document, return_pages=True, inplace=True)[0]
        for page in pred.pages():
            if page.number in (1, 3, 5):
                assert page.is_first_page
            else:
                assert not page.is_first_page
            assert page.is_first_page_confidence == 1
        assert pred == test_document

    def test_suggest_first_pages(self):
        """Test Splitting AI's suggesting first Pages."""
        splitting_ai = SplittingAI(self.file_splitting_model)
        test_document = self.file_splitting_model.tokenizer.tokenize(deepcopy(self.test_document))
        pred = splitting_ai.propose_split_documents(test_document, return_pages=True)[0]
        for page in pred.pages():
            if page.number in (1, 3, 5):
                assert page.is_first_page
            else:
                assert not page.is_first_page
            assert page.is_first_page_confidence == 1
        pathlib.Path(self.file_splitting_model.path).unlink()


TEST_WITH_FULL_DATASET = False


class TestMultimodalFileSplittingModel(unittest.TestCase):
    """Test Multimodal File Splitting Model."""

    @classmethod
    def setUpClass(cls) -> None:
        """Initialize the tested class."""
        cls.project = Project(id_=46)
        cls.file_splitting_model = MultimodalFileSplittingModel(categories=cls.project.categories)
        if not TEST_WITH_FULL_DATASET:
            cls.file_splitting_model.documents = [
                document for category in cls.file_splitting_model.categories for document in category.documents()
            ][:10]
        cls.test_document = cls.file_splitting_model.test_documents[-1]

    def test_model_training(self):
        """Test model's fit() method."""
        self.file_splitting_model.fit()
        assert self.file_splitting_model.model

    def test_run_page_prediction(self):
        """Test model's prediction."""
        for doc in self.file_splitting_model.test_documents:
            for page in doc.pages():
                page.is_first_page = None
                page = self.file_splitting_model.predict(page)
                assert page.is_first_page
                assert page.is_first_page_confidence

    def test_run_splitting_ai_prediction(self):
        """Test Splitting AI integration with the Multimodal File Splitting Model."""
        splitting_ai = SplittingAI(self.file_splitting_model)
        pred = splitting_ai.propose_split_documents(self.test_document)
        assert len(pred) == 1
        for page in pred[0].pages():
            if page.number == 1:
                assert page.is_first_page
                assert page.is_first_page_confidence == 1
            else:
                assert not page.is_first_page
                assert page.is_first_page_confidence

    @pytest.mark.skip(reason="Takes too long to test upon pushing; skipping can be removed for local testing.")
    def test_save_load_model(self):
        """Test saving and loading pickle file of the model."""
        path = self.file_splitting_model.save()
        loaded = load_model(path)
        splitting_ai = SplittingAI(model=loaded)
        assert isinstance(splitting_ai.model, MultimodalFileSplittingModel)
        pathlib.Path(path).unlink()

    def test_splitting_ai_evaluate_full_on_training(self):
        """Test Splitting AI's evaluate_full on training Documents."""
        splitting_ai = SplittingAI(self.file_splitting_model)
        splitting_ai.evaluate_full(use_training_docs=True)
        if TEST_WITH_FULL_DATASET:
            assert splitting_ai.full_evaluation.tp() == 25
        else:
            assert splitting_ai.full_evaluation.tp() == 10
        assert splitting_ai.full_evaluation.fp() == 0
        assert splitting_ai.full_evaluation.fn() == 0
        assert splitting_ai.full_evaluation.tn() == 0
        assert splitting_ai.full_evaluation.precision() == 1.0
        assert splitting_ai.full_evaluation.recall() == 1.0
        assert splitting_ai.full_evaluation.f1() == 1.0

    def test_splitting_ai_evaluate_full_on_testing(self):
        """Test Splitting AI's evaluate_full on testing Documents."""
        splitting_ai = SplittingAI(self.file_splitting_model)
        splitting_ai.evaluate_full()
        print(splitting_ai.full_evaluation.evaluation_results)
        assert splitting_ai.full_evaluation.tp() == 3
        assert splitting_ai.full_evaluation.fp() == 0
        assert splitting_ai.full_evaluation.fn() == 0
        assert splitting_ai.full_evaluation.tn() == 0
        assert splitting_ai.full_evaluation.precision() == 1.0
        assert splitting_ai.full_evaluation.recall() == 1.0
        assert splitting_ai.full_evaluation.f1() == 1.0
