##Last edit: March 2024

# DNA to RNA Pipeline

This pipeline facilitates the conversion of any given text input into a simulated DNA sequence, and subsequently transcribes this DNA sequence into an RNA sequence. It consists of two main components: the DNA Generator and the RNA Transcriber. Outputs from both stages can optionally be saved as text files for further analysis or reference.

## Components

- **dna_generator.py**: This script converts a given string into a simulated DNA sequence. The conversion logic is encapsulated within this module, making it a standalone tool for generating DNA sequences from arbitrary text inputs.

- **rna_transcriber.py**: Once a DNA sequence is available, this script can be used to transcribe the DNA into RNA. It specifically replaces all occurrences of the nucleotide "T" with "U", simulating the transcription process in biological systems.

## Output Files

Both components of the pipeline offer the option to save their outputs (the DNA and RNA sequences) as text files. This functionality allows users to easily store and review the results of the conversion processes.

## Usage

To ensure proper functionality of the pipeline, place both `dna_generator.py` and `rna_transcriber.py` in the same directory. Then, follow these steps for the conversion process:

1. **String to DNA**: Run `dna_generator.py` with your input string to generate a DNA sequence. If desired, save the output to a text file.

2. **DNA to RNA**: With the DNA sequence generated, run `rna_transcriber.py` to transcribe this sequence into RNA. Again, you have the option to save the output as a text file.

## Example

Given an input string "Hello World!", the pipeline will first convert this string into a simulated DNA sequence. Then, the DNA sequence will be transcribed into an RNA sequence by `rna_transcriber.py`.

Please note: The specific logic and parameters for conversion and transcription are defined within the respective scripts. Review the script documentation for detailed information on customization options and advanced usage.
