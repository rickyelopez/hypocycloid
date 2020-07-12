#!/usr/bin/python

"""Hypocycloid cam generator
Generate dxfs of hypocycloid cams for cycloid drives

Copyright 	2009, Alex Lait
Version 	v0.2 (09/13/09)
License 	GPL
Homepage 	http://www.zincland.com/hypocycloid

Python 3 Port:
    https://github.com/rickyelopez
    https://github.com/rickyerlopez/hypocycloid

Credit to:
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

import math
import sys
from argparse import ArgumentParser
from datetime import datetime

import ezdxf

from modules.profile import HypProfile
from modules.args import create_argparse

# create the argument parser object populated with all of the arguments we need
parser = create_argparse()
# convert the cmdline arguments to a dictionary for processing
args = vars(parser.parse_args(x.lower() for x in sys.argv[1:]))
# create a profile object with those arguments
prof = HypProfile(args)

doc = ezdxf.new()
doc.layers.new("text", dxfattribs={"color": 2})
doc.layers.new("cam", dxfattribs={"color": 1})
doc.layers.new("roller", dxfattribs={"color": 5})
doc.layers.new("pressure", dxfattribs={"color": 3})

msp = doc.modelspace()

x_pos = prof.pitch * prof.num_teeth + prof.pin_diam

msp.add_text(
    f"pitch={str(prof.pitch)}", dxfattribs={"layer": "text", "height": 0.1}
).set_pos((x_pos, 0.7))

msp.add_text(
    f"pin diameter={str(prof.pin_diam)}", dxfattribs={"layer": "text", "height": 0.1}
).set_pos((x_pos, 0.5))

msp.add_text(
    f"eccentricity={str(prof.eccentricity)}",
    dxfattribs={"layer": "text", "height": 0.1},
).set_pos((x_pos, 0.3))

msp.add_text(
    f"# of teeth={str(prof.num_teeth)}", dxfattribs={"layer": "text", "height": 0.1}
).set_pos((x_pos, 0.1))

msp.add_text(
    f"pressure angle limit={str(prof.press_ang)}",
    dxfattribs={"layer": "text", "height": 0.1},
).set_pos((x_pos, -0.1))

msp.add_text(
    f"pressure angle offset={str(prof.press_offset)}",
    dxfattribs={"layer": "text", "height": 0.1},
).set_pos((x_pos, -0.3))


for i in range(180):
    x = prof.calc_pressure_angle(float(i) * math.pi / 180)
    if (x < prof.press_ang) and (prof.min_angle < 0):
        prof.min_angle = float(i)
    if (x < -prof.press_ang) and (prof.max_angle < 0):
        prof.max_angle = float(i - 1)

msp.add_text(
    f"min angle={str(prof.min_angle)}", dxfattribs={"layer": "text", "height": 0.1}
).set_pos((x_pos, -0.5))

msp.add_text(
    f"max angle={str(prof.max_angle)}", dxfattribs={"layer": "text", "height": 0.1}
).set_pos((x_pos, -0.7))

prof.calc_radii()

msp.add_circle(
    (-prof.eccentricity, 0), prof.min_radius, dxfattribs={"layer": "pressure"}
)
msp.add_circle(
    (-prof.eccentricity, 0), prof.max_radius, dxfattribs={"layer": "pressure"}
)

# generate the cam profile - note: shifted in -x by eccentricity amount
i = 0
x1 = prof.calc(0, "x")
y1 = prof.calc(0, "y")
x1, y1 = prof.check_limit(x1, y1)
for i in range(1, prof.segments + 1):
    x2 = prof.calc(prof.q * i, "x")
    y2 = prof.calc(prof.q * i, "y")
    x2, y2 = prof.check_limit(x2, y2)
    msp.add_line(
        (x1 - prof.eccentricity, y1),
        (x2 - prof.eccentricity, y2),
        dxfattribs={"layer": "cam"},
    )
    x1 = x2
    y1 = y2

# add a circle in the center of the cam
msp.add_circle((-prof.eccentricity, 0), prof.pin_diam / 2, dxfattribs={"layer": "cam"})

# generate the pin locations
for i in range(0, prof.num_teeth + 1):
    p = (
        lambda func: prof.pitch
        * prof.num_teeth
        * func(2 * math.pi / (prof.num_teeth + 1) * i)
    )
    msp.add_circle(
        (p(math.cos), p(math.sin)), prof.pin_diam / 2, dxfattribs={"layer": "roller"}
    )
# add a circle in the center of the pins
msp.add_circle((0, 0), prof.pin_diam / 2, dxfattribs={"layer": "roller"})


try:
    doc.saveas(prof.file_name)
except:
    print("Problem saving file")
    sys.exit(2)
