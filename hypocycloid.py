#!/usr/bin/python

"""Hypocycloid cam generator
Generate dxfs of hypocycloid cams for cycloid drives

Copyright       2009, Alex Lait
Version         v0.2 (09/13/09)
License         GPL
Homepage        http://www.zincland.com/hypocycloid

Python 3 Port:
    https://github.com/rickyelopez
    https://github.com/rickyerlopez/hypocycloid

Credit to
        Formulas to describe a hypocycloid cam
        http://gears.ru/transmis/zaprogramata/2.139.pdf

        Insperational thread on CNCzone
        http://www.cnczone.com/forums/showthread.php?t=72261

        Documenting and updating the sdxf library
        http://www.kellbot.com/sdxf-python-library-for-dxf/

        Formulas for calculating the pressure angle and finding the limit circles
        http://imtuoradea.ro/auo.fmte/files-2007/MECATRONICA_files/Anamaria_Dascalescu_1.pdf

Notes:
        Does not currently do ANY checking for sane input values and it
        is possible to create un-machinable cams, use at your own risk

        Suggestions:
        - Eccentricity should not be more than the roller radius
        - Has not been tested with negative values, may have interesting results :)
"""

from math import cos, sin, pi
import sys

from modules.profile import HypProfile  # pylint: disable=import-error
from modules.args import create_argparse  # pylint: disable=import-error
from modules.dxf import (  # pylint: disable=import-error
    init_dxf,
    create_text,
    create_min_max,
    create_centers,
)


# create the argument parser object populated with all of the arguments we need
parser = create_argparse()
# convert the cmdline arguments to a dictionary for processing
args = vars(parser.parse_args(x.lower() for x in sys.argv[1:]))
# create a profile object with those arguments
prof = HypProfile(args)

# create the dxf document and modelspace
doc, msp = init_dxf()

##### Find the min and max angle that define the non-relief region of the cam profile   #####
##### any points outside of this min and max will be offset, and form the relief        #####
##### region of the cam profile                                                        #####

# find the minimum angle
i = 0
while True:
    x = prof.calc_pressure_angle(i * pi / 180)
    if x < prof.press_ang:
        prof.min_angle = round(i, 4)
        break
    i += prof.resolution

# find the maximum angle
i = 180
while True:
    x = prof.calc_pressure_angle(i * pi / 180)
    if x > -prof.press_ang:
        prof.max_angle = round(i, 4)
        break
    i -= prof.resolution

##### calculate the min and max radii that define the cutoff for the relief region      #####
##### all of the points within these radii are unrelieved                               #####
prof.calc_radii()

# generate the cam profile - note: shifted in -x by eccentricity amount
x1 = prof.calc(0, "x")
y1 = prof.calc(0, "y")
x1, y1 = prof.check_limit(x1, y1)
for i in range(1, prof.segments):
    x2 = prof.calc(prof.quadrant_frac * i, "x")
    y2 = prof.calc(prof.quadrant_frac * i, "y")
    x2, y2 = prof.check_limit(x2, y2)
    msp.add_line(
        (x1 - prof.eccentricity, y1),
        (x2 - prof.eccentricity, y2),
        dxfattribs={"layer": "cam"},
    )
    x1 = x2
    y1 = y2

# generate the pin locations
p = (
    lambda func, i: prof.pitch
    * prof.num_teeth
    * func(2 * pi / (prof.num_teeth + 1) * i)
)
for i in range(0, prof.num_teeth + 1):
    msp.add_circle(
        (p(cos, i), p(sin, i)), prof.pin_diam / 2, dxfattribs={"layer": "roller"}
    )


##### Generate and save the DXF file #####
# choose the x position of all the descriptive text
x_pos = prof.pitch * prof.num_teeth + prof.pin_diam
# create the descriptive text
create_text(msp, prof, x_pos)
# create the min and max circles
create_min_max(msp, prof)
# create the center circles
create_centers(msp, prof)

try:
    doc.saveas(prof.file_name)
except:  # TODO: except something specific here
    print("Problem saving file")
    sys.exit(2)
