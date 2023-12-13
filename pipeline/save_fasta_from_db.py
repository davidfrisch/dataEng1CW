import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from pipeline.constants import ROOT_DIR
from pipeline.database import create_session
from pipeline.models.proteome import Proteomes
import argparse


def create_fasta_file(list_ids: list, output_file: str):
    try:
        session = create_session()
        proteins = session.query(Proteomes).filter(Proteomes.id.in_(list_ids)).all()
        session.close()
    except Exception as e:
        print(e)
  
    with open(output_file, "w") as f:
        for protein in proteins:
            f.write(f">{protein.id}\n{protein.sequence}\n")

    return proteins



if __name__ == "__main__":
  
    list_ids = None
    argparser = argparse.ArgumentParser(description="Get proteins from the database")
    argparser.add_argument("-f", "--file", help="File with protein ids", required=False)
    argparser.add_argument("-l", "--list", help="List of protein ids separated by commas. Start and close the list with double quotes", required=False)
    argparser.add_argument("-o", "--output", help="Output file", required=False)
    args = argparser.parse_args()

    if not args.file and not args.list:
        print("No input given")
        exit(0)

    if args.file and args.list:
        print("Only one input allowed, either -f or -l")
        exit(0)

    if args.file:
        with open(args.file, "r") as f:
            list_ids = [line.strip() for line in f.readlines()]
    elif args.list:
        list_ids = args.list.split(",")

    if not list_ids:
        print("No ids in input")
        exit(0)

    output_file = f"{ROOT_DIR}/data/proteins.fasta" if not args.output else args.output    
    proteins = create_fasta_file(list_ids, output_file)

    for id in list_ids:
        if id not in proteins:
            print(f"Not found: {id}")
    
    print(f"{len(proteins)} /{len(list_ids)} Proteins saved in {output_file}")


