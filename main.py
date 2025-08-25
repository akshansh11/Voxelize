import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from stl import mesh
import trimesh
from scipy import ndimage
from skimage import measure
import tempfile
import os

def load_stl_file(uploaded_file):
    """Load STL file and return trimesh object"""
    try:
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.stl') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # Load with trimesh
        mesh_obj = trimesh.load_mesh(tmp_file_path)
        
        # Clean up temp file
        os.unlink(tmp_file_path)
        
        return mesh_obj
    except Exception as e:
        st.error(f"Error loading STL file: {str(e)}")
        return None

def voxelize_mesh(mesh_obj, resolution=50):
    """Convert mesh to voxel representation"""
    try:
        # Get mesh bounds
        bounds = mesh_obj.bounds
        
        # Calculate pitch based on the largest dimension
        max_dimension = max(bounds[1] - bounds[0])
        pitch = max_dimension / resolution
        
        # Create voxel grid
        voxel_grid = mesh_obj.voxelized(pitch=pitch)
        
        # Store pitch for later use
        voxel_grid._pitch = pitch
        
        return voxel_grid
    except Exception as e:
        st.error(f"Error voxelizing mesh: {str(e)}")
        return None

def create_voxel_visualization(voxel_grid, colormap="Viridis", color_by="Z-coordinate", marker_size=4, opacity=0.8):
    """Create 3D visualization of voxels with customizable colormaps"""
    # Get filled voxel positions
    filled_positions = np.argwhere(voxel_grid.matrix)
    
    if len(filled_positions) == 0:
        st.warning("No voxels found in the mesh")
        return None
    
    x, y, z = filled_positions[:, 0], filled_positions[:, 1], filled_positions[:, 2]
    
    # Calculate color values based on selection
    if color_by == "Z-coordinate":
        color_values = z
        color_title = "Z"
    elif color_by == "Y-coordinate":
        color_values = y
        color_title = "Y"
    elif color_by == "X-coordinate":
        color_values = x
        color_title = "X"
    elif color_by == "Distance from Center":
        center_x, center_y, center_z = np.mean(x), np.mean(y), np.mean(z)
        color_values = np.sqrt((x - center_x)**2 + (y - center_y)**2 + (z - center_z)**2)
        color_title = "Distance"
    elif color_by == "Radial (XY)":
        center_x, center_y = np.mean(x), np.mean(y)
        color_values = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        color_title = "Radial XY"
    else:  # Random
        np.random.seed(42)  # For consistent colors
        color_values = np.random.rand(len(x))
        color_title = "Random"
    
    fig = go.Figure(data=go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers',
        marker=dict(
            size=marker_size,
            color=color_values,
            colorscale=colormap,
            opacity=opacity,
            showscale=True,
            line=dict(width=0.5, color='rgba(0,0,0,0.1)')
        ),
        text=[f'Voxel ({i},{j},{k})' for i,j,k in zip(x,y,z)],
        hovertemplate=f'<b>Voxel</b><br>X: %{{x}}<br>Y: %{{y}}<br>Z: %{{z}}<br>{color_title}: %{{marker.color:.2f}}<extra></extra>'
    ))
    
    # Update colorbar title
    fig.update_coloraxes(colorbar_title=color_title)
    
    fig.update_layout(
        title=f'Voxelized STL Model ({len(x):,} voxels)',
        scene=dict(
            xaxis_title='X Coordinate',
            yaxis_title='Y Coordinate',
            zaxis_title='Z Coordinate',
            aspectmode='cube',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.2)
            ),
            bgcolor='rgba(240,240,240,0.1)'
        ),
        width=900,
        height=700,
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    
    return fig

def create_slice_visualization(voxel_grid, slice_axis='z', slice_index=None, colormap="Viridis"):
    """Create 2D slice visualization of voxels with customizable colormaps"""
    volume = voxel_grid.matrix
    
    if slice_index is None:
        slice_index = volume.shape[{'x': 0, 'y': 1, 'z': 2}[slice_axis]] // 2
    
    if slice_axis == 'x':
        slice_data = volume[slice_index, :, :]
        title = f'X-slice at index {slice_index}'
        labels = {'x': 'Y Coordinate', 'y': 'Z Coordinate'}
    elif slice_axis == 'y':
        slice_data = volume[:, slice_index, :]
        title = f'Y-slice at index {slice_index}'
        labels = {'x': 'X Coordinate', 'y': 'Z Coordinate'}
    else:  # z-axis
        slice_data = volume[:, :, slice_index]
        title = f'Z-slice at index {slice_index}'
        labels = {'x': 'X Coordinate', 'y': 'Y Coordinate'}
    
    fig = px.imshow(slice_data, 
                    title=title,
                    color_continuous_scale=colormap,
                    aspect='equal',
                    labels=labels)
    
    fig.update_layout(
        title=dict(x=0.5, font=dict(size=16)),
        width=600,
        height=500,
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    
    # Add colorbar title
    fig.update_coloraxes(colorbar_title="Voxel Density")
    
    return fig

def display_mesh_info(mesh_obj, voxel_grid):
    """Display information about the mesh and voxelization"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Mesh Information")
        st.write(f"**Vertices:** {len(mesh_obj.vertices)}")
        st.write(f"**Faces:** {len(mesh_obj.faces)}")
        st.write(f"**Volume:** {mesh_obj.volume:.4f}")
        st.write(f"**Surface Area:** {mesh_obj.area:.4f}")
        
        bounds = mesh_obj.bounds
        st.write(f"**Bounding Box:**")
        st.write(f"  X: [{bounds[0][0]:.2f}, {bounds[1][0]:.2f}]")
        st.write(f"  Y: [{bounds[0][1]:.2f}, {bounds[1][1]:.2f}]")
        st.write(f"  Z: [{bounds[0][2]:.2f}, {bounds[1][2]:.2f}]")
    
    with col2:
        st.subheader("Voxel Information")
        voxel_count = np.sum(voxel_grid.matrix)
        total_voxels = np.prod(voxel_grid.matrix.shape)
        fill_ratio = voxel_count / total_voxels
        
        st.write(f"**Grid Size:** {voxel_grid.matrix.shape}")
        st.write(f"**Filled Voxels:** {int(voxel_count)}")
        st.write(f"**Total Voxels:** {total_voxels}")
        st.write(f"**Fill Ratio:** {fill_ratio:.4f}")
        
        # Handle pitch attribute safely
        if hasattr(voxel_grid, '_pitch'):
            st.write(f"**Voxel Pitch:** {voxel_grid._pitch:.4f}")
        elif hasattr(voxel_grid, 'pitch'):
            st.write(f"**Voxel Pitch:** {voxel_grid.pitch:.4f}")
        else:
            # Calculate pitch from bounds and grid size
            bounds = mesh_obj.bounds
            max_dimension = max(bounds[1] - bounds[0])
            estimated_pitch = max_dimension / max(voxel_grid.matrix.shape)
            st.write(f"**Estimated Voxel Pitch:** {estimated_pitch:.4f}")

def main():
    st.set_page_config(
        page_title="Voxelize",
        page_icon="🧊",
        layout="wide"
    )
    
    st.title("Voxelize")
    
    # Display image after title
    try:
        st.image("image.png", use_column_width=False)
    except:
        st.warning("Image 'image.png' not found in the current directory")
    
    st.markdown("Upload an STL file to visualize it as voxels")
    
    # Sidebar controls
    st.sidebar.header("Controls")
    
    uploaded_file = st.file_uploader("Choose an STL file", type=['stl'])
    
    if uploaded_file is not None:
        # Load mesh
        with st.spinner("Loading STL file..."):
            mesh_obj = load_stl_file(uploaded_file)
        
        if mesh_obj is not None:
            # Voxelization controls
            st.sidebar.subheader("Voxelization Settings")
            resolution = st.sidebar.slider("Resolution", 10, 200, 50, 
                                         help="Higher resolution = more voxels = longer processing time")
            
            # Voxelize mesh
            with st.spinner("Voxelizing mesh..."):
                voxel_grid = voxelize_mesh(mesh_obj, resolution)
            
            if voxel_grid is not None:
                # Display mesh and voxel information
                display_mesh_info(mesh_obj, voxel_grid)
                
                st.markdown("---")
                
                # Visualization controls
                st.sidebar.subheader("Visualization Settings")
                
                # Colormap options
                colormap_options = [
                    "Viridis", "Plasma", "Inferno", "Magma", "Cividis",
                    "Turbo", "Rainbow", "Jet", "Hot", "Cool", "Spring", "Summer",
                    "Autumn", "Winter", "Spectral", "RdYlBu", "RdBu", "PiYG",
                    "BrBG", "RdGy", "PuOr", "Sunset", "Sunsetdark", "Oryel",
                    "Peach", "Pinkyl", "Mint", "BluGrn", "Darkmint", "Electric",
                    "Plotly3", "Deep", "Dense", "Haline", "Ice", "Thermal"
                ]
                
                selected_colormap = st.sidebar.selectbox(
                    "Color Scheme",
                    colormap_options,
                    index=0,
                    help="Choose a colormap for visualization"
                )
                
                # Color mapping options
                color_by_options = [
                    "Z-coordinate", "Y-coordinate", "X-coordinate", 
                    "Distance from Center", "Radial (XY)", "Random"
                ]
                
                color_by = st.sidebar.selectbox(
                    "Color Mapping",
                    color_by_options,
                    help="Choose what property to use for coloring voxels"
                )
                
                # Advanced visualization options
                with st.sidebar.expander("Advanced Options"):
                    opacity = st.slider("Opacity", 0.1, 1.0, 0.8, 0.1)
                    marker_size = st.slider("Marker Size", 1, 10, 4, 1)
                
                # Main visualization
                st.subheader("3D Voxel Visualization")
                
                with st.spinner("Creating 3D visualization..."):
                    fig_3d = create_voxel_visualization(
                        voxel_grid, selected_colormap, color_by, marker_size, opacity
                    )
                
                if fig_3d:
                    st.plotly_chart(fig_3d, use_container_width=True)
                
                # Slice visualization
                st.markdown("---")
                st.subheader("2D Slice Visualization")
                
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    slice_axis = st.selectbox("Slice Axis", ['x', 'y', 'z'])
                    max_slice = voxel_grid.matrix.shape[{'x': 0, 'y': 1, 'z': 2}[slice_axis]] - 1
                    slice_index = st.slider(f"{slice_axis.upper()}-slice Index", 0, max_slice, max_slice // 2)
                    
                    # Slice colormap (can be different from 3D)
                    slice_colormap = st.selectbox(
                        "Slice Color Scheme",
                        colormap_options,
                        index=colormap_options.index(selected_colormap),
                        help="Color scheme for 2D slices"
                    )
                
                with col2:
                    fig_slice = create_slice_visualization(
                        voxel_grid, slice_axis, slice_index, slice_colormap
                    )
                    st.plotly_chart(fig_slice, use_container_width=True)
                
                # Download options
                st.markdown("---")
                st.subheader("Export Options")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("Download Voxel Data (NPY)"):
                        voxel_data = voxel_grid.matrix.astype(np.uint8)
                        
                        # Create download
                        import io
                        buffer = io.BytesIO()
                        np.save(buffer, voxel_data)
                        buffer.seek(0)
                        
                        st.download_button(
                            label="Download Voxel Array",
                            data=buffer,
                            file_name=f"{uploaded_file.name[:-4]}_voxels.npy",
                            mime="application/octet-stream"
                        )
                
                with col2:
                    if st.button("Download Coordinates (CSV)"):
                        filled_positions = np.argwhere(voxel_grid.matrix)
                        
                        import pandas as pd
                        df = pd.DataFrame(filled_positions, columns=['X', 'Y', 'Z'])
                        csv = df.to_csv(index=False)
                        
                        st.download_button(
                            label="Download Voxel Coordinates",
                            data=csv,
                            file_name=f"{uploaded_file.name[:-4]}_coordinates.csv",
                            mime="text/csv"
                        )
    else:
        st.info("Upload an STL file to get started!")
        
        # Show example/demo information
        with st.expander("How to use this app"):
            st.markdown("""
            1. **Upload an STL file** using the file uploader above
            2. **Adjust the resolution** in the sidebar (higher = more detailed but slower)
            3. **Explore the 3D visualization** with different color schemes
            4. **View 2D slices** to analyze internal structure
            5. **Download the voxel data** for further analysis
            
            **Tips:**
            - Start with lower resolution (20-50) for large/complex models
            - 2D slices are great for analyzing cross-sections
            - Exported data can be used in other applications (NumPy, MATLAB, etc.)
            """)

if __name__ == "__main__":
    main()
