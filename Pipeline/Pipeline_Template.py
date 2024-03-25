
"""
Simple pipeline that takes a string and turns it into an array of characters with each caracter capitalized 
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

# Example usage:
pipeline = Pipeline()
pipeline.add(StringReader())
pipeline.add(CharacterCapitalizer())

input_string = "I need a job"
output = pipeline.execute(input_string)
print(output)
