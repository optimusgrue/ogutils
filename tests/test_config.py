import os
import sys

import pytest

from ogutils.config import load_config
from ogutils.config import load_yaml_from_file
from ogutils.config import load_ini_from_file
from ogutils.config import load_toml_from_file
from ogutils.config import load_json_from_file


def test_load_yaml_from_file():
    path = os.path.dirname(os.path.realpath(__file__))
    d = load_yaml_from_file(path + "/static/config.yaml")

    assert d["core"]["loglevel"] == "debug"
    assert d["sources"]["db01"]["pwd"] == "ketchup"


def test_load_ini_from_file():
    path = os.path.dirname(os.path.realpath(__file__))
    d = load_ini_from_file(path + "/static/config.ini")

    assert d["core"]["sleep"] == "5"
    assert d["db02"]["pwd"] == "mayo"


def test_load_toml_from_file():
    path = os.path.dirname(os.path.realpath(__file__))
    d = load_toml_from_file(path + "/static/config.toml")

    assert d["core"]["sleep"] == 5
    assert d["sources"]["db02"]["pwd"] == "apple"


def test_load_json_from_file():
    path = os.path.dirname(os.path.realpath(__file__))
    d = load_json_from_file(path + "/static/config.json")

    assert d["core"]["soap_orders"] == "NewOrder"
    assert d["sources"]["db01"]["pwd"] == "howard"


class TestLoadConfig:
    def test_abs_yaml(self):
        path = os.path.dirname(os.path.realpath(__file__))

        d = load_config(path + "/static/config.yaml")
        assert d["sources"]["db01"]["pwd"] == "ketchup"

        d = load_config(path + "/static/config.YML")
        assert d["sources"]["db01"]["pwd"] == "ketchup"

    def test_abs_ini(self):
        path = os.path.dirname(os.path.realpath(__file__))

        d = load_config(path + "/static/config.ini")
        assert d["db02"]["pwd"] == "mayo"

    def test_abs_toml(self):
        path = os.path.dirname(os.path.realpath(__file__))

        d = load_config(path + "/static/config.toml")
        assert d["sources"]["db02"]["pwd"] == "apple"

        d = load_config(path + "/static/Config.Tml")
        assert d["sources"]["db02"]["pwd"] == "apple"

    def test_abs_json(self):
        path = os.path.dirname(os.path.realpath(__file__))

        d = load_config(path + "/static/config.json")
        assert d["sources"]["db01"]["pwd"] == "howard"

    def test_abs_unknown(self):
        path = os.path.dirname(os.path.realpath(__file__))

        with pytest.raises(ValueError):
            d = load_config(path + "/static/config.foo")

    def test_search_yaml(self):
        here = os.path.dirname(os.path.realpath(__file__))

        d = load_config("config.yaml", ["/etc", here + "/static"])
        assert d["sources"]["db01"]["pwd"] == "ketchup"

        with pytest.raises(FileNotFoundError):
            d = load_config("abc_config_xyz.yaml", ["/etc", here + "/static"])
