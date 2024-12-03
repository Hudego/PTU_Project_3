from Bio.PDB import PDBParser
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO
import os

def extract_sequences(pdb_folder, output_fasta):
    parser = PDBParser(QUIET=True)
    records = []

    for pdb_file in os.listdir(pdb_folder):
        if pdb_file.endswith(".pdb"):
            structure = parser.get_structure(pdb_file, os.path.join(pdb_folder, pdb_file))
            for model in structure:
                for chain in model:
                    seq = ""
                    for residue in chain:
                        if residue.has_id("CA"):  
                            seq += residue.resname
                    if seq:
                        seq_record = SeqRecord(Seq(seq), id=f"{pdb_file}_{chain.id}")
                        records.append(seq_record)

    SeqIO.write(records, output_fasta, "fasta")
    print(f"Fichier FASTA généré : {output_fasta}")

pdb_folder = "/Users/unluismail/Downloads/fragments_nettoyes"
output_fasta = "fragmentfasta2"
extract_sequences(pdb_folder, output_fasta)
