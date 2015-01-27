import argparse
import os
import sys


ERROR_FILE=99
ERROR_NOT_SEC_FILE_EXT=98



single_line_keyword = ["type=","ptype=","pattern=","desc=","thresh=","window=",
           "pattern2=","ptype2=","desc2=","thresh2=","window2=","time=",
           "context=","varmap=","script=","continue=","context2=","varmap2=",
           "continue2=","init=","slide=","end=","label="]

sMaxBasicKW = 0
for k in single_line_keyword:
    if sMaxBasicKW < len(k):
        sMaxBasicKW  = len(k)


class ExceptionNotValidFile(Exception):
    def __init__(self, value):
         self.value = value

    def __str__(self):
         return repr(self.value)


def parserBasicKey(nRule, key, line):

    result[nRule] = dict()
    value=line.split(key+"=")
    result[nRule][key]='='.join(value[1:])
    print key, '='.join(value[1:])
    return result[nRule]

def parserpType(line):
    print "parserType()"

def parseAction(line):
    pass

def parserGlobal(lines):

    result = dict()
    nRule = 0

    for line in lines:
        if "#" in line:
            #manage comment
            continue

        for keyword in single_line_keyword:
            if keyword in line[:sMaxBasicKW]:
                if keyword == "type=":
                    nRule += 1
                parserBasicKey(nRule, k, line)
                continue




def parse_secfile(input):
    if ".sec" != input[-4:]:
        raise ExceptionNotValidFile("Not valid file")

    with open(input, "r") as myfile:
        parserGlobal(myfile.readlines())


def main():
    parser = argparse.ArgumentParser(description='Edit SEC Rules')
    parser.add_argument('input', help='directory or file')
    args = parser.parse_args()

    if os.path.isfile(args.input):
        try:
            parse_secfile(args.input)
        except ExceptionNotValidFile as error:
            print "Not a valide file"
    elif os.path.isdir(args.input):
        print "this is an directory: "+args.input
        for item in os.listdir(args.input):
            try:
                parse_secfile(os.path.join(args.input,item))
            except ExceptionNotValidFile as error:
                print "Not a valide filel"
    else:
        print "Error, you do not provide a regular file or a directory"
        sys.exit(ERROR_FILE)


if __name__ == '__main__':
    main()
