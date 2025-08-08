from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from screens.home_screen import HomeScreen
from screens.settings_screen import SettingsScreen
from screens.article_screen import ArticleScreen

from settings import SettingsManager

KV = '''
ScreenManager:
    HomeScreen:
        name: 'home'
    SettingsScreen:
        name: 'settings'
    ArticleScreen:
        name: 'article'
'''

class RSSReaderApp(MDApp):
    def build(self):
        self.settings_manager = SettingsManager()
        self.settings = self.settings_manager.load_settings()

        # Apply saved theme preference
        self.theme_cls.theme_style = "Dark" if self.settings.get("dark_mode", False) else "Light"

        self.sm = Builder.load_string(KV)
        return self.sm

    def switch_theme(self, dark_mode: bool):
        self.theme_cls.theme_style = "Dark" if dark_mode else "Light"
        self.settings["dark_mode"] = dark_mode
        self.settings_manager.save_settings(self.settings)

if __name__ == '__main__':
    RSSReaderApp().run()

