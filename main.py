import pygame
import ship
import asteroid
import timer
import asyncio
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    FONT,
    PLAYER_COLOR,
    ENEMY_COLOR,
    POS_COLOR,
    VELOCITY_COLOR,
    ACCELERATION_COLOR,
    MISSILE_COLOR,
    MISSILE_RADIUS,
    ASTEROID_COLOR
)

async def main():
    screen = pygame.display.set_mode((1200, 760))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()
    
    asteroids = []
    missiles = []
    player = ship.Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    enemy = ship.Enemy(150, 100)
    
    number_hit = 0
    
    for i in range(10): # initialize the list of asteroids
        asteroid.add_new(asteroids, player)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        for a in asteroids:
            if a.pos.distance_squared_to(player.pos) < (a.radius + 20) ** 2:
                print("An asteroid hit you! You died.")
                running = False
        
        dt = 1/FPS
        
        pressed = pygame.key.get_pressed()
        accelerating = False
        
        if pressed[pygame.K_w]:
            player.accelerate()
            accelerating = True
            
        if timer.player_shoot_timer.update(dt) and pressed[pygame.K_SPACE]:
            missiles.append(player.create_missile())
            timer.player_shoot_timer.reset()
            
        if not accelerating:
            player.decelerate()
        
        screen.fill((0, 0, 0))
        
        player.update(dt)
        wants_to_shoot = enemy.update(player, dt)
        if timer.enemy_shoot_timer.update(dt) and wants_to_shoot:
            missiles.append(enemy.create_missile())
            timer.enemy_shoot_timer.reset()
        
        pygame.draw.polygon(screen, PLAYER_COLOR, (player.front, player.left, player.right))
        pygame.draw.polygon(screen, ENEMY_COLOR, (enemy.front, enemy.left, enemy.right))
        
        for m in missiles:
            number_hit += m.update(asteroids, missiles, dt)
            if not m.owner == player and m.pos.distance_squared_to(player.pos) < (20) ** 2:
                print("The enemy hit you! You died.")
                running = False
            pygame.draw.circle(screen, MISSILE_COLOR, (m.pos.x, m.pos.y), MISSILE_RADIUS)
            
        if timer.creation_timer.update(dt):
            asteroid.add_new(asteroids, player)
            timer.creation_timer.reset(timer.creation_timer.default_time * (asteroids.__len__() / 10))

        for a in asteroids:
            a.update(dt)
            
            for b in asteroids:
                if b == a:
                    continue
                if a.pos.distance_squared_to(b.pos) < (a.radius + b.radius) ** 2:
                    asteroid.collide(a, b)
                    
            pygame.draw.circle(screen, ASTEROID_COLOR, (a.pos.x, a.pos.y), a.radius)
            
        text = [
            FONT.render(f"Position: <{player.pos.x: .2f}, {player.pos.y: .2f}>", False, POS_COLOR),
            FONT.render(f"Velocity: <{player.velocity.x: .2f}, {player.velocity.y: .2f}>", False, VELOCITY_COLOR),
            FONT.render(f"Acceleration: <{player.acceleration.x: .2f}, {player.acceleration.y: .2f}>", False, ACCELERATION_COLOR),
            FONT.render(f"Number of asteroids hit: {number_hit}", False, POS_COLOR)
        ]
        
        i = 0
        for t in text:
            screen.blit(t, (0, i))
            i += FONT.get_height()
        
        pygame.display.flip()
                
        clock.tick(FPS)
        await asyncio.sleep(0)
        
    pygame.quit()

asyncio.run(main())
