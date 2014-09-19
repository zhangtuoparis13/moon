gui
=================================
Introduction
---------------------------------
Graphic interface to access the admin interface

Description
---------------------------------

None

URL that return HTML data
-------------------------
|HTTP PROTO | URL                                           |Description                            |
|-----------|-----------------------------------------------|---------------------------------------|
|GET        |/                                              |get the index                          |
|GET        |/intra-extensions                              |get the page for Intra-Extensions      |
|GET        |/inter-extensions                              |get the page for Inter-Extensions      |
|GET        |/logs                                          |get the page dedicated to logs         |

URL that return JSON data
-------------------------

|HTTP PROTO | URL                                                   |Description                                        |
|-----------|-------------------------------------------------------|---------------------------------------------------|
|GET        |/json/intra-extensions/                                |get all Intra-Extension uuids                      |
|GET        |/json/intra-extension/{uuid}                           |get one intra-extension                            |
|POST       |/json/intra-extension/                                 |add an intra-extension                             |
|DELETE     |/json/intra-extension/{uuid}                           |delete an intra-extension                          |
|GET        |/json/intra-extension/{uuid}/subjects                  |get all subjects for an intra-extension            |
|GET        |/json/intra-extension/{uuid}/objects                   |get all objects for an intra-extension             |
|POST       |/json/intra-extension/{uuid}/subject                   |add a subject for an intra-extension               |
|POST       |/json/intra-extension/{uuid}/object                    |add an object for an intra-extension               |
|DELETE     |/json/intra-extension/{uuid}/subject                   |delete one subject for an intra-extension          |
|DELETE     |/json/intra-extension/{uuid}/object                    |delete one objects for an intra-extension          |
|GET        |/json/intra-extension/{uuid}/subject_categories        |get all subject categories                         |
|POST       |/json/intra-extension/{uuid}/subject_category          |add a new subject category                         |
|DELETE     |/json/intra-extension/{uuid}/subject_category          |delete a new subject category                      |
|GET        |/json/intra-extension/{uuid}/object_categories         |get all object categories                          |
|POST       |/json/intra-extension/{uuid}/object_category           |add a new object category                          |
|DELETE     |/json/intra-extension/{uuid}/object_category           |delete a new object category                       |
|GET        |/json/intra-extension/{uuid}/subject_category_values   |get all values for a subject category              |
|POST       |/json/intra-extension/{uuid}/subject_category_values   |add a new value for a subject category             |
|DELETE     |/json/intra-extension/{uuid}/subject_category_values   |delete a value for a subject category              |
|GET        |/json/intra-extension/{uuid}/object_category_values    |get all values for a subject category              |
|POST       |/json/intra-extension/{uuid}/object_category_values    |add a new value for a subject category             |
|DELETE     |/json/intra-extension/{uuid}/object_category_values    |delete a value for a subject category              |
|GET        |/json/intra-extension/{uuid}/subject_assignments       |get all assignments for a subject                  |
|POST       |/json/intra-extension/{uuid}/subject_assignment        |add a new assignment for a subject                 |
|DELETE     |/json/intra-extension/{uuid}/subject_assignment        |delete an assignment for a subject                 |
|GET        |/json/intra-extension/{uuid}/object_assignments        |get all assignments for a subject                  |
|POST       |/json/intra-extension/{uuid}/object_assignment         |add a new assignment for a subject                 |
|DELETE     |/json/intra-extension/{uuid}/object_assignment         |delete an assignment for a subject                 |
|GET        |/json/intra-extension/{uuid}/rules                     |get all rules for an intra-extension               |
|POST       |/json/intra-extension/{uuid}/rule                      |add a new rule of an intra-extension               |
|DELETE     |/json/intra-extension/{uuid}/rule                      |delete a rule of an intra-extension                |
|GET        |/json/inter-extensions/                                |get all inter-extensions uuids                     |
|GET        |/json/inter-extension/{uuid}                           |get one inter-extension                            |
|POST       |/json/inter-extension/                                 |add a new inter-extension                          |
|DELETE     |/json/inter-extension/{uuid}                           |delete an inter-extension                          |
|DELETE     |/json/inter-extension/{uuid}/vents                     |get all virtual entities for an inter-extension    |

