import sys
import os
import re
import json

regexp = [ 
        ("type",r"type=(\w+)\n") ,
        ("time",r"time=([\w *]+)\n") ,
        ("ptype",r"ptype=(\w+)\n"),
        ("rem",r"rem=([\w:\s]+)\n"),
        ("context",r"context=([\w:\s]+)\n"),
        ("pattern",r"pattern=([\w\s\(\)\[\]\\\.\+\*\?:!><\|-]+)\n"),
        ("desc",r"desc=([\w '\.\$>=]+)\n"),
        ("thresh",r"thresh=([0-9]+)\n"),
        ("window",r"window=([0-9]+)\n"),
        ("action",r"action=([\w %:,;$\S\n]+)\n"),
        ]

set_rules =  {
        "active" : list(),
        "commented" : list()
        }

def parse_block(blocks, prefix= "^"):
    """
    :block : list of strings which contain a rule
    :prefix : specify a prefix for a rule, by default the value was set at '^'
              It means a beginning of line.
    """
    rules = list()
    for block_rule in blocks:
        rule = dict()
        for reg in regexp:
            m=re.search(prefix+reg[1], block_rule+"\n", re.MULTILINE)
            # If a regexp match, we add it in dictionnary
            if m is not None:
                rule[reg[0]] = m.group(1)

        rules.append(rule)
    return rules


# Open file and load it in variable data
with open(sys.argv[1]) as handle:
    data = handle.read()


    # divide data in many block.
    # hypothesis, each rule need to be seperated by two \n
    # so an occured appears  with ssh-brute.sec
    blocs = data.split('\n\n')
    active_rule = list()
    commented_rule = list()
    for bloc in blocs:
        if "type=" == bloc[:5]:
            active_rule.append(bloc)
        if "#type=" == bloc[:6]:
            commented_rule.append(bloc)

    set_rules["active"] = parse_block(active_rule)
    set_rules["commented"] = parse_block(commented_rule, "#")

    print json.dumps(set_rules,indent=4)

with open("output.json","w") as handle:
    handle.write(json.dumps(set_rules,indent=4))

