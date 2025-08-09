from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.properties import ObjectProperty, ListProperty
from kivymd.app import MDApp

class HomeScreen(MDScreen):
    feed_list = ObjectProperty(None)
    feeds = ListProperty([])  # List of dicts with feed info and articles

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None

    def on_pre_enter(self):
        # Refresh feeds when screen appears
        print("IDs available:", self.ids.keys())
        self.load_feeds()

    def load_feeds(self):
        app = MDApp.get_running_app()
        raw_feeds = app.load_feeds()  # Could be list of strings or dicts

        # Normalize feeds: convert strings to dicts with default values
        self.feeds = [
            f if isinstance(f, dict) else {"url": f, "category": "", "articles": []}
            for f in raw_feeds
        ]

        self.ids.feed_list.clear_widgets()

        if not self.feeds:
            self.ids.status_label.text = "No feeds added. Tap + to add."
            self.ids.status_label.opacity = 1
            return
        else:
            self.ids.status_label.opacity = 0

        for feed in self.feeds:
            title = feed.get('url', 'No URL')
            articles = feed.get('articles', [])
            display_text = f"{title} ({len(articles)} articles)"
            item = OneLineListItem(text=display_text, on_release=lambda x, f=feed: self.open_feed(f))
            self.ids.feed_list.add_widget(item)

    def open_feed(self, feed):
        app = MDApp.get_running_app()
        app.current_feed = feed
        app.root.current = "article"

    def show_add_feed_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Add RSS Feed",
                type="custom",
                content_cls=AddFeedContent(),
                buttons=[
                    MDFlatButton(text="CANCEL", on_release=self.dismiss_dialog),
                    MDFlatButton(text="ADD", on_release=self.add_feed),
                ],
            )
        self.dialog.open()

    def dismiss_dialog(self, *args):
        self.dialog.dismiss()

    def add_feed(self, *args):
        content = self.dialog.content_cls
        url = content.url_input.text.strip()
        category = content.category_input.text.strip()
        if url:
            app = MDApp.get_running_app()
            app.add_feed(url, category)
            self.load_feeds()
        self.dialog.dismiss()


from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty

class AddFeedContent(MDBoxLayout):
    url = StringProperty("")
    category = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = "12dp"
        self.size_hint_y = None
        self.height = "120dp"
        from kivymd.uix.textfield import MDTextField

        self.url_input = MDTextField(
            hint_text="Feed URL",
            required=True,
            helper_text_mode="on_error",
            multiline=False,
        )
        self.category_input = MDTextField(
            hint_text="Category/Tag (optional)",
            multiline=False,
        )
        self.add_widget(self.url_input)
        self.add_widget(self.category_input)
