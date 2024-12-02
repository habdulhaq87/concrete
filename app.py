import streamlit as st
import matplotlib.pyplot as plt
import random

# Streamlit app configuration
st.set_page_config(page_title="Concrete Composition Visualizer", layout="centered")

# App title
st.title("Concrete Composition Visualizer")
st.markdown("Visualize and generate concrete mixes based on the ACI code.")

# Initialize default proportions
default_proportions = {"Cement": 15, "Water": 10, "Sand": 25, "Coarse Aggregate": 50, "Additives": 0}
proportions = st.session_state.get("proportions", default_proportions)

# Helper function to adjust proportions
def adjust_proportions(selected_material, new_value, proportions):
    remaining_total = 100 - new_value
    other_materials = {k: v for k, v in proportions.items() if k != selected_material}
    total_others = sum(other_materials.values())
    
    # Scale other materials proportionally to maintain total = 100
    for material in other_materials:
        proportions[material] = (remaining_total * other_materials[material]) / total_others
    
    proportions[selected_material] = new_value
    return proportions

# Helper function to generate random mix based on ACI
def generate_aci_mix():
    random.seed()  # Generate a new random seed
    # Typical ACI ranges for concrete mix components
    cement = random.randint(12, 20)  # Cement: 12-20%
    water = random.randint(8, 12)    # Water: 8-12%
    additives = random.randint(0, 5) # Additives: 0-5%
    remaining = 100 - (cement + water + additives)
    sand = random.randint(int(0.3 * remaining), int(0.5 * remaining))  # Sand: 30-50% of remaining
    coarse_aggregate = 100 - (cement + water + sand + additives)       # Remaining is coarse aggregate
    return {"Cement": cement, "Water": water, "Sand": sand, "Coarse Aggregate": coarse_aggregate, "Additives": additives}

# Button to generate ACI mix
if st.sidebar.button("Generate ACI Mix"):
    proportions = generate_aci_mix()
    st.session_state["proportions"] = proportions

# Input sliders with dynamic adjustments
st.sidebar.header("Adjust Material Proportions (%)")
for material in proportions:
    new_value = st.sidebar.slider(material, min_value=0, max_value=100, value=int(proportions[material]), step=1)
    if new_value != proportions[material]:
        proportions = adjust_proportions(material, new_value, proportions)

# Save updated proportions in session state
st.session_state["proportions"] = proportions

# Data preparation for visualization
labels = list(proportions.keys())
values = list(proportions.values())

# Plot the pie chart
fig, ax = plt.subplots()
ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
ax.axis("equal")  # Equal aspect ratio ensures the pie chart is circular.

# Display the chart
st.pyplot(fig)

# Display the proportions as a table
st.markdown("### Material Proportions")
st.table({"Material": labels, "Proportion (%)": values})
