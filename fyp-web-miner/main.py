from web.parser import Parser

from lxml import etree
from lxml import html
from lxml.html import tostring, html5parser

# import tensorflow as tf

if __name__ == "__main__":
    parser = Parser()

    parser.start_parsing()

    # parser.start_parsing_with_js()
