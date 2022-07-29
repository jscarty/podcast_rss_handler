import os
import feedparser
from tkinter import *
from tkinter import ttk

class Feed:

    def __init__(self, root):

        root.title("RSS Feed")

        mainframe = ttk.Frame(root, padding="10 10 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.title_list = Listbox(mainframe, height=20, width=40)
        self.feed_location = StringVar()
        feed_entry = ttk.Entry(mainframe, width=30, textvariable=self.feed_location)
        feed_entry.grid(column=3, row=1, sticky=(W, E))
        ttk.Label(mainframe, text="Feed").grid(column=2, row=1, sticky=(W, E))


        ttk.Button(mainframe, text="Get Feed", command=self.get_feed_from_url).grid(column=5, row=1, sticky=E)

        ttk.Label(mainframe, text="Titles").grid(column=2, row=3, sticky=N)
        ttk.Button(mainframe, text="Get Titles", command=self.print_episode_titles).grid(column=3, row=3, sticky=W)

        feed_entry.focus()

    def get_feed_from_url(self, *args):
        try:

            feed_url = self.feed_location.get()
            print(feed_url)
            feed = feedparser.parse(feed_url)
            self.feed_object = feed
            print("Got feed")
            print(type(self.feed_object))
            return feed
        except ValueError: "No URL provided"
        pass

    def get_feed_from_file(self, feed_file):
        file = os.path.join(os.getcwd(), feed_file)
        feed = feedparser.parse(file)
        return feed

    def print_episode_titles(self, *args):

        titles = []
        print(type(self.feed_object))
        print("trying")
        episode_number = len(self.feed_object.entries)
        for episode in self.feed_object.entries:

            print(episode.title)
            titles.append(episode.title)
            self.title_list.insert(episode_number, episode.title)
            episode_number -= 1
            self.title_list.grid(column=0, row=4, sticky=S)
            # self.title_list.pack()
            # yield episode.title
        # titles_string = StringVar(value=titles)
        # Listbox  = Listbox(ma)
        # ttk.Label(mainframe, textvariable=self.)


root = Tk()
Feed(root)
root.mainloop()