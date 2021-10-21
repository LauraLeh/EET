import sys
import os
from html.parser import HTMLParser


"""Reads the contents of each html file into a string."""
def read_file(path):
    with open(path, "r", encoding='utf-8') as f:
        return f.read()

"""Gets the absolute filepaths of the crawled html files only.
Each of the files' content is appended to a list, which is returned."""
def get_files(directory_path):
    html_files = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                html_files.append(read_file(file_path))
    return html_files


"""The HTML Parser looks out for relevant tags. If one such start-tag 
is encountered, its content is read into a string, until the tag closes."""
class Parser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.relevant_tags = ["p", "div", "h1", "h2", "h3", "blockquote"]
        self.is_reading_text = False
        self.current_tag = ""
        self.text = ""

    def handle_starttag(self, tag, attrs):
        if tag in self.relevant_tags:
            self.current_tag = tag
            # the "div" tag has a specific relevance constraint:
            # consider only if it describes the article's author.
            if tag == "div":
                for name, value in attrs:
                    if name == "class" and value == "authorline__author":
                        self.is_reading_text = True
            else:
                self.is_reading_text = True

    def handle_endtag(self, tag):
        if tag == self.current_tag:
            self.is_reading_text = False

    def handle_data(self, data):
        if self.is_reading_text:
            self.text += data


def main():
    if len(sys.argv) != 2:
        exit()

    doc_directory = str(sys.argv[1])
    html_files = get_files(doc_directory)
    # initialize parser and process the html files
    parser = Parser()
    for file in html_files:
        parser.feed(file)

    print(" ".join(parser.text.split()))


if __name__ == '__main__':
    main()