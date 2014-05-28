TODO
====

Global things to do
-------------------

- [ ] Add a testing framework
- [x] Add a logging system
- [ ] Add a documentation system

Specific modifications for moon
-------------------------------

Legend:
- ~10% work initiated
- ~90% work almost finished

###Moon Core

| Module            | Description                               | Percentage of work |
| ----------------- | ----------------------------------------- | ------------------ |
| PAP               | Policy Administration Point               | 50%                |
| PIP               | Policy Information Point                  | 50%                |
| PDP               | Policy Decision Point                     | 50%                |
| Info Repository   | DB for objects                            | 90%                |
| Tenant Repository | DB for tenants and relations between them | 90%                |
| Policy Repository | DB for Policy authorization               | 50%                |
| MRM               | model-based reference monitor             | 80%                |

###Redirect keystone Auth to Moon

| Module        | Description                               | Percentage of work |
| ------------- | ----------------------------------------- | ------------------ |
| moon_hook     | Hook Keystone authorization               | 70%                |
| keystone_sync | Synchronisation between Moon and Keystone | 0%                 |

###Admin interface on Django

|Module       | Description                              | Percentage of work |
|------------ | ---------------------------------------- | ------------------ |
|GI (Users)   | Users administration                     | 70%                |
|GI (Tenants) | Tenants administration                   | 70%                |
|GI (Roles)   | Roles administration                     | 10%                |
|GI (Userdb)  | Administration of all objects of user_db | 90%                |
|GI (Policy)  | Policy administration                    | 30%                |
