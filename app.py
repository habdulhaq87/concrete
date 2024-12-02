import streamlit as st
from ui import visualize_mix, display_feedback  # Import visualization and feedback functions
from compression_test import compression_test_with_animation, visualize_cube  # Import compression test and 3D cube visualization
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # For 3D plotting

# Streamlit app configuration
st.set_page_config(page_title="Concrete Application", layout="wide")

# Sidebar for page navigation
page = st.sidebar.selectbox("Select Page", ["Mix Visualization", "Compression Test"])

if page == "Mix Visualization":
    # App title
    st.title("Concrete Mix Visualization")
    st.markdown("Visualize and generate concrete mixes based on the ACI code with strength feedback.")

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

    # Function to calculate strength feedback
    def get_strength_feedback(proportions):
        cement = proportions["Cement"]
        water = proportions["Water"]
        coarse_aggregate = proportions["Coarse Aggregate"]
        water_cement_ratio = water / cement if cement > 0 else float('inf')

        # Logical feedback based on mix proportions
        if water_cement_ratio < 0.4:
            feedback = "High strength mix: Suitable for structural applications like columns and beams."
        elif 0.4 <= water_cement_ratio <= 0.6:
            feedback = "Moderate strength mix: Suitable for general-purpose applications like slabs and pavements."
        elif water_cement_ratio > 0.6:
            feedback = "Low strength mix: May have high workability but reduced strength. Suitable for non-load-bearing elements."
        else:
            feedback = "Invalid mix: Check proportions."

        # Consider coarse aggregate content for workability
        if coarse_aggregate > 55:
            feedback += " Note: High coarse aggregate content may reduce workability."
        elif coarse_aggregate < 40:
            feedback += " Note: Low coarse aggregate content may affect structural integrity."

        return feedback

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

    # Data preparation
    labels = list(proportions.keys())
    values = list(proportions.values())

    # Visualization
    visualize_mix(labels, values)

    # Display the proportions as a table
    st.markdown("### Material Proportions")
    st.table({"Material": labels, "Proportion (%)": values})

    # Strength feedback
    feedback = get_strength_feedback(proportions)
    display_feedback(feedback)

elif page == "Compression Test":
    # Compression test page
    st.title("Concrete Compression Test")
    st.markdown("Simulate a lab-based compression test for a 15 cm × 15 cm × 15 cm concrete cube.")

    if st.button("Run Compression Test"):
        st.markdown("#### Compression Test Animation:")
        video_path = compression_test_with_animation()
        st.video(video_path)


        # Running the compression test with animation
        st.markdown("#### Compression Test Animation:")
        compression_test_with_animation()
