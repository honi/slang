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


def parse(raw_src):
    src = []
    labels = {}
    for ins in raw_src.split('\n'):
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


def run(src, labels, args):
    vars = defaultdict(int)
    labels = defaultdict(lambda: len(src), labels)

    for i, x in enumerate(args.x):
        vars[f'X{i+1}'] = x

    pc = 0 # program counter
    steps = 0
    while True:
        if pc == len(src):
            break

        if args.max_steps > 0 and steps == args.max_steps:
            print('Max steps executed, program killed')
            sys.exit(1)

        ins = src[pc]
        pc += 1
        steps += 1

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

    return vars['Y']


def main(args):
    if args.src == '-':
        raw_src = sys.stdin.read()
    else:
        with open(args.src) as f:
            raw_src = f.read()
    src, labels = parse(raw_src)
    result = run(src, labels, args)
    print(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('x', metavar='X1, X2, ...', type=int, nargs='*')
    parser.add_argument('--src', dest='src', type=str, metavar='', default='-', help='input source file (default stdin)')
    parser.add_argument('--max-steps', dest='max_steps', metavar='', type=int, default=0, help='max steps before stopping execution (0 runs forever)')
    args = parser.parse_args()
    main(args)
