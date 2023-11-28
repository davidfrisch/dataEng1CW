from models.proteome import Proteomes
from database import create_session
from Bio import SeqIO
import sys

def save_fasta_in_db(fasta_file):
    session = create_session()
    for record in SeqIO.parse(fasta_file, "fasta"):
        proteome = Proteomes(
            id=record.id,
            description=record.description,
            sequence=str(record.seq)
        )
        # check if the record exists
        if session.query(Proteomes).filter_by(id=record.id).first():
            print("Already in database, Skipping", record.id)
            continue
        
        session.add(proteome)
        print("Added", record.id)

    session.commit()
    session.close()
    print("Saved all records in the database")

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1:
        print("Usage: python save_fasta_in_db.py <fasta_file>")
        sys.exit(1)

    fasta_file = args[0]
    save_fasta_in_db(fasta_file)
