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

nought = "nought"
tensor_product = sympy.Function("") #tensor_product
tensor_product.unicode_representation = u"\u2297"
unknown_node = sympy.Symbol('UNKNOWN')
quantum_if = sympy.Symbol('IF')
measured = sympy.Symbol('0')
sqrt2 = sympy.sqrt(2)