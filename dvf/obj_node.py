import warnings
import inspect
import collections


from .utils import is_descriptor, safe_getattr
from .constant import leaf_type_tuple, UnknownDesc, Ellipsis_, builtin_type_tuple
from .conditions import ConditionManager
from .magic import magic_set


class ObjNode:

    expanded_obj_id_set = set()

    def __init__(self, parent, name, _obj, from_dir=False):
        self.parent = parent
        self.name = name

        # deal with descriptors
        self._obj = _obj
        self.obj = None

        self.from_dir = from_dir

        self.type_str = None
        self.value_str = None
        self.length = None

        # if self.obj isn't simple data structure such as list and dict
        # self._complex_obj = None

        self.init_conditions()
        self.init_obj()
        self.init_type()
        self.init_len()
        self.init_value_str()

        self.children = []

    @property
    def visible(self):
        return self.visible_conditions.judge(self)

    @property
    def should_expand(self):
        return self.visible and self.expand_conditions.judge(self)

    def init_conditions(self):
        if self.parent is None:
            self.visible_conditions = ConditionManager.default_visible()
            self.expand_conditions = ConditionManager.default_expand()
        else:
            self.visible_conditions = self.parent.visible_conditions.copy()
            self.expand_conditions = self.parent.expand_conditions.copy()


    @property
    def is_module(self):
        return inspect.ismodule(self.obj)

    @property
    def is_descriptor(self):
        return is_descriptor(self._obj)

    @property
    def is_routine(self):
        return inspect.isroutine(self.obj)

    @property
    def is_generator(self):
        return inspect.isgenerator(self.obj)

    @property
    def is_leaf_type(self):
        return isinstance(self.obj, leaf_type_tuple)

    @property
    def is_class(self):
        return inspect.isclass(self.obj)

    @property
    def is_magic(self):
        return self.name in magic_set

    @property
    def is_collection(self):
        return isinstance(self.obj, collections.abc.Collection)

    @property
    def is_sequence(self):
        if isinstance(self.obj, collections.abc.Sequence):
            # check it's *really* iterable
            # duck typing my ass
            try:
                for item in self.obj:
                    break
            except Exception:
                return False
            else:
                return True
        else:
            return False

    @property
    def is_set(self):
        return isinstance(self.obj, collections.abc.Set)

    @property
    def is_mapping(self):
        return isinstance(self.obj, collections.abc.Mapping)

    @property
    def is_builtin_type(self):
        return isinstance(self.obj, builtin_type_tuple)

    @property
    def is_finite_iterable(self):
        # mapping is partly finite iterable so ommited here
        return self.is_sequence or self.is_set

    @property
    def is_ordered(self):
        return self.is_sequence or isinstance(self.obj, collections.OrderedDict)

    # from https://stackoverflow.com/questions/2166818/python-how-to-check-if-an-object-is-an-instance-of-a-namedtuple
    @property
    def is_namedtuple(self):
        bases = type(self.obj).__bases__
        if len(bases) != 1 or bases[0] != tuple:
            return False
        f = getattr(self.obj, "_fields", None)
        if not isinstance(f, tuple):
            return False
        return all(type(n) == str for n in f)

    def init_obj(self):
        # in this case no need to discuss descriptor
        if not self.from_dir:
            self.obj = self._obj
        if is_descriptor(self._obj):
            try:
                self.obj = self._obj.__get__(self.parent.obj)
            except Exception as e:
                # some descriptors may not be implemented properly
                warnings.warn("An error occured while trying to process a descriptor.")
                self.obj = UnknownDesc
                self.expand_conditions += ConditionManager.always_false()
            else:
                self.expand_conditions += ConditionManager.limit_children(self)
        else:
            self.obj = self._obj

    def init_type(self):
        if self.obj is Ellipsis_:
            type_str = ""
        elif inspect.isclass(self.obj):
            type_str = "class"
        else:
            type_str = str(type(self.obj).__name__)
        if (type_str == 'type'):
            assert False
        self.type_str = type_str

    def init_len(self):
        if isinstance(self.obj, collections.abc.Sized):
            # any error can raise from user-defined `__len__`
            try:
                self.length = len(self.obj)
            except Exception:
                self.length = None

    def init_value_str(self):
        if self.is_leaf_type:
            value = repr(self.obj)
        elif self.obj is Ellipsis_:
            value = ""
        elif inspect.isclass(self.obj):
            value = self.obj.__name__
        elif inspect.isroutine(
            self.obj
        ):  # not using abc.Callable because it's too broad
            doc = getattr(self.obj, "__doc__", None)
            if isinstance(doc, str) and doc:
                value = doc.splitlines()[0]
            else:
                value = ""
        else:
            value = ""
        self.value_str = value

    def expand(self):

        # check from most specific to most broad case
        if self.is_namedtuple:
            for k, v in zip(self.obj._fields, self.obj):
                # k must be string no need to cast
                self.children.append(ObjNode(self, k, v))

        elif self.is_mapping:
            for k, v in self.obj.items():
                self.children.append(ObjNode(self, str(k), v))
        elif self.is_finite_iterable:
            for item in self.obj:
                self.children.append(ObjNode(self, "", item))
        else:
            for name in dir(self.obj):
                try:
                    attr = safe_getattr(self.obj, name)
                except AttributeError:
                    continue
                self.children.append(ObjNode(self, name, attr, True))
        self.expanded_obj_id_set.add(id(self.obj))

    def get_output_children(self):
        visible_children = [child for child in self.children if child.visible]
        if not self.is_ordered:
            visible_children.sort(key=lambda node: node.type_str)
        if not visible_children:
            return []
        if not visible_children[0].from_dir:
            if 6 < len(visible_children):
                visible_children = visible_children[:2] + visible_children[-2:]
                visible_children.insert(2, ObjNode(self, "···", Ellipsis_))

        return visible_children
