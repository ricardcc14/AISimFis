import numpy as np

def observe(ball, platforms, screen_height):
    i1 = ball.body.position.y
    i2 = ball.body.linearVelocity.y

    closest_platform = None
    min_dy = float('inf')
    for p in platforms:
        dy = p.body.position.y - i1
        if dy > 0 and dy < min_dy:
            min_dy = dy
            closest_platform = p

    if closest_platform:
        i3 = min_dy
        i4 = closest_platform.body.position.x - ball.body.position.x
    else:
        i3 = screen_height / 30
        i4 = 0

    return np.array([i1, i2, i3, i4], dtype=np.float32)