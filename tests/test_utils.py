from flask import Flask

from dvf.utils import is_descriptor, safe_getattr


def test_is_descriptor():
    assert is_descriptor(property(lambda x: x))
    assert not is_descriptor(list([1, 2]))
    # test exception handling
    app = Flask("app")
    assert not is_descriptor(app.jinja_env.globals["request"])


class Base:
    base = "base"

    @property
    def prop(self):
        return "prop"


class Deriv(Base):
    deriv = "deriv"


def test_getattr():
    d = Deriv()
    d.inst = "inst"
    cls_expected_list = [("base", "base"), ("deriv", "deriv"), ("prop", Base.prop)]
    inst_expected_list = cls_expected_list + [("inst", "inst")]
    for attr, expected in inst_expected_list:
        assert safe_getattr(d, attr) == expected
    for attr, expected in cls_expected_list:
        assert safe_getattr(Deriv, attr) == expected
