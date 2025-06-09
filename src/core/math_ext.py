from math import sqrt, acos, degrees

def distance(x, y, other_x, other_y):
    return sqrt((other_x - x)**2 + (other_y - y)**2)

def safe_div(x, y):
    return x / y if y != 0 else 0

def angle_from_north(v):
    u = [0, 1]
    dot_product = sum(i*j for i, j in zip(u, v))
    norm_u = sqrt(sum(i**2 for i in u))
    norm_v = sqrt(sum(i**2 for i in v))
    cos_theta = safe_div(dot_product, (norm_u * norm_v))
    angle_rad = acos(cos_theta)
    angle_deg = round(degrees(angle_rad))
    if v[0] < 0:
        angle_deg = 360 - angle_deg
    angle_deg = 360 - angle_deg
    return angle_deg