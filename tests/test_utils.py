import os
import ast
import json
import hashlib
import requests
import logging as lg
import datetime as dt

import dummy
import pytest

###

def assert_file_structure(assert_logfile = True):
    app_folder = dummy.settings["app_folder"]

    logs_folder = os.path.join(app_folder, dummy.settings["logs_folder_name"])
    data_folder = os.path.join(app_folder, dummy.settings["data_folder_name"])
    cache_folder = os.path.join(app_folder, dummy.settings["cache_folder_name"])

    if assert_logfile:
        log_filename = os.path.join(app_folder, dummy.settings["logs_folder_name"], '{}_{}.log'.format(dummy.settings["app_name"], dt.datetime.today().strftime('%Y_%m_%d')))
        assert os.path.exists(log_filename)
        os.remove(log_filename)
        assert not os.path.exists(log_filename)

    assert os.path.exists(app_folder)
    assert os.path.exists(logs_folder)
    assert os.path.exists(data_folder)
    assert os.path.exists(cache_folder)

    os.rmdir(logs_folder)
    os.rmdir(data_folder)
    os.rmdir(cache_folder)
    os.rmdir(app_folder)

    assert not os.path.exists(app_folder)
    assert not os.path.exists(logs_folder)
    assert not os.path.exists(data_folder)
    assert not os.path.exists(cache_folder)

###

def test_get_app_folder():
    dummy.settings["app_folder"] == os.path.expanduser("~/.pydummy")

def test_create_folders():
    dummy.create_folders()
    assert_file_structure(assert_logfile = False)

def test_config_immutable_setting():
    with pytest.raises(dummy.ImmutableSetting):
        dummy.config(app_name = "test")

def test_config_invalid_setting():
    with pytest.raises(dummy.InvalidSetting):
        dummy.config(verbose = True)

def test_config():
    dummy.config(log_to_console = True)

    assert dummy.settings["log_to_console"] == True
    assert dummy.settings["cache_http"] == True
    assert dummy.settings["log_default_level"] == lg.INFO

    assert_file_structure(assert_logfile = True)

    dummy.config(app_folder = "/tmp/pydummy")

    assert_file_structure(assert_logfile = True)

def test_cache():
    dummy.config(cache_http = True)

    url = requests.Request('GET', "https://nominatim.openstreetmap.org/?format=json&addressdetails=1&q=Newcastle+A186+Westgate+Rd").prepare().url

    response_json = requests.get(url).json()

    dummy.save_to_cache(url, response_json)

    cache_folder = os.path.join(dummy.settings["app_folder"], dummy.settings["cache_folder_name"])
    cache_file = os.path.join(cache_folder, os.extsep.join([hashlib.md5(url.encode('utf-8')).hexdigest(), 'json']))

    assert os.path.exists(cache_file)

    with open(cache_file, encoding='utf-8') as cache_file_handler:
        cache_content = json.loads(cache_file_handler.read())

    json_str = dummy.make_str(json.dumps(response_json))
    json_str_from_cache = dummy.get_from_cache(url)

    assert ast.literal_eval(json_str) == cache_content
    assert cache_content == json_str_from_cache

    os.remove(cache_file)

    assert_file_structure(assert_logfile = False)
