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
                "https://s.taobao.com/search?q=%E6%89%8B%E6%8F%90%E7%94%B5%E8%84%91&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306",
                "https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=laptop",
                "https://www.schukat.com/schukat/schukat_cms_en.nsf/index/CMSDF15D356B046D53BC1256D550038A9E0?OpenDocument&wg=U1232&refDoc=CMS322921A477B31844C125707B0034EB15",
                "https://www.schukat.com/schukat/schukat_cms_en.nsf/index/CMSB5A38F73D94252D2C125707B00357507?OpenDocument"]

    curr_url = ""

    root_path = ""

    threshold = 0

    def __init__(self):
        pass    

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
            # if curr_url != link and len(curr_url) != len(link):
            if curr_url != link:
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
                    output.write("Curr: {} | {}\n".format(curr.el.tag, curr.el.text))
                    for refer in refer_node_list:
                        if refer.el.text != None:
                            # if curr.el.text == refer.el.text and curr.el.tag == refer.el.tag:
                            if Node.is_same(curr.el, refer.el):
                                output.write("Refer: {} | {}\n".format(refer.el.tag, refer.el.text))
                                output.write("{}\n".format("Same"))
                                curr.duplicate_count = curr.duplicate_count + 1
                                break

        print("Done.")
        print("Counting number of children for each node...")

        result_node_list = []   

        for curr in curr_node_list:
            if curr.duplicate_count == 0 and curr.el.text != None and curr.el.tag not in const.UNWANTED_TAGS:
                # Commented, h* tags are not allowed to set attributes
                # print(curr.el.tag ," ", curr.el.attrib)           
                curr.el.set("fyp-web-miner", "content")
                result_node_list.append(curr)

        for node in curr_node_list:            
            curr_child_el = None
            index = 0
            node.same_child_count.append(0)
            curr_largest = -1

            for child_el in node.el.iterchildren():
                if child_el.tag != "meta":
                    curr_child_el = child_el
                    break

            for child_el in node.el.iterchildren():
                if child_el.tag != "meta":
                    if curr_child_el.tag == child_el.tag and curr_child_el.keys() == child_el.keys():                        
                        node.same_child_count[index] = node.same_child_count[index] + 1
                    else:
                        curr_child_el = child_el
                        index = index + 1                    
                        node.same_child_count.append(0)

                    if node.same_child_count[index] > curr_largest:
                            curr_largest = node.same_child_count[index]
                            node.largest_child_trait["tag"] = curr_child_el.tag
                            node.largest_child_trait["keys"] = curr_child_el.keys()                    

            node.same_child_count.sort(reverse=True)

        selected_node = curr_node_list[0]

        for node in curr_node_list:
            if node.same_child_count[0] > selected_node.same_child_count[0]:
                selected_node = node

        selected_node.el.set("fyp-web-miner", "same-child-count")

        self.write_info(curr_url, curr_node_list)

        print("Done.")
        print("Writing nodes into file...") 

        self.write_same_children(curr_url, selected_node)
        self.write_diff_pages(curr_url, result_node_list)

        print("Done.")

    def build_dom(self, curr_url, root):
        node_list = []

        for element in root.iter():
            # if element.tag != "script" and element.tag != "style":
                node = Node()
                node.el = element
                # node.tag = element.tag

                if node.el.text != None:
                    node.el.text = node.el.text.strip()

                # node.tag = element.tag[const.TAG_TRIM_LEN:]

                for parent in node.el.iterancestors():
                    node.parent_count = node.parent_count + 1

                node_list.append(node)

        # for p_node in node_list:
        #     for c_node in node_list:
        #         if (Node.is_same(p_node.el, c_node.el.getparent())):
        #             p_node.children.append(c_node)

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

    # def calculate_td(self, node):
    #     node.chars += len(node.el.text) if node.el.text != None else 0

    #     for child_node in node.children:
    #         node.tags += child_node.tags

    #         if child_node.el.tag != "a":
    #             node.chars += child_node.chars

    #     node.td = float(node.chars) / node.tags

    # def init_ctd(self, node):
    #     node.all_chars += len(node.el.text) if node.el.text != None else 0

    #     if node.el.tag != "a":
    #         node.non_link_chars += node.all_chars
    #     else:
    #         node.link_chars += node.all_chars
    #         node.link_tags += 1

    #     for child_node in node.children:
    #         node.all_tags += child_node.all_tags
    #         node.all_chars += child_node.all_chars

    #         if child_node.el.tag != "a":
    #             node.non_link_chars += child_node.non_link_chars
    #         else:
    #             node.link_chars += child_node.link_chars
    #             node.link_tags += child_node.link_tags

    #     if node.el.tag == "body":
    #         Node.body_chars = node.all_chars
    #         Node.body_link_chars = node.link_chars

    # def calculate_ctd(self, node):
    #     link_chars_proportion = (float(node.all_chars) /
    #                              node.link_chars) if node.link_chars != 0 else 1
    #     link_tags_proportion = (float(node.all_tags) /
    #                             node.link_tags) if node.link_tags != 0 else 1
    #     non_link_chars = node.non_link_chars if node.non_link_chars != 0 else 1

    #     node.ctd = float(node.all_chars) / node.all_tags * (math.log10(math.log(
    #         (float(node.chars) / non_link_chars * node.link_chars) +
    #         (float(Node.body_link_chars) / Node.body_chars * node.all_chars) + math.e)) *
    #         (link_chars_proportion * link_tags_proportion))
    # def calculate_ctd(self, node):
    #     link_chars_proportion = (float(node.all_chars) /
    #                              node.link_chars) if node.link_chars != 0 else 1
    #     link_tags_proportion = (float(node.all_tags) /
    #                             node.link_tags) if node.link_tags != 0 else 1
    #     non_link_chars = node.non_link_chars if node.non_link_chars != 0 else 1

    #     node.ctd = float(node.all_chars) / node.all_tags * (math.log10(math.log(
    #         (float(node.chars) / non_link_chars * node.link_chars) +
    #         (float(Node.body_link_chars) / Node.body_chars * node.all_chars) + math.e)) *
    #         (link_chars_proportion * link_tags_proportion))

    def write_same_children(self, curr_url, selected_node):
        root_path = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), "../")

        out_name = curr_url

        if curr_url[-1] == "/":
            out_name = curr_url[:len(curr_url) - 1]

        out_name = root_path + const.DIR_OUTPUT_SAME_CHILDREN + helper.as_valid_filename(out_name[out_name.find("//") + 2:]) + ".txt"

        with codecs.open(out_name, "w", "utf-8") as output:
            for el in selected_node.el.iterchildren():
                if selected_node.largest_child_trait.get("tag") == el.tag and selected_node.largest_child_trait.get("keys") == el.keys():
                    for child_el in el.iter():
                        # if child_el.get("fyp-web-miner") == "content":
                        if child_el.text != None and child_el.tag not in const.UNWANTED_TAGS:
                            output.write("{}\n".format(child_el.text))
                
                output.write("{}\n".format("-" * 64))

    def write_diff_pages(self, curr_url, result_node_list):
        root_path = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), "../")

        out_name = curr_url

        if curr_url[-1] == "/":
            out_name = curr_url[:len(curr_url) - 1]

        out_name = root_path + const.DIR_OUTPUT_DIFF_PAGES + helper.as_valid_filename(out_name[out_name.find("//") + 2:]) + ".txt"

        with codecs.open(out_name, "w", "utf-8") as output:
            # for node in reversed(node_list):
            #     self.calculate_td(node)

            #     # print("%8s | Chars: %8d, Tags: %6d, TD: %08.2f" % (node.tag, node.chars, node.tags, node.td))

            #     # if node.tag == "body":
            #     #     threshold = node.td

            #     self.init_ctd(node)

            for node in result_node_list:
                output.write("{} | {}\n".format("-" * node.parent_count, node.el.text))

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
                # Same children test info
                # output.write("{} | {} | {} | {} | {}\n".format("-" * info.parent_count, info.el.tag, info.same_child_count, info.el.text, info.el.items()))

                # Different pages test info
                output.write("{} | {} | {} | {} | {}\n".format("-" * info.parent_count, info.el.tag, info.duplicate_count, info.el.text, info.el.items()))
