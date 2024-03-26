from string_reader import StringReader
from character_capitalizer import CharacterCapitalizer
from dna_base_converter import DNABaseConverter
from space_remover import SpaceRemover
from pipeline import Pipeline

# Instantiate the pipeline
pipeline = Pipeline()

# Add stages to the pipeline
pipeline.add(StringReader())
pipeline.add(CharacterCapitalizer())
pipeline.add(DNABaseConverter())
pipeline.add(SpaceRemover())

# Input string
input_string = "I need a job"

# Execute the pipeline
output = pipeline.execute(input_string)

print(output)
