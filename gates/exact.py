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


import sympy

import constants

# Declaration of valid status (exc. mixed)
x = sympy.Symbol('X')
y = sympy.Symbol('Y')
z = sympy.Symbol('Z')
i = sympy.Symbol('I')

# Declaration of valid gates
h = sympy.Symbol('H')
t = sympy.Symbol('T')
cnot = sympy.Symbol('CNot')

# The quantum abstract domain associations
associations = {
    t: {
        x: (x + y) / constants.sqrt2,
        y: (y - x) / constants.sqrt2,
        z: z,
        i: i
    },
    h: {
        x: z,
        y: -y,
        z: x,
        i: i
    },
    x: {
        x: x,
        y: -y,
        z: -z,
        i: i
    },
    y: {
        x: -x,
        y: y,
        z: -z,
        i: i
    },
    z: {
        x: -x,
        y: -y,
        z: z,
        i: i
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
    },
    True: {
        i: (i + z)/2,
        x: constants.measured,
        y: constants.measured,
        z: (i + z)/2
    },
    False: {
        i: (i - z)/2,
        x: constants.measured,
        y: constants.measured,
        z: (z - i)/2
    }
}
