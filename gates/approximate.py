# Copyright 2017 David A. Zonneveld Michel
# This file is part of Quasim.
#
# Quasim is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Quasim is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>

from constants import *
import sympy

# Declaration of valid status (exc. mixed)
x = sympy.Symbol('X')
z = sympy.Symbol('Z')
y = sympy.Symbol('Y')
i = sympy.Symbol('I')

top = sympy.Symbol("top")
bottom = sympy.Symbol("bottom")

# Declaration of valid gates
h = sympy.Symbol('H')
t = sympy.Symbol('T')
cnot = sympy.Symbol('CNot')

# The quantum abstract domain associations
associations = {
    t: {
        x: bottom,
        y: bottom,
        z: z,
        i: i,
        bottom: bottom,
        top: top
    },
    h: {
        x: z,
        y: -y,
        z: x,
        i: i,
        bottom: bottom,
        top: top
    },
    x: {
        x: x,
        y: -y,
        z: -z,
        i: i,
        bottom: bottom,
        top: top

    },
    y: {
        x: -x,
        y: y,
        z: -z,
        i: i,
        bottom: bottom,
        top: top
    },
    z: {
        x: -x,
        y: -y,
        z: z,
        i: i,
        bottom: bottom,
        top: top
    },
    cnot: {
        (x, x): (x, i),
        (x, y): (y, z),
        (x, z): (-y, y),
        (y, x): (y, i),
        (y, y): (-x, z),
        (y, z): (x, y),
        (z, x): (z, x),
        (z, y): (i, y),
        (z, z): (i, z),
        (i, x): (i, x),
        (i, y): (z, y),
        (i, z): (z, z),
        (x, i): (x, x),
        (y, i): (y, x),
        (z, i): (z, i),
        (i, i): (i, i),
        (bottom, bottom): (bottom, bottom),
        (bottom, top): (bottom, top),
        (top, bottom): (top, bottom),
        (top, top): (top, top),
        (i, i): (i, i)
    },
    True: {
        i: (i + z)/2,
        x: measured,
        y: measured,
        z: (i + z)/2,
        bottom: bottom,
        top: top
    },
    False: {
        i: (i - z)/2,
        x: measured,
        y: measured,
        z: (z - i)/2,
        bottom: bottom,
        top: top
    }
}
