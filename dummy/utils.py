################################################################################
# Module: utils.py
# Description: Global settings, configuration, logging and caching
# License: MIT, see full license in LICENSE.txt
# Web: https://github.com/pedroswits/pydummy
################################################################################
# Based on: Geoff Boeing's OSMnx package
# https://github.com/gboeing/osmnx/blob/master/osmnx/utils.py
################################################################################

from . import settings
import os
import sys
import unicodedata
import logging as lg
import datetime as dt


###
###

def config(app_folder_location = settings.app_folder_location,
           hide_app_folder = settings.hide_app_folder,
           data_folder_name = settings.data_folder_name,
           logs_folder_name = settings.logs_folder_name,
           cache_folder_name = settings.cache_folder_name,
           log_to_file = settings.log_to_file,
           log_to_console = settings.log_to_console,
           log_default_level = settings.log_default_level,
           cache_http = settings.cache_http,
           default_user_agent = settings.default_user_agent,
           default_referer = settings.default_referer,
           default_accept_language = settings.default_accept_language):
    """
    Configure osmnx by setting the default global vars to desired values.

    Parameters
    ---------
    app_folder_location : string
        where to store app data
    hide_app_folder : bool
        whether to hide app folder or not
    data_folder_name : string
        name of folder containing data files
    logs_folder_name : string
        name of folder containing log files
    cache_folder_name : string
        name of folder containing cached http responses
    cache_http : bool
        if True, use a local cache to save/retrieve http responses instead of calling API repetitively for the same request URL
    log_to_file : bool
        if true, save log output to a log file in logs_folder
    log_to_console : bool
        if true, print log output to the console
    log_default_level : int
        one of the logger.level constants
    default_user_agent : string
        HTTP header user-agent
    default_referer : string
        HTTP header referer
    default_accept_language : string
        HTTP header accept-language

    Returns
    -------
    None
    """

    # set each global variable to the passed-in parameter value
    settings.app_folder_location = app_folder_location
    settings.hide_app_folder = hide_app_folder
    settings.data_folder_name = data_folder_name
    settings.logs_folder_name = logs_folder_name
    settings.cache_folder_name = cache_folder_name
    settings.cache_http = cache_http
    settings.log_to_file = log_to_file
    settings.log_to_console = log_to_console
    settings.log_default_level = log_default_level
    settings.default_user_agent = default_user_agent
    settings.default_referer = default_referer
    settings.default_accept_language = default_accept_language

    clean_logger()
    log('Configured {}'.format(settings.app_name))

###
###

def get_app_folder(app_folder_location = None,
                   hide_app_folder = None):
    """
    Build path to app folder

    Parameters
    ----------
    app_folder_location : string
        location of main app directory
    hide_app_folder : bool
        whether to app folder is hidden or not

    Returns
    -------
    string
        path to app folder
    """
    if app_folder_location is None:
        app_folder_location = settings.app_folder_location
    if hide_app_folder is None:
        hide_app_folder = settings.hide_app_folder

    filename = "." + settings.app_name if hide_app_folder else settings.app_name
    return os.path.join(os.path.expanduser(app_folder_location), filename)

###
###

def create_folders(app_folder_location = None,
                   hide_app_folder = None,
                   logs_folder_name = None,
                   data_folder_name = None,
                   cache_folder_name = None):
    """
    Creates app folders: parent, data, logs and cache

    Parameters
    ----------
    app_folder_location : string
        location of main app directory
    hide_app_folder : bool
        whether to app folder is hidden or not
    logs_folder_name : string
        name of folder containing logs
    data_folder_name : string
        name of folder containing data
    cache_folder_name : string
        name of folder containing cached http responses

    Returns
    -------
    None
    """

    if app_folder_location is None:
        app_folder_location = settings.app_folder_location
    if hide_app_folder is None:
        hide_app_folder = settings.hide_app_folder
    if logs_folder_name is None:
        logs_folder_name = settings.logs_folder_name
    if data_folder_name is None:
        data_folder_name = settings.data_folder_name
    if cache_folder_name is None:
        cache_folder_name = settings.cache_folder_name

    app_folder = get_app_folder(app_folder_location, hide_app_folder)
    if not os.path.exists(app_folder):
        os.makedirs(app_folder)

    logs_folder = os.path.join(app_folder, logs_folder_name)

    if not os.path.exists(logs_folder):
        os.mkdir(logs_folder)

    data_folder = os.path.join(app_folder, data_folder_name)

    if not os.path.exists(data_folder):
        os.mkdir(data_folder)

    cache_folder = os.path.join(app_folder, cache_folder_name)

    if not os.path.exists(cache_folder):
        os.mkdir(cache_folder)

###
###

def make_str(value):
    """
    Convert a passed-in value to unicode if Python 2, or string if Python 3.

    Parameters
    ----------
    value : any
        the value to convert to unicode/string

    Returns
    -------
    unicode or string
    """
    try:
        # for python 2.x compatibility, use unicode
        return unicode(value)
    except NameError:
        # python 3.x has no unicode type, so if error, use str type
        return str(value)

###
###

def log(message,
        level = None,
        name = None,
        filename = None):
    """
    Write a message to the log file and/or print to the the console.

    Parameters
    ----------
    message : string
        the content of the message to log
    level : int
        one of the logger.level constants
    name : string
        name of the logger
    filename : string
        name of the log file

    Returns
    -------
    None
    """

    if level is None:
        level = settings.log_default_level
    if name is None:
        name = settings.app_name
    if filename is None:
        name = settings.app_name

    # if logging to file is turned on
    if settings.log_to_file:
        # get the current logger (or create a new one, if none), then log
        # message at requested level
        logger = get_logger(level=level, name=name, filename=filename)
        if level == lg.DEBUG:
            logger.debug(message)
        elif level == lg.INFO:
            logger.info(message)
        elif level == lg.WARNING:
            logger.warning(message)
        elif level == lg.ERROR:
            logger.error(message)

    # if logging to console is turned on, convert message to ascii and print to
    # the console
    if settings.log_to_console:
        # capture current stdout, then switch it to the console, print the
        # message, then switch back to what had been the stdout. this prevents
        # logging to notebook - instead, it goes to console
        standard_out = sys.stdout
        sys.stdout = sys.__stdout__

        # convert message to ascii for console display so it doesn't break
        # windows terminals
        message = unicodedata.normalize('NFKD', make_str(message)).encode('ascii', errors='replace').decode()
        print(message)
        sys.stdout = standard_out

###
###

def get_logger(level = None,
               name = None,
               filename = None):
    """
    Create a logger or return the current one if already instantiated.

    Parameters
    ----------
    level : int
        one of the logger.level constants
    name : string
        name of the logger
    filename : string
        name of the log file

    Returns
    -------
    logger.logger
    """

    if level is None:
        level = settings.log_default_level
    if name is None:
        name = settings.app_name
    if filename is None:
        filename = settings.app_name

    logger = lg.getLogger(name)

    # if a logger with this name is not already set up
    if len(logger.handlers) == 0:

        # get today's date and construct a log filename
        todays_date = dt.datetime.today().strftime('%Y_%m_%d')
        log_filename = os.path.join(get_app_folder(), settings.logs_folder_name, '{}_{}.log'.format(filename, todays_date))

        print(log_filename)

        # if the logs folder does not already exist, create it
        create_folders()

        # create file handler and log formatter and set them up
        handler = lg.FileHandler(log_filename, encoding='utf-8')
        formatter = lg.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)
        logger.handler_set = True

    return logger

###

def clean_logger(name = None):
    """
    Removes all handlers associated with a given logger

    Parameters
    ----------
    name : string
        name of the logger

    Returns
    -------
    None
    """
    if name is None:
        name = settings.app_name

    logger = lg.getLogger(name)

    handlers = logger.handlers
    for handler in handlers:
        logger.removeHandler(handler)

# def save_to_cache(url, response_json):
#     """
#     Save an HTTP response json object to the cache.
#     If the request was sent to server via POST instead of GET, then URL should
#     be a GET-style representation of request. Users should always pass
#     OrderedDicts instead of dicts of parameters into request functions, so that
#     the parameters stay in the same order each time, producing the same URL
#     string, and thus the same hash. Otherwise the cache will eventually contain
#     multiple saved responses for the same request because the URL's parameters
#     appeared in a different order each time.
#     Parameters
#     ----------
#     url : string
#         the url of the request
#     response_json : dict
#         the json response
#     Returns
#     -------
#     None
#     """
#     if settings.use_cache:
#         if response_json is None:
#             log('Saved nothing to cache because response_json is None')
#         else:
#             # create the folder on the disk if it doesn't already exist
#             if not os.path.exists(settings.cache_folder):
#                 os.makedirs(settings.cache_folder)
#
#             # hash the url (to make filename shorter than the often extremely
#             # long url)
#             filename = hashlib.md5(url.encode('utf-8')).hexdigest()
#             cache_path_filename = os.path.join(settings.cache_folder, os.extsep.join([filename, 'json']))
#
#             # dump to json, and save to file
#             json_str = make_str(json.dumps(response_json))
#             with io.open(cache_path_filename, 'w', encoding='utf-8') as cache_file:
#                 cache_file.write(json_str)
#
#             log('Saved response to cache file "{}"'.format(cache_path_filename))
#
#
# def get_from_cache(url):
#     """
#     Retrieve a HTTP response json object from the cache.
#     Parameters
#     ----------
#     url : string
#         the url of the request
#     Returns
#     -------
#     response_json : dict
#     """
#     # if the tool is configured to use the cache
#     if settings.use_cache:
#         # determine the filename by hashing the url
#         filename = hashlib.md5(url.encode('utf-8')).hexdigest()
#
#         cache_path_filename = os.path.join(settings.cache_folder, os.extsep.join([filename, 'json']))
#         # open the cache file for this url hash if it already exists, otherwise
#         # return None
#         if os.path.isfile(cache_path_filename):
#             with io.open(cache_path_filename, encoding='utf-8') as cache_file:
#                 response_json = json.load(cache_file)
#             log('Retrieved response from cache file "{}" for URL "{}"'.format(cache_path_filename, url))
#             return response_json
#
# def get_http_headers(user_agent=None, referer=None, accept_language=None):
#     """
#     Update the default requests HTTP headers with OSMnx info.
#     Parameters
#     ----------
#     user_agent : str
#         the user agent string, if None will set with OSMnx default
#     referer : str
#         the referer string, if None will set with OSMnx default
#     accept_language : str
#         make accept-language explicit e.g. for consistent nominatim result sorting
#     Returns
#     -------
#     headers : dict
#     """
#
#     if user_agent is None:
#         user_agent = settings.default_user_agent
#     if referer is None:
#         referer = settings.default_referer
#     if accept_language is None:
#         accept_language = settings.default_accept_language
#
#     headers = requests.utils.default_headers()
#     headers.update({'User-Agent': user_agent, 'referer': referer, 'Accept-Language': accept_language})
#     return headers
