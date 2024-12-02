import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def visualize_mix(labels, values):
    """Visualizes the concrete mix as a stacked bar chart."""
    fig, ax = plt.subplots(figsize=(6, 8))
    colors = ['#FF7F50', '#1E90FF', '#98FB98', '#FFD700', '#9370DB']
    bottom = 0

    for i, (label, value) in enumerate(zip(labels, values)):
        ax.bar(0, value, bottom=bottom, color=colors[i], label=label, width=0.5)
        bottom += value

    ax.set_xlim(-1, 1)
    ax.set_ylim(0, 100)
    ax.set_xticks([])
    ax.set_yticks(np.arange(0, 101, 10))
    ax.set_ylabel("Percentage (%)")
    ax.set_title("Concrete Mix Composition")
    ax.legend(loc='upper right')

    # Display the chart
    st.pyplot(fig)

def display_feedback(feedback):
    """Displays the strength feedback."""
    st.markdown("### Strength Feedback")
    st.info(feedback)
