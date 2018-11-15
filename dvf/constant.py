import collections

leaf_type_tuple = (int, float, str, bool, type(None))

builtin_type_tuple = leaf_type_tuple + (
    list,
    tuple,
    dict,
    set,
    collections.deque,
    collections.OrderedDict,
)


class Ellipsis_:
    type_str = ""
    name = "···"
    value_str = ""


class Descriptor:
    pass


class UnknownDesc(Descriptor):
    pass


class VerboseDesc(Descriptor):
    pass
