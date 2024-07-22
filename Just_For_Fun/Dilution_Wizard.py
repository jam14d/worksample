import streamlit as st

def calculate_dilution(final_volume, final_concentration, stock_concentration):
    dilution_factor = stock_concentration / final_concentration
    stock_volume = final_volume / dilution_factor
    diluent_volume = final_volume - stock_volume
    return stock_volume, diluent_volume, dilution_factor

def main():
    st.title('Dilution Wizard')

    st.write("""
    This tool helps you calculate the amount of stock solution and diluent needed to prepare a diluted solution.
    It also shows the steps involved in the calculation.
    """)

    final_volume = st.number_input('Final Volume (mL)', min_value=1, value=100)
    final_concentration = st.number_input('Final Concentration (x)', min_value=0.01, value=1.0, step=0.01)
    stock_concentration = st.number_input('Stock Concentration (x)', min_value=1.0, value=10.0, step=0.1)

    if st.button('Calculate'):
        stock_volume, diluent_volume, dilution_factor = calculate_dilution(final_volume, final_concentration, stock_concentration)
        
        st.write(f"**Steps for Dilution:**")
        st.write(f"1. Calculate the Dilution Factor:")
        st.write(f"   Dilution Factor = Stock Concentration / Final Concentration")
        st.write(f"   Dilution Factor = {stock_concentration} / {final_concentration} = {dilution_factor:.2f}")
        
        st.write(f"2. Calculate the Volume of Stock Solution Needed:")
        st.write(f"   Volume of Stock Solution = Final Volume / Dilution Factor")
        st.write(f"   Volume of Stock Solution = {final_volume} mL / {dilution_factor:.2f} = {stock_volume:.2f} mL")
        
        st.write(f"3. Calculate the Volume of Diluent Needed:")
        st.write(f"   Volume of Diluent = Final Volume - Volume of Stock Solution")
        st.write(f"   Volume of Diluent = {final_volume} mL - {stock_volume:.2f} mL = {diluent_volume:.2f} mL")
        
        st.write(f"**Results:**")
        st.write(f"   - Volume of Stock Solution Needed: {stock_volume:.2f} mL")
        st.write(f"   - Volume of Diluent Needed: {diluent_volume:.2f} mL")
        st.write(f"   - Dilution Factor: {dilution_factor:.2f}")

if __name__ == "__main__":
    main()
