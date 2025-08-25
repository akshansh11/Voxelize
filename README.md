# Voxelize

A powerful web-based application for converting STL files into voxel representations with interactive 3D visualization and analysis tools.

<img width="2048" height="2048" alt="image" src="https://github.com/user-attachments/assets/5725ad9f-da07-467b-9f11-fb04e9424dcc" />

## Features

### STL Processing
- **Easy Upload**: Drag and drop STL files directly into the browser
- **Robust Processing**: Built on trimesh library for reliable mesh handling
- **Automatic Validation**: Error handling for corrupted or invalid files

### Advanced Visualization
- **Interactive 3D Rendering**: Fully interactive 3D scatter plots with zoom, pan, and rotate
- **35+ Beautiful Colormaps**: From scientific (Viridis, Plasma) to artistic (Sunset, Electric)
- **Multiple Color Mapping**: Color by coordinates, distance from center, radial patterns, or random
- **Customizable Display**: Adjustable opacity, marker size, and visual properties

### Analysis Tools
- **2D Slice Viewer**: Analyze cross-sections along X, Y, or Z axes
- **Mesh Statistics**: Volume, surface area, vertex count, and bounding box information
- **Voxel Metrics**: Grid size, fill ratio, voxel count, and pitch measurements
- **Interactive Controls**: Real-time parameter adjustment with immediate visual feedback

### Export Options
- **Voxel Data**: Export as NumPy arrays (.npy) for further analysis
- **Coordinate Lists**: CSV export of filled voxel coordinates
- **Cross-Platform**: Compatible with MATLAB, Python, and other analysis tools

## Installation

### Prerequisites
```bash
pip install streamlit numpy plotly numpy-stl trimesh scipy scikit-image pandas
```

### Quick Start
1. Clone the repository:
```bash
git clone https://github.com/yourusername/voxelize.git
cd voxelize
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run main.py
```

4. Open your browser to `http://localhost:8501`

## Usage

### Basic Workflow
1. **Upload STL File**: Use the file uploader to select your STL model
2. **Set Resolution**: Adjust voxel resolution (10-200) based on detail needs
3. **Customize Visualization**: Choose colormaps and color mapping strategies
4. **Analyze**: Use 2D slices to examine internal structure
5. **Export**: Download voxel data for further analysis

### Tips for Best Results
- **Start Small**: Begin with resolution 20-50 for large or complex models
- **Memory Considerations**: Higher resolution = more memory usage
- **Color Selection**: Use perceptually uniform colormaps (Viridis, Plasma) for scientific accuracy
- **Cross-Sections**: 2D slices are excellent for analyzing internal geometry

## Applications

### Materials Science
- **Crystal Structure Analysis**: Visualize unit cells and lattice arrangements
- **Defect Analysis**: Identify and quantify structural defects
- **Porosity Studies**: Analyze pore networks and connectivity
- **Grain Boundary Analysis**: Study polycrystalline structures

### Engineering & Manufacturing
- **Quality Control**: Inspect 3D printed parts for internal defects
- **Design Validation**: Verify complex internal geometries
- **Structural Analysis**: Prepare data for finite element analysis
- **Reverse Engineering**: Convert physical parts to voxel models

### Research & Academia
- **Computational Modeling**: Generate structured grids for simulations
- **Data Visualization**: Create publication-ready 3D visualizations
- **Educational Tools**: Teach 3D geometry and voxel concepts
- **Algorithm Development**: Test voxelization and analysis algorithms

## Technical Details

### Supported Formats
- **Input**: STL (ASCII and Binary)
- **Export**: NumPy arrays (.npy), CSV coordinates

### Performance
- **Resolution Range**: 10-200 voxels per dimension
- **Memory Usage**: Scales with resolution³
- **Processing Time**: Seconds to minutes depending on complexity

### Browser Compatibility
- **Chrome**: Full support (recommended)
- **Firefox**: Full support
- **Safari**: Full support
- **Edge**: Full support

## File Structure
```
voxelize/
├── main.py              # Main Streamlit application
├── requirements.txt     # Python dependencies
├── image.png           # Application logo/banner
├── README.md           # This file
└── examples/           # Sample STL files (optional)
```

## Requirements

Create a `requirements.txt` file with the following dependencies:

```
streamlit>=1.28.0
numpy>=1.21.0
plotly>=5.10.0
numpy-stl>=3.0.0
trimesh>=3.15.0
scipy>=1.7.0
scikit-image>=0.19.0
pandas>=1.3.0
```

## Contributing

We welcome contributions! Here's how you can help:

### Bug Reports
- Use the GitHub Issues tab
- Include STL file details and error messages
- Describe steps to reproduce

### Feature Requests
- Suggest new colormaps or visualization options
- Propose analysis tools or export formats
- Request performance improvements

### Pull Requests
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Trimesh**: Robust 3D mesh processing
- **Plotly**: Interactive visualization capabilities
- **Streamlit**: Rapid web app development
- **Scientific Community**: Inspiration for colormap selection and analysis tools

## Support

- **Documentation**: Check this README and inline help
- **Issues**: Use GitHub Issues for bug reports
- **Discussions**: Use GitHub Discussions for questions and ideas

## Roadmap

### Upcoming Features
- Batch processing of multiple STL files
- Advanced mesh analysis tools
- Custom colormap creation
- 3D mesh overlay on voxel data
- Export to other formats (PLY, OBJ)
- Performance optimizations for large models

### Long-term Goals
- Cloud deployment options
- API for programmatic access
- Integration with CAD software
- Machine learning-based analysis tools

## Screenshots

### Main Interface
The main interface provides an intuitive workflow for STL to voxel conversion with real-time parameter adjustment.

### 3D Visualization
Interactive 3D scatter plots with customizable colormaps and viewing angles for comprehensive model analysis.

### Slice Analysis
2D cross-sectional views allow detailed examination of internal structure and geometry.

---

**Made for the materials science and engineering community**

*Star this repository if you find it useful!*
