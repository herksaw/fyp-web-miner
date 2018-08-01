import time

from lxml import etree
from lxml import html
from lxml.html import tostring, html5parser

from web.parser import Parser
from entity.node import Node
from entity.tree import Tree

# import tensorflow as tf

url_list = ["http://unruffled-leakey-d4e14a.bitballoon.com",
            "https://www.lazada.com.my/catalog/?q=laptop&_keyori=ss&from=input&spm=a2o4k.home.search.go.75f824f6QLmzE4",
            "http://www.11street.my/totalsearch/TotalSearchAction/searchTotal.do?targetTab=T&isGnb=Y&prdType=&category=&cmd=&pageSize=60&lCtgrNo=0&mCtgrNo=0&sCtgrNo=0&ctgrType=&fromACK=&gnbTag=TO&schFrom=&tagetTabNm=T&aKwdTrcNo=&aUrl=&kwd=laptop&callId=7274c0ac642e390b8fc",
            "https://shopee.com.my/search/?keyword=laptop",
            "https://www.lelong.com.my/catalog/all/list?TheKeyword=laptop",
            "https://s.taobao.com/search?q=%E6%89%8B%E6%8F%90%E7%94%B5%E8%84%91&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306",
            "https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=laptop",
            "https://www.schukat.com/schukat/schukat_cms_en.nsf/index/CMSDF15D356B046D53BC1256D550038A9E0?OpenDocument&wg=U1232&refDoc=CMS322921A477B31844C125707B0034EB15",
            "https://www.schukat.com/schukat/schukat_cms_en.nsf/index/CMSB5A38F73D94252D2C125707B00357507?OpenDocument",
            "https://www.w3schools.com/xml/schema_intro.asp",
            "https://www.straitstimes.com/tags/malaysia"]

if __name__ == "__main__":
    curr_url = url_list[1]

    total_time = 0
    start_time = time.time()

    parser = Parser()

    unique_node_list = parser.start_diff_pages(curr_url)

    # highest_nodes = [] 

    # root_node = Tree(Node("div")).get_root()
    
    # for i in range(0, len(unique_node_list), 1):
    #     is_highest = False
    #     parent_node = unique_node_list[i].parent

    #     while True:
    #         if parent_node == None:
    #             is_highest = True
    #             break

    #         if parent_node.is_content == True:
    #             break

    #         parent_node = parent_node.parent

    #     if is_highest:
    #         if unique_node_list[i].parent != None:
    #             is_existed = False

    #             for node in highest_nodes:
    #                 if Node.is_same(node.el, unique_node_list[i].parent.el):
    #                     is_existed = True
    #                     break

    #             if not is_existed:
    #                 highest_nodes.append(unique_node_list[i].parent)
    #                 root_node.children.append(unique_node_list[i].parent)
    #                 print(unique_node_list[i].el.tag ," ", unique_node_list[i].el.text) 
    
    curr_time = time.time()

    print("Grouping nodes based on the highest level parent...")

    same_level_node_list = []

    highest_nodes = []

    for node in unique_node_list:
        is_found = False

        for node_list in same_level_node_list:
            if node_list[0].parent_count == node.parent_count and Node.is_same_without_text(node_list[0].el, node.el):
                is_found = True
                node_list.append(node)

        if not is_found:
            same_level_node_list.append([node])

    for node_list in same_level_node_list:
        next_parent = node_list[0].parent        

        while True:
            is_all_same_parent = True

            if next_parent == None: break

            for node in node_list:
                if not Node.is_same(node.iter_parent.el, next_parent.el):
                    is_all_same_parent = False

                node.iter_parent = node.iter_parent.parent

            if is_all_same_parent:
                has_existed = False

                for h_node in highest_nodes:
                    if Node.is_same(h_node.el, next_parent.el):
                        has_existed = True
                        break

                if not has_existed:
                    next_parent.is_content_group = True
                    highest_nodes.append(next_parent)

                break

            next_parent = next_parent.parent

    print("Done in {}s.".format(str(round(time.time() - curr_time, 2))))
    curr_time = time.time()

    print("Outputing data into result...")

    result_item_list = []

    for i, h_node in enumerate(highest_nodes):
        item_list = { "list_no": i, "list": [] }

        index = 0

        for node in h_node.children:
            item = { "item_no": index, "item": [] }

            child_node_list = Tree(node).traverse(Tree.PRE_ORDER)

            content_node_list = []

            for j, child in enumerate(child_node_list):
                # text = child.el.text if child.el.text != None else ""
                # print(str(j) + " " + str(child.el.tag) + " " + text + " " + str(child.parent_count))

                if child.is_content:
                    parent_node = child.parent
                    is_belong_to_curr = True

                    while True:
                        if parent_node == None: break

                        if parent_node.is_content_group == True:
                            if not Node.is_same(parent_node.el, h_node.el):
                                is_belong_to_curr = False

                            break

                        parent_node = parent_node.parent
                    
                    if is_belong_to_curr:
                        is_found = False

                        for c_node in content_node_list:
                            if Node.is_same(c_node.el, child.el):
                                is_found = True
                                break

                        if not is_found:
                            content_node_list.append(child)
                            item["item"].append(child.el.text)
                            print(str(child.el.tag) + " " + child.el.text)

                        # item["item"].append(str(child.el.tag) + " " + child.el.text)
                        # print(str(child.el.tag) + " " + child.el.text)
            
            if len(item["item"]) > 0:
                item_list["list"].append(item)
                index += 1

        result_item_list.append(item_list)

    parser.write_mdr_diff(curr_url, result_item_list)

    print("Done in {}s.".format(str(round(time.time() - curr_time, 2))))

    print("Total elapsed time: {}s.".format(str(round(time.time() - start_time, 2))))

    print("Run successfully.")

    # parser.start_mdr(root_node)
