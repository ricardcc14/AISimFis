import numpy as np


def observe(ball, platforms, screen_height):
    i1 = ball.body.position.y
    i2 = ball.body.linearVelocity.y

    # Filtra només les plataformes sota la pilota
    below_platforms = [p for p in platforms if p.body.position.y > i1]

    if below_platforms:
        # Troba la plataforma més propera sota la pilota
        closest_platform = min(below_platforms, key=lambda p: p.body.position.y - i1)
        i3 = closest_platform.body.position.y - i1
        i4 = closest_platform.body.position.x - ball.body.position.x
    else:
        i3 = screen_height / 30
        i4 = 0

    return np.array([i1, i2, i3, i4], dtype=np.float32)