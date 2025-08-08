from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem, TwoLineAvatarListItem, ImageLeftWidget
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
import webbrowser

KV = '''
<ArticleScreen>:
    name: "article"
    BoxLayout:
        orientation: "vertical"

        MDToolbar:
            title: "Articles"
            elevation: 10
            left_action_items: [["arrow-left", lambda x: root.go_back()]]

        ScrollView:
            MDList:
                id: article_list

        MDLabel:
            id: status_label
            text: "No articles available."
            halign: "center"
            size_hint_y: None
            height: "48dp"
            opacity: 0
'''

class ArticleScreen(MDScreen):
    article_list = ObjectProperty(None)
    articles = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_string(KV)

    def on_pre_enter(self):
        app = MDApp.get_running_app()
        feed = getattr(app, 'current_feed', None)
        self.ids.article_list.clear_widgets()
        if not feed or not feed.get('articles'):
            self.ids.status_label.opacity = 1
            return
        else:
            self.ids.status_label.opacity = 0

        self.articles = feed['articles']
        for article in self.articles:
            title = article.get('title', 'No Title')
            summary = article.get('summary', '')
            thumbnail = article.get('thumbnail', None)
            item = TwoLineAvatarListItem(
                text=title,
                secondary_text=summary[:100] + '...' if len(summary) > 100 else summary,
                on_release=lambda x, a=article: self.show_article_detail(a)
            )
            if thumbnail:
                image = ImageLeftWidget(source=thumbnail)
                item.add_widget(image)
            self.ids.article_list.add_widget(item)

    def go_back(self):
        app = MDApp.get_running_app()
        app.root.current = "home"

    def show_article_detail(self, article):
        dialog = MDDialog(
            title=article.get('title', 'No Title'),
            text=article.get('summary', ''),
            size_hint=(0.9, None),
            height="400dp",
            buttons=[
                MDFlatButton(
                    text="OPEN IN BROWSER",
                    on_release=lambda x: self.open_in_browser(article.get('link'))
                ),
                MDFlatButton(
                    text="CLOSE",
                    on_release=lambda x: dialog.dismiss()
                ),
            ],
        )
        dialog.open()

    def open_in_browser(self, url):
        if url:
            webbrowser.open(url)

