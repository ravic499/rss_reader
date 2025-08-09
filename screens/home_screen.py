from kivymd.uix.screen import MDScreen
from kivymd.uix.list import TwoLineRightIconListItem, IconRightWidget
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
        app = MDApp.get_running_app()
        app.load_feeds()  # ✅ This ensures articles are fetched
        self.load_feeds()

    def load_feeds(self):
        app = MDApp.get_running_app()
        # Get current feeds directly from the app instance
        raw_feeds = app.feeds

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

            item = TwoLineRightIconListItem(
                text=display_text,
                secondary_text=feed.get('category', ''),
                on_release=lambda x, f=feed: self.open_feed(f)
            )
            delete_button = IconRightWidget(icon="delete", on_release=lambda x, f=feed: self.delete_feed(f))
            item.add_widget(delete_button)
            self.ids.feed_list.add_widget(item)

    def open_feed(self, feed):
        app = MDApp.get_running_app()
        app.set_current_feed(feed)  # ✅ Updated to use method from main.py
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

    def delete_feed(self, feed):
        app = MDApp.get_running_app()

        def confirm_delete(*args):
            app.remove_feed(feed.get('url'))
            self.load_feeds()
            dialog.dismiss()

        dialog = MDDialog(
            title="Delete Feed?",
            text=f"Are you sure you want to delete the feed:\n{feed.get('url')}?",
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: dialog.dismiss()),
                MDFlatButton(text="DELETE", on_release=confirm_delete),
            ],
        )
        dialog.open()


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
