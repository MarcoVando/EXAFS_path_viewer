import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import re
import sys
from io import StringIO

# Define a color map for common elements
element_colors = {
    'Fe': 'orange',
    'O': 'red',
    'Si': 'orange',
    'C': 'black',
    'H': 'white',
    'N': 'blue',
    'P': 'purple',
    'S': 'yellow',
    'default': 'gray'
}

def get_element_color(element):
    """Get color for an element, default to gray if not found."""
    return element_colors.get(element, element_colors['default'])

def find_line_number(pattern, lines):
    for i, line in enumerate(lines):
        if re.search(pattern, line):
            return i
    return None

class CrystalViewer:
    def __init__(self, inp_file, dot_size=100, show_labels=False):
        """
        Initialize CrystalViewer with customizable parameters.
        
        Parameters:
        -----------
        inp_file : str
            Path to the input file
        dot_size : int, optional
            Size of the scatter points (default: 100)
        show_labels : bool, optional
            Whether to show atom labels (default: True)
        """
        self.inp_file = inp_file
        self.atoms = self._parse_inp_file()
        self.dot_size = dot_size
        self.show_labels = show_labels
        
    def _parse_inp_file(self):
        """Parse the FEFF inp file and extract atom coordinates."""
        atoms = []
        with open(self.inp_file, 'r') as f:
            lines = f.readlines()

            # Find the ATOMS section
        atoms_start_ln = find_line_number("ATOMS", lines) +1
        if atoms_start_ln is None:
                raise ValueError("Could not find ATOMS section in inp file")
        else:
            print(f"Found ATOMS section starting at line {atoms_start_ln}")
        
        atoms_end_ln = find_line_number("END", lines[atoms_start_ln:]) -1
        if atoms_end_ln is None:
            raise ValueError("Could not find END ATOMS section in inp file")
        else:
            atoms_end_ln += atoms_start_ln
            print(f"Found END ATOMS section at line {atoms_end_ln}")
        
        lines_model = lines[atoms_start_ln:atoms_end_ln]

        # Build the dataframe containing atom coordinates
        for i in range(len(lines_model)):    #fix the lines
            lines_model[i] = lines_model[i].replace("*", "")
            lines_model[i] = lines_model[i].replace("\n", "")
        header = lines_model[0].split()  # Get the header

        df = pd.DataFrame(data=[line.split() for line in lines_model[1:]], columns=header)

        # Convert the dataframe to a list of dictionaries with float coordinates
        for index, row in df.iterrows():
            atoms.append({
                'element': row['tag'],
                'label': row['site_info'],
                'x': float(row['x']),
                'y': float(row['y']),
                'z': float(row['z'])   
            })
        return atoms

    def plot_all_views(self, fig=None, ax3d=None, ax_xy=None, ax_xz=None, ax_yz=None):
        """Plot the crystal structure on the given axes."""
        if ax3d is None or fig is None:
            fig = plt.figure(figsize=(12, 8))
            ax_xy = fig.add_subplot(221)
            ax_xz = fig.add_subplot(222)
            ax_yz = fig.add_subplot(223)
            ax3d = fig.add_subplot(224, projection='3d')

        # Group atoms by element for plotting
        elements = set(atom['element'] for atom in self.atoms)
        for element in elements:
            element_atoms = [atom for atom in self.atoms if atom['element'] == element]
            x = [atom['x'] for atom in element_atoms]
            y = [atom['y'] for atom in element_atoms]
            z = [atom['z'] for atom in element_atoms]
            color = get_element_color(element)
            
            # Calculate alpha based on z position (perpendicular to XY plane)
            z_range = max(z) - min(z)
            alphas = [(z_val - min(z)) / z_range * 0.9 + 0.1 for z_val in z]  # Range 0.1-1.0
            
            # Create arrays of dot sizes for each point
            sizes = [self.dot_size] * len(x)
            
            # Plot with varying alpha
            for x_val, y_val, z_val, alpha, size in zip(x, y, z, alphas, sizes):
                ax3d.scatter(x_val, y_val, z_val,
                            s=size,  # Use individual size
                            alpha=alpha,
                            color=color,
                            label=element if alpha == alphas[0] else "")  # Only label first point
            
            # Add labels
            if self.show_labels:
                for atom in element_atoms:
                    ax3d.text(atom['x'], atom['y'], atom['z'], atom['label'],
                             color='black', size=10, zorder=1)
            
            # Add legend manually since we suppressed labels
            if element_atoms:
                ax3d.scatter([], [], [], s=self.dot_size, alpha=1.0, color=color, label=element)
        
        ax3d.set_xlabel('X')
        ax3d.set_ylabel('Y')
        ax3d.set_zlabel('Z')
        ax3d.set_title('3D View')
        ax3d.legend()
        
        # XY plane
        for element in elements:
            element_atoms = [atom for atom in self.atoms if atom['element'] == element]
            x = [atom['x'] for atom in element_atoms]
            y = [atom['y'] for atom in element_atoms]
            z = [atom['z'] for atom in element_atoms]  # For alpha calculation
            color = get_element_color(element)
            
            # Calculate alpha based on z position (perpendicular to XY plane)
            z_range = max(z) - min(z)
            alphas = [(z_val - min(z)) / z_range * 0.9 + 0.1 for z_val in z]  # Range 0.1-1.0
            
            # Create arrays of dot sizes for each point
            sizes = [self.dot_size] * len(x)
            
            # Plot with varying alpha
            for x_val, y_val, alpha, size in zip(x, y, alphas, sizes):
                ax_xy.scatter(x_val, y_val, 
                            s=size,  # Use individual size
                            alpha=alpha,
                            color=color,
                            label=element if alpha == alphas[0] else "")  # Only label first point
            
            # Add labels
            if self.show_labels:
                for atom in element_atoms:
                    ax_xy.text(atom['x'], atom['y'], atom['label'],
                             color='black', size=10, zorder=1)
            
            # Add legend manually since we suppressed labels
            if element_atoms:
                ax_xy.scatter([], [], s=self.dot_size, alpha=1.0, color=color, label=element)
        
        ax_xy.set_xlabel('X')
        ax_xy.set_ylabel('Y')
        ax_xy.set_title('XY Plane')
        ax_xy.legend()
        
        # XZ plane
        for element in elements:
            element_atoms = [atom for atom in self.atoms if atom['element'] == element]
            x = [atom['x'] for atom in element_atoms]
            z = [atom['z'] for atom in element_atoms]
            y = [atom['y'] for atom in element_atoms]  # For alpha calculation
            color = get_element_color(element)
            
            # Calculate alpha based on y position (perpendicular to XZ plane)
            y_range = max(y) - min(y)
            alphas = [(y_val - min(y)) / y_range * 0.9 + 0.1 for y_val in y]  # Range 0.1-1.0
            
            # Create arrays of dot sizes for each point
            sizes = [self.dot_size] * len(x)
            
            # Plot with varying alpha
            for x_val, z_val, alpha, size in zip(x, z, alphas, sizes):
                ax_xz.scatter(x_val, z_val, 
                            s=size,  # Use individual size
                            alpha=alpha,
                            color=color,
                            label=element if alpha == alphas[0] else "")  # Only label first point
            
            # Add labels
            if self.show_labels:
                for atom in element_atoms:
                    ax_xz.text(atom['x'], atom['z'], atom['label'],
                             color='black', size=10, zorder=1)
            
            # Add legend manually since we suppressed labels
            if element_atoms:
                ax_xz.scatter([], [], s=self.dot_size, alpha=1.0, color=color, label=element)
        
        ax_xz.set_xlabel('X')
        ax_xz.set_ylabel('Z')
        ax_xz.set_title('XZ Plane')
        ax_xz.legend()
        
        # YZ plane
        for element in elements:
            element_atoms = [atom for atom in self.atoms if atom['element'] == element]
            y = [atom['y'] for atom in element_atoms]
            z = [atom['z'] for atom in element_atoms]
            x = [atom['x'] for atom in element_atoms]  # For alpha calculation
            color = get_element_color(element)
            
            # Calculate alpha based on x position (perpendicular to YZ plane)
            x_range = max(x) - min(x)
            alphas = [(x_val - min(x)) / x_range * 0.9 + 0.1 for x_val in x]  # Range 0.1-1.0
            
            # Create arrays of dot sizes for each point
            sizes = [self.dot_size] * len(y)
            
            # Plot with varying alpha
            for y_val, z_val, alpha, size in zip(y, z, alphas, sizes):
                ax_yz.scatter(y_val, z_val, 
                            s=size,  # Use individual size
                            alpha=alpha,
                            color=color,
                            label=element if alpha == alphas[0] else "")  # Only label first point
            
            # Add labels
            if self.show_labels:
                for atom in element_atoms:
                    ax_yz.text(atom['y'], atom['z'], atom['label'],
                             color='black', size=10, zorder=1)
            
            # Add legend manually since we suppressed labels
            if element_atoms:
                ax_yz.scatter([], [], s=self.dot_size, alpha=1.0, color=color, label=element)
        
        ax_yz.set_xlabel('Y')
        ax_yz.set_ylabel('Z')
        ax_yz.set_title('YZ Plane')
        ax_yz.legend()
        
        return fig, ax3d, ax_xy, ax_xz, ax_yz

    def plot_3d(self, ax=None):
        """Plot the crystal structure in 3D on the given axis."""
        if ax is None:
            fig = plt.figure(figsize=(8, 8))
            ax = fig.add_subplot(111, projection='3d')
        
        # Group atoms by element for plotting
        elements = set(atom['element'] for atom in self.atoms)
        for element in elements:
            element_atoms = [atom for atom in self.atoms if atom['element'] == element]
            x = [atom['x'] for atom in element_atoms]
            y = [atom['y'] for atom in element_atoms]
            z = [atom['z'] for atom in element_atoms]
            color = get_element_color(element)
            
            # Plot with alpha=0.5
            ax.scatter(x, y, z, 
                      s=self.dot_size,
                      alpha=0.5,
                      color=color,
                      label=element)
            
            # Add labels
            if self.show_labels:
                for atom in element_atoms:
                    ax.text(atom['x'], atom['y'], atom['z'], atom['label'],
                            color='black', size=10, zorder=1)
            
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('3D Crystal Structure')
        ax.legend()
        
        return fig, ax

def main():
    import argparse
    
    # Create argument parser
    parser = argparse.ArgumentParser(description='Visualize crystal structure from FEFF input file')
    parser.add_argument('-inp','--input_file', help='Path to the FEFF input file')
    parser.add_argument('-ds','--dot-size', type=int, default=100,
                       help='Size of the scatter points (default: 100)')
    parser.add_argument('-lbl','--labels', action='store_true',
                       help='Do not show atom labels')
    
    args = parser.parse_args()
    
    # Create viewer with specified parameters
    viewer = CrystalViewer(args.input_file, 
                         dot_size=args.dot_size,
                         show_labels=args.labels)
    viewer.plot_all_views()
    # viewer.plot_3d()

if __name__ == '__main__':
    main()
