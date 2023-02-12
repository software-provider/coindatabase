.. image:: https://travis-ci.org/lorien/coindatabase.png?branch=master
    :target: https://travis-ci.org/lorien/coindatabase?branch=master

About CoinDataBase project
--------------------------

TLDR; Get me to the `list of coins <#coins>`_

CoinDataBase is a database of crypto currencies basic properties like market
symbol, website, privacy/scalability/governor features, etc.

The main idea of database is to provide not only the data but also proofs -
URLs of web documents providing details about the values specified in database
(see Policy for adding/changing data below).

This database would be useful to all people studying the crypto world.

Feel free to submit pull requests with new coins or corrections of existing
data.


How to add new coin
-------------------

Fork the repository.

Copy `coin_template.json <coin_template.json>`_ to coin/ directory and name it
with coin name. Use common coin name, do not lowercase all letters, use
underscore instead of space.

Good names:

* Ethereum_Classic.json
* NEM.json
* iDice.json

Bad names:

* Ethereum Classic.json
* ethereum_classic.json
* Nem.json
* nem.json
* idice.json

Edit the new file and fill all coin propertes you know. If you do knot know or
do not understand some properties just put "?" string there. Do not delete
keys, just put "?" string e.g.:

.. code:: json

    "tx_per_second": "?"

Keys which names ends with "_url" are list of urls. They could contain up
to 3 items. Each item have to be valid URL.

The required minimum set of non-blank properties to add new coin is:

* name
* symbol 
* website_url

Add link to new coin file to README.rst. List of coins are sorted in alphabetic
order.

When you are ready create pull request and check in few minutes if automatic
travis tests passed. Travis checks your changes for missing keys, invalid data
types and other possible mistakes. If pull requests passed the tests I'll merge
it in main repo or will write comment if something concerns me.


References property
-------------------

The "references" key points to object which keys are the usual coin properties 
and values are list of urls to web documents that proofs the value of 
the corresponding coin property is correct e.g.:

.. code:: json

    "references": {
        "tx_min_fee": [
            "https://ripple.com/build/transaction-cost/"
        ]
    }

Each list could contains up to 3 items.


Conventions
-----------

Numbers could be specified in short form using suffixes K (thousands),
M (millions) and B (billions) e.g. 21M equals to 21000000

Values of `block_size` key have to used another suffixes: KB (kilobytes) and
MB (megabytes).

For boolean properties like `anonymous` the "yes" and "no" values must be used.

If the property can not be applied to the coin e.g. `masternode_supply` for
Ethereum, set the value to "NA" (not applicable).

If the value is unlimited use "Inf" string e.g.:

.. code:: json

    "max_supply": "Inf"


Policy for adding/changing data
-------------------------------

For any property except `name`, `symbol` and `%_url` one of the rules have
to be satisfied:

* the value of property is "?" or empty list
* at least one proof URL exists at corresponding key in `references`
  property

Properties `name`, `symbol` and `%_url` do not require proof URLs. But they
could be annotated with proof URLs if you think it makes sense.

How to validate data
--------------------

This is completely optional.

In case of you want to run tests on your local machine you will need python
interpreter.

Install additional libraries with command:

.. code:: shell

    pip install pytest
    pip install jsonschema

Now run test with command:

.. code:: shell

    pytest

Also you can just send github pull request and wait few minutes for travis CI
makes testing for you. You'll see results of testing inside your pull request
on github.

Donation
--------

If you would like to support the project with money feel free to send it to
following addresses

BTC: 1L1e1L85zpxb1BYsRh7neFMifa96XWpSTd

LTC: 0x00CFb6B03733F52dEBB77B889a95cde2c78cD81f


Coins
-----

* `Bitcoin <coin/Bitcoin.json>`_
* `Ethereum <coin/Ethereum.json>`_
* `Ripple <coin/Ripple.json>`_
* `Litecoin <coin/Litecoin.json>`_
* `Ethereum Classic <coin/Ethereum_Classic.json>`_
* `Dash <coin/Dash.json>`_
* `NEM <coin/NEM.json>`_
