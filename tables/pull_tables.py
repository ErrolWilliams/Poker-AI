#!/usr/bin/python3


import urllib.request
from lxml import html
import pprint
pp = pprint.PrettyPrinter(indent=2)

def pull_table(num_players):
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
        if num_players == 2:
            r[tds[0].text] = {"win": tds[1].text, "lose": tds[2].text, "draw": tds[3].text, "expected_val": tds[4].text, "probability": tds[5].text, "additive_probability": tds[6].text}
        else:
            r[tds[0].text] = {"win": tds[1].text, "lose": tds[2].text, "expected_val": tds[3].text, "probability": tds[4].text, "additive_probability": tds[5].text}
        
    return r

def to_array(table):

    char_to_num = {
            'A' : 0,
            '2' : 1,
            '3' : 2,
            '4' : 3,
            '5' : 4,
            '6' : 5,
            '7' : 6,
            '8' : 7,
            '9' : 8,
            'T' : 9,
            'J' : 10,
            'Q' : 11,
            'K' : 12,
            't' : -1
    }

    r = ['0']*(13*13*2)

    for key in table:
        c1 = None
        c2 = None
        suited = None
        if "Pair of" in key:
            suited = 0
            c1 = c2 = char_to_num[key[-3]]
        else:
            c1 = char_to_num[key[0]]
            c2 = char_to_num[key[2]]
            if "unsuited" in key:
                suited = 0
            else:
                suited = 1
        index = c1*(13*2) + c2*2 + suited
        #print("Key: '{}', c1: {}, c2: {}, suited: {}, index: {}".format(key, c1, c2, suited, index))
        r[index] = table[key]["win"][:-1]
    return r
        
def get_num(arr, c1, c2, suited):
    index = c1*(13*2) + c2*2 + suited
    return arr[index]


def to_java(num_players, array):
    out = "float[] {}p = {{".format(num_players)
    for num in array:
        out += num + ", "

    out = out[:-2] + "};"
    return out



    


for i in [2,3,4,6,8,10]:
    table = pull_table(i)
    #pp.pprint(table)
    
    arr = to_array(table)
    j_arr = to_java(i, arr)
    with open('stats.java', 'a+') as f:
        f.write(j_arr + "\n\n")


