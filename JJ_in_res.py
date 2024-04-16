# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2021.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

import numpy as np
from qiskit_metal import draw, Dict
from qiskit_metal.qlibrary.core import BaseQubit


class JJinRes(BaseQubit):  # pylint: disable=invalid-name

    default_options = Dict(
        prime_width = '20um',
        taper_width = '10um',
        prime_gap = "5um"
    )
    """Default options."""

    component_metadata = Dict(short_name='JJRes',
                              _qgeometry_table_poly='True',
                              _qgeometry_table_junction='True')
    """Component metadata"""

    TOOLTIP = """Simple Metal Transmon Cross."""

    ##############################################MAKE######################################################

    def make(self):
        """This is executed by the GUI/user to generate the qgeometry for the
        component."""
        self.make_pocket()
        # self.make_connection_pads()

###################################TRANSMON#############################################################

    def make_pocket(self):
        # """Makes a basic Crossmon, 4 arm cross."""

        # self.p allows us to directly access parsed values (string -> numbers) form the user option
        p = self.p

        # access to chip name
        chip = p.chip
        width = p.prime_width
        t_width = p.taper_width

        left_bank = draw.Polygon([(-width/2, width/2), (-width/2, -width/2), (-t_width/2, -t_width/2), (-t_width/2, t_width/2)])
        right_bank = draw.Polygon([(width/2, width/2), (width/2, -width/2), (t_width/2, -t_width/2), (t_width/2, t_width/2)])

        banks = draw.shapely.ops.unary_union([left_bank, right_bank])
        banks_etch = draw.rectangle(width+2*p.prime_gap, width+2*p.prime_gap)

        # The junction/SQUID
        rect_jj = draw.LineString([(-t_width/2, 0),
                                   (t_width/2, 0)])
        
        left_port = draw.LineString([(-width/2, -width/2), (-width/2, width/2)])
        right_port = draw.LineString([(width/2, width/2), (width/2, -width/2)])

        #rotate and translate
        polys = [banks, banks_etch, rect_jj, left_port, right_port]
        polys = draw.rotate(polys, p.orientation, origin=(0, 0))
        polys = draw.translate(polys, p.pos_x, p.pos_y)

        [banks, banks_etch, rect_jj, left_port, right_port] = polys

        # generate qgeometry
        self.add_qgeometry('poly', dict(banks=banks), chip=chip)
        self.add_qgeometry('poly',
                           dict(banks_etch=banks_etch),
                           subtract=True,
                           chip=chip)
        self.add_qgeometry('junction',
                           dict(rect_jj=rect_jj),
                           width=t_width,
                           chip=chip)
        self.add_pin("left_pin",
                     left_port.coords,
                     width)
        self.add_pin("right_pin",
                     right_port.coords,
                     width)