import os
import tkinter

import feedparser
from tkinter import *
from tkinter import ttk
from tkhtmlview import HTMLLabel
import threading
import queue
from functools import partial
import os
import requests


# https://archive81.libsyn.com/rss
class Feed:

    def __init__(self, root):

        root.title("RSS Feed")

        mainframe = ttk.Frame(root, padding="10 10 12 12")
        self.mainframe = mainframe

        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.right_click = ttk.Label(root, text="Right click menu")
        # self.right_click.pack()
        self.menu = tkinter.Menu(root, tearoff=0)
        self.menu.add_command(label="Cut")
        self.menu.add_command(label="Copy")
        self.menu.add_command(label="Paste")
        self.menu.add_separator()
        self.right_click.bind("<Button-3>", self.do_popup)
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
        self.filename_to_download = ttk.Entry(self.mainframe, width=30)

        feed_entry.focus()

    def do_popup(self, event):
        try:
            self.menu(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()
    def get_feed_from_url(self):
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

    def print_episode_titles(self):

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
        # filename_to_download = ttk.Entry(self.mainframe, width=30)
        self.filename_to_download.grid(column=3, row=4, sticky=(S))

        ttk.Label(self.mainframe, text="Episode name").grid(column=2, row=4, sticky=(W, S))
        self.select_episode_index = None
        ttk.Button(self.mainframe, text="Download Episode", command=self.download_episode).grid(column=4, row=4, sticky=(E, S))

    def show_episode_description(self):

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
            # , textvariable = self.download_name
            self.filename_to_download.delete(0, END)
            self.filename_to_download.insert(0, episode.title + '.mp3')
            print(episode.title)

    def download(self, q, download_file, destination):
        print('working')
        response = requests.get(download_file, stream=True)
        file_size = int(response.headers.get('Content-Length'))
        with open(destination, 'wb') as file:
            for chunk in response.iter_content(chunk_size=100_000):
                file.write(chunk)
                q.put(len(chunk)/ file_size * 100)

                self.mainframe.event_generate('<<Progress>>')
        self.mainframe.event_generate('<<Done>>')
        # with requests.get(download_file, stream=True) as downloading:
        #     downloading.raise_for_status()
        #     file_size = int(downloading.headers.get('Content-Length'))

    def updater(self, pb, q, event):
        pb['value'] += q.get()
    def download_complete(self):
        print('FINISHED')
    def download_episode(self):
        print('hello')
        try:
            download_name = self.download_name.get()
            if self.select_episode_index is None:
                print(f"select episode has not been chosen yet.")
            else:
                download_location = self.feed_object.entries[self.select_episode_index]
                print(self.filename_to_download.get())
                print(f'Printing {download_location.title} with the file name \" {download_name} \" ')
                curent_dir = os.path.abspath(os.getcwd())

                download_destination = os.path.join(curent_dir, self.filename_to_download.get())

                download_from = 0
                for dictionary in download_location.links:
                    if dictionary.type == 'audio/mpeg':
                        download_from = dictionary.href
                        break

                print(download_from)
                q = queue.Queue()
                progress = ttk.Progressbar(self.mainframe, orient='horizontal', mode='determinate', length=280 )
                # progress.pack(padd=20)
                progress.grid( column=6, row=4, sticky=(E, S) )
                update_handler = partial(self.updater, progress, q)
                self.mainframe.bind('<<Progress>>', update_handler)

                thread = threading.Thread(target=self.download, args=( q , download_from, download_destination), daemon=True)
                print('start')
                print(download_destination)
                thread.start()
                print('working')
                self.mainframe.bind('<<Done>>', lambda event: self.download_complete() )
                # with requests.get(download_location.links[0]['href'], stream=True) as download:
                #     download.raise_for_status()
                #     print(download.status_code)
                #     file_size = int(download.headers.get('Content-Length'))
                #     progress["maximum"] = file_size
                #     chunks = 0
                #     with open(download_path, 'wb') as file:
                #         for chunk in download.iter_content(chunk_size=30):
                #             file.write(chunk)
                #             q.put(len(chunk)/ file_size * 100)
                #             self.mainframe.event_generate('<<Progress>>')
                #
                #             # chunks_as_len = (len(chunk))
                #             # chunks += int(chunks_as_len)
                #             # progress["value"] += int(chunks_as_len)
                #             # # progress["value"] = chunk
                #         self.mainframe.event_generate('<<Done>>')
                #         print('done')
                #         print('Chunks total: ' + str(chunks))
                #         print("file size: " + str(file_size))

                # open(download_path, 'wb').write(download.content)
                # episode = urllib.request.urlretrieve(download_location.link, download_name)

        except ValueError: "file_not_downloaded"
        # pass
        # urllib.request.urlretrieve("http://www.example.com/songs/mp3.mp3", "mp3.mp3")



root = Tk()
Feed(root)
root.mainloop()
