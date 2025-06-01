import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import re
import sys
class PathViewer:
    def __init__(self, feff_file):
        self.feff_file = feff_file
        self.atoms = self._parse_feff_file()
        
    def _parse_feff_file(self):
        """Parse the FEFF path file and extract atom coordinates."""
        atoms = []
        with open(self.feff_file, 'r') as f:
            lines = f.readlines()
            # Find the coordinates section (starts with line containing 'x y z pot at#')
            coord_start = None
            for i, line in enumerate(lines):
                if re.findall("x\s+y\s+z\s+pot\s+", line):
                    coord_start = i + 1  # Start reading coordinates from next line
                    break
            
            if coord_start is None:
                raise ValueError("Could not find coordinates section in FEFF file")
            
            # Read coordinates until we reach the k-value section
            for line in lines[coord_start:]:
                if not line.strip():
                    continue
                if re.findall("k\s+real\[2\*phc\]", line):
                    break
                
                parts = line.split()
                if len(parts) >= 6:  # x, y, z, pot, at#, element
                    atom = {
                        'element': parts[5],  # element is last column
                        'x': float(parts[0]),
                        'y': float(parts[1]),
                        'z': float(parts[2]),
                        'pot': int(parts[3]),
                        'at#': int(parts[4])
                    }
                    atoms.append(atom)
        
        return atoms

    def plot_2d(self):
        """Create a 2D plot of the atomic structure."""
        plt.figure(figsize=(8, 8))

        # Plot atoms
        for atom in self.atoms:
            plt.scatter(atom['x'], atom['y'], label=atom['element'])
            plt.text(atom['x'], atom['y'], atom['element'])

        # Plot connections in correct order: Fe-C, C-C, then back to absorber
        # First, find Fe and C atoms
        fe_atoms = [a for a in self.atoms if a['element'] == 'Fe']
        c_atoms = [a for a in self.atoms if a['element'] == 'C']

        # Plot Fe-C connections
        for fe in fe_atoms:
            for c in c_atoms:
                plt.plot([fe['x'], c['x']],
                         [fe['y'], c['y']],
                         'r-', label='Fe-C' if 'Fe-C' not in plt.get_legend_handles_labels()[1] else '')

        # Plot C-C connections
        for i in range(len(c_atoms) - 1):
            c1 = c_atoms[i]
            c2 = c_atoms[i + 1]
            plt.plot([c1['x'], c2['x']],
                     [c1['y'], c2['y']],
                     'b-', label='C-C' if 'C-C' not in plt.get_legend_handles_labels()[1] else '')

        # Plot back to absorber (first atom)
        for c in c_atoms:
            plt.plot([c['x'], self.atoms[0]['x']],
                     [c['y'], self.atoms[0]['y']],
                     'g-', label='Back to Absorber' if 'Back to Absorber' not in plt.get_legend_handles_labels()[1] else '')

        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('2D Atomic Structure')
        plt.legend()

    def plot_all_views(self, fig=None, ax3d=None, ax_xy=None, ax_xz=None, ax_yz=None):
        """Plot the structure on the given axes."""
        if ax3d is None or fig is None:
            fig = plt.figure(figsize=(12, 8))
            ax3d = fig.add_subplot(221, projection='3d')
            ax_xy = fig.add_subplot(222)
            ax_xz = fig.add_subplot(223)
            ax_yz = fig.add_subplot(224)

        # 3D plot
        for atom in self.atoms:
            ax3d.scatter(atom['x'], atom['y'], atom['z'], label=atom['element'])
            ax3d.text(atom['x'], atom['y'], atom['z'], atom['element'])

        # Plot connections in correct order: Fe-C, C-C, then back to absorber
        # First, find Fe and C atoms
        fe_atoms = [a for a in self.atoms if a['element'] == 'Fe']
        c_atoms = [a for a in self.atoms if a['element'] == 'C']

        # Plot Fe-C connections
        for fe in fe_atoms:
            for c in c_atoms:
                ax3d.plot([fe['x'], c['x']],
                         [fe['y'], c['y']],
                         [fe['z'], c['z']],
                         'r-', label='Fe-C' if 'Fe-C' not in ax3d.get_legend_handles_labels()[1] else '')

        # Plot C-C connections
        for i in range(len(c_atoms)):
            for j in range(i + 1, len(c_atoms)):
                c1 = c_atoms[i]
                c2 = c_atoms[j]
                ax3d.plot([c1['x'], c2['x']],
                         [c1['y'], c2['y']],
                         [c1['z'], c2['z']],
                         'b-', label='C-C' if 'C-C' not in ax3d.get_legend_handles_labels()[1] else '')

        # Plot back to absorber (first atom)
        for c in c_atoms:
            ax3d.plot([c['x'], self.atoms[0]['x']],
                     [c['y'], self.atoms[0]['y']],
                     [c['z'], self.atoms[0]['z']],
                     'g-', label='Back to Absorber' if 'Back to Absorber' not in ax3d.get_legend_handles_labels()[1] else '')

        ax3d.set_xlabel('X')
        ax3d.set_ylabel('Y')
        ax3d.set_zlabel('Z')
        ax3d.set_title('3D View')
        ax3d.legend()

        # XY plane
        for atom in self.atoms:
            ax_xy.scatter(atom['x'], atom['y'], label=atom['element'])
            ax_xy.text(atom['x'], atom['y'], atom['element'])
        for i in range(1, len(self.atoms)):
            ax_xy.plot([self.atoms[0]['x'], self.atoms[i]['x']],
                      [self.atoms[0]['y'], self.atoms[i]['y']],
                      'k--')
        ax_xy.set_xlabel('X')
        ax_xy.set_ylabel('Y')
        ax_xy.set_title('XY Plane')
        
        # XZ plane
        for atom in self.atoms:
            ax_xz.scatter(atom['x'], atom['z'], label=atom['element'])
            ax_xz.text(atom['x'], atom['z'], atom['element'])
        for i in range(1, len(self.atoms)):
            ax_xz.plot([self.atoms[0]['x'], self.atoms[i]['x']],
                      [self.atoms[0]['z'], self.atoms[i]['z']],
                      'k--')
        ax_xz.set_xlabel('X')
        ax_xz.set_ylabel('Z')
        ax_xz.set_title('XZ Plane')
        
        # YZ plane
        for atom in self.atoms:
            ax_yz.scatter(atom['y'], atom['z'], label=atom['element'])
            ax_yz.text(atom['y'], atom['z'], atom['element'])
        for i in range(1, len(self.atoms)):
            ax_yz.plot([self.atoms[0]['y'], self.atoms[i]['y']],
                      [self.atoms[0]['z'], self.atoms[i]['z']],
                      'k--')
        ax_yz.set_xlabel('Y')
        ax_yz.set_ylabel('Z')
        ax_yz.set_title('YZ Plane')


        return fig, ax3d, ax_xy, ax_xz, ax_yz


def main():
    if len(sys.argv) != 2:
        print("Usage: python path_viewer.py <feff_file>")
        sys.exit(1)
    
    viewer = PathViewer(sys.argv[1])
    viewer.plot_all_views()
    #iewer.plot_3d()
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
