import argparse
from crystal_viewer import CrystalViewer
from path_viewer import PathViewer
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser(description='Visualize crystal structures and paths')
    parser.add_argument('-i', '--inp', help='Path to the FEFF input file')
    parser.add_argument('-p', '--path', help='Path to the FEFF path file')
    parser.add_argument('-ds', '--dot-size', type=int, default=100,
                       help='Size of the scatter points (default: 100)')
    parser.add_argument('-l', '--labels', action='store_true',
                       help='Show atom labels')
    
    args = parser.parse_args()
    
    if not args.inp and not args.path:
        print("Error: Please provide either an inp file or a path file")
        parser.print_help()
        return
    
    # If only inp file is provided, show crystal structure
    if args.inp and not args.path:
        viewer = CrystalViewer(args.inp, dot_size=args.dot_size, show_labels=args.labels)
        ax3d, ax_xy, ax_xz, ax_yz = viewer.plot_all_views()
        plt.show()
        return
    
    # If only path file is provided, show path viewer
    if args.path and not args.inp:
        viewer = PathViewer(args.path)
        viewer.plot_all_views()
        plt.show()
        return
    
    # If both inp and path files are provided, show both
    if args.inp and args.path:
        # First plot the crystal structure
        crystal_viewer = CrystalViewer(args.inp, dot_size=args.dot_size, show_labels=args.labels)
        fig, ax3d, ax_xy, ax_xz, ax_yz = crystal_viewer.plot_all_views()
        
       
        
        # Now plot the path viewer on top
        path_viewer = PathViewer(args.path)
        fig, ax3d, ax_xy, ax_xz, ax_yz = path_viewer.plot_all_views(fig, ax3d, ax_xy, ax_xz, ax_yz)
        
    plt.show()

if __name__ == '__main__':
    main()
