# Copyright 2014 Orange
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


class AuthzException(Exception):
    def __init__(self, message):
        self.__message = message
    
    def __str__(self):
        return self.__message


class SubjectNotFoundException(Exception):
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return self.__message


class ObjectNotFoundException(Exception):
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return self.__message


class SubjectAttributeNotFoundException(Exception):
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return self.__message


class ObjectAttributeNotFoundException(Exception):
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return self.__message


class DuplicateSubjectException(Exception):
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return self.__message


class DuplicateObjectException(Exception):
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return self.__message


class SubjectAssignmentNotFoundException(Exception):
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return self.__message


class ObjectAssignmentNotFoundException(Exception):
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return self.__message


class DuplicateSubjectAttributeException(Exception):
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return self.__message


class DuplicateObjectAttributeException(Exception):
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return self.__message


class RuleNotFoundException(Exception):
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return self.__message


class AdminException(Exception):
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return self.__message

