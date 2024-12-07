import streamlit as st
import base64

# Define the common compounds with their molecular weights and formulas
compounds = {
    'Imidazole': {'MW': 68.08, 'Formula': 'C3H4N2'},
    'KCl': {'MW': 74.5513, 'Formula': 'KCl'},
    'Tris': {'MW': 121.14, 'Formula': 'C4H11NO3'},
    'HEPES': {'MW': 238.3, 'Formula': 'C8H18N2O4S'}
}

# Function to convert text content to a downloadable link
def create_download_link(text, filename):
    b64 = base64.b64encode(text.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">Download {filename}</a>'
    return href

# Streamlit app
def main():
    st.title("Stock Solution Wizard")

    # Input compound name and molecular weight
    compound_name = st.selectbox('Select Compound:', list(compounds.keys()) + ['Other'])
    if compound_name == 'Other':
        compound_name = st.text_input('Enter Compound Name:')
    molecular_weight = st.number_input('Enter Molecular Weight (g/mol):', min_value=0.0, step=0.01, key='mw_input')

    # Input desired molarity and volume
    molarity = st.number_input('Desired Molarity (M):', min_value=0.0, step=0.01, key='molarity_input')
    volume = st.number_input('Final Volume (L):', min_value=0.0, step=0.01, key='volume_input')

    # Input recipe notes
    recipe_notes = st.text_area("Recipe Notes:", height=100)

    # Input file name for the text file
    txt_filename = st.text_input("Text File Name (without extension):", value="stock_solution_recipe")

    # Step 1: Determine Molecular Weight
    st.header("Step 1: Determine the Molecular Weight of the Compound")
    if compound_name != 'Other':
        mol_weight = compounds[compound_name]['MW']
        st.write(f"The molecular weight (MW) of {compound_name} is {mol_weight:.2f} g/mol.")
    else:
        mol_weight = molecular_weight
        st.write(f"The molecular weight (MW) of {compound_name} is {mol_weight:.2f} g/mol.")

    # Step 2: Calculate Number of Moles Needed
    st.header("Step 2: Calculate Number of Moles Needed")
    st.write("Use the formula to calculate the number of moles needed:")
    st.latex(r'\text{Moles} = \text{Molarity} \times \text{Volume}')
    if st.button('Calculate Number of Moles Needed'):
        if molarity > 0 and volume > 0:
            moles = molarity * volume
            st.write(f"Moles = {molarity:.2f} M × {volume:.2f} L = {moles:.2f} moles")
        else:
            st.error("Please enter valid Molarity and Volume.")

    # Step 3: Convert Moles to Grams
    st.header("Step 3: Convert Moles to Grams")
    st.write("Use the molecular weight to convert the number of moles to grams:")
    st.latex(r'\text{Grams} = \text{Moles} \times \text{MW}')
    if st.button('Convert Moles to Grams'):
        if molarity > 0 and volume > 0:
            moles = molarity * volume
            grams = moles * mol_weight
            st.write(f"Grams = {moles:.2f} moles × {mol_weight:.2f} g/mol = {grams:.2f} grams")
        else:
            st.error("Please calculate the number of moles first.")

    # Step 4: Prepare the Solution
    st.header("Step 4: Prepare the Solution")
    if st.button('Prepare Solution'):
        if molarity > 0 and volume > 0:
            moles = molarity * volume
            grams = moles * mol_weight
            st.write(f"Weigh {grams:.2f} grams of {compound_name if compound_name else 'Compound'}.")
            st.write(f"Dissolve it in enough water to make a final volume of {volume:.2f} L.")
            st.write("Mix until the compound is completely dissolved.")

            # Create and display text file content
            content = (
                f"Compound Name: {compound_name}\n"
                f"Molecular Weight (g/mol): {mol_weight}\n"
                f"Desired Molarity (M): {molarity}\n"
                f"Final Volume (L): {volume}\n"
                f"Number of Moles Needed: {moles:.2f}\n"
                f"Amount Needed (g): {grams:.2f}\n"
                f"Recipe Notes:\n{recipe_notes}\n"
            )

            st.subheader("Download Recipe as Text File")
            st.markdown(create_download_link(content, f"{txt_filename}.txt"), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
