import pygame
from math import (
    cos,
    sin,
    radians
)
from pygame.math import Vector2
from missile import Missile
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SHIP_ACCELERATION,
    SHIP_DECELERATION,
    SHIP_LENGTH_FRONT,
    SHIP_LENGTH_SIDES,
    VELOCITY_CAP,
    ENEMY_FOV,
    DISTANCE_LIMIT_SQUARED,
    FIRING_DISTANCE_SQUARED
)

class Ship:
    def __init__(this, x: float, y: float, target = None):
        this.pos = Vector2(x, y)
        this.velocity = Vector2(0, 0)
        this.acceleration = Vector2(0, 0)
        this.angle = 0
        this.front, this.left, this.right = this.set_points()
        this.target = target
        this.forward = Vector2(cos(radians(this.angle)), -sin(radians(this.angle)))
    
    def update(this, dt: float):
        if not this.target == None:
            this.angle = (this.target.get_pos() - this.pos).angle_to(Vector2(1, 0))
            this.pos += this.velocity * dt
            
            if this.pos.x < 0:
                this.pos.x = 0
                this.velocity.x = 0
            elif this.pos.x > SCREEN_WIDTH:
                this.pos.x = SCREEN_WIDTH
                this.velocity.x = 0
            if this.pos.y < 0:
                this.pos.y = 0
                this.velocity.y = 0
            elif this.pos.y > SCREEN_HEIGHT:
                this.pos.y = SCREEN_HEIGHT
                this.velocity.y = 0
                
            this.front, this.left, this.right = this.set_points()
    
    def create_missile(this) -> Missile:
        return Missile(this, this.front.x, this.front.y, pygame.mouse.get_pos())
    
    def accelerate(this):
        dir = this.target.get_pos() - this.pos
        this.acceleration = dir / dir.magnitude() * SHIP_ACCELERATION
        this.velocity += this.acceleration
        
        if this.velocity.magnitude_squared() > VELOCITY_CAP ** 2:
            this.velocity *= VELOCITY_CAP / this.velocity.magnitude()
    def decelerate(this):
        this.acceleration = Vector2(0, 0)
        
        prev = Vector2(this.velocity)
        if this.velocity.x > 0:
            this.velocity.x -= SHIP_DECELERATION
        elif this.velocity.x < 0:
            this.velocity.x += SHIP_DECELERATION
        
        if this.velocity.y > 0:
            this.velocity.y -= SHIP_DECELERATION
        elif this.velocity.y < 0:
            this.velocity.y += SHIP_DECELERATION
        
        if prev.x * this.velocity.x < 0:
            this.velocity.x = 0
        if prev.y * this.velocity.y < 0:
            this.velocity.y = 0
    
    def set_points(this):
        this.forward = Vector2(cos(radians(this.angle)), -sin(radians(this.angle)))
        front = this.pos + this.forward * SHIP_LENGTH_FRONT
        left = this.pos + this.forward.rotate(130) * SHIP_LENGTH_SIDES
        right = this.pos + this.forward.rotate(-130) * SHIP_LENGTH_SIDES

        return front, left, right

    def get_pos(this):
        return this.pos
    
class Player(Ship):
    def __init__(this, spawn_x: float, spawn_y: float):
        super().__init__(spawn_x, spawn_y, pygame.mouse)

class Enemy(Ship):
    def update(this, player: Player, dt: float):
        if this.detects(player):
            this.target = player
            this.accelerate()
        else:
            this.target = None
            this.decelerate()
        
        super().update(dt)
        
        if not this.target == None and this.attempt_shoot():
            return True
    
    def detects(this, player: Player):
        dist = player.pos - this.pos
        dist /= dist.magnitude()
        if ((this.forward.dot(dist) >= ENEMY_FOV and
            this.pos.distance_squared_to(player.pos) <= DISTANCE_LIMIT_SQUARED) or
            this.pos.distance_squared_to(player.pos) <= FIRING_DISTANCE_SQUARED):
           return True
        return False
    
    def attempt_shoot(this):
        if (this.pos - this.target.get_pos()).magnitude_squared() <= FIRING_DISTANCE_SQUARED:
            return True