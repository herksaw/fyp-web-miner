from web.parser import Parser

from lxml import etree
from lxml import html
from lxml.html import tostring, html5parser

if __name__ == "__main__":
    parser = Parser()
    
    print(html.tostring(parser.start_parsing()))
