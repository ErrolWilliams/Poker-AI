#!/usr/bin/python3

import urllib.request
from lxml import html
import json
import os

JSON_PATH = 'tables.json'

def _classify(key):
    c1 = None
    c2 = None
    suited = None
    if "Pair of" in key:
        suited = 'u'
        c1 = c2 = key[-3]
    else:
        c1 = key[0]
        c2 = key[2]
        if "unsuited" in key:
            suited = 'u'
        else:
            suited = 's'
    return c1 + c2 + suited

def _p2f(p):
    return float(p.strip('%'))/100

def _pull_table(num_players):
    url = "https://wizardofodds.com/games/texas-hold-em/{}-player-game".format(num_players)
    data = None

    with urllib.request.urlopen(url) as file:
        data = file.read()

    tree = html.fromstring(data)
    table = tree.xpath("//table[@class='data']")[0]
    trs = table.xpath("*")[1:-1]

    r = {}

    for tr in trs:
        tds = tr.xpath("*")
        key = _classify(tds[0].text)
        if num_players == 2:
            r[key] = {"win": _p2f(tds[1].text), "lose": _p2f(tds[2].text), "draw": _p2f(tds[3].text), "expected_val": _p2f(tds[4].text), "probability": _p2f(tds[5].text), "additive_probability": _p2f(tds[6].text)}
        else:
            r[key] = {"win": _p2f(tds[1].text), "lose": _p2f(tds[2].text), "expected_val": _p2f(tds[3].text), "probability": _p2f(tds[4].text), "additive_probability": _p2f(tds[5].text)}

    return r

def pull():
    print("Pulling tables...")

    big_dict = {}

    for i in [2,3,4,6,8,10]:
        table = _pull_table(i)
        big_dict[i] = table

    with open(JSON_PATH, 'w') as f:
        f.write(json.dumps(big_dict, indent=4))

    print("Pulled tables")

tables = None

def get_chance(players, c1, c2):
    if players > 10:
        players = 10
    elif players == 9 or players == 7 or players == 5:
        players = players - 1

    return win_chance(players, c1[0], c2[0], 's' if c1[1] == c2[1] else 'u')

def win_chance(players, c1, c2, suitedness):
    ptable = tables[str(players)]
    key = c1 + c2 + suitedness
    if not key in ptable:
        key = c2 + c1 + suitedness
        if not key in ptable:
            print(f"{key} not found in {players} player table")
            return 0.2
    return ptable[key]['win']


if __name__ == "__main__":
    pull()
    exit()

#Init module
if not os.path.isfile(JSON_PATH):
    pull()

with open(JSON_PATH, 'r') as json_file:
    tables = json.loads(json_file.read())
