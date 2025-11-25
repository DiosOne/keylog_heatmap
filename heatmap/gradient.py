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
