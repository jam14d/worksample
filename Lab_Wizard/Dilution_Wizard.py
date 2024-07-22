import streamlit as st
import pandas as pd

def calculate_antibody_dilution(stock_concentration, final_concentration, final_volume):
    dilution_factor = stock_concentration / final_concentration
    stock_volume = final_volume / dilution_factor
    diluent_volume = final_volume - stock_volume
    return stock_volume, diluent_volume, dilution_factor

def calculate_stock_dilution(stock_concentration, final_concentration, final_volume):
    dilution_factor = stock_concentration / final_concentration
    stock_volume = final_volume / dilution_factor
    diluent_volume = final_volume - stock_volume
    return stock_volume, diluent_volume, dilution_factor

def concentration_conversion_table():
    data = {
        'Concentration (mg/mL)': ['1', '0.1', '0.01', '0.001'],
        'Concentration (µg/mL)': ['1000', '100', '10', '1']
    }
    df = pd.DataFrame(data)
    return df

def volume_conversion_table():
    data = {
        'Volume (L)': ['1', '0.1', '0.01', '0.001', '0.0001'],
        'Volume (mL)': ['1000', '100', '10', '1', '0.1'],
        'Volume (µL)': ['1000000', '100000', '10000', '1000', '100'],
        'Volume (nL)': ['1000000000', '100000000', '10000000', '1000000', '100000']
    }
    df = pd.DataFrame(data)
    return df

def display_results(results):
    st.write("**Results:**")
    df_results = pd.DataFrame(results.items(), columns=['Label', 'Value'])
    st.write(df_results)

def main():
    st.title('Dilution Wizard')

    st.write("""
    This tool helps you with two types of dilutions:
    1. Preparing a working solution from a stock antibody solution.
    2. Diluting stock solutions (e.g., making 0.5x from 10x).

    Use the calculators below to perform these dilutions and understand the conversion references for concentrations and volumes.
    """)

    # Sidebar for conversion tables
    st.sidebar.header("Conversion References")
    with st.sidebar.expander("Concentration Conversion Reference"):
        df_concentration = concentration_conversion_table()
        st.sidebar.write(df_concentration)

    with st.sidebar.expander("Volume Conversion Reference"):
        df_volume = volume_conversion_table()
        st.sidebar.write(df_volume)

    # Layout with two columns
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader('1. Antibody Dilution Calculator')
        st.write("""
        Use this section to prepare a working solution of an antibody for immunofluorescence staining.
        Example Scenario: You need to prepare 10 mL of a working solution from a stock solution of 1 mg/mL to a final concentration of 1 µg/mL.
        """)
        
        stock_concentration_ab = st.number_input('Stock Antibody Concentration (mg/mL)', min_value=0.001, value=1.0, step=0.001, key='stock_concentration_ab')
        final_concentration_ab = st.number_input('Final Antibody Concentration (µg/mL)', min_value=0.001, value=1.0, step=0.001, key='final_concentration_ab')
        final_volume_ab = st.number_input('Final Volume (mL)', min_value=1, value=10, key='final_volume_ab')

        if st.button('Calculate Antibody Dilution', key='calculate_antibody_dilution'):
            stock_volume_ab, diluent_volume_ab, dilution_factor_ab = calculate_antibody_dilution(
                stock_concentration_ab, final_concentration_ab / 1000, final_volume_ab
            )

            # Steps and results are handled in col2
            with col2:
                st.write(f"**Steps for Antibody Dilution:**")
                
                st.write(f"### 1. Calculate the Dilution Factor:")
                st.markdown(f"""
                **Formula:** 
                Dilution Factor = 
                ```
                {stock_concentration_ab} mg/mL
                ---------------
                {final_concentration_ab / 1000:.3f} mg/mL
                ```

                **Calculation:** 
                Dilution Factor = {stock_concentration_ab} / ({final_concentration_ab / 1000:.3f}) = **{dilution_factor_ab:.2f}**
                """)
                
                st.write(f"### 2. Calculate the Volume of Stock Solution Needed:")
                st.markdown(f"""
                **Formula:** 
                Volume of Stock Solution = 
                ```
                {final_volume_ab:.2f} mL
                ----------------------
                {dilution_factor_ab:.2f}
                ```

                **Calculation:** 
                Volume of Stock Solution = {final_volume_ab:.2f} mL / {dilution_factor_ab:.2f} = **{stock_volume_ab:.2f} mL**
                """)
                
                st.write(f"### 3. Calculate the Volume of Diluent Needed:")
                st.markdown(f"""
                **Formula:** 
                Volume of Diluent = 
                ```
                {final_volume_ab:.2f} mL
                ----------------------
                {stock_volume_ab:.2f} mL
                ```

                **Calculation:** 
                Volume of Diluent = {final_volume_ab:.2f} mL - {stock_volume_ab:.2f} mL = **{diluent_volume_ab:.2f} mL**
                """)

                results_ab = {
                    'Volume of Stock Solution Needed': f"{stock_volume_ab:.2f} mL",
                    'Volume of Diluent Needed': f"{diluent_volume_ab:.2f} mL",
                    'Dilution Factor': f"{dilution_factor_ab:.2f}"
                }
                
                display_results(results_ab)

    with col1:
        st.subheader('2. Stock Solution Dilution Calculator')
        st.write("""
        Use this section to dilute a stock solution to a desired final concentration.
        Example Scenario: You need to prepare a 0.5x solution from a 10x stock solution.
        """)
        
        stock_concentration_stock = st.number_input('Stock Solution Concentration (x)', min_value=0.01, value=10.0, step=0.01, key='stock_concentration_stock')
        final_concentration_stock = st.number_input('Final Solution Concentration (x)', min_value=0.01, value=0.5, step=0.01, key='final_concentration_stock')
        final_volume_stock = st.number_input('Final Volume (mL)', min_value=1, value=10, key='final_volume_stock')

        if st.button('Calculate Stock Solution Dilution', key='calculate_stock_dilution'):
            stock_volume_stock, diluent_volume_stock, dilution_factor_stock = calculate_stock_dilution(
                stock_concentration_stock, final_concentration_stock, final_volume_stock
            )

            # Steps and results are handled in col2
            with col2:
                st.write(f"**Steps for Stock Solution Dilution:**")
                
                st.write(f"### 1. Calculate the Dilution Factor:")
                st.markdown(f"""
                **Formula:** 
                Dilution Factor = 
                ```
                {stock_concentration_stock}
                -------------------------
                {final_concentration_stock}
                ```

                **Calculation:** 
                Dilution Factor = {stock_concentration_stock} / {final_concentration_stock} = **{dilution_factor_stock:.2f}**
                """)
                
                st.write(f"### 2. Calculate the Volume of Stock Solution Needed:")
                st.markdown(f"""
                **Formula:** 
                Volume of Stock Solution = 
                ```
                {final_volume_stock:.2f} mL
                -------------------------
                {dilution_factor_stock:.2f}
                ```

                **Calculation:** 
                Volume of Stock Solution = {final_volume_stock:.2f} mL / {dilution_factor_stock:.2f} = **{stock_volume_stock:.2f} mL**
                """)
                
                st.write(f"### 3. Calculate the Volume of Diluent Needed:")
                st.markdown(f"""
                **Formula:** 
                Volume of Diluent = 
                ```
                {final_volume_stock:.2f} mL
                -------------------------
                {stock_volume_stock:.2f} mL
                ```

                **Calculation:** 
                Volume of Diluent = {final_volume_stock:.2f} mL - {stock_volume_stock:.2f} mL = **{diluent_volume_stock:.2f} mL**
                """)

                results_stock = {
                    'Volume of Stock Solution Needed': f"{stock_volume_stock:.2f} mL",
                    'Volume of Diluent Needed': f"{diluent_volume_stock:.2f} mL",
                    'Dilution Factor': f"{dilution_factor_stock:.2f}"
                }
                
                display_results(results_stock)

if __name__ == "__main__":
    main()
