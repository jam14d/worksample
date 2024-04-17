import dna_generator  # Ensure this module is available
import matplotlib.pyplot as plt

def transcribe_dna_to_rna(dna_sequence):
    """
    Transcribes a DNA sequence into an RNA sequence by replacing every "T" with "U".
    """
    return dna_sequence.replace("T", "U")

def save_to_file(content, file_name="rna_sequence.txt"):
    """
    Saves the given content to a text file.
    """
    with open(file_name, 'w') as file:
        file.write(content)
    print(f"Content saved to {file_name}")

def count_nucleotides(sequence):
    """
    Counts the occurrences of each nucleotide in a sequence.
    """
    base_counts = {"A": 0, "C": 0, "G": 0, "T": 0, "U": 0}
    for base in sequence:
        if base in base_counts:
            base_counts[base] += 1
    return base_counts

def count_bases(sequence):
    """
    Counts the number of pyrimidines and purines in a sequence.
    """
    base_counts = {"Pyrimidines": 0, "Purines": 0}
    for base in sequence:
        if base in "CU":
            base_counts["Pyrimidines"] += 1
        elif base in "AG":
            base_counts["Purines"] += 1
    return base_counts

def plot_counts(base_counts, title, xlabel, ylabel, figure_number):
    """
    Generic plotting function for both nucleotide and base type counts, with separate figures.
    """
    plt.figure(figure_number, figsize=(8, 4))
    categories = list(base_counts.keys())
    counts = list(base_counts.values())
    plt.bar(categories, counts, color=['blue', 'green', 'red', 'purple', 'orange'])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

if __name__ == "__main__":
    input_string = "I need a jobbbbbb!!! thank you! beep boop adding more stuff to the string"
    
    save_to_file_flag = True
    
    dna_sequence = dna_generator.run_pipeline(input_string, save_to_file=False)
    print("DNA Sequence:", dna_sequence)
    
    rna_sequence = transcribe_dna_to_rna(dna_sequence)
    print("RNA Sequence:", rna_sequence)

    if save_to_file_flag:
        save_to_file(rna_sequence, "RNA_output.txt")
    
    # Count nucleotides in DNA and RNA
    dna_counts = count_nucleotides(dna_sequence)
    rna_counts = count_nucleotides(rna_sequence)

    # Adjust DNA counts for plotting (DNA doesn't have U)
    adjusted_dna_counts = {k: v for k, v in dna_counts.items() if k != "U"}
    print("DNA Nucleotide Counts:", adjusted_dna_counts)
    print("RNA Nucleotide Counts:", rna_counts)
    
    # Plot the nucleotide counts
    plot_counts(adjusted_dna_counts, 'Count of Each Nucleotide in DNA Sequence', 'Nucleotide', 'Count', 1)
    plot_counts(rna_counts, 'Count of Each Nucleotide in RNA Sequence', 'Nucleotide', 'Count', 2)

    # Count and plot pyrimidines and purines in RNA
    base_counts = count_bases(rna_sequence)
    plot_counts(base_counts, 'Count of Pyrimidines and Purines in RNA Sequence', 'Base Type', 'Count', 3)

    # Show all plots simultaneously
    plt.show()
