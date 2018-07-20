# import numpy

import decimal
import math
import queue
import pdb

from entity.node import Node
from entity.data_region import DataRegion
from entity.generalized_node import GeneralizedNode
from entity.tree import Tree

class MDRUtil:
    def __init__(self):
        decimal.setcontext(decimal.BasicContext)
        self.total_preorder_pos = 0

    def traverse_dom(self, node):
        self.total_preorder_pos += 1

        node.preorder_pos = self.total_preorder_pos
        node.relative_pos = len(node.children)

        for i, child in enumerate(node.children):
            child.prev_sibling = node.children[i - 1] if i > 0 and i < len(node.children) else None
            child.next_sibling = node.children[i + 1] if i >= 0 and i < len(node.children) - 1 else None

            self.traverse_dom(child)        

    def mdr(self, node, k):
        if node.height() >= 3:
            self.comb_comp(node, k)

            for child in node.children:
                self.mdr(child, k)

    def comb_comp(self, node, maxComb):
        children = node.children

        # node.child_distance_matrix = numpy.zeros((maxComb, len(children)))
        node.child_distance_matrix = [[None for x in range(len(children))] for y in range(maxComb)]

        for i in range(0, min([maxComb, math.ceil(len(children) / 2)]), 1):
        # for i in range(0, maxComb, 1):
            for j in range(i + 1, maxComb + 1, 1):
                if (i + 2 * j - 1) < len(children):
                    st = i

                    for k in range(i + j, len(children), j):
                        if (k + j - 1) < len(children):
                            nd = self.normalized_edit_distance(children, st, k, k + j - 1)
                            node.child_distance_matrix[j - 1][st] = nd

                            st = k

    def normalized_edit_distance(self, children, st, k, en):
        first_child_list = children[st:k]
        second_child_list = children[k:en]

        sw_first = []

        for child in first_child_list:
            sw_first.extend(child.to_preorder_string())

        str1 = "".join(sw_first)

        sw_second = []

        for child in second_child_list:
            sw_second.extend(child.to_preorder_string())

        str2 = "".join(sw_second)

        edit_distance = decimal.Decimal(self.xlevenshte_in_distance(str1, str2))

        # mean_length = decimal.Decimal(len(str1) + len(str2) / 2.0)
        mean_length = decimal.Decimal((len(str1) + len(str2)) / 2.0) # Changed to actual mean length

        normalized_edit_distance = edit_distance / mean_length

        return float(normalized_edit_distance)

    def xlevenshte_in_distance(self, str1, str2):
        if len(str2) > len(str1):
            temp = str1
            str1 = str2
            str2 = temp

        row0_distance = [0] * (len(str2) + 1)
        row1_distance = [0] * (len(str2) + 1)

        row_id = 0
        column_id = 0

        for column_id in range(0, len(str2) + 1, 1):
            row0_distance[column_id] = column_id

        for row_id in range(0, len(str1) + 1, 1):
            for column_id in range(0, len(str2) + 1, 1):
                if column_id == 0:
                    row1_distance[column_id] = row_id
                else:
                    row1_distance[column_id] = min([min([row0_distance[column_id] + 1, row1_distance[column_id - 1] + 1]),
                    row0_distance[column_id - 1] + (0 if str1[row_id - 1] == str2[column_id - 1] else 1)])

            row0_distance = row1_distance
            row1_distance = [0] * (len(str2) + 1)

        distance = row0_distance[len(str2)]

        return distance

    def find_DR(self, node, k, t):
        if node.height() >= 3:
            node.data_regions = self.identify_DRs(0, node, k, t)

            temp_DRs = []

            for child in node.children:
                self.find_DR(child, k, t)

                uncovers_DRs = self.uncover_DRs(node, child)

                if uncovers_DRs != None and len(uncovers_DRs) != 0:
                    temp_DRs.extend(uncovers_DRs)
                
            node.data_regions.extend(temp_DRs)

    def identify_DRs(self, start, node, k, t):
        iden_DRs = []

        maxDR = DataRegion(0, 0, 0, 0)
        curDR = DataRegion(0, 0, 0, 0)

        for j in range(1, min([k, math.ceil(len(node.children) / 2)]) + 1, 1):
        # for j in range(1, k + 1, 1):
            for f in range(start, start + j + 1, 1):
                flag = True

                for i in range(f, len(node.children) - 1, j):
                    distanceij = node.child_distance_matrix[j - 1][i]

                    current_child_node_preorder_position = node.children[i].preorder_pos

                    # print(current_child_node_preorder_position, " ", node.children[i].el.tag, " ", node.children[i].el.text)

                    if distanceij != None and distanceij < t:
                        if flag == True:
                            curDR = DataRegion(current_child_node_preorder_position, i, j, 2 * j)
                            flag = False
                        else:
                            curDR.set_node_count(curDR.get_node_count() + j)
                    elif (not flag):
                        break

                if maxDR.get_node_count() < curDR.get_node_count() and (maxDR.get_region_start_relative_position() == 0 or \
                maxDR.get_region_start_relative_position() >= curDR.get_region_start_relative_position()):
                # maxDR.get_node_count() >= curDR.get_node_count()):                
                    maxDR = curDR

        if maxDR.get_node_count() != 0:
            if maxDR.get_region_start_relative_position() + maxDR.get_node_count() != len(node.children):
                iden_DRs.extend(self.identify_DRs(maxDR.get_region_start_relative_position() + maxDR.get_node_comb(), node, k, t))
            else:
                iden_DRs.append(maxDR)
        
        return iden_DRs

    def uncover_DRs(self, node, child):
        for dr in node.data_regions:
            if child.relative_pos >= dr.get_region_start_relative_position() and \
            child.relative_pos <= dr.get_region_start_relative_position() + dr.get_node_count():
                return None

        return child.data_regions

    def get_DRs(self, node):
        dr_list = []

        for dr in node.data_regions:
            generalized_node_list = []
            tag_node = None

            for i in range(0, int(dr.get_node_count() / dr.get_node_comb()), 1):
                g = GeneralizedNode()

                for j in range(0, dr.get_node_comb(), 1):
                    if i == 0 and j == 0:
                        tag_node = node.get_child_at_preorder_position(dr.get_region_start_preorder_position())
                        g.add(tag_node)
                    else:
                        tag_node = node.get_child_at_preorder_position(tag_node.next_sibling.preorder_pos)
                        g.add(tag_node)

                generalized_node_list.append(g)

            dr_list.append(generalized_node_list)

        return dr_list

    def find_record1(self, generalized_node):
        tag_node = generalized_node.get(0)

        similar_children = False

        child_iter = iter(tag_node.children)

        next_node = next(child_iter, None)

        if next_node != None:
            child = next_node

            next_node = next(child_iter, None)

            if next_node == None:
                similar_children = True
            else:
                next_child = next_node

                if "".join(child.to_preorder_string()).lower() == "".join(next_child.to_preorder_string()).lower():
                    similar_children = True

                    while next_node != None:
                        next_node = next(child_iter, None)

                        if next_node == None: break

                        child = next_child
                        next_child = next_node

                        if "".join(child.to_preorder_string()).lower() == "".join(next_child.to_preorder_string()).lower():
                            similar_children = True
                        else:
                            similar_children = False
                            break

        if tag_node.el.tag != "tr" and similar_children == True:
            generalized_node.data_record_indicator = GeneralizedNode.CHILD_CONT
        else:
            generalized_node.data_record_indicator = GeneralizedNode.SELF
                        
    def find_recordN(self, generalized_node):
        gi = iter(generalized_node)

        similar_children = False

        next_node = Node()

        while next_node != None:
            next_node = next(gi, None)

            if next_node == None: break

            tag_node = next_node

            next_node = next(gi, None)

            if next_node != None:
                next_tag_node = tag_node.next_sibling

                if len(tag_node.children) != len(next_tag_node.children):
                    similar_children = False
                    break

            child_iter = iter(tag_node.children)

            next_child_node = next(child_iter, None)

            if next_child_node == None:
                child = next_child_node

                next_child_node = next(child_iter, None)

                if next_child_node == None:
                    similar_children = True
                else:
                    next_child = next_child_node

                    if "".join(child.to_preorder_string()).lower() == "".join(next_child.to_preorder_string()).lower():
                        similar_children = True                    

                        while next_child_node != None:
                            next_child_node = next(child_iter, None)

                            if next_child_node == None: break

                            child = next_child
                            next_child = next_child_node

                            if "".join(child.to_preorder_string()).lower() == "".join(next_child.to_preorder_string()).lower():
                                similar_children = True
                            else:
                                similar_children = False
                                break

        if similar_children == True:
            generalized_node.data_record_indicator = GeneralizedNode.CHILD_NON_CONT
        else:
            generalized_node.data_record_indicator = GeneralizedNode.SELF

    def build_data_record_tree(self, dr):
        # data_record_queue = queue.PriorityQueue()
        data_record_queue = []

        di = None

        for i in range(0, len(dr), 1):
            g = dr[i]

            if i == 0:
                di = g.data_record_indicator

            if g.size() == 1:
                if di == GeneralizedNode.SELF:
                    data_record_queue.append(Tree(g.get(0)))
                elif di == GeneralizedNode.CHILD_CONT:
                    for child in g.get(0).children:
                        data_record_queue.append(Tree(child))
                elif di == GeneralizedNode.CHILD_NON_CONT:
                    pass
            else:
                tag_tree = Tree(Node("p"))

                if di == GeneralizedNode.SELF:
                    for node in g.get_nodes():
                        tag_tree.get_root().children.append(node)

                    data_record_queue.append(tag_tree)
                    break
                elif di == GeneralizedNode.CHILD_CONT:
                    break
                elif di == GeneralizedNode.CHILD_NON_CONT:
                    for j in range(0, len(g.get(0).children), 1):
                        tag_tree = Tree(Node("p"))

                        for tag_node in g.get_nodes():
                            tag_tree.get_root().children.append(tag_node.children[j])

                        data_record_queue.append(tag_tree)

                    break

        return data_record_queue

    def partial_tree_alignment(self, sQ):
        sQ = sorted(sQ)
        ts = sQ.pop(0)
        flag = False
        rQ = []
        i = False

        while len(sQ) > 0:
            ti = sQ.pop(0)

            matched_count = ts.simple_tree_matching(ti)

            if matched_count < ti.size():
                i = self.insert_into_seed(ts, ti)

                if (not i):
                    rQ.append(ti)

            if matched_count > 0 or i == True:
                flag = True

            if len(sQ) == 0 and flag == True:
                sQ = rQ
                rQ = []
                flag = False
                i = False

    def insert_into_seed(self, ts, ti):
        unaligned_nodes = []
        
        child = None

        if len(ti.get_root().children) != 0:
            child = ti.get_root().children[0]

        while child != None:
            if not child.aligned:
                unaligned_nodes.append(child)
                
                child = child.next_sibling
            else:
                left_node = unaligned_nodes[0].prev_sibling
                right_node = unaligned_nodes[len(unaligned_nodes) - 1].next_sibling

                break

        return True
