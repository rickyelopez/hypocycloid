# Hypocycloid Profile Generator

This is a Python 3 port of the Hypocycloidal Gear Profile generator from http://www.zincland.com/hypocycloid/

I'm going to patch some bugs and make it more stable, and then I'll move on to trying to add some new features (like a UI)

GNU GPL v3.0 


## Usage

The following commandline arguments exist:
  - One (and only one) of the following arguments must be used:
    - `-p/--pitch`: Tooth Pitch
      - Diameter of valleys
    - `-b/--bolt_circ_diam`: Pin bolt circle diameter (overrides -p)
      - Diameter of bolt circle of pins can be used instead of using the tooth pitch
  - All of the following arguments must be supplied: 
    - `-d/--pin_diam`: Roller Diameter
      - Diameter of the pins/rollers you will be using
    - `-e/--eccentricity`: Eccentricity
      - How far the center of rotation is from the center of the profile
    - `-c/--pressure_offset`: Offset in pressure angle
      - Gap between profile and pins
    - `-n/--num_teeth`: Number of teeth in cam
      - Number of teeth, also sets gear reduction (i.e. 10 teeth = 10:1 reduction)
  - The following arguments can optionally be supplied
    - `-a/--pressure_angle`: Pressure angle limit
      - Max pressure angle you want to have (default/recommended is 50)
    - `-s/--num_lines`: Line segments in dxf 
      - Number of line segments to use to represent the paths 
	  (more is better, but will impact cad performance)
    - `-f/--file_name`: Output file name
      - File name to save profile as, defaults to "output.txt" if not set
    - `-h/--help`: Prints help info

All of the information above is printed to the console when the `-h/--help` argument is passed
