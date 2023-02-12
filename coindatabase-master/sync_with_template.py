#!/usr/bin/env python
from pprint import pprint
import json
import sys
from glob import glob
from collections import OrderedDict
from argparse import ArgumentParser


def main():
    parser = ArgumentParser()
    parser.add_argument(
        '-d', '--drop-invalid-keys',
        action='store_true', default=False
    )
    opts = parser.parse_args()
    with open('coin_template.json') as inp:
        tpl = json.load(inp, object_pairs_hook=OrderedDict)
    tpl_keys = list(tpl.keys())
    for fname in glob('coin/*.json'):
        with open(fname) as inp:
            coin = json.load(inp, object_pairs_hook=OrderedDict)
            for key in coin.keys():
                if key not in tpl:
                    if opts.drop_invalid_keys:
                        del coin[key]
                        print('Coin %s, drop key %s' % (
                            fname, key
                        ))
                    else:
                        raise Exception('Coin %s, key %s is not valid' % (
                            fname, key
                        ))
            for key in tpl.keys():
                if not key in coin:
                    coin[key] = '?'
                    print('Coin %s, new key %s' % (
                        fname, key
                    ))
            new_coin = OrderedDict(
                sorted(coin.items(), key=lambda x: tpl_keys.index(x[0]))
            )
            with open(fname, 'w') as out:
                json.dump(
                    new_coin, out, indent=4, ensure_ascii=False,
                    separators=(',', ': ')
                )


if __name__ == '__main__':
    main()
