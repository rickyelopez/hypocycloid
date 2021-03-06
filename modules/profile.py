"""
Profile Class contains all of the information pertaining to a Hypocycloid Gear
Profile, as well as all of the math required to generate them
"""
from math import atan2, sin, asin, cos, atan, pi, sqrt


class HypProfile:
    """ Object to generate and contain a hypocycloid gear profile """

    # pylint: disable=too-many-instance-attributes
    # More than 7 is reasonable in this case.
    def __init__(self, args):
        self.bolt_circ_radius = args["bolt_circ_radius"]
        self.num_teeth = args["num_teeth"]
        pitch = args["pitch"]
        self.pitch = (
            (self.bolt_circ_radius / self.num_teeth) if pitch is None else pitch
        )
        self.pin_diam = args["pin_diam"]
        eccentricity = args["eccentricity"]
        self.eccentricity = (
            round(self.pitch / (12 / self.num_teeth), 2)
            if eccentricity is None
            else eccentricity
        )
        self.segments = args["num_lines"]
        self.press_ang = args["pressure_angle"]
        self.press_offset = args["pressure_offset"]
        self.file_name = args["file_name"]
        self.resolution = args["resolution"]
        self.min_angle = self.max_angle = -1
        self.min_radius = self.max_radius = 0
        self.quadrant_frac = 2 * pi / self.segments

    def calc(self, quadrant_frac, coord):
        """ Calculate X or Y coordinate of the next point given the parameters and
            fraction of the quadrant the process is at """
        # calculate y_p
        n_x_a = self.num_teeth * quadrant_frac
        t_2 = (self.num_teeth * self.pitch) / (self.eccentricity * (self.num_teeth + 1))
        den = cos(n_x_a) + t_2
        y_p = atan(sin(n_x_a) / den)

        # calculate point
        func = cos if coord == "x" else sin
        t_1 = self.num_teeth * self.pitch * func(quadrant_frac)
        t_2 = self.eccentricity * func((self.num_teeth + 1) * quadrant_frac)
        t_3 = self.pin_diam / 2 * func(y_p + quadrant_frac)
        return t_1 + t_2 - t_3

    def calc_pressure_angle(self, angle):
        """ Calculate Pressure Angle from parameters"""
        ex = sqrt(2)
        t_1 = self.pitch * self.num_teeth
        t_2 = t_1 / ex
        t_3 = t_2 * sqrt(ex ** 2 + 1 - 2 * ex * cos(angle)) - self.pin_diam / 2
        return asin((t_1 * cos(angle) - t_2) / (t_3 + self.pin_diam / 2)) * 180 / pi

    def calc_pressure_limit(self, angle):
        """ Calculate Pressure Angle Limit for relief from parameters"""
        ex = sqrt(2)
        t_1 = self.pitch * self.num_teeth
        t_2 = t_1 / ex
        t_3 = sqrt(t_1 ** 2 + t_2 ** 2 - 2 * t_1 * t_2 * cos(angle))
        t_4 = t_3 - self.pin_diam / 2
        p_x = t_2 - self.eccentricity + t_4 * (t_1 * cos(angle) - t_2) / t_3
        p_y = t_4 * t_1 * sin(angle) / t_3
        return sqrt(p_x ** 2 + p_y ** 2)

    def calc_radii(self):
        """ Calculate minimum and maximum radii """
        self.min_radius = self.calc_pressure_limit(self.min_angle * pi / 180)
        self.max_radius = self.calc_pressure_limit(self.max_angle * pi / 180)

    def check_limit(self, rect_x, rect_y):
        """
        Apply pressure angle offset to points that fall into the relief region
        return the point values, as well as a bool indicating whether an offset
        was applied
        """
        mod = False
        pol_r, pol_a = sqrt(rect_x ** 2 + rect_y ** 2), atan2(rect_y, rect_x)
        if not self.min_radius <= pol_r <= self.max_radius:
            pol_r = pol_r - self.press_offset
            rect_x, rect_y = pol_r * cos(pol_a), pol_r * sin(pol_a)
            mod = True
        return rect_x, rect_y, mod
