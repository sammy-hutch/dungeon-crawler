from math import sqrt, acos, degrees

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

def dist_to_mouse_target(player, target, mouse_pos, camera):
    """
    Calculates distance from player's sprite to all sprites, returning result if sprite is at mouse location
    Args:
        player: player entity
        target: target entity, e.g. usable entity, enemy entity
        mouse_pos: pygame.mouse.get_pos()
        camera: pygame rect
    Returns:
        distance if sprite at mouse location, otherwise None
    """
    from components.sprite import Sprite
    target_sprite = target.get(Sprite)
    x_sprite = target.x - camera.x
    y_sprite = target.y - camera.y
    width_sprite = target_sprite.image.get_width()
    height_sprite = target_sprite.image.get_height()
    
    # Check if the mouse is clicking this
    if x_sprite < mouse_pos[0] < x_sprite + width_sprite and \
        y_sprite < mouse_pos[1] < y_sprite + height_sprite:
        player_sprite = player.get(Sprite)
        # Calculate the distance between these two sprites, from their centres
        # TODO: simplify this using tilesizes
        d = distance(x_sprite + target_sprite.image.get_width()/2,
                        y_sprite + target_sprite.image.get_height()/2,
                        player.x - camera.x + player_sprite.image.get_width()/2,
                        player.y - camera.y + player_sprite.image.get_height()/2)
        return d
    else:
        return None

def distance(x, y, other_x, other_y):
    return sqrt((other_x - x)**2 + (other_y - y)**2)

def safe_div(x, y):
    return x / y if y != 0 else 0