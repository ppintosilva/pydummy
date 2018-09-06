import pytest
import logging as lg
import dummy
import os
import datetime as dt

def test_get_app_folder():
    dummy.get_app_folder() == "./.pydummy"

def test_get_app_folder_visible():
    dummy.get_app_folder(
        app_folder_location = "/tmp",
        hide_app_folder = False) == "/tmp/pydummy"

def test_get_app_folder_expandsuser():
    dummy.get_app_folder(
        app_folder_location = "~",
        hide_app_folder = False) == os.path.expanduser("~/pydummy")

def test_create_folders():
    dummy.create_folders(
                app_folder_location = "/tmp",
                hide_app_folder = False)

    app_folder = dummy.get_app_folder(
                        app_folder_location = "/tmp",
                        hide_app_folder = False)

    logs_folder = os.path.join(app_folder, dummy.settings.logs_folder_name)
    data_folder = os.path.join(app_folder, dummy.settings.data_folder_name)
    cache_folder = os.path.join(app_folder, dummy.settings.cache_folder_name)

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

def test_config_default():
    dummy.config()

    assert dummy.settings.app_name == "pydummy"
    assert dummy.settings.app_folder_location == "~"
    assert dummy.settings.hide_app_folder == True
    assert dummy.settings.data_folder_name == "data"
    assert dummy.settings.logs_folder_name == "logs"
    assert dummy.settings.cache_folder_name == "cache"
    assert dummy.settings.log_to_file == True
    assert dummy.settings.log_to_console == False
    assert dummy.settings.log_default_level == lg.INFO
    assert dummy.settings.cache_http == True
    assert dummy.settings.default_user_agent == 'Python pydummy package (https://github.com/pedroswits/pydummy)'
    assert dummy.settings.default_referer == 'Python pydummy package (https://github.com/pedroswits/pydummy)'
    assert dummy.settings.default_accept_language == 'en'

    app_folder = dummy.get_app_folder()

    logs_folder = os.path.join(app_folder, dummy.settings.logs_folder_name)
    data_folder = os.path.join(app_folder, dummy.settings.data_folder_name)
    cache_folder = os.path.join(app_folder, dummy.settings.cache_folder_name)

    log_filename = os.path.join(app_folder, dummy.settings.logs_folder_name, '{}_{}.log'.format(dummy.settings.app_name, dt.datetime.today().strftime('%Y_%m_%d')))

    dummy.log("THIS IS A TEST")

    assert os.path.exists(app_folder)
    assert os.path.exists(logs_folder)
    assert os.path.exists(data_folder)
    assert os.path.exists(cache_folder)
    assert os.path.exists(log_filename)

    os.remove(log_filename)
    os.rmdir(logs_folder)
    os.rmdir(data_folder)
    os.rmdir(cache_folder)
    os.rmdir(app_folder)

    assert not os.path.exists(app_folder)
    assert not os.path.exists(logs_folder)
    assert not os.path.exists(data_folder)
    assert not os.path.exists(cache_folder)
