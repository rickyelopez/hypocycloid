# Hypocycloid Profile Generator

This is a Python 3 port of the Hypocycloidal Gear Profile generator from http://www.zincland.com/hypocycloid/

Now uses arcs where possible isntead of multiple line segments! See the [Changes](#changes) section for more info.

Now uses splines for the hyperbolic profile instead of multiple line segments! See the [Changes](#changes) section for more info.

GNU GPL v3.0 


## <a name="usage"> Usage

The following commandline arguments exist:
- One (and only one) of the following arguments must be used:
  - `-p/--pitch`: Tooth Pitch
    - Diameter of valleys
  - `-b/--bolt_circ_radius`: Pin bolt circle radius (overrides -p)
    - Radius of bolt circle of pins can be used instead of using the tooth pitch
- All of the following arguments must be supplied: 
  - `-d/--pin_diam`: Roller Diameter
    - Diameter of the pins/rollers you will be using
  - `-c/--pressure_offset`: Offset in pressure angle
    - Gap between profile and pins
  - `-n/--num_teeth`: Number of teeth in cam
    - Number of teeth, also sets gear reduction (i.e. 10 teeth = 10:1 reduction)
- The following arguments can optionally be supplied
  - `-a/--pressure_angle`: Pressure angle limit
    - Max pressure angle you want to have (default/recommended is 50)
  - `-e/--eccentricity`: Eccentricity
    - How far the center of rotation is from the center of the profile (recommended is pitch/(12/num_teeth)
	or bolt_circ_radius/12) (default is the recommended ratio)
  - `-s/--num_lines`: Line segments in dxf 
   - Number of line segments to use to represent the paths
   (more is better, but will impact cad performance)
  - `-r/--resolution`: Step size used to find angle limits (smaller is better but might slow 
    down script execution) (default=0.15)
  - `-f/--file_name`: Output file name
    - File name to save profile as, defaults to "output.txt" if not set
  - `-h/--help`: Prints help info

All of the information above is printed to the console when the `-h/--help` argument is passed

## <a name="changes"> Changes

1. Allow for increased resolution when finding min and max angles (to maintain desired pressure angle)
2. Now uses actual arcs where possible rather than representing arcs as many line segments
3. Restructured code to be more Pythonic, hopefully allowing for more improvements down the line
4. Represent the part of the cam that actually uses the hypocycloidal profile as a spline
    * In theory, this will further improve resultant CAD quality, and will make for a more machineable cam
	* Rather than starting with a badly interpolated CAD, and then being limited in terms of machineability, the limiting factor would be CAD/CAM or Machine performance

## <a name="goals"> Further Development Goals 
1. Add self-checking, sanity checking, and rules of thumb to follow when using
	* Right now, once the values get to a point where the profile isn't possible, the script just generates a super messed up dxf. Would be nice if you got a warning instead...
2. Add a UI (maybe even GUI) so that you don't have to do everything with command line arguments
