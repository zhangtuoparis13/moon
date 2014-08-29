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


class RuleNotFoundException(Exception):
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return self.__message


class DuplicateObjectException(Exception):
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return self.__message


class DuplicateSubjectException(Exception):
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


class AdminException(Exception):
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return self.__message

