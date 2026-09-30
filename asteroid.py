import pygame
import random as rand
import math
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    ASTEROID_DENSITY
)

class Asteroid:
    def __init__(this, pos: pygame.math.Vector2, radius: int):
        this.pos = pos
        this.velocity = pygame.math.Vector2(rand.randint(-5, 5) * FPS, rand.randint(-1, 1) * FPS)
        
        while this.velocity.magnitude_squared() == 0:
            this.velocity = pygame.math.Vector2(rand.randint(-5, 5) * FPS, rand.randint(-1, 1) * FPS)
        
        this.radius = radius
        this.area = math.pi * (this.radius ** 2)
        this.mass = this.area * ASTEROID_DENSITY
        
    def update(this, dt: float):
        this.pos += this.velocity * dt
        if this.pos.x + this.radius <= 0:
            this.pos.x = SCREEN_WIDTH + this.radius
        elif this.pos.x - this.radius >= SCREEN_WIDTH:
            this.pos.x = -this.radius
        
        if this.pos.y + this.radius <= 0:
            this.pos.y = SCREEN_HEIGHT + this.radius
        elif this.pos.y - this.radius >= SCREEN_HEIGHT:
            this.pos.y = -this.radius

def add_new(asteroids: list[Asteroid], player):
    radius = rand.randint(15, 25)
    test_pos = pygame.math.Vector2(rand.randint(0 + radius, SCREEN_WIDTH - radius), 
                        rand.randint(0 + radius, SCREEN_HEIGHT - radius))
    
    while not check_unique_pos(asteroids, test_pos, radius, player):
        test_pos = pygame.math.Vector2(rand.randint(0 + radius, SCREEN_WIDTH - radius), 
                            rand.randint(0 + radius, SCREEN_HEIGHT - radius))
    
    asteroids.append(Asteroid(test_pos, radius))

def check_unique_pos(list: list[Asteroid], pos: pygame.math.Vector2, r: int, player): # make sure each asteroid starts in a unique position
    for asteroid in list:
        if pygame.math.Vector2.distance_squared_to(asteroid.pos, pos) <= (r + asteroid.radius) ** 2:
            return False
    if pygame.math.Vector2.distance_squared_to(pos, player.pos) <= (r * 4) ** 2:
        return False
    return True

def collide(ast_1: Asteroid, ast_2: Asteroid):
    norm = ast_1.pos - ast_2.pos
    
    ast_1.pos = ast_2.pos + (ast_1.radius + ast_2.radius) * (norm) / norm.magnitude()
        
    k = ast_1.mass * ast_1.velocity.magnitude() + ast_2.mass * ast_2.velocity.magnitude()
    c = ast_1.mass * (ast_1.velocity.magnitude() ** 2) + ast_2.mass * (ast_2.velocity.magnitude() ** 2)
    a = ast_1.mass + ((ast_1.mass ** 2) / ast_2.mass)
    b = -2 * (k * ast_1.mass / ast_2.mass)
    
    ast_1.velocity = ((-b - math.sqrt((b ** 2) + 4 * a * c)) / (2 * a)) * ast_1.velocity / ast_1.velocity.magnitude()
    ast_2.velocity = ((k - ast_1.mass * ast_1.velocity.magnitude()) / ast_2.mass) * ast_2.velocity / ast_2.velocity.magnitude()
    
    ast_1.velocity.rotate(2 * ast_1.velocity.angle_to(norm))
    ast_2.velocity.rotate(-2 * ast_2.velocity.angle_to(norm))