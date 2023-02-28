.. meta::
   :description: Documentation of the coordinates system of the bounding boxes used in Konfuzio and some simple 
examples of how to use it for visualization, for example.

## Coordinates System

The size of a page of a Document can be obtained in the Document object.
The format is [width, height].

Original size of the Document is the size of the uploaded Document (which can be a PDF file or an image). The bounding 
boxes of the Annotations are based on this size.
   E.g.: [1552, 1932]
   

Current size can be accessed via calling `height` and `width` from the Page object. They show the dimensions of the 
image representation of a Document Page. These representations are used for computer vision tasks and the SmartView.
   E.g.: [372.48, 463.68]

.. literalinclude:: /sdk/boilerplates/test_coordinates_system.py
   :language: python
   :lines: 2,5-13

The coordinates system used has its start in the bottom left corner of the page.

![coordinates_system](../_static/img/coordinates_schema.png)


To visualize the character bounding boxes of a document and overlapping them in the image opened with the python
library PIL, for example, we can resize the image to the size in which they are based (original_size).
The following code can be used for this:

.. literalinclude:: /sdk/boilerplates/test_visualize_bboxes.py
   :language: python
   :lines: 2-6,8-21,24-29,31-42

![characters_bboxes](../_static/img/bboxes_characters.png)

The coordinates obtained from the segmentation endpoint of the API are based on the image array shape.
To visualize the segmentation bounding boxes of a page on an image opened with the python library PIL, for example,
we can overlap them directly.

.. literalinclude:: /sdk/boilerplates/test_segmentation.py
   :language: python
   :lines: 2-7,9-27

![segmentation_bboxes](../_static/img/bboxes_segmentation.png)

To visualize both at the same time we can convert the coordinates from the segmentation result to be based on the image
size used for the characters' bbox.

.. literalinclude:: /sdk/boilerplates/test_segmentation_and_bboxes.py
   :language: python
   :lines: 2-7,9-23,26-33,35-49

![characters_and_segmentation_bboxes](../_static/img/bboxes_overlap.png)
