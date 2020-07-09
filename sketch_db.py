#!/usr/bin/env python3

import argparse
import os
import subprocess
import glob
import screed
import sourmash
from create_db import create_connection
from sourmash import SourmashSignature, save_signatures


def parse_args():
    parser = argparse.ArgumentParser(usage='sketch_db.py -database <database name>')
    parser.add_argument("-database", help="<string>: name of the database")
    return parser.parse_args()


# Download the assembly according to the sra database
def skesa_assembly_download(SRR):
    try:
        subprocess.check_call(
            "dump-ref-fasta http://sra-download.ncbi.nlm.nih.gov/srapub_files/" + SRR + "_" + SRR + ".realign > " +
            "database/" + SRR + "_skesa.fa", shell=True)
        print("Downloaded assembly for " + SRR)
    except subprocess.CalledProcessError:
        print("Can't download SKEASA assembly for " + SRR)
        return


def get_signatures():
    genomes = glob.glob('database/*_skesa.fa')
    minhashes = []
    for g in genomes:
        mh = sourmash.MinHash(n=1000, ksize=21)
        for record in screed.open(g):
            mh.add_sequence(record.sequence, True)
        minhashes.append(mh)
    siglist = []
    for i in range(len(minhashes)):
        siglist.append(SourmashSignature(minhashes[i], name=genomes[i].strip('database/').strip('_skesa.fa')))
    with open('database.sig', 'wt') as fp:
        save_signatures(siglist, fp)


def main():
    args = parse_args()

    if os.path.exists(args.database + '.db'):
        pass
    else:
        print("Database does not exist. Please make sure the name is correct or run create_db.py and "
              "metadata_sra_db.py first")
        exit()

    conn = create_connection(args.database + '.db')
    if os.path.exists("database"):
        pass
    else:
        os.mkdir("database")

    c = conn.cursor()
    cursor = c.execute("SELECT srr from sra")
    # get the assembly
    for row in cursor:
        if os.path.exists("database/" + row[0] + "_skesa.fa"):
            print("The assembly already exists.")
            continue
        else:
            skesa_assembly_download(row[0])

    # delete all the empty assembly generated by error
    subprocess.check_call("find ./database -empty -type f -delete", shell=True)

    # get a collection of the genome signatures
    get_signatures()
    conn.close()


if __name__ == '__main__':
    main()