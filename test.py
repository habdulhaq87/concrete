import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Constants for the test
CUBE_SIZE = 0.15  # Cube size in meters (15 cm)
CROSS_SECTIONAL_AREA = CUBE_SIZE**2  # Cross-sectional area in m²
LOAD_INCREMENT = 1000  # Load increment in Newtons
MAX_LOAD = 1000000  # Maximum load in Newtons (for simulation)

def visualize_cube():
    """Visualize the cube in 3D."""
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection="3d")
    
    # Define the vertices of the cube
    vertices = np.array([
        [0, 0, 0], [CUBE_SIZE, 0, 0], [CUBE_SIZE, CUBE_SIZE, 0], [0, CUBE_SIZE, 0],
        [0, 0, CUBE_SIZE], [CUBE_SIZE, 0, CUBE_SIZE], [CUBE_SIZE, CUBE_SIZE, CUBE_SIZE], [0, CUBE_SIZE, CUBE_SIZE]
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
    ax.add_collection3d(Poly3DCollection(edges, facecolors="skyblue", edgecolors="black", linewidths=1, alpha=0.8))
    
    # Set axis limits and labels
    ax.set_xlim([0, CUBE_SIZE])
    ax.set_ylim([0, CUBE_SIZE])
    ax.set_zlim([0, CUBE_SIZE])
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_zlabel("Z (m)")
    ax.set_title("Concrete Cube (15cm × 15cm × 15cm)")
    plt.show()

def compression_test():
    """Simulate the compression test."""
    load = 0  # Initial load in Newtons
    results = []
    
    print("Starting Compression Test...")
    print(f"Cube Size: {CUBE_SIZE*100} cm × {CUBE_SIZE*100} cm × {CUBE_SIZE*100} cm")
    print(f"Cross-Sectional Area: {CROSS_SECTIONAL_AREA:.4f} m²")
    print(f"Incremental Load: {LOAD_INCREMENT} N")
    
    while load <= MAX_LOAD:
        # Calculate stress (in Pascals)
        stress = load / CROSS_SECTIONAL_AREA  # Stress = Load / Area
        results.append((load, stress))
        
        # Output to console
        print(f"Load: {load:.2f} N, Stress: {stress:.2f} Pa")
        
        # Simulate failure condition (example: stress exceeds 40 MPa)
        if stress > 40e6:  # 40 MPa in Pascals
            print("\nFailure Condition Reached!")
            print(f"Ultimate Load: {load:.2f} N")
            print(f"Compressive Strength: {stress/1e6:.2f} MPa")
            break
        
        # Increment the load
        load += LOAD_INCREMENT
    
    return results

if __name__ == "__main__":
    # Visualize the cube
    visualize_cube()
    
    # Run the compression test
    results = compression_test()
