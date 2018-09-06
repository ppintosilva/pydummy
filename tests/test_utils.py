import pytest
import logging as lg
import dummy
import os

def test_config_default():
    dummy.config()

    assert dummy.settings.app_name == "pydummy"
    assert dummy.settings.app_folder_location == "."
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

def test_config_changed():
    dummy.config(
        app_folder_location = "test",
        hide_app_folder = False,
        data_folder_name = "test",
        logs_folder_name = "test",
        cache_folder_name = "test",
        log_to_file = False,
        log_to_console = True,
        log_default_level = lg.WARNING,
        cache_http = False,
        default_user_agent = "test",
        default_referer = "test",
        default_accept_language = "test")

    assert dummy.settings.app_name == "pydummy"
    assert dummy.settings.app_folder_location == "test"
    assert dummy.settings.hide_app_folder == False
    assert dummy.settings.data_folder_name == "test"
    assert dummy.settings.logs_folder_name == "test"
    assert dummy.settings.cache_folder_name == "test"
    assert dummy.settings.log_to_file == False
    assert dummy.settings.log_to_console == True
    assert dummy.settings.log_default_level == lg.WARNING
    assert dummy.settings.cache_http == False
    assert dummy.settings.default_user_agent == 'test'
    assert dummy.settings.default_referer == 'test'
    assert dummy.settings.default_accept_language == 'test'


def test_get_app_folder():
    dummy.get_app_folder() == "./.pydummy"

def test_get_app_folder_visible():
    dummy.get_app_folder(
        app_folder_location = "/tmp",
        hide_app_folder = False) == "/tmp/pydummy"

def test_create_folders():
    dummy.config()
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
