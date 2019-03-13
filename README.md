# nanotube-scad
A python script for generating SCAD models of carbon nanotubes from avogadro coordinate lists.

```
$ python nanotube_gen.py -h
usage: nanotube_gen.py [-h] [--bond [BOND]] [--bond-length [BOND_LENGTH]]
                       [--bond-length-err [BOND_LENGTH_ERR]] [--atom [ATOM]]
                       [-o [OUTPUT]] [-s [SCALE]] [--segments [SEGMENTS]] [-v]
                       INPUT

Nanotube generation utility

positional arguments:
  INPUT                 the xyz input file

optional arguments:
  -h, --help            show this help message and exit
  --bond [BOND]         diameter of the bond cylinder (default: 4.0)
  --bond-length [BOND_LENGTH]
                        length of the bonds (default: 1.421)
  --bond-length-err [BOND_LENGTH_ERR]
                        allowed bond-length threshold (default: 0.05)
  --atom [ATOM]         diameter of the atom sphere (default: 6.0)
  -o [OUTPUT], --output [OUTPUT]
                        openscad output file (default: ./inputfilename.scad)
  -s [SCALE], --scale [SCALE]
                        all coordinates are scaled by this factor (default:
                        5.0)
  --segments [SEGMENTS]
                        adds this as $fn parameter to the output file
  -v, --verbose         increase output verbosity
```

# Dependencies
- [SolidPython](https://github.com/SolidCode/SolidPython)
