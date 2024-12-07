import os
import pandas as pd

def reformat_txt_to_csv(input_dir, output_dir):
    """
    Converts all text files in a directory to CSV format.
    
    Parameters:
        input_dir (str): Directory containing the text files.
        output_dir (str): Directory to save the CSV files.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.txt'):
            file_path = os.path.join(input_dir, file_name)
            
            # Detect the delimiter (assuming tab-delimited files for now)
            with open(file_path, 'r') as file:
                first_line = file.readline()
                delimiter = '\t' if '\t' in first_line else ' '

            # Read the file into a DataFrame
            try:
                df = pd.read_csv(file_path, delimiter=delimiter, engine='python')
                
                # Save as CSV
                output_file = os.path.join(output_dir, file_name.replace('.txt', '.csv'))
                df.to_csv(output_file, index=False)
                print(f"Converted {file_name} to {output_file}")
            except Exception as e:
                print(f"Failed to process {file_name}: {e}")

# Example usage
input_directory = "/Users/jamieannemortel/Downloads/RawData_Composite/annotation results"  # Replace with your input directory
output_directory = "/Users/jamieannemortel/Downloads/annotation_csv"  # Replace with your output directory
reformat_txt_to_csv(input_directory, output_directory)
