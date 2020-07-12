""" Functions to work with the dxf output file"""

import ezdxf


def init_dxf():
    """ Initialize the document and return the handler """
    doc = ezdxf.new()
    doc.layers.new("text", dxfattribs={"color": 2})
    doc.layers.new("cam", dxfattribs={"color": 1})
    doc.layers.new("roller", dxfattribs={"color": 5})
    doc.layers.new("pressure", dxfattribs={"color": 3})
    doc.layers.new("test", dxfattribs={"color":4})
    return doc, doc.modelspace()


def create_text(msp, prof, pos):
    """ Create the text that describes the profile """
    msp.add_text(
        f"pitch={str(prof.pitch)}", dxfattribs={"layer": "text", "height": 0.1}
    ).set_pos((pos, 0.7))
    
    msp.add_text(
        f"pin diameter={str(prof.pin_diam)}",
        dxfattribs={"layer": "text", "height": 0.1},
    ).set_pos((pos, 0.5))

    msp.add_text(
        f"eccentricity={str(prof.eccentricity)}",
        dxfattribs={"layer": "text", "height": 0.1},
    ).set_pos((pos, 0.3))

    msp.add_text(
        f"# of teeth={str(prof.num_teeth)}", dxfattribs={"layer": "text", "height": 0.1}
    ).set_pos((pos, 0.1))

    msp.add_text(
        f"pressure angle limit={str(prof.press_ang)}",
        dxfattribs={"layer": "text", "height": 0.1},
    ).set_pos((pos, -0.1))

    msp.add_text(
        f"pressure angle offset={str(prof.press_offset)}",
        dxfattribs={"layer": "text", "height": 0.1},
    ).set_pos((pos, -0.3))

    msp.add_text(
        f"min angle={str(prof.min_angle)}", dxfattribs={"layer": "text", "height": 0.1}
    ).set_pos((pos, -0.5))

    msp.add_text(
        f"max angle={str(prof.max_angle)}", dxfattribs={"layer": "text", "height": 0.1}
    ).set_pos((pos, -0.7))


def create_min_max(msp, prof):
    """ Create the circles representing min and max radii"""
    msp.add_circle(
        (-prof.eccentricity, 0), prof.min_radius, dxfattribs={"layer": "pressure"}
    )
    msp.add_circle(
        (-prof.eccentricity, 0), prof.max_radius, dxfattribs={"layer": "pressure"}
    )


def create_centers(msp, prof):
    """ Create the circles at the center of the cam and the center of the pins"""
    # add circle in the center of the cam
    msp.add_circle(
        (-prof.eccentricity, 0), prof.pin_diam / 2, dxfattribs={"layer": "cam"}
    )
    # add circle at the center of the pins
    msp.add_circle((0, 0), prof.pin_diam / 2, dxfattribs={"layer": "roller"})
