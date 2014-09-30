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

|HTTP PROTO | URL                                                               | Parameters                                        |Description                                        |
|-----------|-------------------------------------------------------------------|---------------------------------------------------|---------------------------------------------------|
|GET        |/json/intra-extensions/                                            |                                                   |get all Intra-Extension uuids                      |
|GET        |/json/intra-extension/{uuid}                                       |                                                   |get one intra-extension                            |
|POST       |/json/intra-extension/                                             | tenant_uuid, policy model                         |add an intra-extension                             |
|DELETE     |/json/intra-extension/{uuid}                                       |                                                   |delete an intra-extension                          |
|GET        |/json/intra-extension/{uuid}/subjects                              |                                                   |get all subjects for an intra-extension            |
|GET        |/json/intra-extension/{uuid}/objects                               |                                                   |get all objects for an intra-extension             |
|POST       |/json/intra-extension/{uuid}/subject                               | subject_uuid                                      |add a subject for an intra-extension               |
|POST       |/json/intra-extension/{uuid}/object                                | object_uuid                                       |add an object for an intra-extension               |
|DELETE     |/json/intra-extension/{uuid}/subject/{uuid}                        |                                                   |delete one subject for an intra-extension          |
|DELETE     |/json/intra-extension/{uuid}/object/{uuid}                         |                                                   |delete one objects for an intra-extension          |
|GET        |/json/intra-extension/{uuid}/subject_categories                    |                                                   |get all subject categories                         |
|POST       |/json/intra-extension/{uuid}/subject_category                      | category_id                                       |add a new subject category                         |
|DELETE     |/json/intra-extension/{uuid}/subject_category/{name}               |                                                   |delete a new subject category                      |
|GET        |/json/intra-extension/{uuid}/object_categories                     |                                                   |get all object categories                          |
|POST       |/json/intra-extension/{uuid}/object_category                       | category_id                                       |add a new object category                          |
|DELETE     |/json/intra-extension/{uuid}/object_category/{name}                |                                                   |delete a new object category                       |
|GET        |/json/intra-extension/{uuid}/subject_category_values               |                                                   |get all values for a subject category              |
|POST       |/json/intra-extension/{uuid}/subject_category_value                | category_id, value                                |add a new value for a subject category             |
|DELETE     |/json/intra-extension/{uuid}/subject_category_value/{cat}/{value}  |                                                   |delete a value for a subject category              |
|GET        |/json/intra-extension/{uuid}/object_category_values                |                                                   |get all values for a subject category              |
|POST       |/json/intra-extension/{uuid}/object_category_value                 | category_id, value                                |add a new value for a subject category             |
|DELETE     |/json/intra-extension/{uuid}/object_category_value/{cat}/{value}   |                                                   |delete a value for a subject category              |
|GET        |/json/intra-extension/{uuid}/subject_assignments                   |                                                   |get all assignments for a subject                  |
|POST       |/json/intra-extension/{uuid}/subject_assignment                    | category_id, subject_id, category_value           |add a new assignment for a subject                 |
|DELETE     |/json/intra-extension/{uuid}/subject_assignment/{uuid}             |                                                   |delete an assignment for a subject                 |
|GET        |/json/intra-extension/{uuid}/object_assignments                    |                                                   |get all assignments for a subject                  |
|POST       |/json/intra-extension/{uuid}/object_assignment                     | category_id, object_id, category_value            |add a new assignment for a subject                 |
|DELETE     |/json/intra-extension/{uuid}/object_assignment/{uuid}              |                                                   |delete an assignment for a subject                 |
|GET        |/json/intra-extension/{uuid}/rules                                 |                                                   |get all rules for an intra-extension               |
|POST       |/json/intra-extension/{uuid}/rule                                  | sub_cat_value, obj_cat_value                      |add a new rule of an intra-extension               |
|DELETE     |/json/intra-extension/{uuid}/rule/{uuid}                           | TODO later                                        |delete a rule of an intra-extension                |
|-----------|-------------------------------------------------------------------|---------------------------------------------------|---------------------------------------------------|
|GET        |/json/inter-extensions/                                            |                                                   |get all inter-extensions uuids                     |
|GET        |/json/inter-extension/{uuid}                                       |                                                   |get one inter-extension                            |
|POST       |/json/inter-extension/                                             | requesting_intra_extension_uuid, requested_intra_extension_uuid, type, sub_list, obj_list, act    |add a new inter-extension                          |
|DELETE     |/json/inter-extension/{uuid}                                       |                                                   |delete an inter-extension                          |
|GET        |/json/inter-extension/{uuid}/vents                                 |                                                   |get all virtual entities for an inter-extension    |
|-----------|-------------------------------------------------------------------|---------------------------------------------------|---------------------------------------------------|
|GET        |/pip/projects/                                                     |                                                   |get all tenants                                    |
|GET        |/pip/projects/{project_uuid}                                       |                                                   |get one tenant                                     |
|GET        |/pip/projects/{project_uuid}/subjects/{tenant_uuid}                |                                                   |get all subjects                                   |
|GET        |/pip/projects/{project_uuid}/objects/{tenant_uuid}                 |                                                   |get all objects (ie. all virtual machines)         |
|GET        |/pip/projects/{project_uuid}/roles/{user_uuid}                     |                                                   |get all roles                                      |
|GET        |/pip/projects/{project_uuid}/groups/{user_uuid}                    |                                                   |get all groups                                     |
|GET        |/pip/projects/{project_uuid}/assignments/roles/{user_uuid}         |                                                   |get all role assignments for user                  |
|GET        |/pip/projects/{project_uuid}/assignments/groups/{user_uuid}        |                                                   |get all group assignments for user                 |
|-----------|-------------------------------------------------------------------|---------------------------------------------------|---------------------------------------------------|
|GET        |/logs                                                              |                                                   |get logs                                           |

