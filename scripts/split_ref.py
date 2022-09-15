#!/usr/bin/env python3
"""
Parse StrobeMap output

Andrea Telatin 2022
"""
import sys
import os

def read_fasta(path):
    import gzip
    seqName = None
    seqComment = None
    with (gzip.open if path.endswith('.gz') else open)(path, 'rt') as fasta:
        for line in fasta:
            if line.startswith('>'):
                if seqName is not None:
                    yield seqName, seqComment, sequence
                seqName = line[1:].split()[0]
                seqComment = line[1:].split()[1:] if len(line[1:].split()) > 1 else ""
                sequence = ""
                
            else:
                sequence += line.strip()
    yield seqName, seqComment, sequence
   

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Parse strob output')
    parser.add_argument('FASTA', help='FASTA file')
    parser.add_argument('-o', '--output', help='output basename')
    parser.add_argument('-n', '--parts', help='number of parts', type=int, default=3)
    args = parser.parse_args()

    out = sys.stdout if args.output is None else open(args.output, 'w')

    for name, comment, seq in read_fasta(args.FASTA):
        seqlen = len(seq)
        partlen = seqlen // args.parts
        for i in range(args.parts):
            partnum = i + 1
            start = i * partlen
            end = start + partlen
            if i == args.parts - 1:
                end = seqlen
            print(f">{name}_{partnum}\n{seq[start:end]}", file=out)