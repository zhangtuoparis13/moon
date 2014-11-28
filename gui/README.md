gui
=================================
Introduction
---------------------------------
Graphic interface to access the admin interface

Description
---------------------------------
None

Installation
---------------------------------
<pre><code>~ apt-get install npm
~ npm install bower -g
~ bower install
</code></pre>

URL that return HTML data
-------------------------
|HTTP PROTO | URL                                           | Interfaces                                        |Description                            |
|-----------|-----------------------------------------------|---------------------------------------------------|---------------------------------------|
|GET        |/                                              |                                                   |get the index                          |
|GET        |/intra-extensions                              |                                                   |get the page for Intra-Extensions      |
|GET        |/inter-extensions                              |                                                   |get the page for Inter-Extensions      |
|GET        |/logs                                          |                                                   |get the page dedicated to logs         |

URL that return JSON data
-------------------------

|HTTP PROTO | URL                                                               | Interfaces                                        | Parameters                                        |Description                                        |
|-----------|-------------------------------------------------------------------|---------------------------------------------------|---------------------------------------------------|---------------------------------------------------|
|GET        |/json/intra-extensions/                                            | get_intra_extensions                              |                                                   |get all Intra-Extension uuids                      |
|GET        |/json/intra-extension/{uuid}                                       | get_intra_extensions                              |                                                   |get one intra-extension                            |
|POST       |/json/intra-extension/                                             | add_from_json                                     | tenant_uuid, policy model                         |add an intra-extension                             |
|DELETE     |/json/intra-extension/{uuid}                                       | delete_intra_extension                            |                                                   |delete an intra-extension                          |
|GET        |/json/intra-extension/{uuid}/subjects                              | get_subjects                                      |                                                   |get all subjects for an intra-extension            |
|GET        |/json/intra-extension/{uuid}/objects                               | get_objects                                       |                                                   |get all objects for an intra-extension             |
|POST       |/json/intra-extension/{uuid}/subject                               | add_subject                                       | subject_uuid                                      |add a subject for an intra-extension               |
|POST       |/json/intra-extension/{uuid}/object                                | add_object                                        | object_uuid                                       |add an object for an intra-extension               |
|DELETE     |/json/intra-extension/{uuid}/subject/{uuid}                        | delete_subject                                    |                                                   |delete one subject for an intra-extension          |
|DELETE     |/json/intra-extension/{uuid}/object/{uuid}                         | delete_object                                     |                                                   |delete one objects for an intra-extension          |
|GET        |/json/intra-extension/{uuid}/subject_categories                    | get_subject_categories                            |                                                   |get all subject categories                         |
|POST       |/json/intra-extension/{uuid}/subject_category                      | add_subject_category                              | category_id                                       |add a new subject category                         |
|DELETE     |/json/intra-extension/{uuid}/subject_category/{name}               | del_subject_category                              |                                                   |delete a new subject category                      |
|GET        |/json/intra-extension/{uuid}/object_categories                     | get_object_categories                             |                                                   |get all object categories                          |
|POST       |/json/intra-extension/{uuid}/object_category                       | add_object_category                               | category_id                                       |add a new object category                          |
|DELETE     |/json/intra-extension/{uuid}/object_category/{name}                | del_object_category                               |                                                   |delete a new object category                       |
|GET        |/json/intra-extension/{uuid}/subject_category_values               | get_subject_category_values                       |                                                   |get all values for a subject category              |
|POST       |/json/intra-extension/{uuid}/subject_category_value                | add_subject_category_value                        | category_id, value                                |add a new value for a subject category             |
|DELETE     |/json/intra-extension/{uuid}/subject_category_value/{cat}/{value}  | del_subject_category_value                        |                                                   |delete a value for a subject category              |
|GET        |/json/intra-extension/{uuid}/object_category_values                | get_object_category_values                        |                                                   |get all values for a subject category              |
|POST       |/json/intra-extension/{uuid}/object_category_value                 | add_object_category_value                         | category_id, value                                |add a new value for a subject category             |
|DELETE     |/json/intra-extension/{uuid}/object_category_value/{cat}/{value}   | del_object_category_value                         |                                                   |delete a value for a subject category              |
|GET        |/json/intra-extension/{uuid}/subject_assignments                   | get_subject_assignments                           |                                                   |get all assignments for a subject                  |
|POST       |/json/intra-extension/{uuid}/subject_assignment                    | add_subject_assignment                            | category_id, subject_id, category_value           |add a new assignment for a subject                 |
|DELETE     |/json/intra-extension/{uuid}/subject_assignment/{uuid}             | del_subject_assignment                            |                                                   |delete an assignment for a subject                 |
|GET        |/json/intra-extension/{uuid}/object_assignments                    | get_object_assignments                            |                                                   |get all assignments for a subject                  |
|POST       |/json/intra-extension/{uuid}/object_assignment                     | add_object_assignment                             | category_id, object_id, category_value            |add a new assignment for a subject                 |
|DELETE     |/json/intra-extension/{uuid}/object_assignment/{uuid}              | del_object_assignment                             |                                                   |delete an assignment for a subject                 |
|GET        |/json/intra-extension/{uuid}/rules                                 | get_rules                                         |                                                   |get all rules for an intra-extension               |
|POST       |/json/intra-extension/{uuid}/rule                                  | add_rule                                          | sub_cat_value, obj_cat_value                      |add a new rule of an intra-extension               |
|DELETE     |/json/intra-extension/{uuid}/rule/{uuid}                           | del_rule                                          | TODO later                                        |delete a rule of an intra-extension                |
|-----------|-------------------------------------------------------------------|---------------------------------------------------|---------------------------------------------------|---------------------------------------------------|
|GET        |/json/inter-extensions/                                            | inter_extension.get_installed_inter_extensions    |                                                   |get all inter-extensions uuids                     |
|GET        |/json/inter-extension/{uuid}                                       | inter_extension.get_installed_inter_extensions    |                                                   |get one inter-extension                            |
|POST       |/json/inter-extension/                                             | inter_extension.create_collaboration              | requesting_intra_extension_uuid, requested_intra_extension_uuid, type, sub_list, obj_list, act    |add a new inter-extension                          |
|DELETE     |/json/inter-extension/{uuid}                                       | inter_extension.destroy_collaboration             | inter_extension_uuid, genre, vent_uuid            |delete an inter-extension                          |
|GET        |/json/inter-extension/{uuid}/vents                                 | inter_extension.get_vents                         | tenant_uuid, intra_extension_uuid                 |get all virtual entities for an inter-extension    |
|-----------|-------------------------------------------------------------------|---------------------------------------------------|---------------------------------------------------|---------------------------------------------------|
|GET        |/json/super-extensions/                                            | TenantIntraExtensionMapping.list_mappings         |                                                   |get all inter-extensions uuids                     |
|POST       |/json/super-extension/                                             | TenantIntraExtensionMapping.create_mappings       | tenant_uuid, intra_extension_uuid                 |add a new mapping between 2 intra_extensions       |
|DELETE     |/json/super-extension/                                             | TenantIntraExtensionMapping.destroy_mappings      | tenant_uuid, intra_extension_uuid                 |destroy a mapping                                  |
|GET        |/json/super-extension/delegate                                     | super_extension.delegate                          | delegator_uuid, privilege                         |delegate privileges                                |
|-----------|-------------------------------------------------------------------|---------------------------------------------------|---------------------------------------------------|---------------------------------------------------|
|GET        |/pip/projects/                                                     | get_projects                                      |                                                   |get all tenants                                    |
|GET        |/pip/projects/{project_uuid}                                       | get_projects                                      |                                                   |get one tenant                                     |
|GET        |/pip/projects/{project_uuid}/subjects/{tenant_uuid}                | get_subjects                                      |                                                   |get all subjects                                   |
|GET        |/pip/projects/{project_uuid}/objects/{tenant_uuid}                 | get_objects                                       |                                                   |get all objects (ie. all virtual machines)         |
|GET        |/pip/projects/{project_uuid}/roles/{user_uuid}                     | get_roles                                         |                                                   |get all roles                                      |
|GET        |/pip/projects/{project_uuid}/groups/{user_uuid}                    | get_groups                                        |                                                   |get all groups                                     |
|GET        |/pip/projects/{project_uuid}/assignments/roles/{user_uuid}         | get_role_assignments                              |                                                   |get all role assignments for user                  |
|GET        |/pip/projects/{project_uuid}/assignments/groups/{user_uuid}        | get_group_assignments                             |                                                   |get all group assignments for user                 |
|-----------|-------------------------------------------------------------------|---------------------------------------------------|---------------------------------------------------|---------------------------------------------------|
|GET        |/logs                                                              |                                                   |                                                   |get logs                                           |

