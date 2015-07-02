# -*- coding: utf-8 -*-
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer


class NoekuSyncVknoeLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)


COLLECTIVE_UTILS_FIXTURE = NoekuSyncVknoeLayer()
COLLECTIVE_UTILS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_UTILS_FIXTURE,),
    name='CollectiveUtilsLayer:IntegrationTesting'
)
