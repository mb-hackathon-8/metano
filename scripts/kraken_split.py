#!/usr/bin/env python

import os
import sys
import argparse

LIST = """abaumannii,Acinetobacter baumannii,470
abaumannii_2,Acinetobacter baumannii,470
achromobacter,Achromobacter,222
aeromonas,Aeromonas,642
arcobacter,Arcobacter,28196
bburgdorferi,Borrelia burgdorferi,139
bcc,Burkholderia cepacia,292
bcereus,Bacillus cereus,1396
bhampsonii,Brachyspira hampsonii,1287055
bhenselae,Bartonella henselae,38323
bhyodysenteriae,Brachyspira hyodysenteriae,159
bintermedia,Brachyspira intermedia,84377
blicheniformis,Bacillus licheniformis,1402
bordetella,Bordetella pertussis,520
borrelia,Borrelia,138
bpilosicoli,Brachyspira pilosicoli,52584
brachyspira,Brachyspira,29521
bsubtilis,Bacillus subtilis,1423
calbicans,Candida albicans,5476
campylobacter,Campylobacter coli,195
campylobacter,Campylobacter jejuni,197
cbotulinum,Clostridium botulinum,1491
cconcisus,Campylobacter concisus,199
cdifficile,Peptoclostridium difficile,1496
cdiphtheriae,Corynebacterium diphtheriae,1717
cfetus,Campylobacter fetus,196
cfreundii,Citrobacter freundii,546
cglabrata,Candida glabrata,5478
chelveticus,Campylobacter helveticus,28898
chlamydiales,Chlamydia,810
chyointestinalis,Campylobacter hyointestinalis,198
cinsulaenigrae,Campylobacter insulaenigrae,260714
ckrusei,Candida krusei,4909"""

def load_species(speciesTab):
    """
    Load a Species, Taxid, code, name TSV table to dictionary
    taxid -> [code, name]
    """
    species = {}
    for line in speciesTab.split('\n'):
        if line.startswith("#"):
            continue
        try:
            code, name, taxid = line.strip().split(",")
            species[taxid] = [code, name]
        except Exception as e:
            continue
    return species

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("-k", "--kraken-tsv", help="Kraken classification file")
    args.add_argument("-f", "--fastq-reads", help="Raw reads")
    args.add_argument("-o", "--output-dir", help="Output directory")
    args.add_argument("-l", "--min-length",  type=int, help="Min read length [default: %(default)s]", default=800)
    args.add_argument("-m", "--min-reads-per-species",  type=int, help="Min read per species [default: %(default)s]", default=3000)
    args = args.parse_args()

    taxid_to_tuple = load_species(LIST)
    print(f"Loaded {len(taxid_to_tuple)} species")
    # Load the kraken classification
    reads_to_taxid = {}
    with open(args.kraken_tsv) as fh:
        for line in fh:
            is_class, readName, taxid, seq_len, description = line.strip().split("\t")
            if is_class == "C" and int(seq_len) > args.min_length:
                if taxid in taxid_to_tuple:
                    reads_to_taxid[readName] = taxid
    
    # Number of distinct reads_to_taxid values
    for i, t in reads_to_taxid.items():
        print(i, "\t", t)

"""
U       46a0b354-9b84-4614-a78d-437c7bb46208    0       6293    0:6259
C       bb2314c5-475d-40e0-a333-30bd1fecf531    1351    5506    0:150 1351:5 0:3 1351:3 0:683 1351:2 0:144 51663:1 0:676 765910:5 0:264 1351:3 0:784 1351:5 0:294 1351:2 0:128 1351:5 0:57 1351:4 0:15 1351:4 0:292 1351:1 0:178 1351:3 0:682 1351:1 0:54 1351:1 0:3 1351:2 0:66 1351:2 0:21 1351:5 0:6 1351:1 0:126 1351:2 0:271 1351:5 0:15 1351:5 0:1 1351:1 0:491
"""