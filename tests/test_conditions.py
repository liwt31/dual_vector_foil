from dvf.conditions import ConditionManager
from dvf.obj_node import ObjNode


def test_base_condition():
    node1 = ObjNode(None, 'node1', 'node1')
    node2 = ObjNode(None, 'node2', list([1, 23]))
    always_true = ConditionManager.always_true()
    assert always_true(node1)
    always_false = ConditionManager.always_false()
    assert not always_false(node1)

    class_node = ObjNode(node1, 'class', ObjNode, True)
    import dvf
    module_node = ObjNode(node1, 'module', dvf, True)
    default_visible = ConditionManager.default_visible()
    assert not default_visible(class_node)
    assert not default_visible(module_node)
    # if not from dir, then always visible
    class_node.from_dir = False
    assert default_visible(class_node)
    default_expand = ConditionManager.default_expand()
    assert default_expand(node2)
    assert not default_expand(node1)


def test_multiple_condition():
    node1 = ObjNode(None, 'node1', list([1, 2]))
    node2 = ObjNode(node1, 'node2', property(lambda x: 42), True)
    conditions = ConditionManager.default_expand()
    conditions += ConditionManager.limit_children(node1)
    assert conditions(node1)
    assert not conditions(node2)
