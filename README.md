# EXAFS_path_viewer
**EXAFS_path_viewer** is a Python package designed to visualize FEFF-generated EXAFS paths. It enables users to import a FEFF input structure and specific FEFF paths, then explore them both in:

- 3D Cartesian space  
- 2D projections: XY, XZ, and YZ planes  
- Selected paths can be highlighted on top of the atomic structure, providing intuitive insight into scattering contributions.  

## 🚧 Features
Current Capabilities
- Load FEFF input (feff.inp) and FEFF path (paths.dat, feffNNNN.dat) files
- Visualize:
  - 3D 2D projections (XY, XZ, YZ) atomic positions
  <img src="https://github.com/user-attachments/assets/399d2779-5992-4192-bc11-b961b9d4eb2c" width="500">

  - 3D and 2D projections (XY, XZ, YZ) FEFF path vectors
  <img src="https://github.com/user-attachments/assets/c8b43553-45c0-4273-a60d-422cd5457c4c" width="500">

  - Highlight selected paths directly on the input structure

## Planned for Future Versions 
- Batch import of all generated FEFF paths
- Interactive 3D view with  Plotly
- Plotting of:
  - χ(k), k²χ(k), and k³χ(k)
  - χ(R)
  - Path-specific amplitude, phase, and real/imaginary components
  - GUI interface for interactive exploration

## 📦 Dependencies  
numpy, pandas, matplotlib


## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the script with a FEFF path file as input:
```bash
python path_viewer.py -p path/to/your/feff_file.dat -i path/to/your/feff_inp_file.inp 
```

The program will generate three types of visualizations:
1. 2D plot (XY plane)
2. 3D plot using matplotlib
3. Interactive 3D plot using Plotly (future)
