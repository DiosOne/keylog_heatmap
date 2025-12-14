# heatmap/gradient.py
# Copyright (C) 2025 Dom Andrewartha
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from typing import Tuple

START= (32, 204, 0)  # Decepticon Green
FINISH= (173, 0, 204) # Decepticon Purple

def clamp_to(val: float) -> float:
    return max(0.0, min(1.0, float(val)))

def linear_interp(a: float, b: float, t: float) -> float:
    return a + (b-a) * t

def grad_colour(t: float) -> Tuple[int, int, int]:
    '''return rgb for normalised value'''
    t= clamp_to(t)
    r= int(round(linear_interp(START[0], FINISH[0], t)))
    g= int(round(linear_interp(START[1], FINISH[1], t)))
    b= int(round(linear_interp(START[2], FINISH[2], t)))
    return (r, g, b)
