""" Module to create the command line arguments for this script """


from argparse import ArgumentParser
from datetime import datetime

def create_argparse():
    """ Create the arguments for this script """
    # create argument parser object
    parser = ArgumentParser(description="Hypocycloidal Gear Profile Generator")

    # create group for required named arguments
    group_req = parser.add_argument_group(title="required named arguments")
    # add mutually exclusive group to the above group
    group_p_b = group_req.add_mutually_exclusive_group(required=True)

    # add the pitch arg to the mutually exclusive group
    group_p_b.add_argument(
        "-p",
        "--pitch",
        type=float,
        help="the pitch of the cam (can be used instead of -b/--bolt_circ_diam)",
        metavar="pitch",
    )

    # add the bolt circle diameter argument to the mutually exclusive group
    group_p_b.add_argument(
        "-b",
        "--bolt_circ_diam",
        type=float,
        help="the bolt circle diameter of the pins (can be used instead of -p/--pitch)",
        metavar="bolt circle diameter",
    )

    # add the pin diameter argument to the named group
    group_req.add_argument(
        "-d",
        "--pin_diam",
        type=float,
        help="the diameter of the pins",
        metavar="pin diameter",
        required=True,
    )

    # add the eccentricity argument to the named group
    group_req.add_argument(
        "-e",
        "--eccentricity",
        type=float,
        help="center of rotation offset from center of cam",
        metavar="eccentricity",
        required=True,
    )

    # add the pressure angle argument to the named group
    parser.add_argument(
        "-a",
        "--pressure_angle",
        type=float,
        help="pressure angle limit",
        metavar="pressure angle",
        required=True,
        default=50,
    )

    # add the pressure angle offset argument to the named group
    group_req.add_argument(
        "-c",
        "--pressure_offset",
        type=float,
        help="pressure angle offset",
        metavar="pressure angle offset",
        required=True,
    )

    # add the number of teeth argument to the named group
    group_req.add_argument(
        "-n",
        "--num_teeth",
        type=int,
        help="number of teeth on the cam, also chooses reduction (i.e. 10 teeth = 10:1 reduction)",
        metavar="number of teeth",
        required=True,
    )

    # add the dxf resolution to the optional group
    parser.add_argument(
        "-s",
        "--num_lines",
        type=int,
        help="number of line segments used to represent curves in dxf \
            (more is better, but might impact CAD software performance) (default=500)",
        metavar="number of lines",
        default=500,
    )

    # add the filename argument to the optional group
    parser.add_argument(
        "-f",
        "--file_name",
        type=str,
        help="output file name (default is 'date_time.dxf')",
        metavar="file name",
        default=datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".dxf",
    )
    return parser
