from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem, OneLineAvatarListItem, IRightBodyTouch
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.picker import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import BooleanProperty, StringProperty
from kivymd.app import MDApp

KV = '''
<SettingsScreen>:
    name: "settings"
    BoxLayout:
        orientation: "vertical"

        MDToolbar:
            title: "Settings"
            elevation: 10
            left_action_items: [["arrow-left", lambda x: root.go_back()]]

        MDList:
            OneLineAvatarListItem:
                text: "Dark Mode"
                on_release: root.toggle_dark_mode_switch()

                RightWidget:
                    id: dark_mode_switch
                    MDSwitch:
                        on_active: root.on_dark_mode_switch(self.active)

            OneLineListItem:
                text: "Refresh Interval: " + root.refresh_interval
                on_release: root.open_refresh_menu()
'''

class RightWidget(IRightBodyTouch, MDSwitch):
    pass

class SettingsScreen(MDScreen):
    dark_mode = BooleanProperty(False)
    refresh_interval = StringProperty("15 minutes")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_string(KV)
        self.menu_items = [
            {"viewclass": "OneLineListItem", "text": "5 minutes", "on_release": lambda x="5 minutes": self.set_refresh_interval(x)},
            {"viewclass": "OneLineListItem", "text": "15 minutes", "on_release": lambda x="15 minutes": self.set_refresh_interval(x)},
            {"viewclass": "OneLineListItem", "text": "30 minutes", "on_release": lambda x="30 minutes": self.set_refresh_interval(x)},
            {"viewclass": "OneLineListItem", "text": "1 hour", "on_release": lambda x="1 hour": self.set_refresh_interval(x)},
        ]
        self.menu = MDDropdownMenu(
            caller=self,
            items=self.menu_items,
            width_mult=4,
        )

    def on_pre_enter(self):
        app = MDApp.get_running_app()
        settings = app.settings.load_settings()
        self.dark_mode = settings.get('dark_mode', False)
        self.refresh_interval = settings.get('refresh_interval', '15 minutes')
        self.ids.dark_mode_switch.active = self.dark_mode

    def toggle_dark_mode_switch(self):
        self.ids.dark_mode_switch.active = not self.ids.dark_mode_switch.active

    def on_dark_mode_switch(self, active):
        self.dark_mode = active
        app = MDApp.get_running_app()
        app.theme_cls.theme_style = "Dark" if active else "Light"
        settings = app.settings.load_settings()
        settings['dark_mode'] = active
        app.settings.save_settings(settings)

    def open_refresh_menu(self):
        self.menu.caller = self.ids['refresh_interval_label'] if hasattr(self.ids, 'refresh_interval_label') else self
        self.menu.open()

    def set_refresh_interval(self, interval):
        self.refresh_interval = interval
        app = MDApp.get_running_app()
        settings = app.settings.load_settings()
        settings['refresh_interval'] = interval
        app.settings.save_settings(settings)
        self.menu.dismiss()
        self.ids.refresh_interval_text = interval

    def go_back(self):
        app = MDApp.get_running_app()
        app.root.current = "home"

