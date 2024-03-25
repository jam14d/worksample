
"""
Simple pipeline that takes a string and turns it into an array of characters with each caracter capitalized. 
"""

class StringReader:
    def process(self, text):
        return text

class CharacterCapitalizer:
    def process(self, text):
        return [char.upper() for char in text]

class Pipeline:
    def __init__(self):
        self.stages = []

    def add(self, stage):
        self.stages.append(stage)
    
    def execute(self, input):
        for stage in self.stages:
            input = stage.process(input)
        return input

# Instantiate the pipeline
pipeline = Pipeline()

# ‘add’ method that accepts instances of other classes
pipeline.add(StringReader())
pipeline.add(CharacterCapitalizer())

# Input string
input_string = "I need a job"

# Execute the pipeline
output = pipeline.execute(input_string)

print(output)