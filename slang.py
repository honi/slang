#!/usr/bin/env python3

import re
import sys
import argparse
from collections import defaultdict


add_syntax = re.compile(r'^\s*([XYZ]\d*)\s*<-\s*(\1)\s*\+\s*1\s*$')
sub_syntax = re.compile(r'^\s*([XYZ]\d*)\s*<-\s*(\1)\s*-\s*1\s*$')
ifgoto_syntax = re.compile(r'^\s*IF\s*([XYZ]\d*)\s*!=\s*0\s*GOTO\s*([A-Z]\d*)\s*$')
label_syntax = re.compile(r'^\s*\[\s*([A-Z0-9])+\s*\](.+)$')
comment_syntax = re.compile(r'^\s*#.+$')


def parse(src_file):
    src = []
    labels = {}
    with open(src_file) as f:
        for ins in f.readlines():
            ins = ins.strip().upper()
            if not ins or comment_syntax.match(ins):
                continue
            if m := label_syntax.match(ins):
                label = m[1]
                if label not in labels:
                    labels[label] = len(src)
                ins = m[2]
            src.append(ins.strip())
    return src, labels


def run(src_file, args):
    src, labels = parse(src_file)
    vars = defaultdict(int)
    labels = defaultdict(lambda: len(src), labels)

    for i, x in enumerate(args):
        vars[f'X{i+1}'] = x

    pc = 0 # program counter
    while True:
        if pc == len(src):
            break
        ins = src[pc]
        pc += 1
        if m := add_syntax.match(ins):
            v = m[1]
            vars[v] += 1
        elif m := sub_syntax.match(ins):
            v = m[1]
            if vars[v] > 0: vars[v] -= 1
        elif m := ifgoto_syntax.match(ins):
            v = m[1]
            l = m[2]
            if vars[v] != 0: pc = labels[l]
        else:
            print(f'Invalid instruction: {ins}')
            sys.exit(1)

    print('Y =', vars['Y'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('x', metavar='X1, X2, ...', type=int, nargs='*')
    parser.add_argument('--src', dest='src', type=str)
    args = parser.parse_args()
    run(args.src, args.x)
