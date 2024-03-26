from string_reader import StringReader
from character_capitalizer import CharacterCapitalizer
from dna_base_converter import DNABaseConverter
from space_remover import SpaceRemover
from special_characters_remover import SpecialCharactersRemover
from pipeline import Pipeline

def save_output_to_file(output, file_path='output.txt'):
    """
    Saves the given output to a text file.

    :param output: The text to save.
    :param file_path: The path of the file where the output will be saved.
    """
    with open(file_path, 'w') as file:
        file.write(output)
    print(f"Output saved to {file_path}")

# Instantiate the pipeline
pipeline = Pipeline()

# Add stages to the pipeline
pipeline.add(StringReader())
pipeline.add(CharacterCapitalizer())
pipeline.add(DNABaseConverter())
pipeline.add(SpaceRemover())
pipeline.add(SpecialCharactersRemover())

# Input string
input_string = "I really need a job, please!"

# Execute the pipeline
output = pipeline.execute(input_string)

# Print output
print(output)

# Optional: Save output to a file
save_to_file = True # Set this to False if you don't want to save to a file

if save_to_file:
    file_path = "output.txt"  
    save_output_to_file(output, file_path)
