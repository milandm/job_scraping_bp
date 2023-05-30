import json
import os
import re
import sys
import time
from datetime import datetime
from whois import whois
from config.models.data_config import DataConfig
from utils.custom_exceptions import ConfigReadException
from utils.constants import RunAppConstants, MongoDbConstants, ExportConstants, AffinityPresence, SourcesConstants
import ast
import asyncwhois
import random

from utils.sources_constants import GithubConstants


def fetch_csv_sources_and_files(csv_files_dir):
    file_set = set()
    for directory, _, files in os.walk(csv_files_dir):
        for file_name in files:
            full_file_path = os.path.join(directory, file_name)
            source_name = os.path.basename(os.path.normpath(directory))
            file_set.add((source_name, full_file_path))
    return list(file_set)


def get_domain_from_url(full_web_address, my_logger=None):
    try:
        return whois(full_web_address).domain
    except Exception as e:
        if my_logger:
            my_logger.debug('Exception')
            my_logger.debug(e)
    return ""


async def async_get_domain_from_url(url, logger=None):
    res = None
    print(url)
    try:
        try:
            res = await asyncwhois.aio_whois_domain(url)
            logger.debug(f'{url} done')
        except ConnectionResetError as e:
            logger.debug(f'{url} exception: {e}')
        except TimeoutError as e:
            logger.debug(f'{url} exception: {e}')
        if not res:
            time.sleep(random.randint(1, 5))
            try:
                res = await asyncwhois.aio_whois_domain(url)
                logger.debug(f'{url} done')
            except ConnectionResetError as e:
                logger.debug(f'{url} exception: {e}')
            except TimeoutError as e:
                logger.debug(f'{url} exception: {e}')
    except Exception as e:
        logger.debug(f'{url} exception: {e}')
    if res:
        return f'{res.tld_extract_result.domain}.{res.tld_extract_result.suffix}'
    return ""


def remove_non_alpha(string: str):
    regex = re.compile('[^a-zA-Z]')
    # First parameter is the replacement, second parameter is your input string
    return regex.sub('', string)


def get_config(logger, db_config=None):
    try:
        with open(file=RunAppConstants.CONFIG_JSON_PATH, mode='r') as conf_file:
            config_json = json.load(conf_file)
        if not config_json:
            raise ConfigReadException("Couldn't read data_config.json")
        return DataConfig(json_object=config_json, db_config=db_config)
    except ConfigReadException as e:
        logger.error(f'Exception: {e}')
        sys.exit(1)


def get_date_from_string(string_date=None, my_logger=None):
    if string_date and isinstance(string_date, str):
        try:
            return datetime.strptime(string_date, MongoDbConstants.DATE_FORMAT).timestamp()
        except Exception as e:
            if my_logger:
                my_logger.debug('get_raw_text_html ' + str(e))
    return None


def get_date_now_timestamp():
    date_timestamp = datetime.today().replace(microsecond=0).timestamp()
    date_str = datetime.utcfromtimestamp(date_timestamp).strftime(MongoDbConstants.DATE_FORMAT)
    date_timestamp = datetime.strptime(date_str, MongoDbConstants.DATE_FORMAT).timestamp()
    return date_timestamp


def get_date_str_now():
    return datetime.now().replace(microsecond=0).strftime(MongoDbConstants.DATE_FORMAT)


def get_date_str_from_timestamp(date_timestamp, my_logger=None):
    date_str = None
    if date_timestamp:
        try:
            if isinstance(date_timestamp, str):
                date_timestamp = int(date_timestamp)
            date_str = datetime.utcfromtimestamp(date_timestamp).strftime(MongoDbConstants.DATE_FORMAT)
        except Exception as e:
            if my_logger:
                my_logger.debug('get_date_str_from_timestamp ' + str(e))
    return date_str


def get_bucket_path_list_from_string(my_logger, bucket_path_list_str: str):
    bucket_path_list = []
    if bucket_path_list_str and type(bucket_path_list_str) is str:
        try:
            bucket_path_list = ast.literal_eval(bucket_path_list_str)
        except Exception as exception:
            if my_logger:
                my_logger.debug("from_dict bucket_path_list ", exception)
    if not bucket_path_list:
        try:
            bucket_path_list = eval(bucket_path_list_str)
        except Exception as exception:
            if my_logger:
                my_logger.debug("from_dict bucket_path_list ", exception)
    return bucket_path_list


def get_predictions_csv_filename(filename, data_source=None):
    if not data_source:
        main_source_name = ''
    else:
        main_source_name = data_source + '_'
    csv_file_extension = '.csv'
    datetime_str = f"{datetime.now():{ExportConstants.PREDICTIONS_EXPORT_FILENAME_DATETIME_FORMAT}}"
    return main_source_name + filename + datetime_str + csv_file_extension


def get_affinity_label(company_internal_profile):
    affinity_source = None
    if company_internal_profile.company_external_items_dict:
        affinity_source = company_internal_profile.company_external_items_dict.get(SourcesConstants.AFFINITY, None)
    if affinity_source:
        return AffinityPresence.PRESENT
    else:
        return AffinityPresence.NOT_PRESENT


def merge_dicts(old_list_dict, new_list_dict):
    empty_key_list = list()
    for key, value in new_list_dict.items():
        old_list_dict[key] = value
        if not value:
            empty_key_list.append(key)
    for key in empty_key_list:
        del old_list_dict[key]
    return old_list_dict


def make_list_unique(old_list, get_list_unique_key_method):
    item_dict = dict()
    for item in old_list:
        item_dict[get_list_unique_key_method(item)] = item

    new_item_list = list()
    for key, value in item_dict.items():
        new_item_list.append(value)

    return new_item_list


def merge_lists(old_list, new_list, get_list_unique_key_method):
    item_dict = dict()
    for item in old_list:
        item_dict[get_list_unique_key_method(item)] = item

    for item in new_list:
        item_dict[get_list_unique_key_method(item)] = item

    new_item_list = list()
    for key, value in item_dict.items():
        new_item_list.append(value)

    return new_item_list


def add_new_items_to_existing_company_internal_profile(company_internal_profile, old_company_internal_profile):
    if not company_internal_profile.company_name:
        company_internal_profile.company_name = old_company_internal_profile.company_name
    if not company_internal_profile.full_web_address:
        company_internal_profile.full_web_address = old_company_internal_profile.full_web_address
    if not company_internal_profile.base_web_address:
        company_internal_profile.base_web_address = old_company_internal_profile.base_web_address
    if not company_internal_profile.language:
        company_internal_profile.language = old_company_internal_profile.language
    if old_company_internal_profile.latest_date_published:
        company_internal_profile.latest_date_published = old_company_internal_profile.latest_date_published
    if old_company_internal_profile.date:
        company_internal_profile.date = old_company_internal_profile.date
    if old_company_internal_profile.id:
        company_internal_profile.id = old_company_internal_profile.id

    get_list_unique_key_method = lambda company_internal_item: company_internal_item.bucket_path_list[0]
    company_internal_profile.company_internal_items = merge_lists(
        old_company_internal_profile.company_internal_items,
        company_internal_profile.company_internal_items,
        get_list_unique_key_method
    )

    company_internal_profile.company_external_items_dict = external_item_dated_version(
        old_company_internal_profile.company_external_items_dict,
        company_internal_profile.company_external_items_dict
    )
    company_internal_profile.company_internal_item_labels_dict = merge_dicts(
        old_company_internal_profile.company_internal_item_labels_dict,
        company_internal_profile.company_internal_item_labels_dict
    )
    company_internal_profile.company_internal_item_predictions_dict = merge_dicts(
        old_company_internal_profile.company_internal_item_predictions_dict,
        company_internal_profile.company_internal_item_predictions_dict
    )
    return company_internal_profile


def external_item_dated_version(old_company_external_items_dict, company_external_items_dict):
    old_company_company_external_github = old_company_external_items_dict.get(SourcesConstants.GITHUB,None)
    company_company_external_github = company_external_items_dict.get(SourcesConstants.GITHUB, None)
    if old_company_company_external_github and company_company_external_github:
        old_stargazers_count_dict = old_company_company_external_github.get(GithubConstants.STARGAZERS_COUNT)
        stargazers_count_dict = company_company_external_github.get(GithubConstants.STARGAZERS_COUNT)
        if old_stargazers_count_dict and stargazers_count_dict:
            stargazers_count_dict = merge_dicts(old_stargazers_count_dict, stargazers_count_dict)
            company_company_external_github[GithubConstants.STARGAZERS_COUNT] = stargazers_count_dict

        old_watchers_count_dict = old_company_company_external_github.get(GithubConstants.WATCHERS_COUNT)
        watchers_count_dict = company_company_external_github.get(GithubConstants.WATCHERS_COUNT)
        if old_watchers_count_dict and watchers_count_dict:
            watchers_count_dict = merge_dicts(old_watchers_count_dict, watchers_count_dict)
            company_company_external_github[GithubConstants.WATCHERS_COUNT] = watchers_count_dict
    company_external_items_dict[SourcesConstants.GITHUB] = company_company_external_github

    return merge_dicts(old_company_external_items_dict, company_external_items_dict)