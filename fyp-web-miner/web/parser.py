import urllib
from urllib.request import urlopen
import codecs
import math
import urllib.parse as urlparse

from lxml import etree
from lxml.html import tostring, html5parser
from lxml.html.clean import Cleaner
import lxml

from requests_html import HTMLSession

from pprint import pprint
import os.path

from entity.node import Node
from misc import const, helper

# import tensorflow as tf


class Parser:
    url_list = ["https://www.lazada.com.my/catalog/?q=laptop&_keyori=ss&from=input&spm=a2o4k.home.search.go.75f824f6QLmzE4",
                "http://www.11street.my/totalsearch/TotalSearchAction/searchTotal.do?targetTab=T&isGnb=Y&prdType=&category=&cmd=&pageSize=60&lCtgrNo=0&mCtgrNo=0&sCtgrNo=0&ctgrType=&fromACK=&gnbTag=TO&schFrom=&tagetTabNm=T&aKwdTrcNo=&aUrl=&kwd=laptop&callId=7274c0ac642e390b8fc",
                "https://shopee.com.my/search/?keyword=laptop",
                "https://www.lelong.com.my/catalog/all/list?TheKeyword=laptop",
                "https://www.tarc.com.my"]

    curr_url = ""

    root_path = ""

    threshold = 0

    def __init__(self):
        pass

    def start_parsing_with_js(self):
        root_path = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), "../")

        curr_url = self.url_list[5]

        session = HTMLSession()
        r = session.get(curr_url)

        r.html.render()

        out_name = ""

        if curr_url[-1] == "/":
            out_name = curr_url[:len(curr_url) - 1]

        out_name = root_path + const.DIR_OUTPUT + \
            out_name[out_name.find("//") + 2:] + ".txt"

        with codecs.open(out_name, "w", "utf-8") as output:
            output.write("{}\n".format(r.html.lxml.getroot()))

    def start_parsing(self):
        # path = os.path.join(os.path.abspath(
        #     os.path.dirname(__file__)), self.url_list[2])       

        curr_url = self.url_list[0]

        # cleaner=Cleaner()

        # cleaner.style=True
        # cleaner.kill_tags=["textarea"]

        # request=urllib.request.Request(curr_url)
        # request.add_header('User-Agent', 'Mozilla/5.0')

        # url=urlopen(request)

        # tree = cleaner.clean_html(lxml.html.parse(url))

        # tree=lxml.html.parse(url)
        # root=tree.getroot()

        #############################################       

        print("Rendering page for current url...")
        
        session = HTMLSession()
        r = session.get(curr_url)

        r.html.render()
        root = r.html.lxml

        link_list = r.html.absolute_links

        link_dict_list = []

        curr_url_qs = urlparse.parse_qs(urlparse.urlparse(curr_url).query)

        link_dict_list.append({"url": curr_url, "query": curr_url_qs})

        print("Done.")
        print("Searching for similar url by queries...")

        for link in link_list:
            link_qs = urlparse.parse_qs(urlparse.urlparse(link).query)

            has_same_query = True

            # if len(curr_url_qs) <= len(link_qs) and curr_url != link:
            if curr_url != link and len(curr_url) != len(link):
                for key, value in curr_url_qs.items():
                    if key not in link_qs:
                        has_same_query = False
                        break
            else:
                has_same_query = False

            if has_same_query:
                link_dict_list.append({"url": link, "query": link_qs})

        def sort_link(a):
            return len(a["url"])

        link_dict_list.sort(key=sort_link)

        ##############################################

        self.write_query(curr_url, link_dict_list)
        
        print("Done.")
        print("Building DOM for current page...")

        curr_node_list = self.build_dom(curr_url, root)

        self.write_info(curr_url, curr_node_list)

        print("Done.")
        print("Reference url: ", link_dict_list[1]["url"])
        print("Rendering page for reference url...")

        session = HTMLSession()
        r = session.get(link_dict_list[1]["url"])

        r.html.render()
        root = r.html.lxml

        print("Done.")
        print("Building DOM for reference page...")

        refer_node_list = self.build_dom(link_dict_list[1]["url"], root)

        self.write_info(link_dict_list[1]["url"], refer_node_list)

        result_node_list = []

        print("Done.")
        print("Searching for duplicated nodes...")    

        root_path = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), "../")

        out_name = curr_url

        if curr_url[-1] == "/":
            out_name = curr_url[:len(curr_url) - 1]

        out_name = root_path + const.DIR_OUTPUT_LOG + helper.as_valid_filename(out_name[out_name.find("//") + 2:]) + ".txt"

        with codecs.open(out_name, "w", "utf-8") as output:
            for curr in curr_node_list:
                if curr.el.text != None:
                    output.write("Curr: {} | {}\n".format(curr.tag, curr.el.text))
                    for refer in refer_node_list:
                        if refer.el.text != None:
                            if curr.el.text == refer.el.text and curr.tag == refer.tag:
                                output.write("Refer: {} | {}\n".format(refer.tag, refer.el.text))
                                output.write("{}\n".format("Same"))
                                curr.duplicate_count = curr.duplicate_count + 1
                                break                    

        for curr in curr_node_list:
            if curr.duplicate_count == 0 and curr.el.text != None:
                result_node_list.append(curr)

        print("Done.")
        print("Writing nodes into file...")

        self.write_node(curr_url, result_node_list)

        print("Done.")

    def build_dom(self, curr_url, root):
        node_list = []

        for element in root.iter():
            if element.tag != "script" and element.tag != "style":
                node = Node()
                node.el = element
                node.tag = element.tag
                # node.tag = element.tag[const.TAG_TRIM_LEN:]

                node_list.append(node)

        for p_node in node_list:
            for c_node in node_list:
                if (Node.is_same(p_node.el, c_node.el.getparent())):
                    p_node.children.append(c_node)

        # self.write_node(curr_url, node_list)

        return node_list

        #     # print("Tag: %s, TD: %s, Threshold: %s" % (node.tag, node.td, threshold))

        #     if node.td >= threshold:
        #         node.is_content = True

        #         if node.el.text != None:
        #             output.write("{}\n".format(node.el.text))
        #             # print("%s" % (node.el.text))

        # for node in node_list:
        #     self.calculate_ctd(node)
        #     print("%8s | All chars: %4d, All tags: %3d, Link chars: %4d, Non-link chars: %4d, Link tags: %4d, TD: %04.2f, CTD: %06.2f" %
        #         (node.tag, node.all_chars, node.all_tags, node.link_chars, node.non_link_chars, node.link_tags, node.td, node.ctd))

        # return root

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
        link_chars_proportion = (float(node.all_chars) /
                                 node.link_chars) if node.link_chars != 0 else 1
        link_tags_proportion = (float(node.all_tags) /
                                node.link_tags) if node.link_tags != 0 else 1
        non_link_chars = node.non_link_chars if node.non_link_chars != 0 else 1

        node.ctd = float(node.all_chars) / node.all_tags * (math.log10(math.log(
            (float(node.chars) / non_link_chars * node.link_chars) +
            (float(Node.body_link_chars) / Node.body_chars * node.all_chars) + math.e)) *
            (link_chars_proportion * link_tags_proportion))

    def write_node(self, curr_url, node_list):
        root_path = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), "../")

        out_name = curr_url

        if curr_url[-1] == "/":
            out_name = curr_url[:len(curr_url) - 1]

        out_name = root_path + const.DIR_OUTPUT_NODE + helper.as_valid_filename(out_name[out_name.find("//") + 2:]) + ".txt"

        with codecs.open(out_name, "w", "utf-8") as output:
            # for node in reversed(node_list):
            #     self.calculate_td(node)

            #     # print("%8s | Chars: %8d, Tags: %6d, TD: %08.2f" % (node.tag, node.chars, node.tags, node.td))

            #     # if node.tag == "body":
            #     #     threshold = node.td

            #     self.init_ctd(node)

            for node in node_list:
                output.write("{}\n".format(node.el.text))
                # pass

    def write_query(self, curr_url, query_list):
        root_path = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), "../")

        out_name = curr_url

        if curr_url[-1] == "/":
            out_name = curr_url[:len(curr_url) - 1]

        out_name = root_path + const.DIR_OUTPUT_QUERY + helper.as_valid_filename(out_name[out_name.find("//") + 2:]) + ".txt"

        with codecs.open(out_name, "w", "utf-8") as output:
            for query in query_list:
                output.write("{}\n".format(query.items()))

    def write_info(self, curr_url, info_list):
        root_path = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), "../")

        out_name = curr_url

        if curr_url[-1] == "/":
            out_name = curr_url[:len(curr_url) - 1]

        out_name = root_path + const.DIR_OUTPUT_INFO + helper.as_valid_filename(out_name[out_name.find("//") + 2:]) + ".txt"

        with codecs.open(out_name, "w", "utf-8") as output:
            for info in info_list:
                output.write("{} | {} | {}\n".format(info.tag, info.el.text, info.el.items()))
