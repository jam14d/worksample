import streamlit as st
import random
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool

from pipeline import Pipeline
from string_reader import StringReader
from character_capitalizer import CharacterCapitalizer
from dna_base_converter import DNABaseConverter
from space_remover import SpaceRemover
from special_characters_remover import SpecialCharactersRemover
from protein_synthesis import translate_rna_to_protein

def mutate_dna(dna_sequence, mutation_rate):
    """Mutates the given DNA sequence based on the mutation rate."""
    dna_list = list(dna_sequence)
    mutations_occurred = False
    for i in range(len(dna_list)):
        if random.random() < mutation_rate:
            mutations = {'A': 'CGT', 'C': 'AGT', 'G': 'ACT', 'T': 'ACG'}
            base_to_mutate = dna_list[i]
            mutated_base = random.choice(mutations[base_to_mutate])
            dna_list[i] = mutated_base
            mutations_occurred = True
    return ''.join(dna_list), mutations_occurred

def transcribe_dna_to_rna(dna_sequence):
    """Transcribes DNA sequence into RNA by replacing all instances of 'T' with 'U'."""
    return dna_sequence.replace('T', 'U')

def run_pipeline(input_string, mutation_rate=0, prepend_start_codon=False):
    """Runs the transformation pipeline on an input string and applies mutations if specified."""
    pipeline = Pipeline()
    pipeline.add(StringReader())
    pipeline.add(CharacterCapitalizer())
    pipeline.add(DNABaseConverter())
    pipeline.add(SpaceRemover())
    pipeline.add(SpecialCharactersRemover())

    original_dna_output = pipeline.execute(input_string)
    if prepend_start_codon:
        original_dna_output = 'ATG' + original_dna_output

    mutated_dna_output, mutations_occurred = mutate_dna(original_dna_output, mutation_rate)
    return original_dna_output, mutated_dna_output, mutations_occurred

def create_sequence_plot(sequence, title="Sequence Visualization"):
    """Creates an interactive plot for a DNA/RNA sequence using Bokeh."""
    source = ColumnDataSource(data={
        'base': list(sequence),
        'color': ['green' if base in 'GC' else 'blue' if base in 'AT' else 'red' for base in sequence],
        'index': list(range(len(sequence)))
    })
    p = figure(title=title, x_axis_label='Position', y_axis_label='Base', tools="", toolbar_location=None,
               sizing_mode="stretch_width", height=150)
    p.title.text_font_size = '12pt'
    p.circle(x='index', y=0, size=8, color='color', source=source)
    hover = HoverTool()
    hover.tooltips = [("Index", "@index"), ("Base", "@base")]
    p.add_tools(hover)
    p.xgrid.visible = False
    p.ygrid.visible = False
    p.yaxis.visible = False
    p.xaxis.visible = False
    return p

# Streamlit interface setup
st.title('DNA to Protein Simulator')
user_input = st.text_area("Enter your text to convert into DNA:", "Type your text here...")
mutation_rate = st.slider("Mutation rate (in percentage):", min_value=0.0, max_value=100.0, value=0.0, step=0.1) / 100
prepend_start_codon = st.checkbox("Prepend 'ATG' to DNA sequence", value=False)

if st.button('Transcribe and Translate'):
    if user_input:
        # Generate and mutate DNA
        original_dna, mutated_dna, mutations_occurred = run_pipeline(user_input, mutation_rate, prepend_start_codon)
        
        # Use columns to display both text and Bokeh plots side by side
        col1, col2 = st.columns(2)
        with col1:
            st.text("Original DNA Sequence (before mutation):")
            st.write(original_dna)
        with col2:
            st.bokeh_chart(create_sequence_plot(original_dna, title="Original DNA Sequence"))

        col1, col2 = st.columns(2)
        with col1:
            st.text("Mutated DNA Sequence:")
            st.write(mutated_dna)
        with col2:
            st.bokeh_chart(create_sequence_plot(mutated_dna, title="Mutated DNA Sequence"))
        
        # Transcribe to RNA and show the RNA sequence with its plot
        rna_output = transcribe_dna_to_rna(mutated_dna)
        col1, col2 = st.columns(2)
        with col1:
            st.text("Resulting RNA Sequence:")
            st.write(rna_output)
        with col2:
            st.bokeh_chart(create_sequence_plot(rna_output, title="Resulting RNA Sequence"))
        
        # Protein translation
        if prepend_start_codon and mutated_dna[:3] != 'ATG':
            st.text("ATG mutated, no AUG, translation aborted.")
        else:
            protein_sequence, stop_codon_present = translate_rna_to_protein(rna_output)
            if stop_codon_present:
                st.text("Stop codon detected, translation stopped.")
            st.text("Translated Protein Sequence:")
            st.write(protein_sequence)
    else:
        st.error("Please enter some text to process.")
