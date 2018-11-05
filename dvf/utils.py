import inspect
import functools


def is_descriptor(obj):
    for name in ["__get__", "__set__", "__delete__"]:
        # some objs (such as local proxy in flask) tweaks __getattr__
        # and `hasattr` may raise any errors
        try:
            if hasattr(obj, name):
                return True
        except Exception:
            return False


def safe_getattr(attr_obj, attr_name):
    if inspect.isclass(attr_obj):
        obj_list = [attr_obj] + list(attr_obj.__mro__)
    else:
        obj_list = [attr_obj] + list(attr_obj.__class__.__mro__)
    for obj in obj_list:
        if hasattr(obj, "__dict__") and attr_name in obj.__dict__:
            return obj.__dict__[attr_name]
    raise AttributeError
