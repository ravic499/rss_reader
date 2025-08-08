from kivy.app import App
from kivy.uix.label import Label

class RSSReader(App):
    def build(self):
        return Label(text="Welcome to RSS Reader!")

if __name__ == "__main__":
    RSSReader().run()
