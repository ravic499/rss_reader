from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDIconButton
# import other KivyMD widgets you use in KV files here

from screens.home_screen import HomeScreen
from screens.settings_screen import SettingsScreen
from screens.article_screen import ArticleScreen

from settings import SettingsManager
from rss_handler import fetch_all_feeds


class RSSReaderApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.settings_manager = SettingsManager()
        self.settings = self.settings_manager.load_settings()
        self.feeds = self.settings.get('feeds', [])
        # Normalize feeds to dict format if needed
        self.feeds = [
            f if isinstance(f, dict) else {"url": f, "category": "", "articles": []}
            for f in self.feeds
        ]

    def build(self):
        # Load all KV files BEFORE creating screen instances
        Builder.load_file("screens/home_screen.kv")
        Builder.load_file("screens/settings_screen.kv")
        Builder.load_file("screens/article_screen.kv")

        # Apply saved theme preference
        self.theme_cls.theme_style = "Dark" if self.settings.get("dark_mode", False) else "Light"

        # Create ScreenManager and add screen instances
        self.sm = ScreenManager()
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(SettingsScreen(name='settings'))
        self.sm.add_widget(ArticleScreen(name='article'))

        return self.sm

    def switch_theme(self, dark_mode: bool):
        self.theme_cls.theme_style = "Dark" if dark_mode else "Light"
        self.settings["dark_mode"] = dark_mode
        self.settings_manager.save_settings(self.settings)

    def load_feeds(self):
        # Return the list of feeds with articles fetched
        all_articles = fetch_all_feeds(self.feeds)
        self.all_articles = all_articles  # Store if needed
        return all_articles

    def add_feed(self, url, category):
        # Add new feed dict to feeds list
        new_feed = {"url": url, "category": category, "articles": []}
        # Avoid duplicates (optional)
        if not any(feed['url'] == url for feed in self.feeds):
            self.feeds.append(new_feed)
            self.save_feeds()
        else:
            print(f"Feed with URL '{url}' already exists.")

    def save_feeds(self):
        # Save feeds list back to settings and persist
        self.settings['feeds'] = self.feeds
        self.settings_manager.save_settings(self.settings)


if __name__ == '__main__':
    RSSReaderApp().run()
