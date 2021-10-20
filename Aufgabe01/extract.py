
import os

for root, dirs, files in os.walk("www.tagesschau.de"):
    for name in files:
        if name.endswith(".html"):
            #
    for name in dirs:
        print(os.path.join(root, name))


from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):