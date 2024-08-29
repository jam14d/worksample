import streamlit as st
import pandas as pd

def convert_concentration(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    if from_unit == 'mg/mL' and to_unit == 'µg/mL':
        return value * 1000
    if from_unit == 'µg/mL' and to_unit == 'mg/mL':
        return value / 1000
    raise ValueError("Invalid units for concentration conversion")

def convert_volume(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    if from_unit == 'mL' and to_unit == 'µL':
        return value * 1000
    if from_unit == 'µL' and to_unit == 'mL':
        return value / 1000
    raise ValueError("Invalid units for volume conversion")

def choose_pipette(volume):
    volume_uL = volume * 1000  # Convert volume to µL
    if volume_uL >= 1000:
        return 'P1000'
    elif volume_uL >= 200:
        return 'P200'
    elif volume_uL >= 20:
        return 'P20'
    elif volume_uL >= 2:
        return 'P10'
    else:
        return 'P2'

def calculate_antibody_dilution(stock_concentration, ratio, final_volume, concentration_unit, volume_unit):
    stock_concentration = convert_concentration(stock_concentration, concentration_unit, 'µg/mL')
    final_concentration = convert_concentration(stock_concentration / ratio, 'µg/mL', concentration_unit)
    final_volume_mL = convert_volume(final_volume, volume_unit, 'mL')
    
    dilution_factor = ratio
    stock_volume_mL = final_volume_mL / dilution_factor
    diluent_volume_mL = final_volume_mL - stock_volume_mL

    return convert_volume(stock_volume_mL, 'mL', volume_unit), convert_volume(diluent_volume_mL, 'mL', volume_unit), final_concentration, dilution_factor

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
    This tool helps you with antibody dilutions and stock solution dilutions.
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

    with st.sidebar.expander("How to Read a Pipette"):
        st.sidebar.write("""
        **P1000 / P200 / P100 / P20**

        1   1000’s / 100’s / 10’s \n
        0   100’s / 10’s / 1’s \n
        0   10’s / 1’s / 1/10ths \n
        """)

    # Layout with two columns
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader('1. Antibody Dilution Calculator')
        st.write("""
        Use this section to prepare a working solution of an antibody for immunofluorescence staining.
        You can calculate the dilution based on specific ratios and switch between concentration and volume units.
        """)

        stock_concentration_ab = st.number_input('Stock Antibody Concentration', min_value=0.001, value=1.0, step=0.001, key='stock_concentration_ab')
        concentration_unit_ab = st.selectbox('Concentration Unit', ['mg/mL', 'µg/mL'], key='concentration_unit_ab')
        final_volume_ab = st.number_input('Final Volume', min_value=1, value=10, key='final_volume_ab')
        volume_unit_ab = st.selectbox('Volume Unit', ['mL', 'µL'], key='volume_unit_ab')

        ratio = st.selectbox(
            'Choose a Dilution Ratio:',
            options=['1:1000', '1:250', '1:500', '1:100']
        )
        ratio_value = int(ratio.split(':')[1])

        if st.button('Calculate Antibody Dilution', key='calculate_antibody_dilution'):
            stock_volume_ab, diluent_volume_ab, final_concentration_ab, dilution_factor_ab = calculate_antibody_dilution(
                stock_concentration_ab, ratio_value, final_volume_ab, concentration_unit_ab, volume_unit_ab
            )

            with col2:
                st.write(f"**Steps for Antibody Dilution:**")

                st.write(f"### 1. Calculate the Final Concentration:")
                st.markdown(f"""
                **Formula:** 
                Final Concentration = 
                ```
                {convert_concentration(stock_concentration_ab, concentration_unit_ab, 'µg/mL')} µg/mL
                ----------------------------
                {ratio_value}
                ```

                **Calculation:** 
                Final Concentration = {convert_concentration(stock_concentration_ab, concentration_unit_ab, 'µg/mL')} / {ratio_value} = **{final_concentration_ab:.3f} {concentration_unit_ab}**
                """)

                st.write(f"### 2. Calculate the Volume of Ab Stock Solution Needed:")
                st.markdown(f"""
                **Formula:** 
                Volume of Ab Stock Solution = 
                ```
                {convert_volume(final_volume_ab, volume_unit_ab, 'mL'):.2f} mL
                ----------------------
                {ratio_value}
                ```

                **Calculation:** 
                Volume of Stock Solution = {convert_volume(final_volume_ab, volume_unit_ab, 'mL'):.2f} mL / {ratio_value} = **{stock_volume_ab:.2f} {volume_unit_ab}**
                """)

                st.write(f"### 3. Calculate the Volume of Diluent Needed:")
                st.markdown(f"""
                **Formula:** 
                Volume of Diluent = 
                ```
                {convert_volume(final_volume_ab, volume_unit_ab, 'mL'):.2f} mL
                ----------------------
                {stock_volume_ab:.2f} {volume_unit_ab}
                ```

                **Calculation:** 
                Volume of Diluent = {convert_volume(final_volume_ab, volume_unit_ab, 'mL'):.2f} mL - {stock_volume_ab:.2f} {volume_unit_ab} = **{diluent_volume_ab:.2f} {volume_unit_ab}**
                """)

                st.write(f"### 4. Recommended Pipette:")
                pipette = choose_pipette(stock_volume_ab)
                st.markdown(f"**Use a** {pipette} **for measuring the stock solution.**")

                results_ab = {
                    'Volume of Stock Solution Needed': f"{stock_volume_ab:.2f} {volume_unit_ab}",
                    'Volume of Diluent Needed': f"{diluent_volume_ab:.2f} {volume_unit_ab}",
                    'Final Concentration': f"{final_concentration_ab:.3f} {concentration_unit_ab}",
                    'Dilution Ratio': ratio,
                    'Recommended Pipette': pipette
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
        final_volume_stock = st.number_input('Final Volume', min_value=1, value=10, key='final_volume_stock')
        volume_unit_stock = st.selectbox('Volume Unit', ['mL', 'µL'], key='volume_unit_stock')

        if st.button('Calculate Stock Solution Dilution', key='calculate_stock_solution_dilution'):
            stock_volume_stock, diluent_volume_stock, final_concentration, dilution_factor_stock = calculate_antibody_dilution(
                stock_concentration_stock, stock_concentration_stock / final_concentration_stock, final_volume_stock, 'mg/mL', volume_unit_stock
            )

            with col2:
                st.write(f"**Steps for Stock Solution Dilution:**")

                st.write(f"### 1. Calculate the Dilution Factor:")
                st.markdown(f"""
                **Formula:** 
                Dilution Factor = 
                ```
                {stock_concentration_stock} x
                --------------------
                {final_concentration_stock} x
                ```

                **Calculation:** 
                Dilution Factor = {stock_concentration_stock} / {final_concentration_stock} = **{dilution_factor_stock:.2f}**
                """)

                st.write(f"### 2. Calculate the Volume of Stock Solution Needed:")
                st.markdown(f"""
                **Formula:** 
                Volume of Stock Solution = 
                ```
                {convert_volume(final_volume_stock, volume_unit_stock, 'mL'):.2f} mL
                ----------------------
                {dilution_factor_stock}
                ```

                **Calculation:** 
                Volume of Stock Solution = {convert_volume(final_volume_stock, volume_unit_stock, 'mL'):.2f} mL / {dilution_factor_stock} = **{stock_volume_stock:.2f} {volume_unit_stock}**
                """)

                st.write(f"### 3. Calculate the Volume of Diluent Needed:")
                st.markdown(f"""
                **Formula:** 
                Volume of Diluent = 
                ```
                {convert_volume(final_volume_stock, volume_unit_stock, 'mL'):.2f} mL
                ----------------------
                {stock_volume_stock:.2f} {volume_unit_stock}
                ```

                **Calculation:** 
                Volume of Diluent = {convert_volume(final_volume_stock, volume_unit_stock, 'mL'):.2f} mL - {stock_volume_stock:.2f} {volume_unit_stock} = **{diluent_volume_stock:.2f} {volume_unit_stock}**
                """)

                st.write(f"### 4. Recommended Pipette:")
                pipette = choose_pipette(stock_volume_stock)
                st.markdown(f"**Use a** {pipette} **for measuring the stock solution.**")

                results_stock = {
                    'Volume of Stock Solution Needed': f"{stock_volume_stock:.2f} {volume_unit_stock}",
                    'Volume of Diluent Needed': f"{diluent_volume_stock:.2f} {volume_unit_stock}",
                    'Dilution Factor': dilution_factor_stock,
                    'Recommended Pipette': pipette
                }

                display_results(results_stock)

if __name__ == '__main__':
    main()
