import feedparser
from kivy.uix.button import Button
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.textinput import TextInput
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivymd.uix.screenmanager import ScreenManager
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import MDList, OneLineListItem


class MainBox(MDFloatLayout):
    def __init__(self, **kwargs):
        super(MainBox, self).__init__(**kwargs)
        self.cols = 2
        # self.add_widget(MDLabel(text="Enter RSS URL:"), pos=(250, 400))
        self.URL = TextInput(font_size=25, multiline=False, size_hint=(0.9, 0.1), pos=(25, 400))
        self.add_widget(self.URL)
class RssApp(MDApp):
    def build(self):
        self.screenManager = ScreenManager()
        self.mainScreen = Screen(name="main screen")
        self.tableScreen = Screen(name="table screen")
        self.mainBox = MainBox()
        self.buttonGo = Button(text="Go!", font_size=30, background_color=[1, 0, 0, 1], size_hint=(0.9, 0.1),
                               pos=(25, 100))
        self.buttonGo.bind(on_press=self.search)
        self.mainBox.add_widget(self.buttonGo)
        self.mainScreen.add_widget(self.mainBox)
        self.screenManager.add_widget(self.mainScreen)
        self.screenManager.current = "main screen"
        self.listView = MDList()
        scroll = ScrollView()
        scroll.add_widget(self.listView)
        self.tableScreen.add_widget(scroll)
        self.tableScreen.add_widget(Button(text="Exit!", font_size=30, background_color=[1, 0, 0, 1], size_hint=(1, 0.1),
                                 pos=(0, 0), on_press=self.returnMain))
        self.screenManager.add_widget(self.tableScreen)

        return self.screenManager
    def search(self, instance):
        URL = self.mainBox.URL.text
        self.mainBox.URL.text = ""
        feed = parser(URL)
        if feed.bozo == True:
            return
        allHeadlines = getHeadlines(feed)
        for i in allHeadlines:
            items = OneLineListItem(text=i)
            self.listView.add_widget(items)
        self.screenManager.current = "table screen"

    def returnMain(self,intstance):
        self.listView.clear_widgets()
        self.screenManager.current = "main screen"


def parser(rss_url):  # функция получает линк на рсс ленту, возвращает распаршенную ленту с помощью feedpaeser
    return feedparser.parse(rss_url)


def getHeadlines(feed):  # функция для получения заголовков новости
    headlines = []
    for newsitem in feed['items']:
        headlines.append(newsitem['title'])
    return headlines


def getDates(feed):  # функция для получения даты публикации новости
    dates = []
    for newsitem in feed['items']:
        dates.append(newsitem['published'])
    return dates

if __name__ == "__main__":
    RssApp().run()
