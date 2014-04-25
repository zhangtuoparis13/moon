import logging

logger = logging.getLogger('moon.info_repository')

# t = {
#     't1': {
#         'attributes': (
#                 {'name': "a1", "type": "string", "length": 254},
#                 {'name': "a2", "type": "string", "length": 254},
#                 )
#     },
#     't2': {
#         'attributes': (
#                 {'name': "a3", "type": "string", "length": 254},
#                 {'name': "a4", "type": "string"},
#                 )
#     },
# }
#
# template_key = """class {name}:
#     __tablename__ = "{name}"
# """
# template_value = "    uuid = Column({type}({length}))\n"
#
# constructor = ""
#
# for key in t.keys():
#     constructor += "{tk}\n".format(tk=template_key.format(name=key))
#     for a in t[key]['attributes']:
#         _type = a["type"]
#         if _type == "string": _type = "String"
#         _length = 0
#         if "length" in a.keys():
#             _length = a['length']
#         else:
#             _length = 32
#         constructor += template_value.format(type=_type, length=_length)
#
# print(constructor)
#
# exec(constructor)


# class AttrName:
#     """
#     Abstract class to describe Attribute keys
#     """
#     uuid = ""
#     __type__ = "key"
#     __tablename__ = ''
#
#
# class AttrValue:
#     """
#     Abstract class to describe Attribute values
#     """
#     uuid = ""
#     __type__ = "value"
#     __tablename__ = ''


template_key = """
class {name}:
    \"\"\"
    {desc}
    \"\"\"
    __tablename__ = "{name}"
    __attrtype__ = "{attrtype}" """
template_value = "    {name} = {type}()\n"
template_service = """\n    def __repr__(self):
        return "{attrkey}: {attrvalues}".format({attrdef})
"""

__list__ = {}


def build_class_from_dict(cls):
    """
    Build classes from a dictionary and execute them
    param: dict cls: the dictionary source
    example of dictionary:
        {
        # Subject attributes
          'Subject': {
            'attributes': (
                    {'name': "uuid", "type": "String", "length": 32},
                    {'name': "name", "type": "String", "length": 254},
                    ),
            'type': "AttrKey",
            'description': "A user in the system.",
        },
    """
    constructor = ""
    for key in cls.keys():
        logger.info("Initializing class {}".format(key))
        constructor += "{tk}\n".format(
            tk=template_key.format(
                name=key,
                attrtype=cls[key]['type'],
                desc=cls[key]['description']
            )
        )
        for attr in cls[key]['attributes']:
            if "length" not in attr.keys():
                attr['length'] = 32
            _type = attr["type"].\
                replace("String", "str").\
                replace("Int", "int").\
                replace("Boolean", "bool")
            constructor += template_value.format(
                name=attr["name"],
                type=_type,
                length=attr['length']
            )
        constructor += template_service.format(
            attrkey=key,
            attrvalues=' '.join(map(lambda x: "{x}={{{x}}}".format(x=x['name']), cls[key]['attributes'])),
            attrdef=', '.join(map(lambda x: "{x}=self.{x}".format(x=x['name']), cls[key]['attributes'])),
        )
        constructor += "__list__['{name}'] = {name}".format(name=key)
    # Warning: possible security hazard here!!!
    # TODO: check that all attributes are only string or boolean or int
    exec constructor


# class Subject(AttrName):
#     """
#     Model for a User
#     """
#     __tablename__ = 'user'
#     uuid = ""
#     name = ""
#     password = ""
#     email = ""
#     description = ""
#     enabled = ""
#     domain = "Default"
#     project = ""
#
#     def __repr__(self):
#         return "Subject: {domain}/{user} ({uuid}) {email} enable: {enabled}".format(
#             user=self.name,
#             uuid=self.uuid,
#             email=self.email,
#             enabled=self.enabled,
#             domain=self.domain
#         )
#
#
# class Role():
#     """
#     Database Model for a Role
#     """
#     __tablename__ = 'role'
#     uuid = ""
#     name = ""
#     tenant_uuid = ""
#     description = ""
#     enabled = ""
#
#     def __repr__(self):
#         return "Role: {role} ({uuid}) {tenant_uuid} {description} {enabled}".format(
#             role=self.name,
#             uuid=self.uuid,
#             tenant_uuid=self.tenant_uuid,
#             description=self.description,
#             enabled=self.enabled
#         )
#
#
# class UserRoleAssignment:
#     """
#     Database Model for relations between User and Role
#     """
#     __tablename__ = 'user_role_assignment'
#     uuid = ""
#     user_uuid = ""
#     role_uuid = ""
#
#     def __repr__(self):
#         return "{user_uuid} -> {role_uuid}".format(
#             user_uuid=self.user_uuid,
#             role_uuid=self.role_uuid,
#         )
#
#
# class Type:
#     pass
#
#
# class Action:
#     pass