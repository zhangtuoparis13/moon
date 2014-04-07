from django.db import models
from django.utils.translation import ugettext_lazy as _


# class PdP(models.Model):
#     content = models.CharField(_(u'name'), max_length=255)
#     is_auth = models.BooleanField(_(u'Authorized?'))
#
#     def __unicode__(self):
#         return u'PolicyDecisionPoint %d : %s' % (self.id, self.content)
#
#
# class PaP(models.Model):
#     content = models.CharField(_(u'name'), max_length=255)
#     is_auth = models.BooleanField(_(u'Authorized?'))
#
#     def __unicode__(self):
#         return u'PolicyAdministrationPoint %d : %s' % (self.id, self.content)
