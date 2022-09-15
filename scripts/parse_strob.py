#!/usr/bin/env python3
"""
Parse StrobeMap output

Andrea Telatin 2022
"""
import sys
import os

class Match:
    def __init__(self, line):
        #ref_id  ref_pos query_pos   match_length_on_reference
        self.reference, self.ref_pos, self.query_pos, self.length = line.strip().split()

    def __str__(self):
        return "{}:{}\t{}\tlen={}".format(self.reference, self.ref_pos, self.query_pos, self.length)

    def __repr__(self):
        return f"({self.reference}:{self.ref_pos}, len={self.length})"

    def __eq__(self, __o: object) -> bool:
        return self.reference == __o.reference and self.ref_pos == __o.ref_pos and self.query_pos == __o.query_pos and self.length == __o.length

    def __hash__(self) -> int:
        # Hashable so we can use set() and dict()
        return hash((self.reference, self.ref_pos, self.query_pos, self.length))
     
def read_smap(path):
    import gzip
    seqName = None
    seqStrand = None
    matches = []
    with (gzip.open if path.endswith('.gz') else open)(path, 'rt') as fasta:
        for line in fasta:
            if line.startswith('>'):
                if seqName is not None:
                    yield  seqName, seqStrand, matches
                seqName = line[1:].split()[0].strip().rstrip()
                seqStrand = "-" if  "Reverse" in line else "+"
                matches = []
                
            else:
                matches.append(Match(line))
    yield seqName, seqStrand, matches

def parse_matches(list_of_matches, minlen):
    # Sort by reference position
    list_of_matches.sort(key=lambda x: str(x.reference))
    # Group by reference
    ref_dict = {}
    for match in list_of_matches:
        if match.reference not in ref_dict:
            ref_dict[match.reference] = match.length
        else:
            ref_dict[match.reference] += match.length

    # Filter by length
    return [ref for ref, length in ref_dict.items() if int(length) >= minlen]

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Parse strob output')
    parser.add_argument('strob', help='strob output file')
    parser.add_argument('-o', '--output', help='output file')
    parser.add_argument('-m', '--min-length', type=int, default=800, help='minimum length of the match on the reference')
    args = parser.parse_args()

    out = sys.stdout if args.output is None else open(args.output, 'w')

    for name, strand, matches in read_smap(args.strob):
        if len(matches) > 0:
            
            parsed = parse_matches(matches, args.min_length)
            #print(f"{name}\tst={strand}\t{len(matches)}\t{matches}\t{parsed}", file=out)
            for x in parsed:
                print(f"{name}\t{x}\t{len(matches)}\t{matches}", file=out)
                
    