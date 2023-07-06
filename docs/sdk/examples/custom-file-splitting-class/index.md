### Create a custom File Splitting AI

This section explains how to train a custom File Splitting AI locally, how to save it and upload it to the Konfuzio 
Server. 

By default, any [File Splitting AI](sourcecode.html#file-splitting-ai) class should derive from the 
`AbstractFileSplittingModel` class and implement the following interface:

.. exec_code::

   from konfuzio_sdk.trainer.file_splitting import AbstractFileSplittingModel
   from konfuzio_sdk.data import Page, Category
   from typing import List

   class CustomFileSplittingModel(AbstractFileSplittingModel):
       def __init__(self, categories: List[Category], *args, **kwargs):
           super().__init__(categories)
           pass

       # initialize key variables required by the custom AI
       # for instance, self.categories to determine which Categories will be used for training the AI, self.documents
       # and self.test_documents to define training and testing Documents, self.tokenizer for a Tokenizer that will
       # be used in processing the Documents

       def fit(self):
           pass

       # Define architecture and training that the model undergoes, i.e. a NN architecture or a custom hardcoded logic
       # for instance, how it is done in ContextAwareFileSplittingModel:
       #
       # for category in self.categories:
       #     cur_first_page_strings = category.exclusive_first_page_strings(tokenizer=self.tokenizer)
       #
       # This method is allowed to be implemented as a no-op if you provide the trained model in other ways

       def predict(self, page: Page) -> Page:
           pass

       # Define how the model determines a split point for a Page, for instance, how it is implemented in
       # ContextAwareFileSplittingModel:
       #
       # for category in self.categories:
       #     cur_first_page_strings = category.exclusive_first_page_strings(tokenizer=self.tokenizer)
       #     intersection = {span.offset_string.strip('\f').strip('\n') for span in page.spans()}.intersection(
       #                 cur_first_page_strings
       #             )
       #     if len(intersection) > 0:
       #         page.is_first_page = True
       #         break
       #
       # **NB:** The classification needs to be run on the Page level, not the Document level – the result of
       # classification is reflected in `is_first_page` attribute value, which is unique to the Page class and is not
       # present in Document class. Pages with `is_first_page = True` become potential splitting points, thus, each new
       # sub-Document has a Page predicted as first as its starting point.

       def check_is_ready(self) -> bool:
           pass

       # define if all components needed for training/prediction are set, for instance, is self.tokenizer set or are
       # all Categories non-empty – containing training and testing Documents.

