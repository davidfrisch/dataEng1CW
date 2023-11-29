import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from comp0235_pipeline.database import create_session
from comp0235_pipeline.models.proteome import Proteomes
import argparse


def get_proteins(list_ids: list):
    session = create_session()
    proteins = session.query(Proteomes).filter(Proteomes.id.in_(list_ids)).all()
    session.close()
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

    proteins = get_proteins(list_ids)

    if not proteins:
        print("No proteins found")
        exit(0)


    output_file = "./proteins.csv" if not args.output else args.output    
    with open(output_file, "w") as f:
        f.write("id,description,sequence\n")
        for protein in proteins:
            f.write(f"{protein.id},{protein.description},{protein.sequence}\n")


