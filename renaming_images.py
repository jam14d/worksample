import os

# Define the directory containing the files
directory = "/Volumes/hnaskolab/Lotfi/Projects/ASAP/Zeiss pictures/241222_Pitx2 mice_JM most recent IHC"

# Read the mapping from a text file
def load_mapping(file_path):
    mapping = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 2):
            key = lines[i].strip().lstrip("*").strip()
            value = lines[i + 1].strip().lstrip("*").strip()
            mapping[key] = value
    return mapping

# Path to the text file containing the mappings
mapping_file = "/Users/jamieannemortel/Downloads/slides from 12.19.24 renaming images.txt"

# Load the mapping
mapping = load_mapping(mapping_file)

# Iterate over files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".czi"):
        # Check for the specific prefix and extract the identifier
        prefix = "12192024-RecognizedCode-"
        if filename.startswith(prefix):
            identifier = filename[len(prefix):].split(".")[0]  # Extract the number part of the filename

            # Check if the identifier is in the mapping
            if identifier in mapping:
                # Build the new filename
                new_name = f"{mapping[identifier]}.czi"

                # Get the full paths
                old_path = os.path.join(directory, filename)
                new_path = os.path.join(directory, new_name)

                try:
                    # Rename the file
                    os.rename(old_path, new_path)
                    print(f"Renamed: {filename} -> {new_name}")
                except OSError as e:
                    print(f"Error renaming {filename}: {e}")
            else:
                print(f"No mapping found for: {filename}")
        else:
            print(f"Skipping file without expected prefix: {filename}")

