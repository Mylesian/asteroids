import pygame
from asteroid import Asteroid
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    MISSILE_VELOCITY,
    MISSILE_RADIUS
)

class Missile:
    def __init__(this, owner, x: float, y: float, target: pygame.math.Vector2):
        this.pos = pygame.math.Vector2(x, y)
        this.velocity = this.set_velocity(target)
        this.owner = owner
        
    def set_velocity(this, target: pygame.math.Vector2) -> pygame.math.Vector2:
        direction = target - this.pos
        return direction / direction.magnitude() * MISSILE_VELOCITY * FPS
        
    def update(this, asteroids: list[Asteroid], missiles: list, dt: float) -> int:
        this.pos += this.velocity * dt
        
        for ast in asteroids[:]:
            if this.pos.distance_squared_to(ast.pos) <= (MISSILE_RADIUS + ast.radius) ** 2:
                asteroids.remove(ast)
                missiles.remove(this)
                return 1
        
        if this.pos.x < 0 or this.pos.x > SCREEN_WIDTH or this.pos.y < 0 or this.pos.y > SCREEN_HEIGHT:
            if not missiles.index(this) == -1:
                missiles.remove(this)
        
        return 0