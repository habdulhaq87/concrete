import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

def visualize_mix(labels, values):
    """Visualizes the concrete mix as an enhanced stacked bar chart with annotations."""
    # Create a gradient color map for better visualization
    cmap = LinearSegmentedColormap.from_list(
        "mix_colors", ['#FFC300', '#FF5733', '#C70039', '#900C3F', '#581845']
    )
    colors = [cmap(i / (len(labels) - 1)) for i in range(len(labels))]

    fig, ax = plt.subplots(figsize=(6, 8))
    bottom = 0

    for i, (label, value) in enumerate(zip(labels, values)):
        ax.bar(0, value, bottom=bottom, color=colors[i], width=0.5, label=label)

        # Add annotation for each bar segment
        ax.text(0, bottom + value / 2, f"{value}%", ha="center", va="center", fontsize=10, color="white")
        bottom += value

    # Customize the chart
    ax.set_xlim(-1, 1)
    ax.set_ylim(0, 100)
    ax.set_xticks([])
    ax.set_yticks(np.arange(0, 101, 10))
    ax.set_ylabel("Percentage (%)", fontsize=12)
    ax.set_title("Concrete Mix Composition", fontsize=14, fontweight="bold")

    # Move legend outside the plot
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Materials", fontsize=10)

    # Display the chart
    st.pyplot(fig)

def display_feedback(feedback):
    """Displays the strength feedback with improved UI."""
    st.markdown("### Strength Feedback")
    st.info(feedback, icon="💡")
