import streamlit as st
import matplotlib.pyplot as plt

# Streamlit app configuration
st.set_page_config(page_title="Concrete Composition Visualizer", layout="centered")

# App title
st.title("Concrete Composition Visualizer")
st.markdown("Visualize the proportions of materials used in concrete mix design.")

# Input sliders for material proportions
st.sidebar.header("Input Material Proportions (%)")
cement = st.sidebar.slider("Cement", min_value=0, max_value=100, value=15)
water = st.sidebar.slider("Water", min_value=0, max_value=100, value=10)
sand = st.sidebar.slider("Sand", min_value=0, max_value=100, value=25)
coarse_aggregate = st.sidebar.slider("Coarse Aggregate", min_value=0, max_value=100, value=50)
additives = st.sidebar.slider("Additives", min_value=0, max_value=100, value=0)

# Ensure total proportions do not exceed 100%
total = cement + water + sand + coarse_aggregate + additives
if total > 100:
    st.error(f"Total proportions exceed 100% ({total}%). Adjust the values.")
else:
    # Data preparation
    labels = ["Cement", "Water", "Sand", "Coarse Aggregate", "Additives"]
    proportions = [cement, water, sand, coarse_aggregate, additives]

    # Plot the pie chart
    fig, ax = plt.subplots()
    ax.pie(proportions, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")  # Equal aspect ratio ensures the pie chart is circular.

    # Display the chart
    st.pyplot(fig)

    # Display the proportions as a table
    st.markdown("### Material Proportions")
    st.table({"Material": labels, "Proportion (%)": proportions})
