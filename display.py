import os
import feedparser
from tkinter import *
from tkinter import ttk
from tkinterhtml import HtmlFrame
from tkhtmlview import HTMLLabel
import urllib.request

# https://archive81.libsyn.com/rss
class Feed:

    def __init__(self, root):

        root.title("RSS Feed")

        mainframe = ttk.Frame(root, padding="10 10 12 12")
        self.mainframe = mainframe
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.title_list = Listbox(self.mainframe, height=20, width=40)
        self.title_list.bind('<<ListboxSelect>>', self.show_episode_description)
        # self.status_message = StringVar()
        self.scrollbar = ttk.Scrollbar(self.mainframe, orient=VERTICAL, command=self.title_list.yview)
        # self.status = ttk.Label(self.mainframe, textvariable=self.status_message, anchor=W).grid(row=3, column=6, columnspan=4)
        self.status = HTMLLabel(self.mainframe)
        self.status.grid(row=3, column=6, columnspan=4)
        self.feed_location = StringVar()
        feed_entry = ttk.Entry(self.mainframe, width=30, textvariable=self.feed_location)
        feed_entry.grid(column=3, row=1, sticky=(W, E))
        ttk.Label(self.mainframe, text="Feed").grid(column=2, row=1, sticky=(W, E))
        description = StringVar()
        self.description_message = ttk.Label(self.mainframe, textvariable=description, anchor='w')

        ttk.Button(self.mainframe, text="Get Feed", command=self.get_feed_from_url).grid(column=4, row=1, sticky=E)

        ttk.Label(self.mainframe, text="Titles").grid(column=2, row=2, sticky=(W, E))
        ttk.Button(self.mainframe, text="Get Titles", command=self.print_episode_titles).grid(column=3, row=2, sticky=W)

        feed_entry.focus()

    def get_feed_from_url(self, *args):
        try:

            feed_url = self.feed_location.get()
            feed = feedparser.parse(feed_url)
            self.feed_object = feed

            return feed
        except ValueError: "No URL provided"
        pass

    def get_feed_from_file(self, feed_file):
        file = os.path.join(os.getcwd(), feed_file)
        feed = feedparser.parse(file)
        return feed

    def print_episode_titles(self, *args):

        print(type(self.feed_object))
        for index, episode in enumerate(self.feed_object.entries):

            # print(f"episode number is {episode_number} and title is {episode.title}")
            self.title_list.insert(index, episode.title)

            self.title_list.grid(column=1, row=3, columnspan=3, rowspan=2)

            # self.title_list.pack()
            # yield episode.title
        self.scrollbar.grid(column=4, row=3, sticky=(N, S))
        self.title_list['yscrollcommand'] = self.scrollbar.set
        # self.title_list.configure(yscrollcommand= self.scrollbar.set)
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        self.title_list.select_set(0)
        self.title_list.bind('<<>ListboxSelect>', self.show_episode_description())

        self.download_name = StringVar()
        filename_to_download = ttk.Entry(self.mainframe, width=30, textvariable=self.download_name)
        filename_to_download.grid(column=3, row=4, sticky=(S))
        ttk.Label(self.mainframe, text="Episode name").grid(column=2, row=4, sticky=(W, S))
        self.select_episode_index = None
        ttk.Button(self.mainframe, text="Download Episode", command=self.download_episode()).grid(column=4, row=4, sticky=(E, S))

    def show_episode_description(self, *args):

        indexs = self.title_list.curselection()
        if len(indexs) ==1:

            index = int(indexs[0])

            episode = self.feed_object.entries[index]
            self.select_episode_index = index

            self.status.set_html(episode.description)
            """
            At the moment tkhtmlview needed to be modified so the change in this github issue is added
            https://github.com/bauripalash/tkhtmlview/pull/17
            
            Hopefully it will be updated on pypi
            """

    def download_episode(self, *args):
        print('hello')
        try:
            download_name = self.download_name.get()
            if self.select_episode_index is None:
                print(f"select episode has not been chosen yet.")
            else:
                download_location = self.feed_object.entries[self.select_episode_index]
                print(f'Printing {download_location} with the file name {download_name}')
            # episode = urllib.request.urlretrieve(download_location.link, download_name)

        except ValueError: "file_not_downloaded"
        # pass
        # urllib.request.urlretrieve("http://www.example.com/songs/mp3.mp3", "mp3.mp3")

    # def display_description(self, *args):
    #     print('working')
    #     description = StringVar()


root = Tk()
Feed(root)
root.mainloop()