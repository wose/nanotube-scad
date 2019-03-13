#!/usr/bin/env python
#
# nanotube_gen.py
# Written by David Cutting
# Version 0.1, 5/6/18

# Nanotube generation utility. Takes a list of coordinates in a .txt file from
# avogadro, removes preceding C and all whitespace, and then creates an openscad
# file that contains all atoms and all bonds.

from solid import *
from math import *
import os, re, sys, argparse, logging

def main(args, loglevel):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    sys.setrecursionlimit(10000)
    scale = args.scale
    dia = args.bond
    sphere_d = args.atom
    bond_length = args.bond_length
    bond_length_err = args.bond_length_err

    logging.debug("scale           : %f", scale)
    logging.debug("bond            : %f", dia)
    logging.debug("atom            : %f", sphere_d)
    logging.debug("bond length     : %f", bond_length)
    logging.debug("bond length err : %f", bond_length_err)

    input_file = open(args.INPUT, 'r')

    if args.output is not None:
        output_file_name = args.output
    else:
        output_file_name = os.path.splitext(os.path.basename(args.INPUT))[0] + '.scad'

    atom_coord = []

    for line in input_file:
        exp = re.compile("(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+")
        string = exp.search(line)
        if string:
            atom_coord.append([float(string.group(1)),
            float(string.group(2)),
            float(string.group(3))])

    tube_solid = translate([0,0,0])

    def bond_length_util():
        for atom in range(0,len(atom_coord)-1):
            coord = atom_coord[atom]
            cooord = atom_coord[atom+1]
            add = sqrt(pow(coord[0]-cooord[0],2)+pow(coord[1]-cooord[1],2)+pow(coord[2]-cooord[2],2))
            print(add)

    # bond_length_util() # Uncomment to print all bond lengths between one atom and the following.

    for atom in range(0,len(atom_coord)):
        coord = atom_coord[atom]
        atom_gen = sphere(d=sphere_d)
        atom_gen = translate(v=[coord[0]*scale, coord[1]*scale, coord[2]*scale])(atom_gen)
        tube_solid += atom_gen
        for atom_bond in range(0,len(atom_coord)):
            bond_coord = atom_coord[atom_bond]
            bond_len = sqrt(pow(coord[0]-bond_coord[0],2)+pow(coord[1]-bond_coord[1],2)+pow(coord[2]-bond_coord[2],2))
            if(bond_len > bond_length-bond_length_err and bond_len < bond_length+bond_length_err):

                bond_solid = cylinder(h=bond_len*scale, d=dia, center=False)
                diff_x = coord[0]*scale-bond_coord[0]*scale
                diff_y = coord[1]*scale-bond_coord[1]*scale
                diff_z = coord[2]*scale-bond_coord[2]*scale

                yaw = degrees(atan2(diff_y, diff_x))
                pitch = 270-degrees(atan2(diff_z, sqrt(diff_x**2 + diff_y**2)))

                bond_solid = rotate([0,pitch, 0])(bond_solid)
                bond_solid = rotate([0, 0, yaw])(bond_solid)
                bond_solid = translate([coord[0]*scale, coord[1]*scale, coord[2]*scale])(bond_solid)


                tube_solid += bond_solid

    if args.segments is not None:
        scad_render_to_file(tube_solid,
                                    filepath=output_file_name,
                                    file_header='$fn = ' + str(args.segments) + ';',
                                    include_orig_code=False)
    else:
        scad_render_to_file(tube_solid,
                                    filepath=output_file_name,
                                    include_orig_code=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Nanotube generation utility')
    parser.add_argument('INPUT', help='the xyz input file')
    parser.add_argument('--bond', nargs='?', type=float, default=4.0, help='diameter of the bond cylinder (default: 4.0)')
    parser.add_argument('--bond-length', nargs='?', type=float, default=1.421, help='length of the bonds (default: 1.421)')
    parser.add_argument('--bond-length-err', nargs='?', type=float, default=0.05, help='allowed bond-length threshold (default: 0.05)')
    parser.add_argument('--atom', nargs='?', type=float, default=6.0, help='diameter of the atom sphere (default: 6.0)')
    parser.add_argument('-o', '--output', nargs='?', help='openscad output file (default: ./inputfilename.scad)')
    parser.add_argument('-s', '--scale', nargs='?', type=float, default=5.0, help='all coordinates are scaled by this factor (default: 5.0)')
    parser.add_argument('--segments', nargs='?', type=int, help='adds this as $fn parameter to the output file')
    parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')
    args = parser.parse_args()

    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    main(args, loglevel)
