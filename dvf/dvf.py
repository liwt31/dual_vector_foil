from collections import deque

from print_tree import print_tree

from .obj_node import ObjNode
from .format import default_formatter


class print_dvf(print_tree):
    def get_node_str(self, obj_node):
        return default_formatter(obj_node)

    def get_children(self, obj_node):
        return obj_node.get_output_children()


def dvf(obj, paging=True):
    ObjNode.expanded_obj_id_set.clear()
    dummy = ObjNode(None, "_dummy", object)
    root = ObjNode(dummy, "root", obj, True)
    nexts = deque([root])
    # BFS
    while nexts:
        next_node = nexts.popleft()
        if next_node.should_expand:
            next_node.expand()
            nexts.extend(next_node.children)
    print_dvf(root, paging=paging)
