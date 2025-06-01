# EXAFS_path_viewer
**EXAFS_path_viewer** is a Python package designed to visualize FEFF-generated EXAFS paths. It enables users to import a FEFF input structure and specific FEFF paths, then explore them both in:

- 3D Cartesian space  
- 2D projections: XY, XZ, and YZ planes  
- Selected paths can be highlighted on top of the atomic structure, providing intuitive insight into scattering contributions.  

**🚧 Features**
Current Capabilities
- Load FEFF input (feff.inp) and FEFF path (paths.dat, feffNNNN.dat) files
- Visualize:
  - 3D atomic positions
  - 3D FEFF path vectors
  - 2D projections (XY, XZ, YZ)
  - Highlight selected paths directly on the input structure

**Planned for Future Versions**
- Batch import of all generated FEFF paths
- Plotting of:
  - χ(k), k²χ(k), and k³χ(k)
  - χ(R)
  - Path-specific amplitude, phase, and real/imaginary components
  - GUI interface for interactive exploration

**📦 Dependencies**
``import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import re
import sys
from io import StringIO``
