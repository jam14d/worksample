import streamlit as st
import random

from pipeline import Pipeline
from string_reader import StringReader
from character_capitalizer import CharacterCapitalizer
from dna_base_converter import DNABaseConverter
from space_remover import SpaceRemover
from special_characters_remover import SpecialCharactersRemover

def mutate_dna(dna_sequence, mutation_rate):
    """Mutates the given DNA sequence based on the mutation rate."""
    dna_list = list(dna_sequence)
    for i in range(len(dna_list)):
        if random.random() < mutation_rate:
            mutations = {'A': 'CGT', 'C': 'AGT', 'G': 'ACT', 'T': 'ACG'}
            base_to_mutate = dna_list[i]
            mutated_base = random.choice(mutations[base_to_mutate])
            dna_list[i] = mutated_base
    return ''.join(dna_list)

def transcribe_dna_to_rna(dna_sequence):
    """Transcribes DNA sequence into RNA by replacing all instances of 'T' with 'U'."""
    return dna_sequence.replace('T', 'U')

def highlight_stop_codons(rna_sequence):
    """Highlights stop codons in the RNA sequence."""
    stop_codons = ['UAA', 'UAG', 'UGA']
    for codon in stop_codons:
        rna_sequence = rna_sequence.replace(codon, f"<span style='color:red; font-weight:bold;'>{codon}</span>")
    return rna_sequence

def translate_rna_to_protein(rna_sequence):
    """Translates RNA sequence into protein based on codon mapping."""
    codon_to_amino_acid = {
        'UUU': 'Phe', 'UUC': 'Phe', 'UUA': 'Leu', 'UUG': 'Leu',
        'UCU': 'Ser', 'UCC': 'Ser', 'UCA': 'Ser', 'UCG': 'Ser',
        'UAU': 'Tyr', 'UAC': 'Tyr', 'UAA': 'Stop', 'UAG': 'Stop',
        'UGU': 'Cys', 'UGC': 'Cys', 'UGA': 'Stop', 'UGG': 'Trp',
        'CUU': 'Leu', 'CUC': 'Leu', 'CUA': 'Leu', 'CUG': 'Leu',
        'CCU': 'Pro', 'CCC': 'Pro', 'CCA': 'Pro', 'CCG': 'Pro',
        'CAU': 'His', 'CAC': 'His', 'CAA': 'Gln', 'CAG': 'Gln',
        'CGU': 'Arg', 'CGC': 'Arg', 'CGA': 'Arg', 'CGG': 'Arg',
        'AUU': 'Ile', 'AUC': 'Ile', 'AUA': 'Ile', 'AUG': 'Met',
        'ACU': 'Thr', 'ACC': 'Thr', 'ACA': 'Thr', 'ACG': 'Thr',
        'AAU': 'Asn', 'AAC': 'Asn', 'AAA': 'Lys', 'AAG': 'Lys',
        'AGU': 'Ser', 'AGC': 'Ser', 'AGA': 'Arg', 'AGG': 'Arg',
        'GUU': 'Val', 'GUC': 'Val', 'GUA': 'Val', 'GUG': 'Val',
        'GCU': 'Ala', 'GCC': 'Ala', 'GCA': 'Ala', 'GCG': 'Ala',
        'GAU': 'Asp', 'GAC': 'Asp', 'GAA': 'Glu', 'GAG': 'Glu',
        'GGU': 'Gly', 'GGC': 'Gly', 'GGA': 'Gly', 'GGG': 'Gly'
    }
    protein = []
    for i in range(0, len(rna_sequence), 3):
        codon = rna_sequence[i:i+3]
        if codon in codon_to_amino_acid and codon_to_amino_acid[codon] != 'Stop':
            protein.append(codon_to_amino_acid[codon])
        elif codon in codon_to_amino_acid and codon_to_amino_acid[codon] == 'Stop':
            break
    return ' '.join(protein)

def run_pipeline(input_string, mutation_rate=0):
    """
    Runs the transformation pipeline on an input string and applies mutations if specified.
    """
    pipeline = Pipeline()
    pipeline.add(StringReader())
    pipeline.add(CharacterCapitalizer())
    pipeline.add(DNABaseConverter())
    pipeline.add(SpaceRemover())
    pipeline.add(SpecialCharactersRemover())
    
    original_dna_output = pipeline.execute(input_string)
    mutated_dna_output = original_dna_output
    
    if mutation_rate > 0:
        mutated_dna_output = mutate_dna(original_dna_output, mutation_rate)
    
    return original_dna_output, mutated_dna_output

# Streamlit interface
st.title('DNA to Protein Simulator')
user_input = st.text_area("Enter your text to convert into DNA:", "Type your text here...")
mutation_rate = st.slider("Mutation rate (in percentage):", min_value=0.0, max_value=100.0, value=0.0, step=0.1) / 100

if st.button('Transcribe and Translate'):
    if user_input:
        # Generate and mutate DNA
        original_dna, mutated_dna = run_pipeline(user_input, mutation_rate)
        st.text("Original DNA Sequence (before mutation):")
        st.write(original_dna)

        st.text("Mutated DNA Sequence:")
        st.write(mutated_dna)

        # Transcribe to RNA
        rna_output = transcribe_dna_to_rna(mutated_dna)
        st.text("Resulting RNA Sequence:")
        highlighted_rna = highlight_stop_codons(rna_output)
        st.markdown(highlighted_rna, unsafe_allow_html=True)

        # Translate RNA to protein
        protein_sequence = translate_rna_to_protein(rna_output)
        st.text("Translated Protein Sequence:")
        st.write(protein_sequence)
    else:
        st.error("Please enter some text to process.")

# Display the codon table image
codon_table_image_url = "https://www.researchgate.net/profile/Anders-Esberg/publication/267702580/figure/fig2/AS:661826920513537@1534803242980/The-codon-table-The-genetic-code-is-composed-of-four-different-letters-U-C-A-and-G.png"  # Change this URL to the path where your image is hosted
st.image(codon_table_image_url, caption="Codon Table", use_column_width=True)
