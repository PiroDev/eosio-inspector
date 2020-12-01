import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--scan-depth",
    type=str,
    choices=["low", "medium", "full"],
    default="low",
    help="determines the accuracy and speed of scanning ('full' - slow but accurate)",
)

args = parser.parse_args()

from eospy import ChainApi

api_endpoint = "https://eos.dfuse.eosnation.io/"

print("EOS MainNet api endpoint:", api_endpoint)

# Init endpoint connection
chain = ChainApi([api_endpoint])

query = []
# Get first producer
lower_bound = chain.get_table_rows("eosio", "eosio", "producers", limit=1)["rows"][0][
    "owner"
]

is_more = True

# Get all producers
while is_more:
    queryset = chain.get_table_rows(
        "eosio", "eosio", "producers", limit=500, lower_bound=lower_bound
    )
    query += queryset["rows"]
    lower_bound = query[len(query) - 1]["owner"]
    is_more = queryset["more"]

count = len(query)
print("Total producers count:", count)

# Sort producers by votes
query = sorted(query, key=lambda row: float(row["total_votes"]))[::-1]

if args.scan_depth == "low":
    count = 100
elif args.scan_depth == "medium":
    count //= 2

query = query[:count]

producers = []

# Get info about produsers balances
for row in query:
    account = chain.get_account(row["owner"])
    if account["voter_info"] != None and "core_liquid_balance" in account.keys():
        producer_info = {
            "account_name": account["account_name"],
            "liquid_balance": account["core_liquid_balance"],
            "staked": str((float(account["voter_info"]["staked"]) / 10000.0)) + " EOS",
            "last_vote_weight": account["voter_info"]["last_vote_weight"],
        }
        producers.append(producer_info)

# How many producers script should print
top_len = 25

# Sort producers by staked coins
producers = sorted(
    producers,
    key=lambda producer: float(producer["staked"][: producer["staked"].find(" ")]),
)[::-1][:top_len]

print("Top", top_len, "producers (by staked EOS):")

import json

json_data = json.dumps(producers, indent=4)

print(json_data)
