
import xml.etree.ElementTree as ET
import os

def main(rss_file):

    file = os.path.join(os.getcwd(), rss_file)
    tree = ET.parse(file)
    print(tree)
    root = tree.getroot()

    new_kids = []
    for child in root[0]:
        for kids in child:
            # print(f"Tag: {kids.tag} Text: {kids.text}")
            if "enclosure url" == kids.tag:
                print(f"Tag: {kids.tag} Text: {kids.text}")
            elif "title" == kids.tag:
                print(f"Tag: {kids.tag} Text: {kids.text}")
            elif "link" == kids.tag:
                print(f"Tag: {kids.tag} Text: {kids.text}")

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