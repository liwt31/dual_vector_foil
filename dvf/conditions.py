HIGHEST_PRIORITY = 100
USER_PRIORITY = 50
MEDIUM_PRIORITY = 10
DEFAULT_PRIORITY = 0


def is_neglected_type(obj_node):
    return (
        obj_node.is_magic
        or obj_node.is_routine
        or obj_node.is_class
        or obj_node.is_module
        or obj_node.is_generator
    )


class ConditionManager:
    @classmethod
    def always_true(cls):
        return cls([Condition(lambda x: True, HIGHEST_PRIORITY, "always true")])

    @classmethod
    def always_false(cls):
        return cls([Condition(lambda x: False, HIGHEST_PRIORITY, "always false")])

    @classmethod
    def limit_children(cls, parent):
        def pred(obj_node):
            # to skip the limitation for current node
            if obj_node is parent:
                return
            # the node is a descriptor and return type is not simple
            # infinite object generation is possible
            if obj_node.is_descriptor and not obj_node.is_builtin_type:
                return False
            # else return None and allow further judgement

        return cls([Condition(pred, MEDIUM_PRIORITY, "for descriptors")])

    @classmethod
    def default_visible(cls):
        def pred(obj_node):
            # list items always visible
            if not obj_node.from_dir:
                return True
            else:
                return not is_neglected_type(obj_node)

        condition = Condition(pred, DEFAULT_PRIORITY, "default visible")
        return cls([condition])

    @classmethod
    def default_expand(cls):
        def pred(obj_node):
            if (
                is_neglected_type(obj_node)
                or obj_node.is_leaf_type
                or id(obj_node.obj) in obj_node.expanded_obj_id_set
            ):
                return False
            else:
                return True

        return cls([Condition(pred, DEFAULT_PRIORITY, "default expand")])

    def __init__(self, conditions=None):
        self._conditions = conditions or []

    @property
    def conditions(self):
        # use a heap if this is proved to be a bottleneck (not likely)
        return sorted(self._conditions, key=lambda x: x.priority, reverse=True)

    def judge(self, node_obj):
        for condition in self.conditions:
            res = condition.predicate(node_obj)
            if res is None:
                continue
            else:
                return res
        assert False

    def __call__(self, node_obj):
        return self.judge(node_obj)

    def __iadd__(self, other):
        self._conditions.extend(other.conditions)
        return self

    def copy(self):
        return ConditionManager(self._conditions.copy())


class Condition:
    def __init__(self, predicate, priority, doc=""):
        self.predicate = predicate
        self.priority = priority
        self.doc = doc

    def __str__(self):
        return "<Condition doc: {}>".format(self.doc)

    def __repr(self):
        return self.__str__()
