## Data Layer Concepts 

The relations between all major Data Layer concepts of the SDK are 
the following: a [Project](#id1) consists of multiple [Documents](#document). Each one of the Documents consists of 
the [Pages](#page) and belongs to a certain [Category](#category). Text in a Document can be marked by 
[Annotations](#annotation), which can be multi-line, and where each continuous piece of text contained into an 
Annotation is a [Span](#span). Each Annotation is located within a certain [Bbox](#id14) and is defined by a 
[Label](#id11) that is a part of one of the [Label Sets](#label-set). An [Annotation Set](#id9) is a list of Annotations
that share a Label Set. 

For more detailed information on each concept, follow the link on the concept's name which leads to the automatically 
generated documentation.

### Project
[Project](sourcecode.html#project) is essentially a dataset that contains Documents 
belonging to different Categories or not having any Category assigned. To initialize it, call `Project(id_=YOUR_PROJECT_ID)`. 

The Project can also be accessed via the Smartview, with URL typically looking like 
https://YOUR_HOST/admin/server/document/?project=YOUR_PROJECT_ID.

If you have made some local changes to the Project and want to return to the initial version available at the server, or 
if you want to fetch the updates from the server, use the argument `update=True`.

Here are the some of properties and methods of the Project you might need when working with the SDK:
- `project.documents` – training Documents within the Project;
- `project.test_documents` – test Documents within the Project;
- `project.get_category_by_id(YOUR_CATEGORY_ID).documents()` – Documents filtered by a Category of your choice; 
- `project.get_document_by_id(YOUR_DOCUMENT_ID)` – access a particular Document from the Project if you know its ID.

### Document
[Document](sourcecode.html#document) is one of the files that constitute a Project. It 
consists of Pages and can belong to a certain Category. 

A Document can be accessed by `project.get_document_by_id(YOUR_DOCUMENT_ID)` when its ID is known to you; otherwise, it 
is possible to iterate through the output of `project.documents` (or `test_documents`/`_documents`) to see which 
Documents are available and what IDs they have.

The Documents can also be accessed via the Smartview, with URL typically looking like 
https://YOUR_HOST/projects/PROJECT_ID/docs/DOCUMENT_ID/bbox-annotations/.

Here are some of the properties and methods of the Document you might need when working with the SDK:
- `document.id_` – get an ID of the Document;
- `document.text` – get a full text of the Document;
- `document.pages()` – a list of Pages in the Document;
- `document.update()` – download a newer version of the Document from the Server in case you have made some changes in 
the Smartview;
- `document.category()` – get a Category the Document belongs to;
- `document.get_images()` – download PNG images of the Pages in the Document; can be used if you wish to use the visual 
data for training your own models, for example;

### Category
[Category](sourcecode.html#category) is a group of Documents united by common feature or type, i.e. invoice or receipt.

To see all Categories in the Project, you can use `project.get_categories()`. 
To find a Category the Document belongs to, you can use `document.category`.
To get `documents` or `test_documents` under the Category, use `category.documents()` or `category.test_documents()` respectively.

You can also observe all Categories available in the Project via the Smartview: they are listed on the Project's page in the menu on the right.

### Page
[Page](sourcecode.html#page) is a constituent part of the Document. Here are some of the properties and methods of the Page you might need when working with the SDK:
- `page.text` – get text of the Page;
- `page.spans()` – get a list of Spans on the Page;
- `page.number` – get Page's number, starting from 1.

### Span
[Span](sourcecode.html#span) is a part of the Document's text without the line breaks. Each Span has `start_offset` and `end_offset` denoting its starting and finishing characters in `document.text`. 

To access Span's text, you can call `span.offset_string`. We are going to use it later when collecting the Spans from the Documents.

### Annotation 
[Annotation](sourcecode.html#annotation) is a combination of Spans that has a certain Label  (i.e. Issue_Date, Auszahlungsbetrag) assigned to it. They typically denote a certain type of entity that is found in the text. Annotations can be predicted by AI or human-added. 

Like Spans, Annotations also have `start_offset` and `end_offset` denoting the starting and the ending characters. To access the text under the Annotation, call `annotation.offset_string`.

To see the Annotation in the Smartview, you can call `annotation.get_link()` and open the returned URL. 

### Annotation Set
[Annotation Set](sourcecode.html#annotation-set) is a group of Annotations united by Labels 
belonging to the same Label Set. To see Annotations in the set, call `annotation_set.annotations()`.

### Label
[Label](sourcecode.html#label) defines what the Annotation is about (i.e. Issue_Date, 
Auszahlungsbetrag). Labels are grouped into Label Sets. To see Annotations with a current Label, 
call `label.annotations()` .

### Label Set
[Label Set](sourcecode.html#label-set) is a group of Labels united. A Label Set can belong 
to different Categories and multiple Annotation Sets.

### Bbox
[Bbox](sourcecode.html#bbox) is an area of the Page denoted by four rectangle-like 
coordinates. You can access Bboxes of the Document by calling `document.bboxes`.