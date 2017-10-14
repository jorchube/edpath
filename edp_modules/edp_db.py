#!/usr/bin/env python3

import os
import sys
import urllib.request
import json

from support.logging import log


_database_url = 'https://eddb.io/archive/v5/systems_populated.json'
_cache_file = 'cache/systems.json'


def load_data():
    with open(_cache_file) as raw_data:
        json_data = json.load(raw_data)

    return json_data


def retrieve_database(url=_database_url, cache_file=_cache_file):
    urllib.request.urlretrieve(url, cache_file)


## TESTS ##

def _should_retrieve_cache_file():
    test_cache_file = 'cache/test_cache_filename.json'
    if os.path.exists(test_cache_file):
        os.remove(test_cache_file)
    
    retrieve_database(_database_url, test_cache_file)
    assert os.path.exists(test_cache_file)

    os.remove(test_cache_file)


def _should_load_data_from_cache():
    data = load_data()

    assert len(data) > 0
    assert 'name' in data[0]
    assert 'x' in data[0]
    assert 'y' in data[0]
    assert 'z' in data[0]


def tests():
    _should_retrieve_cache_file()
    _should_load_data_from_cache()
    log('edp_db: OK')




