from collections.abc import Sequence
from collections import namedtuple

import pytest

from dvf.obj_node import ObjNode
from dvf.constant import UnknownDesc, Ellipsis_


# helper function
def assert_children(node_or_children, expected_children):
    if isinstance(node_or_children, ObjNode):
        node_children = node_or_children.children
    else:
        node_children = node_or_children
    assert len(node_children) == len(expected_children)
    for child, (name, obj) in zip(node_children, expected_children):
        assert child.name == name
        assert child.obj == obj


def test_attribute():
    node1 = ObjNode(None, "node1", 1)
    assert node1.visible
    assert not node1.should_expand
    assert not node1.is_module
    assert not node1.is_descriptor
    assert not node1.is_routine
    assert not node1.is_generator
    assert node1.is_leaf_type
    assert not node1.is_collection
    assert not node1.is_sequence
    assert not node1.is_set
    assert not node1.is_mapping
    assert node1.is_builtin_type
    assert not node1.is_finite_iterable
    assert not node1.is_ordered
    assert not node1.is_namedtuple

    node2 = ObjNode(None, "node2", list([1, 2]))
    assert node2.visible
    assert node2.should_expand
    assert not node2.is_generator
    assert not node2.is_leaf_type
    assert node2.is_collection
    assert node2.is_sequence
    assert node2.is_builtin_type
    assert node2.is_finite_iterable
    assert node2.is_ordered
    assert not node2.is_namedtuple

    import dvf

    node3 = ObjNode(None, "node3", dvf)
    assert not node3.should_expand
    assert node3.is_module


def test_fake_sequence():
    class Fake(Sequence):
        def __getitem__(self):
            raise NotImplementedError

        def __len__(self):
            raise NotImplementedError

        def __iter__(self):
            raise NotImplementedError

    node = ObjNode(None, "node", Fake())
    assert not node.is_sequence
    assert node.length is None


def test_named_tuple():
    Point = namedtuple("Point", ["x", "y"])
    p = Point(1, 2)
    node = ObjNode(None, "point", p)
    node.expand()
    assert node.is_namedtuple
    assert_children(node, [("x", 1), ("y", 2)])


def test_init_obj():
    # descriptor handled properly
    node1 = ObjNode(None, "node1", 1)
    node2 = ObjNode(node1, "node2", property(lambda x: 1))
    assert node2.obj == 1

    # some descriptors are buggy
    with pytest.warns(UserWarning):
        # The descriptor is not working because function must have 1 arg to
        # become a property. So a warning is issued.
        node3 = ObjNode(node1, "node3", property(lambda: 1))
    assert node3.obj == UnknownDesc
    assert not node3.should_expand


def test_expand():
    node1 = ObjNode(None, "node1", {"1": 1, "2": 2})
    node1.expand()
    assert_children(node1, [("1", 1), ("2", 2)])

    node2 = ObjNode(None, "node2", [1, 2])
    node2.expand()
    assert_children(node2, [("", 1), ("", 2)])

    class Foo:
        def __init__(self):
            self.x = 1
            self.y = 1

        def __dir__(self):
            return ["x", "y", "bla"]

    foo = Foo()
    node3 = ObjNode(None, "node3", foo)
    node3.expand()
    assert_children(node3, [("x", 1), ("y", 1)])


def test_output_children():
    node = ObjNode(None, "node1", range(10))
    node.expand()
    assert_children(node.get_output_children(), [("", 0), ("", 1), (Ellipsis_.name, Ellipsis_), ("", 8), ("", 9)])
