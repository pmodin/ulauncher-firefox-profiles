import os
import re
import subprocess
import configparser
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction


def get_profiles(config_folder):
    config = configparser.ConfigParser()
    config.read(os.path.join(config_folder, 'profiles.ini'))
    regex = r'^Profile.*$'
    return [config[p]['Name'] for p in config.sections() if 'Name' in config[p] and re.search(regex, p, re.IGNORECASE)]


class DemoExtension(Extension):
    def __init__(self):
        super(DemoExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        config_folder = os.path.expanduser(extension.preferences['firefox_folder'])
        profiles = get_profiles(config_folder)

        query = event.get_argument()
        if query:
            query = query.strip().lower()
            profiles = [p for p in profiles if query in p.lower()]

        entries = []
        for profile in profiles:
            entries.append(ExtensionResultItem(
                icon='images/icon.png',
                name=profile,
                on_enter=ExtensionCustomAction(profile, keep_app_open=False)
            ))
        return RenderResultListAction(entries)


class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        subprocess.Popen([extension.preferences['firefox_cmd'], '-p', event.get_data()])


if __name__ == '__main__':
    DemoExtension().run()
