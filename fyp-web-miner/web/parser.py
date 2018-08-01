import urllib
from urllib.request import urlopen
import codecs
import math
import decimal
import urllib.parse as urlparse
import json
from pprint import pprint
import os.path
import time

from lxml import etree
from lxml.html import tostring, html5parser
from lxml.html.clean import Cleaner
import lxml
from requests_html import HTMLSession
import jsonpickle

from entity.node import Node
from entity.tree import Tree
from misc import const, helper
from web.mdr_util import MDRUtil

# import tensorflow as tf


class Parser:
    root_path = ""

    threshold = 0

    def __init__(self):
        pass

    # def start_parsing(self, curr_url):
    #     print("Starting different pages method...")

    #     # path = os.path.join(os.path.abspath(
    #     #     os.path.dirname(__file__)), self.url_list[2])

    #     # cleaner=Cleaner()

    #     # cleaner.style=True
    #     # cleaner.kill_tags=["textarea"]

    #     # request=urllib.request.Request(curr_url)
    #     # request.add_header('User-Agent', 'Mozilla/5.0')

    #     # url=urlopen(request)

    #     # tree = cleaner.clean_html(lxml.html.parse(url))

    #     # tree=lxml.html.parse(url)
    #     # root=tree.getroot()

    #     #############################################

    #     print("Rendering page for current url...")

    #     session = HTMLSession()
    #     r = session.get(curr_url)

    #     r.html.render()
    #     root = r.html.lxml

    #     link_list = r.html.absolute_links

    #     link_dict_list = []

    #     curr_url_qs = urlparse.parse_qs(urlparse.urlparse(curr_url).query)

    #     link_dict_list.append({"url": curr_url, "query": curr_url_qs})

    #     print("Done.")
    #     print("Searching for similar url by queries...")

    #     for link in link_list:
    #         link_qs = urlparse.parse_qs(urlparse.urlparse(link).query)

    #         has_same_query = True

    #         # if len(curr_url_qs) <= len(link_qs) and curr_url != link:
    #         # if curr_url != link and len(curr_url) != len(link):
    #         if curr_url != link:
    #             for key, value in curr_url_qs.items():
    #                 if key not in link_qs:
    #                     has_same_query = False
    #                     break
    #         else:
    #             has_same_query = False

    #         if has_same_query:
    #             link_dict_list.append({"url": link, "query": link_qs})

    #     def sort_link(a):
    #         return len(a["url"])

    #     link_dict_list.sort(key=sort_link)

    #     ##############################################

    #     self.write_query(curr_url, link_dict_list)

    #     print("Done.")
    #     print("Building DOM for current page...")

    #     curr_node_list = self.build_dom(curr_url, root)

    #     self.write_info(curr_url, curr_node_list)

    #     print("Done.")
    #     print("Reference url: ", link_dict_list[1]["url"])
    #     print("Rendering page for reference url...")

    #     session = HTMLSession()
    #     r = session.get(link_dict_list[1]["url"])

    #     r.html.render()
    #     root = r.html.lxml

    #     print("Done.")
    #     print("Building DOM for reference page...")

    #     refer_node_list = self.build_dom(link_dict_list[1]["url"], root)

    #     self.write_info(link_dict_list[1]["url"], refer_node_list)

    #     print("Done.")
    #     print("Searching for duplicated nodes...")

    #     root_path = os.path.join(os.path.abspath(
    #         os.path.dirname(__file__)), "../")

    #     out_name = curr_url

    #     if curr_url[-1] == "/":
    #         out_name = curr_url[:len(curr_url) - 1]

    #     out_name = root_path + const.DIR_OUTPUT_LOG + \
    #         helper.as_valid_filename(
    #             out_name[out_name.find("//") + 2:]) + ".txt"

    #     with codecs.open(out_name, "w", "utf-8") as output:
    #         for curr in curr_node_list:
    #             if curr.el.text != None:
    #                 output.write("Curr: {} | {}\n".format(
    #                     curr.el.tag, curr.el.text))
    #                 for refer in refer_node_list:
    #                     if refer.el.text != None:
    #                         # if curr.el.text == refer.el.text and curr.el.tag == refer.el.tag:
    #                         if Node.is_same(curr.el, refer.el):
    #                             output.write("Refer: {} | {}\n".format(
    #                                 refer.el.tag, refer.el.text))
    #                             output.write("{}\n".format("Same"))
    #                             curr.duplicate_count = curr.duplicate_count + 1
    #                             break

    #     print("Done.")
    #     print("Counting number of children for each node...")

    #     result_node_list = []

    #     for curr in curr_node_list:
    #         if curr.duplicate_count == 0 and curr.el.text != None and curr.el.tag not in const.UNWANTED_TAGS:
    #             # Commented, invalid html tags are not allowed to set attributes
    #             # print(curr.el.tag ," ", curr.el.attrib)
    #             try:
    #                 curr.el.set("fyp-web-miner", "content")
    #                 result_node_list.append(curr)
    #             except TypeError as e:
    #                 print("Skipped, can't set attributes for tag: ",
    #                       curr.el.tag, " text: ", curr.el.text)

    #     for node in curr_node_list:
    #         curr_child_el = None
    #         index = 0
    #         node.same_child_count.append(0)
    #         curr_largest = -1

    #         for child_el in node.el.iterchildren():
    #             if child_el.tag != "meta":
    #                 curr_child_el = child_el
    #                 break

    #         for child_el in node.el.iterchildren():
    #             if child_el.tag != "meta":
    #                 if curr_child_el.tag == child_el.tag and curr_child_el.keys() == child_el.keys():
    #                     node.same_child_count[index] = node.same_child_count[index] + 1
    #                 else:
    #                     curr_child_el = child_el
    #                     index = index + 1
    #                     node.same_child_count.append(0)

    #                 if node.same_child_count[index] > curr_largest:
    #                     curr_largest = node.same_child_count[index]
    #                     node.largest_child_trait["tag"] = curr_child_el.tag
    #                     node.largest_child_trait["keys"] = curr_child_el.keys()

    #         node.same_child_count.sort(reverse=True)

    #     selected_node = curr_node_list[0]

    #     for node in curr_node_list:
    #         if node.same_child_count[0] > selected_node.same_child_count[0]:
    #             selected_node = node

    #     selected_node.el.set("fyp-web-miner", "same-child-count")

    #     self.write_info(curr_url, curr_node_list)

    #     print("Done.")
    #     print("Writing nodes into file...")

    #     self.write_same_children(curr_url, selected_node)
    #     self.write_diff_pages(curr_url, result_node_list)

    #     print("Done.")

    def start_diff_pages(self, curr_url):
        curr_time = time.time()

        print("Rendering page for current url...")
        print(curr_url)

        session = HTMLSession()
        r = session.get(curr_url)

        r.html.render()
        root = r.html.lxml

        print("Done in {}s.".format(str(round(time.time() - curr_time, 2))))        
        curr_time = time.time()

        print("Finding similar pages by queries and edit distance...")

        link_list = r.html.absolute_links

        link_dict_list = []

        curr_url_qs = urlparse.parse_qs(urlparse.urlparse(curr_url).query)

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
                is_valid = True

                if len(curr_url) == len(link):
                    is_all_same = True

                    for key, value in curr_url_qs.items():
                        if link_qs[key] != curr_url_qs[key]:
                            is_all_same = False
                            break

                    if is_all_same:
                        is_valid = False

                if is_valid:
                    link_dict_list.append({"url": link, "query": link_qs})

        def sort_link(a):
            return len(a["url"])

        link_dict_list.sort(key=sort_link)

        if len(link_dict_list) == 0:
            link_dict_list = []

            mdr_util = MDRUtil()

            for link in link_list:
                edit_distance = decimal.Decimal(mdr_util.xlevenshte_in_distance(curr_url, link))

                if edit_distance != 0:
                    link_dict_list.append({"url": link, "edit_distance": edit_distance})

            def sort_link(a):
                return a["edit_distance"]

            link_dict_list.sort(key=sort_link)

        # self.write_query(curr_url, link_dict_list)

        # self.write_info(curr_url, curr_node_list)
        #         
        # print("Reference url: ", link_dict_list[0]["url"])

        print("Done in {}s.".format(str(round(time.time() - curr_time, 2))))
        curr_time = time.time()

        print("Building DOM for current page...")

        curr_node_list = self.build_dom(curr_url, root, True)

        root_node = curr_node_list[0]

        print("Done in {}s.".format(str(round(time.time() - curr_time, 2))))

        have_duplicated_found = False

        for i in range(0, len(link_dict_list), 1):
            curr_time = time.time()

            print("Rendering page for reference url...")

            print(link_dict_list[i]["url"])

            session = HTMLSession()
            r = session.get(link_dict_list[i]["url"])

            r.html.render()
            refer_root = r.html.lxml

            print("Done in {}s.".format(str(round(time.time() - curr_time, 2))))
            curr_time = time.time()

            print("Building DOM for reference page...")

            refer_node_list = self.build_dom(link_dict_list[i]["url"], refer_root)

            # self.write_info(link_dict_list[1]["url"], refer_node_list)

            print("Done in {}s.".format(str(round(time.time() - curr_time, 2))))
            curr_time = time.time()

            print("Calculating duplicated count for each node...")

            for curr in curr_node_list:
                for refer in refer_node_list:
                    # if curr.el.text == refer.el.text and curr.el.tag == refer.el.tag:
                    if Node.is_same(curr.el, refer.el):
                        curr.duplicate_count = curr.duplicate_count + 1
                        break

            print("Done in {}s.".format(str(round(time.time() - curr_time, 2))))
            curr_time = time.time()

            print("Searching for unique nodes...")

            result_node_list = []

            for curr in curr_node_list:
                if curr.duplicate_count == 0 and curr.el.text != None and curr.el.text != "" and curr.el.tag not in const.UNWANTED_TAGS:
                    # Commented, invalid html tags are not allowed to set attributes
                    print(curr.el.tag ," ", curr.el.text)
                    try:
                        have_duplicated_found = True
                        # curr.el.set("fyp-web-miner", "content")
                        curr.is_content = True
                        curr.iter_parent = curr.parent

                        result_node_list.append(curr)

                        # iter_node = curr

                        # while iter_node.parent != None:
                        #     iter_node = iter_node.parent

                        #     if iter_node.data_regions != None and len(iter_node.data_regions) > 0:
                        #         iter_node.is_content_group = True
                        #     elif iter_node.is_content != True:
                        #         iter_node.is_content_holder = True

                    except TypeError as e:
                        print("Skipped, can't set attributes for tag: ",
                            curr.el.tag, " text: ", curr.el.text)

            print("Done in {}s.".format(str(round(time.time() - curr_time, 2))))

            if have_duplicated_found:
                break

        return result_node_list

    def start_mdr(self, root_node):
        start_time = time.time()
        curr_time = time.time()

        k = 1 # The number of combination, {} with {}, {}{} with {}{} and so on, the smaller the faster, while larger to more accurate
        # t = 0.3
        t = 2.5

        mdr_util = MDRUtil()

        print("Traversing DOM...")

        mdr_util.traverse_dom(root_node)        

        print("Done in {}s.".format(str(round(time.time() - curr_time, 2))))
        curr_time = time.time()

        print("Finding combination of each node...")

        mdr_util.mdr(root_node, k)

        print("Done in {}s.".format(str(round(time.time() - curr_time, 2))))
        curr_time = time.time()

        print("Finding data region...")

        mdr_util.find_DR(root_node, k, t)

        print("Done in {}s.".format(str(round(time.time() - curr_time, 2))))

        ##########################################################################

        curr_time = time.time()

        print("Creating generalized nodes...")

        dr_list = mdr_util.get_DRs(root_node)

        print("Done in {}s.".format(str(round(time.time() - curr_time, 2))))

        for i, dr in enumerate(dr_list):
            print(str(i) + ", size: " + str(len(dr.nodes)))

        # curr_time = time.time()

        # print("Finding data records...")

        # for dr in dr_list:
        #     for generalized_node in dr:          
        #         if generalized_node.size() == 1:
        #             mdr_util.find_record1(generalized_node)
        #         else:
        #             mdr_util.find_recordN(generalized_node)

        ###########################################################################

        # curr_time = time.time()

        # print("Getting data records...")

        # dr_node_list = []

        # for node in curr_node_list:
        #     if node.is_content_group == True and node.data_regions != None and len(node.data_regions) > 0 and len(node.data_regions) < 2:
        #         have_found = False

        #         for i in range(0, len(dr_node_list), 1):
        #             dr_node = dr_node_list[i]

        #             if node.preorder_pos < dr_node.preorder_pos:
        #                 if node.data_regions[0].is_same(dr_node.data_regions[0]):
        #                     dr_node_list[i] = node
        #                     have_found = True
        #                     break

        #             # if node.preorder_pos < dr_node.preorder_pos:
        #             #     for j in range(0, len(node.data_regions), 1):
        #             #         for k in range(0, len(dr_node.data_regions), 1):
        #             #             if node.data_regions[j].is_same(dr_node.data_regions[k]):                                    
        #             #                 dr_node_list[i] = node
        #             #                 have_found = True
        #             #                 break

        #         if not have_found:
        #             dr_node_list.append(node)

        # print("Done in {}s.".format(str(round(time.time() - curr_time, 2))))
        # curr_time = time.time()
        
        # print("Extracting data records...")

        # result_item_lists = []

        # item_list_index = 1

        # for node in dr_node_list:
        #     for data_region in node.data_regions:
        #         item_list = []

        #         preorder_pos = data_region.get_region_start_preorder_position()
        #         relative_pos = data_region.get_region_start_relative_position()
        #         node_comb = data_region.get_node_comb()
        #         node_count = data_region.get_node_count()

        #         # parent_node = (Tree(root_node).get_subtree_by_preorder(preorder_pos)).get_root().parent

        #         index = 1

        #         for i in range(relative_pos, relative_pos + node_count, node_comb):
        #             item = { "item_no": index, "item": [] }

        #             for j in range(i, i + node_comb, 1):
        #                 if j >= len(node.children): break

        #                 item_node = node.children[j]

        #                 if item_node.is_content:
        #                     item["item"].append(item_node.el.text)
        #                     index += 1
        #                 elif item_node.is_content_holder:
        #                     traverse_node_list = Tree(item_node).traverse(Tree.PRE_ORDER)

        #                     for child_node in traverse_node_list:
        #                         if child_node.is_content:
        #                             item["item"].append(child_node.el.text)

        #                     index += 1

        #             if len(item["item"]) > 0:
        #                 item_list.append(item)

        #         if len(item_list) > 0:
        #             result_item_lists.append({ "item_list_no": item_list_index, "item_list": item_list })
        #             item_list_index += 1

        # print("Done in {}s.".format(str(round(time.time() - curr_time, 2))))
        # print("Total elapsed time: {}s.".format(str(round(time.time() - start_time, 2))))

        # self.write_mdr_diff(curr_url, result_item_lists)

        ###############################################################################################

        # self.write_mdr_diff(curr_url, jsonpickle.encode(dr_list), "_dr_list")
        # self.write_mdr_diff(curr_url, jsonpickle.encode(curr_node_list), "_curr_node_list")

        print("Run successfully.")

        # print("Done.")
        # print("Building data record tree...")

        # for dr in dr_list:
        #     data_record_queue = mdr_util.build_data_record_tree(dr)
        #     mdr_util.partial_tree_alignment(data_record_queue)

        # result_tree = Tree(root_node).get_subtree_by_preorder(55)

        # print(result_tree.get_root())

    def build_dom(self, curr_url, root, required_link=False):
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

        if required_link == True:
            for p_node in node_list:
                for c_node in node_list:
                    if (Node.is_same(p_node.el, c_node.el.getparent())):
                        c_node.parent = p_node
                        p_node.children.append(c_node)

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

        out_name = root_path + const.DIR_OUTPUT_SAME_CHILDREN + \
            helper.as_valid_filename(
                out_name[out_name.find("//") + 2:]) + ".txt"

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

        out_name = root_path + const.DIR_OUTPUT_DIFF_PAGES + \
            helper.as_valid_filename(
                out_name[out_name.find("//") + 2:]) + ".txt"

        with codecs.open(out_name, "w", "utf-8") as output:
            # for node in reversed(node_list):
            #     self.calculate_td(node)

            #     # print("%8s | Chars: %8d, Tags: %6d, TD: %08.2f" % (node.tag, node.chars, node.tags, node.td))

            #     # if node.tag == "body":
            #     #     threshold = node.td

            #     self.init_ctd(node)

            for node in result_node_list:
                output.write("{} | {}\n".format(
                    "-" * node.parent_count, node.el.text))

    def write_query(self, curr_url, query_list):
        root_path = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), "../")

        out_name = curr_url

        if curr_url[-1] == "/":
            out_name = curr_url[:len(curr_url) - 1]

        out_name = root_path + const.DIR_OUTPUT_QUERY + \
            helper.as_valid_filename(
                out_name[out_name.find("//") + 2:]) + ".txt"

        with codecs.open(out_name, "w", "utf-8") as output:
            for query in query_list:
                output.write("{}\n".format(query.items()))

    def write_info(self, curr_url, info_list):
        root_path = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), "../")

        out_name = curr_url

        if curr_url[-1] == "/":
            out_name = curr_url[:len(curr_url) - 1]

        out_name = root_path + const.DIR_OUTPUT_INFO + \
            helper.as_valid_filename(
                out_name[out_name.find("//") + 2:]) + ".txt"

        with codecs.open(out_name, "w", "utf-8") as output:
            for info in info_list:
                # Same children test info
                # output.write("{} | {} | {} | {} | {}\n".format("-" * info.parent_count, info.el.tag, info.same_child_count, info.el.text, info.el.items()))

                # Different pages test info
                output.write("{} | {} | {} | {} | {}\n".format(
                    "-" * info.parent_count, info.el.tag, info.duplicate_count, info.el.text, info.el.items()))

    def write_mdr_diff(self, curr_url, result_item_lists, str_end = None):
        root_path = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), "../")

        out_name = curr_url

        if curr_url[-1] == "/":
            out_name = curr_url[:len(curr_url) - 1]

        if str_end == None:
            out_name = root_path + const.DIR_OUTPUT_MDR_DIFF + \
                helper.as_valid_filename(
                    out_name[out_name.find("//") + 2:]) + ".json"
        else:
            out_name = root_path + const.DIR_OUTPUT_MDR_DIFF + \
                helper.as_valid_filename(
                    out_name[out_name.find("//") + 2:]) + str_end + ".json"

        with codecs.open(out_name, "w", "utf-8") as output:
            json.dump(result_item_lists, output)
