"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2013 Nathanael C. Fritz, Lance J.T. Stout
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission.
"""

import logging

from sleekxmpp.stanza import Iq
from sleekxmpp.xmlstream.handler import Callback
from sleekxmpp.xmlstream.matcher import MatchXPath
from sleekxmpp.xmlstream import register_stanza_plugin
from sleekxmpp.plugins import BasePlugin
from sleekxmpp.plugins.google_settings import stanza


log = logging.getLogger(__name__)


class GoogleSettings(BasePlugin):

    """
    Google: Gmail Notifications

    Also see <https://developers.google.com/talk/jep_extensions/usersettings>.
    """

    name = 'google_settings'
    description = 'Google: User Settings'
    dependencies = set()
    stanza = stanza

    def plugin_init(self):
        register_stanza_plugin(Iq, stanza.UserSettings)

        self.xmpp.register_handler(
                Callback('Google Settings',
                    MatchXPath('{%s}iq/%s' % (
                        self.xmpp.default_ns,
                        stanza.UserSettings.tag_name())),
                    self._handle_settings_change))

    def plugin_end(self):
        self.xmpp.remove_handler('Google Settings')

    def get(self, block=True, timeout=None, callback=None):
        iq = self.xmpp.Iq()
        iq['type'] = 'get'
        iq.enable('google_settings')
        return iq.send(block=block, timeout=timeout, callback=callback)

    def update(settings, block=True, timeout=None, callback=None):
        iq = self.xmpp.Iq()
        iq['type'] = 'set'
        iq.enable('google_settings')

        for setting, value in settings.items():
            iq['google_settings'][setting] = value

        return iq.send(block=block, timeout=timeout, callback=callback)

    def _handle_settings_change(self, iq):
        self.xmpp.event('google_settings_change', iq)
