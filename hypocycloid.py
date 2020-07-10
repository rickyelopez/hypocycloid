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
from getopt import getopt, GetoptError
import ezdxf
from datetime import datetime
from argparse import ArgumentParser


def usage():
    """
    Print command line arguments
    """

    print("Useage:")
    print("-p = Tooth Pitch              (float)")
    print("-b = Pin bolt circle diameter (float)")
    print("     -b overrides -p")
    print("-d = Roller Diameter          (float)")
    print("-e = Eccentricity             (float)")
    print("-a = Pressure angle limit     (float)")
    print("-c = offset in pressure angle (float)")
    print("-n = Number of Teeth in Cam   (integer)")
    print("-s = Line segements in dxf    (integer)")
    print("-f = output filename          (string)")
    print("-h = this help")
    print(
        "\nExample: hypocycloid.py -p 0.08 -d 0.15\
            -e 0.05 -a 50.0 -c 0.01 -n 10 -s 400 -f foo.dxf"
    )


def toPolar(x, y):
    """ Convert input coords to polar coordinate system """
    return (x ** 2 + y ** 2) ** 0.5, math.atan2(y, x)


def toRect(r, a):
    """ Convert input coords to rectangular coordinate system """
    return r * math.cos(a), r * math.sin(a)


def calcyp(a, e, n):
    """ tbd """
    return math.atan(math.sin(n * a) / (math.cos(n * a) + (n * p) / (e * (n + 1))))


def calcX(p, d, e, n, a):
    """ tbd """
    return (
        (n * p) * math.cos(a)
        + e * math.cos((n + 1) * a)
        - d / 2 * math.cos(calcyp(a, e, n) + a)
    )


def calcY(p, d, e, n, a):
    """ tbd """
    return (
        (n * p) * math.sin(a)
        + e * math.sin((n + 1) * a)
        - d / 2 * math.sin(calcyp(a, e, n) + a)
    )


def calcPressureAngle(p, d, n, a):
    """ Calculate Pressure Angle from parameters"""
    ex = 2 ** 0.5
    r3 = p * n
    rg = r3 / ex
    pp = rg * (ex ** 2 + 1 - 2 * ex * math.cos(a)) ** 0.5 - d / 2
    return math.asin((r3 * math.cos(a) - rg) / (pp + d / 2)) * 180 / math.pi


def calcPressureLimit(p, d, e, n, a):
    """ Calculate Pressure Angle Limit from parameters"""
    ex = 2 ** 0.5
    r3 = p * n
    rg = r3 / ex
    q = (r3 ** 2 + rg ** 2 - 2 * r3 * rg * math.cos(a)) ** 0.5
    x = rg - e + (q - d / 2) * (r3 * math.cos(a) - rg) / q
    y = (q - d / 2) * r3 * math.sin(a) / q
    return (x ** 2 + y ** 2) ** 0.5


def checkLimit(x, y, maxrad, minrad, offset):
    """ tbd """
    r, a = toPolar(x, y)
    if (r > maxrad) or (r < minrad):
        r = r - offset
        x, y = toRect(r, a)
    return x, y


f = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".dxf"
parser = ArgumentParser(description="Hypocycloidal Gear Profile Generator")

group_req = parser.add_argument_group(title="required named arguments")
group_p_b = group_req.add_mutually_exclusive_group(required=True)

group_p_b.add_argument(
    "-p",
    "--pitch",
    type=float,
    help="the pitch of the cam (can be used instead of -b/--bolt_circ_diam)",
    metavar="pitch",
)
group_p_b.add_argument(
    "-b",
    "--bolt_circ_diam",
    type=float,
    help="the bolt circle diameter of the pins (can be used instead of -p/--pitch)",
    metavar="bolt circle diameter",
)

group_req.add_argument(
    "-d",
    "--pin_diam",
    type=float,
    help="the diameter of the pins",
    metavar="pin diameter",
    required=True,
)

group_req.add_argument(
    "-e",
    "--eccentricity",
    type=float,
    help="center of rotation offset from center of cam",
    metavar="eccentricity",
    required=True,
)

group_req.add_argument(
    "-a",
    "--pressure_angle",
    type=float,
    help="pressure angle limit",
    metavar="pressure angle",
    required=True,
    default=50,
)

group_req.add_argument(
    "-c",
    "--pressure_offset",
    type=float,
    help="pressure angle offset",
    metavar="pressure angle offset",
    required=True,
)

group_req.add_argument(
    "-n",
    "--num_teeth",
    type=int,
    help="number of teeth on the cam, also chooses reduction (i.e. 10 teeth = 10:1 reduction)",
    metavar="number of teeth",
    required=True,
)

parser.add_argument(
    "-s",
    "--num_lines",
    type=int,
    help="number of line segments used to represent curves in dxf (more is better, but will impact CAD software performance) (default=500)",
    metavar="number of lines",
    default=500,
)

parser.add_argument(
    "-f",
    "--file_name",
    type=str,
    help="output file name (default is 'date_time.dxf')",
    metavar="file name",
    default=datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".dxf",
)

args = vars(parser.parse_args(x.lower() for x in sys.argv[1:]))

p = args["pitch"]
b = args["bolt_circ_diam"]
d = args["pin_diam"]
e = args["eccentricity"]
n = args["num_teeth"]
s = args["num_lines"]
ang = args["pressure_angle"]
c = args["pressure_offset"]
f = args["file_name"]

# if -b was specifed, calculate the tooth pitch for use in cam generation
if b:
    p = b / n

q = 2 * math.pi / float(s)


doc = ezdxf.new()
doc.layers.new("text", dxfattribs={"color": 2})
doc.layers.new("cam", dxfattribs={"color": 1})
doc.layers.new("roller", dxfattribs={"color": 5})
doc.layers.new("pressure", dxfattribs={"color": 3})

msp = doc.modelspace()


msp.add_text(f"pitch={str(p)}", dxfattribs={"layer": "text", "height": 0.1}).set_pos(
    (p * n + d, 0.7)
)

msp.add_text(
    f"pin diameter={str(d)}", dxfattribs={"layer": "text", "height": 0.1}
).set_pos((p * n + d, 0.5))

msp.add_text(
    f"eccentricity={str(e)}", dxfattribs={"layer": "text", "height": 0.1}
).set_pos((p * n + d, 0.3))

msp.add_text(
    f"# of teeth={str(n)}", dxfattribs={"layer": "text", "height": 0.1}
).set_pos((p * n + d, 0.1))

msp.add_text(
    f"pressure angle limit={str(ang)}", dxfattribs={"layer": "text", "height": 0.1}
).set_pos((p * n + d, -0.1))

msp.add_text(
    f"pressure angle offset={str(c)}", dxfattribs={"layer": "text", "height": 0.1}
).set_pos((p * n + d, -0.3))

min_angle = -1.0
max_angle = -1.0

for i in range(180):
    x = calcPressureAngle(p, d, n, float(i) * math.pi / 180)
    if (x < ang) and (min_angle < 0):
        min_angle = float(i)
    if (x < -ang) and (max_angle < 0):
        max_angle = float(i - 1)

msp.add_text(
    f"min angle={str(min_angle)}", dxfattribs={"layer": "text", "height": 0.1}
).set_pos((p * n + d, -0.5))

msp.add_text(
    f"max angle={str(max_angle)}", dxfattribs={"layer": "text", "height": 0.1}
).set_pos((p * n + d, -0.7))

minRadius = calcPressureLimit(p, d, e, n, min_angle * math.pi / 180)
maxRadius = calcPressureLimit(p, d, e, n, max_angle * math.pi / 180)

msp.add_circle((-e, 0), minRadius, dxfattribs={"layer": "pressure"})
msp.add_circle((-e, 0), maxRadius, dxfattribs={"layer": "pressure"})

# generate the cam profile - note: shifted in -x by eccentricity amount
i = 0
x1 = calcX(p, d, e, n, q * i)
y1 = calcY(p, d, e, n, q * i)
x1, y1 = checkLimit(x1, y1, maxRadius, minRadius, c)
for i in range(0, s):
    x2 = calcX(p, d, e, n, q * (i + 1))
    y2 = calcY(p, d, e, n, q * (i + 1))
    x2, y2 = checkLimit(x2, y2, maxRadius, minRadius, c)
    msp.add_line((x1 - e, y1), (x2 - e, y2), dxfattribs={"layer": "cam"})
    x1 = x2
    y1 = y2

# add a circle in the center of the cam
msp.add_circle((-e, 0), d / 2, dxfattribs={"layer": "cam"})

# generate the pin locations
for i in range(0, n + 1):
    x = p * n * math.cos(2 * math.pi / (n + 1) * i)
    y = p * n * math.sin(2 * math.pi / (n + 1) * i)
    msp.add_circle((x, y), d / 2, dxfattribs={"layer": "roller"})
# add a circle in the center of the pins
msp.add_circle((0, 0), d / 2, dxfattribs={"layer": "roller"})


try:
    doc.saveas(f)
except:
    print("Problem saving file")
    sys.exit(2)
