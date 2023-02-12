"""
To run tests you need to install pytest and jsonschema libs.
"""
from glob import glob
import os
import re
import json
from jsonschema import validate

TEMPLATE_KEYS = json.load(open('coin_schema.json'))['required']

def test_coin_names():
    re_coin_fname = re.compile(r'^[a-z0-9][a-z0-9_]+[a-z0-9]\.json$', re.I)
    for fname in os.listdir('coin'):
        if not re_coin_fname.match(fname):
            assert False, '%s is invalid coin filename' % fname


def test_coin_template_keys():
    tpl = json.load(open('coin_template.json'))
    assert set(tpl.keys()) == set(TEMPLATE_KEYS)


def test_coins_keys():
    for fname in glob('coin/*.json'):
        coin = json.load(open(fname))
        assert set(coin.keys()) == set(TEMPLATE_KEYS)


def test_coins_readme_link():
    for fname in glob('coin/*.json'):
        name = fname.split('/')[1].split('.')[0]
        content = open('README.rst').read()
        if '<coin/%s.json>' % name not in content:
            assert False, 'No link to %s in README.rst' % fname


def test_validate_with_schema():
    schema = json.load(open('coin_schema.json'))
    for fname in glob('coin/*.json'):
        coin = json.load(open(fname))
        validate(coin, schema)


def test_references_are_provided():
    for fname in glob('coin/*.json'):
        coin = json.load(open(fname))
        for key, val in coin.items():
            if coin['symbol'] in ('BTC', 'ETH', 'XRP'):
                # References check for these currencies are
                # temporarly disabled
                pass
            elif (
                    key in ('name', 'symbol', 'references')
                    or key.endswith('_url')
                ):
                pass
            elif val == "?":
                pass
            else:
                if not coin['references'].get(key):
                    raise Exception(
                        'Coin %s does not provide reference URL for %s key'
                        % (fname, key)
                    )
