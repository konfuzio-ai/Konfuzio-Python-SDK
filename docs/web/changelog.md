# CHANGELOG

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Calendar Versioning](https://calver.org/overview.html).

## 2021-05-26_20-16-02

### Added
- Show confidence for categorization results
- Show evaluation of Categorization Ai models
- Track version (number of retrainings) for all Ai models
- Track Project and Template origin of AiModel

## 2021-05-24_13-42-45

### Changed
- Use business evaluation implementation from training package
- Loading time for CSV export evaluation reduced by saving it in the database.

## 2021-05-18_16-37-25

### Added
- Global project switcher
- "Top candidates" filter in SmartView
- "Change dataset" functionality in SmartView
- Landing page in case the user has no projects (i.e. just registered)
- Language switcher (not enabled yet)
- Initial support for German translations (not enabled yet)

### Fixed
- Label threshold is now limited from 0.0 to 1.0

### Changed
- New design for login/signup/reset password pages
- Design improvements in the control panel and SmartView
- New logo and favicon
- API documentation has been improved with types and examples; is now based on OpenAPI 3
- Updated frontend dependencies and tooling

### Removed
- `admin_importer`, `copy_extraction_as_annotation` and related functions have been removed

## 2021-05-04_12-37-16

### Fixed
- Calculation of True Negative when using multiple templates.

## 2021-04-28_12-27-19

### Added
- Filter for top annotations in SmartView

### Changed
- Dont allow training if there are no training documents

## 2021-04-25_20-09-04

### Added
- Protect Signup with captcha

### Fixed
- Editing of annotation if there are already declined annotations.

## 2021-04-19_22-32-19

### Added 
- Add label creation Endpoint
- Token-based authentication for the API

## 2021-04-03_09-46-56

### Added 
- Show Django sidebar in Smartview and Template view.

### Changed
- Save extraction results in a more efficient way.
- Show a warning if an annotation with a custom offset string is created
- Shwo loading indicator in the smartview search

### Fixed
- Default template dropdown sometimes disabled when creating a Template
- Rare case where the document list could not be loaded

## 2021-03-15_15-12-04

### Added
- Add option to accept all annotations.

## 2021-03-07_21-32-41

### Added
- Option to retrain project categorization model
- Improved OCR settings
- System check page https://app.konfuzio.com/check/

### Fixed
- Typo in privacy policy
- Confirmation message when deleting labels
- Performance of csv export

### Changed
- Delete old unrevised annotations when rerunning AiModel.

## 2021-02-25_09-28-07

### Added
- Option to select tokenizer for training (ProjectAdmin)
- Option to add training parameters (SuperuserProjectAdmin)

### Changed
- Set a documents category_template on new documents if there is only one category_template available
- Improved delete / accept performance of annotations

### Fixed
- Count of annotations on the LabelAdmin

## 2021-02-15_18-56-51

### Changed
- Show category template as empty when actual empty (instead of displaying the first available template)
- Improved Smartview performance by changing entity loading

### Added
- Project name added to SectionLabel in the AiModelAdmin
- Assign user to documents ("Assignee"). Can be enabled in the ProjectSuperuserAdmin
- Add status field to the AiModel ("Training", "Failed", "Done")
- Dont allow new retraining if there is a training in progress AiModel.


## 2021-02-13_18-18-52

### Changed
- Use annotation permalink in LabelAdmin

### Fixed
- OCR Read API did not use text embeddings when available
- Files with misssing fonts could not be processed
- Creation of small annotations when accepting or declining

## 2021-02-10_13-52-15

### Added
- Admin action for Microsoft Graph API / Planner API

### Fixed
- SuperUserDocumentAdmin performance
- OutOfMemory errors in the categorization

## 2021-02-03_17-07-23

### Added
- Permalink for annotations
- Add an additional routine to fix corrupted pds
- Improved frontend error tracking

### Fixed
- Validation when edting an annotation

### Changed
- Renamed option 'priority_ocr' to 'priority_processing'
- Allow rerun extraction for documents with revised annotations
- Allow deletion default templates

## 2021-01-26_18-07-11

### Added
- Add column 'category' to csv export

## 2021-01-20_11-17-24

### Added
- Show selection bounding boxes for automtic created annotations

## 2021-01-14_22-06-52

### Added
- Visual annotations: images and area can now be annotate

### Fixed
- Loading time for Smartview

## 2021-01-13_23-26-03

### Fixed
- Retraining now assigns AIModels to templates even if they was no before

### Added
- Add Message when doing evaluation which tells the user if test set is empty.

## 2021-01-12_21-13-48

### Fixed
- Google Analytics integration
- Empty Textextraction for ParagraphExtractions

## 2021-01-10_18-36-49

### Fixed
- Disable link formatting by sendgrid.

## 2021-01-08_22-30-10

### Fixed
- Bbox calculation in ParagraphModel
- Evaluation sometimes not running
- Speedup annotation creating

## 2021-01-05_11-53-22

### Changed
- Two column Annotation selection is now possible

### Added
- ParagraphModel introduced in addition to the Extraction- & CategoryModels, this is set per project via the SuperUserDocumentAdmin.
- Option to update the document document text, this is set per project via the SuperUserDocumentAdmin.
- Document Segmentation API Endpoint

## 2020-12-22_19-04-04

### Changed
- Email Template are now managed within the application.
- Major improvement and refactor in the underlying training package.

### Fixed
- Link to imprint on SignUp
- Smartview when scrolling horizontally

## 2020-12-16_20-17-30

### Added
- Search for Smartview

### Fixed
- TemplateCreationForm does not allow to select parent Template

## 2020-12-16_09-44-30

### Added
- Searchbar for SuperuserProjectAdmin
- Add link to flower (task monitoring) for superusers
- Add support for GoogleTag Manager
- Create Support Ticket for Retraining and Invitation of new Users

### Changed
- Increase SoftTimeLimit for extraction (necessary for large documents >500 pages).

### Fixed
- Fix bbox generation fox Paragraph Annotations
- Fixed Evaluation not triggered for new AiModels

## 2020-12-10_13-15-14

### Added
- Sentry error reporting for Javascript Frontend (i.e. Smartview)
- Allow to add Project specific document CategorizationModel

### Changed
- Document Search now considers filenames and shows links to Dashhboard, Labeling and Smartview
- Allow deletion of Labels

### Fixed
- Allow "None" as confidence for rule-base ExtractionModels

## 2020-12-01_21-08-32

### Added
- Proof of Concept Microsoft Graph API connection (for logged in users): app.konfuzio.com/graph
- Button to upload demo Documents
- SuperuserProjectAdmin added (same like previous ProjectAdmin, however only accessible for Superusers only)
- Google Analytics Tag for app.konfuzio.com

### Changed
- Default permission Group "CanReadProject" replaced with "CanCreateReadUpdateProject". New users can now create new Projects.
- Project Page for "normal" user does not show technical fields like "ocr" and "text_layout" anymore.
- Dont show file endings like '.pkl' for AiModels

## 2020-11-26_19-43-14

### Fixed
- Missing bbox attribute in Document API (prevents retraining via training package)
- Running of proper ExtractionModel in Multi-Document-Template project
- Loading time for the Document page (still room for improvements)

### Added
- Slightly better Categorization model.

## 2020-11-20_20-05-47

### Added
- A public registration page: https://app.konfuzio.com/accounts/signup 
- A Internal registration page to create users manually and faster: https://app.konfuzio.com/register/ (you need to be logged in to see this page)
- Users can invite new users to a project via "ProjectInvitations"
- Password reset functionality

### Fixed
- The Smartview is much faster
- Improved creation of Templates and additional validation logic template inconsistencies.

### Changed
- Save bbox and entity per page in order to improve performance

## 2020-11-09_18-04-28

### Added
- Support for more than one default Template in a project
- Categorization for multi Template projects
- Links to related models in the Project, AIModel, Label and Template view
- Internal user registration form, app.konfuzio.com/register

### Changed
- AiModel belongs now to DefaultTemplates instead of project

## 2020-10-27_10-37-15

### Changed
- Documents are now soft-deleted. There is a hard delete option in the SuperuserDocumentAdmin.
- AiModel are made active automatically for matching DefaultTemplates if the AIMode is better than before.

## 2020-10-21_08-53-42

### Fixed
- Loading time when updating a project.

## 2020-10-19_22-46-49

### Changed
- Increase max allowed workflow time from 90 to 180 seconds.

### Fixed
- sucess messages for 'rerun_workflow' admin action
- loading time of AiModel
- csv export

### Added
- add hocr fied to document api.
- add a project option to hide the Smartview and Labeling tool.

## 2020-10-14_11-39-17

### Changed
- AIModel can be uploaded and evaluted before setting active for a project

## 2020-10-13_15-10-22

### Added
- Multilanguage Support (DE/EN) in the backend (actuall translation are not included yet)

### Changed
- 'create_labels_and_templates' is now a project option (false by default).
- Gunicorn workers restart after 500 requests.
- Flower dashboard is running in separated container now

### Fixed
- Fix upload_ai_model to upload files larger than 2GB
- Loading speed for SequenceAnnotation Admin

## 2020-10-03_15-18-47

### Fixed
- Recover tasks in case celery worker crashes

## 2020-10-01_12-02-37

### Fixed
- Internet Explorer warning badge
- 'Not machine-readable' was not detecting 0 as proper value for normalization.

### Changed
- Remove extraction count from AiModel admin.
- Refactor annotation accept/delete buttons to separate components and SVG

## 2020-09-16_18-19-53

### Added
- Additional normalization formats
- Sentry message if retraining is triggered.
- Detectron (fully imlemented) and preparation for visual classification results in SuperUserDocumetAdmin

### Changed 
- Dont raise sentry error if document got deleted during workflow 

### Fixed
- Creation of Templates
[- Calculation of width and height dimension when creating sandwich pdf and when using azure](https://gitlab.com/konfuzio/training/-/blob/master/src/konfuzio/image.py#L78)

## 2020-09-11_13-47-51

### Added
- Add sentry message if project retraining is triggered.
- Fix cpu minute calculation.

## 2020-09-09_16-12-44

### Added 
- [Forbid Removing Labels from Temapltes (which still have Annotations)](https://gitlab.com/konfuzio/objectives/-/issues/1629)

### Changed
- Allow extractions which does not have an accuracy. 
- On the dashboard: Dont show section.position column if all extractions have the same. Dont show accuracy column if all extraction does not have one.
- Dont show retraining webhook url (on the project detail page). Display is with **** like it is password.

## 2020-09-08_22-38-19

### Added
- Per-project measuring of cpu time.
- Additional date-formats for normalization.
- First draft of boolean-formats for normalization.

## 2020-09-08_09-17-00

### Added
- Document Filter added for 'human feedback required' and '100% machine readable.
- Additional normalization formats for numbers.
- [Document Categorization Classifier](https://gitlab.com/konfuzio/meta-clf) added to DocumentSuperUserAdmin

### Changed
- For the document view and Smartview, rename 'possibly incorrect' to 'not machine-readable'
- For the document view and Smartview, rename 'pending review' to 'require feedback'
- For the document view, divide column NOTES into FEEDBACK REQUIRED and NOT MACHINE-READABLE

### Fixed
- Dont raise an error if ai_model predict section with a template that does not exist.

## 2020-09-07_17-48-22

### Fixed
- Filter for 'possibly incorrect' shows wrong number.
- [Missing username in top right corner.](https://gitlab.com/konfuzio/objectives/-/issues/2431)
- [TypeError when running extract() on a document](https://gitlab.com/konfuzio/objectives/-/issues/2428).
- Sorting in csv is now correctly ordered by document_id and template position.
