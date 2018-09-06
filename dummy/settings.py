################################################################################
# Module: settings.py
# Description: Global settings, can be configured by user by passing values to
#              utils.config()
# License: MIT, see full license in LICENSE.txt
# Web: https://github.com/pedroswits/pydummy
################################################################################
# Based on: Geoff Boeing's OSMnx package
# https://github.com/gboeing/osmnx/blob/master/osmnx/settings.py
################################################################################

import logging as lg

app_name = "pydummy"

app_folder_location = "." # or ~
hide_app_folder = True
data_folder_name = "data"
logs_folder_name = "logs"
cache_folder_name = "cache"

log_to_file = True
log_to_console = False
log_default_level = lg.INFO

cache_http = True
default_user_agent = 'Python pydummy package (https://github.com/pedroswits/pydummy)'
default_referer = 'Python pydummy package (https://github.com/pedroswits/pydummy)'
default_accept_language = 'en'
