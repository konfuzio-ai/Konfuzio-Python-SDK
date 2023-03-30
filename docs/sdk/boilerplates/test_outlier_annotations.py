"""Test searching for the outlier Annotations under a given Label."""
from konfuzio_sdk.data import Project
from konfuzio_sdk.evaluate import ExtractionEvaluation
from konfuzio_sdk.tokenizer.base import ListTokenizer
from konfuzio_sdk.tokenizer.regex import RegexTokenizer
from konfuzio_sdk.trainer.information_extraction import RFExtractionAI
from variables import YOUR_PROJECT_ID

YOUR_LABEL_NAME = 'Austellungsdatum'

project = Project(id_=YOUR_PROJECT_ID)
label = project.get_label_by_name('Bank inkl. IBAN')
outliers = label.get_probable_outliers_by_regex(project.categories)
outliers = label.get_probable_outliers_by_regex(project.categories, top_worst_percentage=1.0)
outlier_spans = [span.offset_string for annotation in outliers for span in annotation.spans]
assert len(outliers) == 16
assert 'Deutsche Bank PGK  Nürnbe' in outlier_spans
assert 'DE73 7607 0024 0568 9745 11' in outlier_spans
label = project.get_label_by_name(YOUR_LABEL_NAME)
pipeline = RFExtractionAI()
pipeline.tokenizer = ListTokenizer(tokenizers=[])
pipeline.category = label.project.get_category_by_id(id_=63)
train_doc_ids = {44823, 44834, 44839, 44840, 44841}
pipeline.documents = [doc for doc in pipeline.category.documents() if doc.id_ in train_doc_ids]
for cur_label in pipeline.category.labels:
    for regex in cur_label.find_regex(category=pipeline.category):
        pipeline.tokenizer.tokenizers.append(RegexTokenizer(regex=regex))
pipeline.test_documents = pipeline.category.test_documents()
pipeline.df_train, pipeline.label_feature_list = pipeline.feature_function(
    documents=pipeline.documents, require_revised_annotations=False
)
pipeline.fit()
predictions = []
for doc in pipeline.documents:
    predicted_doc = pipeline.extract(document=doc)
    predictions.append(predicted_doc)
evaluation = ExtractionEvaluation(documents=list(zip(pipeline.documents, predictions)), strict=False)
outliers = label.get_probable_outliers_by_confidence(evaluation, 0.8)
assert len(outliers) == 1
outliers = label.get_probable_outliers_by_confidence(evaluation)
outlier_spans = [span.offset_string for annotation in outliers for span in annotation.spans]
assert '24.05.2018' in outlier_spans
outliers = label.get_probable_outliers_by_confidence()
assert len(outliers) == 3
for annotation in outliers:
    assert annotation.confidence < 0.5
    assert annotation.is_correct
outliers = label.get_probable_outliers_by_normalization(project.categories)
outlier_spans = [span.offset_string for annotation in outliers for span in annotation.spans]
assert len(outliers) == 1
assert '328927/10103' in outlier_spans
assert '22.05.2018' in outlier_spans
outliers = label.get_probable_outliers(project.categories, confidence_search=False)
outlier_spans = [span.offset_string for annotation in outliers for span in annotation.spans]
assert len(outliers) == 1
assert '328927/10103' in outlier_spans
assert '22.05.2018' in outlier_spans