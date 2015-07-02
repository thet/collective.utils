# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from zope.interface import alsoProvides
from zope.interface import noLongerProvides
from zope.event import notify


"""Example usage:

1) Subclass EnableDisableFeature for a custom browser view::

    class BuyableAction(EnableDisableFeature):
        feature_iface = IBuyable
        potential_feature_iface = IPotentiallyBuyable
        enabled_message = _(u'enabled_buyable', u'Enabled Buyable.')
        disabled_message = _(u'disabled_buyable', u'Disabled Buyable.')

2) Register it in ZCML like so::

    <browser:page
        for="*"
        name="check_buyable"
        class=".buyable_action.BuyableAction"
        allowed_attributes="enableable
                            disableable"
        permission="zope2.View"
        />
    <browser:page
        for="*"
        name="set_buyable"
        class=".buyable_action.BuyableAction"
        allowed_attributes="enable
                            disable"
        permission="cmf.ManagePortal"
        />

3) Register it in portal_actions.xml like so::

    <?xml version="1.0"?>
    <object name="portal_actions" meta_type="Plone Actions Tool" xmlns:i18n="http://xml.zope.org/namespaces/i18n">

     <object name="object_buttons" meta_type="CMF Action Category">
      <object name="enable_buyable" meta_type="CMF Action" i18n:domain="your.package">
       <property name="title" i18n:translate="title_enable_buyable">Enable Buyable</property>
       <property name="description" i18n:translate="help_enable_buyable">Click to make this content item buyable.</property>
       <property name="url_expr">string:$object_url/@@set_buyable/enable</property>
       <property name="available_expr">object/@@check_buyable/enableable|nothing</property>
       <property name="permissions">
        <element value="cmf.ManagePortal" />
       </property>
       <property name="visible">True</property>
      </object>
      <object name="disable_buyable" meta_type="CMF Action" i18n:domain="your.package">
       <property name="title" i18n:translate="title_disable_buyable">Disable Buyable</property>
       <property name="description" i18n:translate="help_disable_buyable">Click to disable content item from being buyable.</property>
       <property name="url_expr">string:$object_url/@@set_buyable/disable</property>
       <property name="available_expr">object/@@check_buyable/disableable|nothing</property>
       <property name="permissions">
        <element value="cmf.ManagePortal" />
       </property>
       <property name="visible">True</property>
      </object>
     </object>

    </object>

"""


class EnableDisableFeature(BrowserView):
    feature_iface = None  # Feature Interface, which is set or removed
    potential_feature_iface = None  # Must be provided by the context in order to enable or disable features.  # noqa
    enabled_message = None  # Statusmessage when enabled
    disabled_message = None  # Statusmessage when disabled
    enabled_event = None  # Event to be fired, when feature is enabled
    disabled_event = None  # Event to be fired, when feature is disabled

    def enable(self):
        """Enable the feature by setting the feature interface on the context.
        """
        ctx = self.context
        req = self.request
        alsoProvides(ctx, self.feature_iface)
        cat = getToolByName(ctx, 'portal_catalog')
        cat.reindexObject(ctx, idxs=['object_provides'], update_metadata=1)
        if self.enabled_event:
            notify(self.enabled_event(ctx))
        IStatusMessage(req).addStatusMessage(self.enabled_message, 'info')
        self.request.response.redirect(ctx.absolute_url())

    def disable(self):
        """Disable the feature by removing the feature interface on the
        context.
        """
        ctx = self.context
        req = self.request
        noLongerProvides(ctx, self.feature_iface)
        cat = getToolByName(ctx, 'portal_catalog')
        cat.reindexObject(ctx, idxs=['object_provides'], update_metadata=1)
        if self.disabled_event:
            notify(self.disabled_event(ctx))
        IStatusMessage(req).addStatusMessage(self.disabled_message, 'info')
        self.request.response.redirect(ctx.absolute_url())

    def enableable(self):
        """Check, if the feature can be enabled, if it isn't already enabled
        and the context provides the potential feature interface.
        """
        return self.potential_feature_iface.providedBy(self.context)\
            and not self.feature_iface.providedBy(self.context)

    def disableable(self):
        """Check, if the feature can be disabled, if it isn't already disabled
        and the context provides the potential feature interface.
        """
        return self.potential_feature_iface.providedBy(self.context)\
            and self.feature_iface.providedBy(self.context)
