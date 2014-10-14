TODO
====

Global things to do
-------------------
- [x] Add a testing framework
- [x] Add a logging system
- [ ] Add a GUI interface
- [ ] Add a sync_db system



Specific modifications for moon
-------------------------------
Legend:
- ~10% work initiated
- ~90% work almost finished


###Core
| Title               | Actor       | Description       | Deadline      | Percentage of work |
| ------------------- | ----------- | ----------------- | ------------- | ------------------ |
| PDP                 | WuKong      |                   | 30/09         | 100%               |
| PAP                 | Tom         |add super_extension| 07/10         | 90%                |
| PIP                 | Tom, WuKong |detele role assi   | 09/10         | 90%                |
| core                | WuKong      |                   | 16/09         | 100%               |
| super_extension     | WuKong      |                   | 30/09         | 100%               |


###MRM
| Title               | Actor       | Description       | Deadline      | Percentage of work |
| ------------------- | ----------- | ----------------- | ------------- | ------------------ |
| mrm                 | Tom, WuKong |                   | 08/10         | 50%                |


###Testing framework
| Title               | Actor       | Description       | Deadline      | Percentage of work |
| ------------------- | ----------- | ----------------- | ------------- | ------------------ |
| Core/PDP            | WuKong      | unit test         | 30/09         | 100%               |
| Core/PAP            | Tom         | unit test         | 01/10         | 100%               |
| Core/PIP            | Tom         | unit test         | 30/09         | 100%               |
| GUI+PAP+PDP+PIP     | Tom         | integration test  | 03/10         | 80%                |
| MRM                 | WuKong      | unit test         | 08/10         | 80%                |


###Implementation and Evaluation on Moon
| Title               | Actor       | Description       | Deadline      | Percentage of work |
| ------------------- | ----------- | ----------------- | ------------- | ------------------ |
| Define Scenario     | Tom, WuKong |                   | 30/09         |  100%              |
| Implement infra     | Tom, WuKong |devstack sur trust3| 10/10         |  40%               |
| Restart Moon        | Tom, WuKong |                   | 17/10         |  0%                |
| SSH                 | Tom, WuKong |                   | 17/10         |  0%                |
| access policies conf| WuKong      | DTE001            | 17/10         |  0%                |
| PAP                 | Tom         | sync Moon and OS  | 17/10         |  0%                |
| PIP                 | Tom         | create vm by Moon | 17/10         |  0%                |


###GUI
| Title               | Actor       | Description       | Deadline      | Percentage of work |
| ------------------- | ----------- | ----------------- | ------------- | ------------------ |
| API                 | Tom, WuKong |add super_extension| 03/10         | 90%                |
| core                | Arnaud      |                   | 30/10         | 0%                 |


# ****************************************************************************
###Logging
| Title               | Actor       | Description       | Deadline      | Percentage of work |
| ------------------- | ----------- | ----------------- | ------------- | ------------------ |
| log                 | Tom, WuKong |                   | 10/10         | 70%                |


###Sync_db
| Title               | Actor       | Description       | Deadline      | Percentage of work |
| ------------------- | ----------- | ----------------- | ------------- | ------------------ |
| sync_db             | Tom, WuKong |                   | 10/10         | 80%                |
| test                | Tom, WuKong |                   | 10/10         | 70%                |


###Delegation
| Title               | Actor       | Description       | Deadline      | Percentage of work |
| ------------------- | ----------- | ----------------- | ------------- | ------------------ |
| model               | WuKong      |                   | 10/10         | 20%                |
| GUI                 | WuKong      |customized for each| 10/10         | 20%                |
| test                | Tom, WuKong |                   | 10/10         | 0%                 |

###Integrate Policy engine with Prolog
| Title               | Actor       | Description       | Deadline      | Percentage of work |
| ------------------- | ----------- | ----------------- | ------------- | ------------------ |
| Design Policy Engine| WuKong      | Understand Prolog | 17/10         | 0%                 | 
| Implenet Engine     | WuKong      | in Moon           | 17/10         | 0%                 |
| Mutiple Sub-rule    | WuKong      | in Moon           | 17/10         | 0%                 |


###Package
| Title               | Actor       | Description       | Deadline      | Percentage of work |
| ------------------- | ----------- | ----------------- | ------------- | ------------------ |
| exception for authz | Tom         |                   |               | 0%                 |
| setup.py            | Tom         |                   |               | 50%                |

