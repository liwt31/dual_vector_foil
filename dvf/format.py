from functools import partial

from colorama import init
from termcolor import colored


init()


def abbr_and_color(string, color_func, max_length=25):
    string = string.replace("\n", r"\n")
    if max_length < len(string):
        half_l = max_length // 2
        cstring = (
            color_func(string[: half_l - 2]) + "..." + color_func(string[-half_l + 2 :])
        )
    elif string:
        cstring = color_func(string)
    else:
        cstring = ""
    return cstring


def default_formatter(node):
    if node.is_descriptor:
        ctype_func = partial(colored, color="blue", attrs=["underline"])
    else:
        ctype_func = partial(colored, color="blue")
    ctype = abbr_and_color(node.type_str, ctype_func)
    if node.length is not None:
        ctype += "({})".format(colored(str(node.length), "magenta"))
    if ctype:
        ctype = f"<{ctype}>"

    cname_func = partial(colored, color="cyan")
    cname = abbr_and_color(node.name, cname_func)
    cvalue_func = partial(colored, attrs=["bold"])
    cvalue = abbr_and_color(node.value_str, cvalue_func, 40)
    if cvalue:
        cvalue = "=" + cvalue

    else:
        cvalue = ""
    return f"{ctype}{cname}{cvalue}"
