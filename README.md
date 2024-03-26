## DNA and RNA Transcription Pipeline

### Description

The DNA and RNA Transcription Pipeline is designed to convert any given text input into a simulated DNA sequence, which is then transcribed into an RNA sequence. This two-step process involves:

- **DNA Generation**: Converting a string to a DNA sequence.
- **RNA Transcription**: Transcribing the DNA sequence into RNA.

### Components

- `dna_generator.py`: Converts a string into a simulated DNA sequence. This script encapsulates the conversion logic, offering a standalone solution for DNA sequence generation from text inputs.

- `rna_transcriber.py`: Transcribes the generated DNA sequence into RNA by replacing all instances of "T" with "U", mimicking biological transcription processes.

### Output and Usage

Both the DNA generation and RNA transcription stages allow for the optional saving of outputs as text files. To use this pipeline, ensure `dna_generator.py` and `rna_transcriber.py` are located in the same directory. You can generate a DNA sequence from your input string with `dna_generator.py`, and transcribe a sequence into RNA with `rna_transcriber.py`.

## Random Folder

The "random" folder within this repository contains a variety of projects at different stages of development. Many of these projects are works in progress, undergoing testing, refinement, or expansion. This folder serves as a creative sandbox, reflecting my ongoing exploration and experimentation with new ideas and technologies. While some projects in this folder may not be fully functional or documented, they offer a glimpse into my interests.