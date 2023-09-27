
import xml.etree.ElementTree as ET
import os
import feedparser
import tkinter as tk
# https://en.wikipedia.org/wiki/Tkinter

def main(rss_file, rss_file_two):

    file = os.path.join(os.getcwd(), rss_file_two)
    # feed = feedparser.parse(file)
    feed = feedparser.parse('https://archive81.libsyn.com/rss')
    print(feed['feed']['title'])
    print(feed['feed']['description'])
    print('----------')
    print(feed.entries)
    print('----------')
    # for entry in feed.entries:
    #     print(entry.title)
    #     print(entry.published)
    #     print(entry.link)
#   tree = ET.parse(file)
#   print(tree)
#   root = tree.getroot()

#   new_kids = []
#   for child in root[0]:
#       for kids in child:
#           # print(f"Tag: {kids.tag} Text: {kids.text}")
#           if "enclosure url" == kids.tag:
#               print(f"Tag: {kids.tag} Text: {kids.text}")
#           elif "title" == kids.tag:
#               print(f"Tag: {kids.tag} Text: {kids.text}")
#           elif "link" == kids.tag:
#               print(f"Tag: {kids.tag} Text: {kids.text}")

            # print(kids.text)
        # new_kids.append(child.getchildren())
        # print(new_kids)



if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("config_file", type=str, help="Path to JSON config file")
    args = parser.parse_args()

    with open(args.config_file) as cf:
        config = json.load(cf)
    main(**config)
