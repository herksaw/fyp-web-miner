import urllib.request

from lxml import etree
from lxml.html import tostring, html5parser

from pprint import pprint

class Parser:
    url_list = ["https://forum.lowyat.net/", "https://www.google.com/"]

    def __init__(self):
        pass

    def start_parsing(self):
        # fp = urllib.request.urlopen(self.url_list[0])
        # in_bytes = fp.read()

        # out_str = str(in_bytes, errors="replace")
        # fp.close()

        # html = etree.HTML(out_str)

        #result = etree.tostring(html, pretty_print=True, method="html")

        tree = html5parser.parse(self.url_list[1])
        
        pprint(dir(tree))
        pprint(dir(tree.getroot()))

        return tree.getroot()

