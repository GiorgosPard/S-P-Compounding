import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_future_value(initial_amount, monthly_contribution, annual_growth_rate, years, compounding_frequency):
    compounding_map = {"Annually": 1, "Monthly": 12, "Daily": 365}
    periods_per_year = compounding_map[compounding_frequency]
    rate_per_period = annual_growth_rate / periods_per_year
    
    future_values = []
    contributions_only = []
    total_value = initial_amount
    total_contributions = initial_amount

    for year in range(1, years + 1):
        for period in range(1, periods_per_year + 1):
            total_value *= (1 + rate_per_period)
            if compounding_frequency == "Monthly" or period % (12 // periods_per_year) == 0:
                total_value += monthly_contribution
                total_contributions += monthly_contribution
        future_values.append(total_value)
        contributions_only.append(total_contributions)

    return future_values, contributions_only

def main():
    st.title("S&P Investment Calculator")

    # Layout: inputs in one column, results in another
    col1, col2 = st.columns([1, 2])

    with col1:
        # User inputs
        initial_amount = st.number_input("Initial Amount ($):", min_value=0.0, value=10000.0, step=100.0)
        monthly_contribution = st.number_input("Monthly Contribution ($):", min_value=0.0, value=500.0, step=50.0)
        annual_growth_rate = st.number_input("Annual Growth Rate (%):", min_value=0.0, value=12.0, step=0.1) / 100
        years = st.number_input("Number of Years:", min_value=1, value=10, step=1)
        compounding_frequency = st.selectbox("Compounding Frequency:", ["Monthly"])

    with col2:
        # Calculate future values
        future_values, contributions_only = calculate_future_value(initial_amount, monthly_contribution, annual_growth_rate, years, compounding_frequency)

        # Create a dataframe for the results
        results_df = pd.DataFrame({"Year": range(1, years + 1), "Future Value": future_values, "Contributions Only": contributions_only})

        # Display the results
        st.header("Future Values Table")
        st.write(results_df)

    # Plot the results
    st.header("Portfolio Growth Over Time")
    plt.figure(figsize=(10, 5))
    plt.plot(results_df["Year"], results_df["Future Value"], marker='o', label="Future Value (with returns)")
    plt.plot(results_df["Year"], results_df["Contributions Only"], marker='o', linestyle='--', label="Initial + Contributions Only")
    plt.title("Portfolio Growth Over Time")
    plt.xlabel("Year")
    plt.ylabel("Future Value ($)")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

    # Explanation of the inputs
    st.header("Explanation")
    st.markdown("""
        - **Initial Amount:** The starting amount you invest.
        - **Monthly Contribution:** The amount you add to your investment each month.
        - **Annual Growth Rate:** The expected annual return rate of your investment.
        - **Number of Years:** The period over which the investment grows.
        - **Compounding Frequency:** How often the investment compounds (Monthly).
    """)

if __name__ == "__main__":
    main()
