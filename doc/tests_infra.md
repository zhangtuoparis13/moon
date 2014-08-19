Tests
=====

Introduction
------------
**Actions sur les vm:**
- get attributes
- list
- volume_attachments:show

La création des tenants se fait avant les tests

**Mesures:**
- durée moyenne de traitement de chaque requête
- caractériser les temps de traitement pour les réponses :
  - OK
  - KO
  - Out of Scope

**Plateforme:**
- plateforme SEAL avec 2 serveurs
  - 1 openstack complet
  - 1 openstack compute
- PC fixe pour le framework Moon

Mono tenant :
-------------
Avec et sans Moon
1) test en augmentant le nombre d'utilisateurs
2) test en augmentant le nombre de VM
3) test en augmentant à la fois le nombre d'utilisateur et de VM

Multi tenants with(out) inter-tenant relations :
------------------------------------------
Avec et sans Moon
1) Sans relation inter-Tenant
   test avec un nombre fixe d'utilisateur et de vm par tenant, on augmente le nombre de tenant
Avec Moon
2) Ajout de relations entre les tenants
   test avec un nombre fixe d'utilisateur et de vm par tenant, on augmente le nombre de tenant