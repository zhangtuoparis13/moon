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

from django.db import models
from django.utils.translation import ugettext_lazy as _


class PdP(models.Model):
    content = models.CharField(_(u'name'), max_length=255)
    is_auth = models.BooleanField(_(u'Authorized?'))

    def __unicode__(self):
        return u'PolicyDecisionPoint %d : %s' % (self.id, self.content)


class PaP(models.Model):
    content = models.CharField(_(u'name'), max_length=255)
    is_auth = models.BooleanField(_(u'Authorized?'))

    def __unicode__(self):
        return u'PolicyAdministrationPoint %d : %s' % (self.id, self.content)
