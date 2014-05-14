TODO
====

Global things to do
-------------------

[ ] Add a testing framework
[X] Add a logging system
[ ] Add a documentation system

Specific modifications for moon
-------------------------------

Legend:
- ~10% work initiated
- ~90% work almost finished

###Moon Core
|Module|Description|percentage of work|
|--|--|--|
|PAP|Policy Administration Point|25%|
|PIP|Policy Information Point|25%|
|PDP|Policy Decision Point|25%|
|Info Repository|DB for objects|90%|
|Tenant Repository|DB for tenants and relations between them|90%|
|Policy Repository|DB for Policy authorization|0%|
|MRM|model-based reference monitor|10%|

###Redirect keystone auth to Moon
|Module|Description|percentage of work|
|--|--|--|
|moon_hook|Hook Keystone authorization|20%|
|keystone_sync|Synchronisation between Moon and Keystone|0%|

###Admin interface on Django
|Module|Description|percentage of work|
|--|--|--|
|GI (Users)|Users administration|70%|
|GI (Tenants)|Tenants administration|70%|
|GI (Roles)|Roles administration|10%|
|GI (Policy)|Policy administration|0%|
