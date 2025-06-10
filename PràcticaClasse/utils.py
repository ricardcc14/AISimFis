import numpy as np
import pygame
import Box2D as b2

def rotate_point(point, angle):
    cos_theta = np.cos(angle)
    sin_theta = np.sin(angle)
    rotated_x = point.x * cos_theta - point.y * sin_theta
    rotated_y = point.x * sin_theta + point.y * cos_theta
    return (rotated_x, rotated_y)


def pixelToWorld(x: float | int | list[float] | b2.b2Vec2, y: float | int | None = None):
    if isinstance(x, (float, int)) and y is None:
        return x / 100  # Case: Single float/int input
    
    elif isinstance(x, (float, int)) and isinstance(y, (float, int)):
        return b2.b2Vec2(x / 100, y / 100)  # Case: Two float/int inputs
    
    elif isinstance(x, list) and len(x) == 2:
        return b2.b2Vec2(x[0] / 100, x[1] / 100)  # Case: List input
    
    elif isinstance(x, b2.b2Vec2):
        return x / 100  # Case: b2Vec2 input (already a vector)
    
    else:
        raise TypeError("Invalid input type for pixelToWorld")
    

def worldToPixel(x: float | int | list[float] | b2.b2Vec2, y: float | int | None = None) -> float | b2.b2Vec2:
    if isinstance(x, (float, int)) and y is None:
        return x * 100  # Case: Single float/int input
    
    elif isinstance(x, (float, int)) and isinstance(y, (float, int)):
        return b2.b2Vec2(x * 100, y * 100)  # Case: Two float/int inputs

    elif isinstance(x, list) and len(x) == 2:
        return b2.b2Vec2(x[0] * 100, x[1] * 100)  # Case: List input

    elif isinstance(x, b2.b2Vec2):
        return x * 100  # Case: b2Vec2 input (already a vector)

    else:
        raise TypeError("Invalid input type for worldToPixel")


def drawRotatedImage(screen:pygame.Surface, image:pygame.Surface, position:b2.b2Vec2, width:float, height:float, angle:float):
    img = pygame.transform.scale(image, (width, height))
    img = pygame.transform.rotate(img, np.rad2deg(angle))
    trig = np.sin(angle%(np.pi/2))+np.cos(angle%(np.pi/2))
    translation_x = width/2*trig
    translation_y = height/2*trig

    screen.blit(img, (position.x-translation_x, position.y-translation_y))
    pass