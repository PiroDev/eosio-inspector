# EOS network inspector

The program gets informations about EOS network producers and prints top rated by votes and staked coins.

## Installation

>Program requires python3

Install python dependencies:

`$ pip3 install -r requirements.txt`

## Usage

`$ python3 eos-inspector.py [--scan-depth=<depth>]`

The program has three network scan-depth modes:

- low (default) - simplified producers sorting
- medium - common producers sorting
- full - advanced producers sorting (can take up to 5-10 minutes)

>Simplified sorting also works pretty well

Example input:

`$ python3 eos-inspector.py --scan-depth=medium`

Example output:

```json
EOS MainNet api endpoint: https://eos.dfuse.eosnation.io/
Total producers count: 629
Top 25 producers (by staked EOS):
[
    {
        "account_name": "eostitanprod",
        "liquid_balance": "1522.0545 EOS",
        "staked": "34702.6841 EOS",
        "last_vote_weight": "671828998417994.00000000000000000"
    },
    ...
    {
        "account_name": "eoseouldotio",
        "liquid_balance": "1691.4063 EOS",
        "staked": "951.4002 EOS",
        "last_vote_weight": "10663710433103.33789062500000000"
    }
]
```

