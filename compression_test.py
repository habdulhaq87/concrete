import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import tempfile
import os

# Constants for the test
CUBE_SIZE = 0.15  # Cube size in meters (15 cm)
CROSS_SECTIONAL_AREA = CUBE_SIZE**2  # Cross-sectional area in m²
LOAD_INCREMENT = 100000  # Load increment in Newtons
MAX_LOAD = 1000000  # Maximum load in Newtons (for simulation)

def visualize_cube(ax):
    """Create the initial 3D cube."""
    # Define the vertices of the cube
    vertices = np.array([
        [0, 0, 0], [CUBE_SIZE, 0, 0], [CUBE_SIZE, CUBE_SIZE, 0], [0, CUBE_SIZE, 0],
        [0, 0, CUBE_SIZE], [CUBE_SIZE, 0, CUBE_SIZE], 
        [CUBE_SIZE, CUBE_SIZE, CUBE_SIZE], [0, CUBE_SIZE, CUBE_SIZE]
    ])
    
    # Define the edges of the cube
    edges = [
        [vertices[0], vertices[1], vertices[2], vertices[3]],  # Bottom face
        [vertices[4], vertices[5], vertices[6], vertices[7]],  # Top face
        [vertices[0], vertices[1], vertices[5], vertices[4]],  # Side face
        [vertices[2], vertices[3], vertices[7], vertices[6]],  # Side face
        [vertices[0], vertices[3], vertices[7], vertices[4]],  # Side face
        [vertices[1], vertices[2], vertices[6], vertices[5]]   # Side face
    ]
    
    # Add cube faces
    cube = Poly3DCollection(edges, facecolors="skyblue", edgecolors="black", linewidths=1, alpha=0.8)
    ax.add_collection3d(cube)
    return cube

def compression_test_with_animation():
    """Simulate the compression test with animation and save as video."""
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    
    # Configure the 3D plot
    ax.set_xlim([0, CUBE_SIZE])
    ax.set_ylim([0, CUBE_SIZE])
    ax.set_zlim([0, CUBE_SIZE])
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_zlabel("Z (m)")
    ax.set_title("Concrete Cube Compression Test")
    
    # Create the cube
    cube = visualize_cube(ax)
    
    # Animation data
    loads = np.arange(0, MAX_LOAD + LOAD_INCREMENT, LOAD_INCREMENT)
    compressions = loads / (CROSS_SECTIONAL_AREA * 40e6)  # Assuming 40 MPa failure stress

    def update(frame):
        compression = min(compressions[frame], 1)  # Stop at maximum compression
        scale = 1 - compression
        vertices = np.array([
            [0, 0, 0], [CUBE_SIZE, 0, 0], [CUBE_SIZE, CUBE_SIZE, 0], [0, CUBE_SIZE, 0],
            [0, 0, scale * CUBE_SIZE], [CUBE_SIZE, 0, scale * CUBE_SIZE], 
            [CUBE_SIZE, CUBE_SIZE, scale * CUBE_SIZE], [0, CUBE_SIZE, scale * CUBE_SIZE]
        ])
        edges = [
            [vertices[0], vertices[1], vertices[2], vertices[3]],  # Bottom face
            [vertices[4], vertices[5], vertices[6], vertices[7]],  # Top face
            [vertices[0], vertices[1], vertices[5], vertices[4]],  # Side face
            [vertices[2], vertices[3], vertices[7], vertices[6]],  # Side face
            [vertices[0], vertices[3], vertices[7], vertices[4]],  # Side face
            [vertices[1], vertices[2], vertices[6], vertices[5]]   # Side face
        ]
        cube.set_verts(edges)
        ax.collections.clear()
        ax.add_collection3d(cube)
        ax.set_title(f"Load: {loads[frame]} N | Stress: {loads[frame] / CROSS_SECTIONAL_AREA:.2f} Pa")
        if compressions[frame] >= 1:
            ax.set_title(f"Cube Failed!\nUltimate Load: {loads[frame]} N | Compressive Strength: 40 MPa")
    
    # Create animation
    anim = FuncAnimation(fig, update, frames=len(loads), interval=100, repeat=False)
    
    # Save animation to a temporary file
    temp_dir = tempfile.gettempdir()
    video_path = os.path.join(temp_dir, "compression_test.mp4")
    anim.save(video_path, fps=10, extra_args=['-vcodec', 'libx264'])
    plt.close(fig)
    return video_path
