# Hypocycloid Profile Generator

This is a Python 3 port of the Hypocycloidal Gear Profile generator from http://www.zincland.com/hypocycloid/

I'm going to patch some bugs and make it more stable, and then I'll move on to trying to add some new features (like a UI)

GNU GPL v3.0 


## Usage

The following commandline arguments are required:

  - *-p*: Tooth Pitch
    - Diameter of valleys
  - *-b*: Pin bolt circle diameter (overrides -p)
    - Diameter of bolt circle of pins can be used instead of using the tooth pitch
  - *-d*: Roller Diameter
    - Diameter of the pins/rollers you will be using
  - *-e*: Eccentricity
    - How far the center of rotation is from the center of the profile
  - *-a*: Pressure angle limit
    - Max pressure angle you want to have (recommended is 50)
  - *-c*: Offset in pressure angle
    - Gap between profile and pins
  - *-n*: Number of teeth in cam
    - Number of teeth, also sets gear reduction (i.e. 10 teeth = 10:1 reduction)
  - *-s*: Line segments in dxf 
    - Number of line segments to use to represent the paths 
	(more is better, but will impact cad performance)
  - *-f*: Output file name
    - File name to save profile as, defaults to "output.txt" if not set
  - *-h*: Prints help info
