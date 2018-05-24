import urllib
from urllib.request import urlopen
import codecs
import math

from lxml import etree
from lxml.html import tostring, html5parser
from lxml.html.clean import Cleaner
import lxml

from pprint import pprint
import os.path

from entity.node import Node
from misc import const

# import tensorflow as tf


class Parser:
    url_list = ["http://www.tarc.edu.my/",
                "https://forum.lowyat.net/",
                "https://www.google.com/",
                "https://www.lazada.com.my/",]

    curr_url = ""

    root_path = ""

    threshold = 0

    def __init__(self):
        pass

    def start_parsing(self):
        # path = os.path.join(os.path.abspath(
        #     os.path.dirname(__file__)), self.url_list[2])

        root_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../")

        curr_url = self.url_list[3]

        cleaner = Cleaner()

        cleaner.style = True
        cleaner.kill_tags = ["textarea"]

        request = urllib.request.Request(curr_url)
        request.add_header('User-Agent', 'Mozilla/5.0')

        url = urlopen(request)

        tree = cleaner.clean_html(lxml.html.parse(url))                

        # print(lxml.html.tostring(tree))

        root = tree.getroot()

        node_list = []

        for element in root.iter():
            node = Node()
            node.el = element
            node.tag = element.tag
            # node.tag = element.tag[const.TAG_TRIM_LEN:]

            node_list.append(node)

        for p_node in node_list:
            for c_node in node_list:
                if (Node.is_same(p_node.el, c_node.el.getparent())):
                    p_node.children.append(c_node)

        out_name = ""

        if curr_url[-1] == "/":
            out_name = curr_url[:len(curr_url) - 1]

        out_name = root_path + const.DIR_OUTPUT + out_name[out_name.find("//") + 2:] + ".txt"

        with codecs.open(out_name, "w", "utf-8") as output:
            for node in reversed(node_list):
                self.calculate_td(node)
                print("%8s | Chars: %8d, Tags: %6d, TD: %08.2f" % (node.tag, node.chars, node.tags, node.td))

                if node.tag == "body":
                    threshold = node.td

                # self.init_ctd(node)

            for node in node_list:
                # print("Tag: %s, TD: %s, Threshold: %s" % (node.tag, node.td, threshold))

                if node.td >= threshold:
                    node.is_content = True

                    if node.el.text != None:
                        output.write("{}\n".format(node.el.text))
                        # print("%s" % (node.el.text))

        # for node in node_list:            
        #     self.calculate_ctd(node)            
        #     print("%8s | All chars: %4d, All tags: %3d, Link chars: %4d, Non-link chars: %4d, Link tags: %4d, TD: %04.2f, CTD: %06.2f" % 
        #         (node.tag, node.all_chars, node.all_tags, node.link_chars, node.non_link_chars, node.link_tags, node.td, node.ctd))

        return root

    def calculate_td(self, node):
        node.chars += len(node.el.text) if node.el.text != None else 0

        for child_node in node.children:
            node.tags += child_node.tags

            if child_node.tag != "a":
                node.chars += child_node.chars
        
        node.td = float(node.chars) / node.tags

    def init_ctd(self, node):
        node.all_chars += len(node.el.text) if node.el.text != None else 0

        if node.tag != "a":
            node.non_link_chars += node.all_chars
        else:
            node.link_chars += node.all_chars
            node.link_tags += 1

        for child_node in node.children:
            node.all_tags += child_node.all_tags
            node.all_chars += child_node.all_chars

            if child_node.tag != "a":
                node.non_link_chars += child_node.non_link_chars
            else:
                node.link_chars += child_node.link_chars
                node.link_tags += child_node.link_tags

        if node.tag == "body":
            Node.body_chars = node.all_chars
            Node.body_link_chars = node.link_chars

    def calculate_ctd(self, node):
        link_chars_proportion = (float(node.all_chars) / node.link_chars) if node.link_chars != 0 else 1
        link_tags_proportion = (float(node.all_tags) / node.link_tags) if node.link_tags != 0 else 1
        non_link_chars = node.non_link_chars if node.non_link_chars != 0 else 1        

        node.ctd = float(node.all_chars) / node.all_tags * (math.log10(math.log(
            (float(node.chars) / non_link_chars * node.link_chars) +
            (float(Node.body_link_chars) / Node.body_chars * node.all_chars) + math.e)) * 
            (link_chars_proportion * link_tags_proportion))
        
