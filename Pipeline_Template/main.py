from pipeline import Pipeline
from string_reader import StringReader
from character_capitalizer import CharacterCapitalizer

# Instantiate the pipeline
pipeline = Pipeline()

# Add stages to the pipeline
pipeline.add(StringReader())
pipeline.add(CharacterCapitalizer())

# Input string
input_string = "I need a job"

# Execute the pipeline
output = pipeline.execute(input_string)

print(output)
