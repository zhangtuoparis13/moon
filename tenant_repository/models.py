import logging

logger = logging.getLogger('moon.tenant_repository')


class Tenant:
    """
    Database Model for a Tenant / Project
    """
    __tablename__ = 'tenant'
    uuid = str()
    name = str()
    domain = str()
    description = str()
    parent = str()
    children = list()
    enabled = bool()

    def __init__(self,
            name="",
            domain="",
            uuid="",
            description="",
            enabled=True):
        self.name = name,
        self.domain = domain,
        self.uuid = uuid,
        self.description = description,
        self.enabled = enabled

    def __repr__(self):
        return "Tenant: {name} ({uuid}) {description} {enabled} parent={parent} children={children}".format(
            name=self.name,
            uuid=self.uuid,
            description=self.description,
            enabled=self.enabled,
            parent=self.parent,
            children=self.children
        )

