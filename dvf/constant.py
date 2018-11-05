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
    pass


class Descriptor:
    pass


class UnknownDesc(Descriptor):
    pass


class VerboseDesc(Descriptor):
    pass
