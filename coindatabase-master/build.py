#!/usr/bin/env python3
from subprocess import check_call
import json
import shutil
from glob import glob
import os
from datetime import datetime
import time
from collections import OrderedDict


CONST_KEYS = (
    'name', 'symbol', 'website_url', 'blockchain_explorer_url',
    'nodes_explorer_url', 'message_board_url',
    'twitter_url', 'reddit_url', 'repo_url',
    'wikipedia_url',
    'whitepaper_url', 'telegram_url',
    'hash_algo', 'consensus',
    'anonymous', 'core_lang',
    'references', 'lightning_network',
    'masternode', 'smart_contracts', 'lighning_network',
    'blockchain_model', 'announcement_url',
    "masternode",
    "tx_anonymity", "treasury", "governance",
    "wikipedia_description"
)
NUM_KEYS = (
    'max_supply', 'block_time', 'block_reward',
    'tx_per_second', 'tx_min_fee',
    "masternode_deposit",
)
SIZE_KEYS = (
    'block_max_size',
)
DATE_KEYS = (
    'genesis_block_date',
)


def parse_num(val):
    if isinstance(val, (int, float)):
        return val
    elif val.endswith(('B', 'M', 'K')):
        num = float(val[:-1])
        factor = {
            'B': 1000**3,
            'M': 1000**2,
            'K': 1000,
        }[val[-1]]
        return int(num * factor)
    else:
        if '.' in val:
            return float(val)
        else:
            return int(val)


def parse_size(val):
    num = int(val[:-2])
    factor = {
        'GB': 1024**3,
        'MB': 1024**2,
        'KB': 1024,
    }[val[-2:]]
    return num * factor


def parse_date(val):
    moment = datetime.strptime(val, '%Y-%m-%d')
    return int(time.mktime(moment.timetuple()))


def normalize_prop_value(key, val):
    if val == "?":
        return None
    elif val == "NA":
        return "NA"
    elif val == "Inf":
        return "Inf"
    elif key in CONST_KEYS:
        return val
    elif key in NUM_KEYS:
        return parse_num(val)
    elif key in SIZE_KEYS:
        return parse_size(val)
    elif key in DATE_KEYS:
        return parse_date(val)
    else:
        assert False, 'Unknown key: %s' % key


def normalize_coin_data(coin):
    res = OrderedDict()
    for key, val in coin.items():
        res[key] = normalize_prop_value(key, val)
    return res


def create_build_files():
    config = json.load(open('config.json'))
    new_version = config['version'] + 1
    print('New build version is %d' % new_version)
    database = OrderedDict([
        ('_ver', new_version),
        ('date', datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')),
        ('items', []),
    ])
    if os.path.exists('build'):
        shutil.rmtree('build')
    os.mkdir('build')
    for fname in glob('coin/*.json'):
        coin = json.load(open(fname), object_pairs_hook=OrderedDict)
        new_fname = 'build/%s.json' % coin['symbol']
        norm_coin = OrderedDict()
        norm_coin['_ver'] = new_version 
        norm_coin.update(normalize_coin_data(coin))
        with open(new_fname, 'w') as out:
            json.dump(norm_coin, out, indent=4, ensure_ascii=False)
        database['items'].append(norm_coin)
    with open('build/coindatabase.json', 'w') as out:
        json.dump(database, out, indent=4, ensure_ascii=False)
    config['version'] = new_version
    json.dump(config, open('config.json', 'w'), indent=4, ensure_ascii=False)
        


def main():
    # First, validate data
    check_call('pytest', shell=True)
    # Now we can be sure data are valid
    # so we do not need to do lot of validation
    # and can focus on data modification
    create_build_files()


if __name__ == '__main__':
    main()
