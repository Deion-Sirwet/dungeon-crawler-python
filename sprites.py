import pygame
import config
import math
import random
import sounds

def trans_img(self):
    return pygame.transform.scale(self, (config.tile_size, config.tile_size))

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(config.black)
        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        
        self.game = game
        self._layer = config.player_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * config.tile_size
        self.y = y * config.tile_size
        self.width = config.tile_size
        self.height = config.tile_size

        # Change for movement
        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        # Sprite image
        self.image = trans_img(self.game.character_spritesheet.get_sprite(0, 0, 16, 16))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.down_animations = [
            trans_img(self.game.character_spritesheet.get_sprite(0, 0, 16, 16)),
            trans_img(self.game.character_spritesheet.get_sprite(0, 16, 16, 16)),
            trans_img(self.game.character_spritesheet.get_sprite(0, 32, 16, 16)),
            trans_img(self.game.character_spritesheet.get_sprite(0, 48, 16, 16))
            ]
        self.up_animations = [
            trans_img(self.game.character_spritesheet.get_sprite(16, 0, 16, 16)),
            trans_img(self.game.character_spritesheet.get_sprite(16, 16, 16, 16)),
            trans_img(self.game.character_spritesheet.get_sprite(16, 32, 16, 16)),
            trans_img(self.game.character_spritesheet.get_sprite(16, 48, 16, 16))
            ]
        self.left_animations = [
            trans_img(self.game.character_spritesheet.get_sprite(32, 0, 16, 16)),
            trans_img(self.game.character_spritesheet.get_sprite(32, 16, 16, 16)),
            trans_img(self.game.character_spritesheet.get_sprite(32, 32, 16, 16)),
            trans_img(self.game.character_spritesheet.get_sprite(32, 48, 16, 16))
            ]
        self.right_animations = [
            trans_img(self.game.character_spritesheet.get_sprite(48, 0, 16, 16)),
            trans_img(self.game.character_spritesheet.get_sprite(48, 16, 16, 16)),
            trans_img(self.game.character_spritesheet.get_sprite(48, 32, 16, 16)),
            trans_img(self.game.character_spritesheet.get_sprite(48, 48, 16, 16))
            ]

    def update(self):
        self.movement()
        self.animate()
        self.collide_enemy()

        # Updates player position
        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        # Resets change before next update
        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()

        # Move the player based on key presses
        if keys[pygame.K_w]:
            self.y_change = -config.player_speed
            self.facing = 'up'
        if keys[pygame.K_s]: 
            self.y_change = config.player_speed
            self.facing = 'down'
        if keys[pygame.K_a]:
            self.x_change = -config.player_speed
            self.facing = 'left'
        if keys[pygame.K_d]:
            self.x_change = config.player_speed
            self.facing = 'right'

        # Change player speed when LSHIFT is held
        if keys[pygame.K_LSHIFT]:
            config.player_speed = 4
        else:
            config.player_speed = 2

    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.right = hits[0].rect.left
                if self.x_change < 0:
                    self.rect.left = hits[0].rect.right
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.bottom = hits[0].rect.top
                if self.y_change < 0:
                    self.rect.top = hits[0].rect.bottom

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.game.current_level_index = 0
            self.kill()
            self.game.playing = False
            sounds.death_sound.play()

    def animate(self):
        # Change animation speed if shift is held down
        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            animation_speed = 0.25  # Faster animation speed when shift is held
        else:
            animation_speed = 0.125  # Default animation speed

        if self.facing == "down":
            if self.y_change == 0:
                self.image = trans_img(self.game.character_spritesheet.get_sprite(0, 0, 16, 16))
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += animation_speed
                if self.animation_loop >= 4:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.y_change == 0:
                self.image = trans_img(self.game.character_spritesheet.get_sprite(16, 0, 16, 16))
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += animation_speed
                if self.animation_loop >= 4:
                    self.animation_loop = 1

        if self.facing == "left":
            if self.x_change == 0:
                self.image = trans_img(self.game.character_spritesheet.get_sprite(32, 0, 16, 16))
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += animation_speed
                if self.animation_loop >= 4:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = trans_img(self.game.character_spritesheet.get_sprite(48, 0, 16, 16))
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += animation_speed
                if self.animation_loop >= 4:
                    self.animation_loop = 1


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        
        self.game = game
        self._layer = config.enemy_layer
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * config.tile_size
        self.y = y * config.tile_size
        self.width = config.tile_size
        self.height = config.tile_size

        # Change for movement
        self.x_change = 0
        self.y_change = 0

        # Enemy health
        self.health = 100  # Max health of the enemy
        self.max_health = 100
        self.health_bar_width = self.width  # Health bar width is the same as the enemy width
        self.health_bar_height = 5  # Height of the health bar

        # Enemy facing and movement length
        self.facing = random.choice(['left', 'right', 'up', 'down'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(40, 90)

        self.image = trans_img(self.game.shaman_spritesheet.get_sprite(0, 0, 16, 16))
        self.image.set_colorkey(config.black)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.down_animations = [
            trans_img(self.game.shaman_spritesheet.get_sprite(0, 0, 16, 16)),
            trans_img(self.game.shaman_spritesheet.get_sprite(0, 16, 16, 16)),
            trans_img(self.game.shaman_spritesheet.get_sprite(0, 32, 16, 16)),
            trans_img(self.game.shaman_spritesheet.get_sprite(0, 48, 16, 16))
        ]
        self.up_animations = [
            trans_img(self.game.shaman_spritesheet.get_sprite(16, 0, 16, 16)),
            trans_img(self.game.shaman_spritesheet.get_sprite(16, 16, 16, 16)),
            trans_img(self.game.shaman_spritesheet.get_sprite(16, 32, 16, 16)),
            trans_img(self.game.shaman_spritesheet.get_sprite(16, 48, 16, 16))
        ]
        self.left_animations = [
            trans_img(self.game.shaman_spritesheet.get_sprite(32, 0, 16, 16)),
            trans_img(self.game.shaman_spritesheet.get_sprite(32, 16, 16, 16)),
            trans_img(self.game.shaman_spritesheet.get_sprite(32, 32, 16, 16)),
            trans_img(self.game.shaman_spritesheet.get_sprite(32, 48, 16, 16))
        ]
        self.right_animations = [
            trans_img(self.game.shaman_spritesheet.get_sprite(48, 0, 16, 16)),
            trans_img(self.game.shaman_spritesheet.get_sprite(48, 16, 16, 16)),
            trans_img(self.game.shaman_spritesheet.get_sprite(48, 32, 16, 16)),
            trans_img(self.game.shaman_spritesheet.get_sprite(48, 48, 16, 16))
        ]

    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        # Handle horizontal movement (left or right)
        if self.facing == 'left':
            self.x_change = -config.enemy_speed
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:  # Negative value for left direction
                # Change direction after completing the movement distance
                self.facing = random.choice(['left', 'right', 'up', 'down'])
                self.movement_loop = 0  # Reset movement loop to prevent jitter

        elif self.facing == 'right':
            self.x_change = config.enemy_speed
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                # Change direction after completing the movement distance
                self.facing = random.choice(['left', 'right', 'up', 'down'])
                self.movement_loop = 0  # Reset movement loop to prevent jitter

        # Handle vertical movement (up or down)
        elif self.facing == 'up':
            self.y_change = -config.enemy_speed  # Move up by decreasing Y
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                # Change direction after completing the movement distance
                self.facing = random.choice(['left', 'right', 'up', 'down'])
                self.movement_loop = 0  # Reset movement loop to prevent jitter

        elif self.facing == 'down':
            self.y_change = config.enemy_speed  # Move down by increasing Y
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:  # Negative value for down direction
                # Change direction after completing the movement distance
                self.facing = random.choice(['left', 'right', 'up', 'down'])
                self.movement_loop = 0  # Reset movement loop to prevent 

    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:  # Moving right
                    self.rect.x = hits[0].rect.left - self.rect.width  # Stop at the left side of the block
                    # Exclude 'right' from the direction options
                    self.facing = random.choice([d for d in ['left', 'up', 'down'] if d != 'right'])
                if self.x_change < 0:  # Moving left
                    self.rect.x = hits[0].rect.right  # Stop at the right side of the block
                    # Exclude 'left' from the direction options
                    self.facing = random.choice([d for d in ['right', 'up', 'down'] if d != 'left'])

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:  # Moving down
                    self.rect.y = hits[0].rect.top - self.rect.height  # Stop at the top side of the block
                    # Exclude 'down' from the direction options
                    self.facing = random.choice([d for d in ['left', 'right', 'up'] if d != 'down'])
                if self.y_change < 0:  # Moving up
                    self.rect.y = hits[0].rect.bottom  # Stop at the bottom side of the block
                    # Exclude 'up' from the direction options
                    self.facing = random.choice([d for d in ['left', 'right', 'down'] if d != 'up'])

    def animate(self):
        if self.facing == "down":
            if self.y_change == 0:
                self.image = trans_img(self.game.shaman_spritesheet.get_sprite(0, 0, 16, 16))
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= 4:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.y_change == 0:
                self.image = trans_img(self.game.shaman_spritesheet.get_sprite(16, 0, 16, 16))
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= 4:
                    self.animation_loop = 1

        if self.facing == "left":
            if self.x_change == 0:
                self.image = trans_img(self.game.shaman_spritesheet.get_sprite(32, 0, 16, 16))
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= 4:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = trans_img(self.game.shaman_spritesheet.get_sprite(48, 0, 16, 16))
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= 4:
                    self.animation_loop = 1

    def draw_health_bar(self, surface, offset):
        # Adjust health bar position using the camera offset
        health_bar_x = self.rect.x - offset.x
        health_bar_y = self.rect.y - 10 - offset.y

        # Draw health bar background (red)
        pygame.draw.rect(surface, (255, 0, 0), (health_bar_x, health_bar_y, self.health_bar_width, self.health_bar_height))

        # Calculate health percentage and draw foreground (green)
        health_width = self.health_bar_width * (self.health / self.max_health)
        pygame.draw.rect(surface, (0, 255, 0), (health_bar_x, health_bar_y, health_width, self.health_bar_height))


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        
        self.game = game
        self._layer = config.block_layer
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * config.tile_size
        self.y = y * config.tile_size
        self.width = config.tile_size
        self.height = config.tile_size

        self.image = trans_img(self.game.terrain_spritesheet.get_sprite(0, 48, 16, 16))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = config.ground_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * config.tile_size
        self.y = y * config.tile_size
        self.width = config.tile_size
        self.height = config.tile_size

        self.image = trans_img(self.game.floor_spritesheet.get_sprite(320, 208, 16, 16))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        self.game = game
        self.x = x
        self.y = y
        self.direction = direction
        self._layer = config.player_layer
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.animation_loop = 0
        self.move_speed = config.tile_size * 0.2  # Move slower (half the size of a tile)
        self.max_distance = config.tile_size * 8  # Maximum distance the attack will move
        self.travelled = 0  # Track how far the attack has moved

        self.image = trans_img(self.game.attack_spritesheet.get_sprite(0, 0, 16, 16))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()
        self.move()
        self.collide()

    def collide(self):
        # Detect collisions with walls or other objects (e.g., enemies)
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if hits:
            self.kill()  # Remove the attack if it hits a wall

        # Detect collisions with enemies
        enemy_hits = pygame.sprite.spritecollide(self, self.game.enemies, False)  # Check for collisions with enemies
        if enemy_hits:
            for enemy in enemy_hits:
                enemy.health -= 25  # Reduce health by 25 for each enemy hit
                if enemy.health <= 0:
                    enemy.kill()  # Optionally kill the enemy if health is 0 or below
                    sounds.death_sound.play()
            self.kill()  # Remove attack after hitting any enemy

    def animate(self):
        any_direction_animation = [
            trans_img(self.game.attack_spritesheet.get_sprite(0, 0, 16, 16)),
            trans_img(self.game.attack_spritesheet.get_sprite(16, 0, 16, 16))
        ]

        # Select animation frames based on the attack's direction
        if self.direction == 'up':
            self.image = any_direction_animation[math.floor(self.animation_loop)]
        elif self.direction == 'down':
            self.image = any_direction_animation[math.floor(self.animation_loop)]
        elif self.direction == 'left':
            self.image = any_direction_animation[math.floor(self.animation_loop)]
        elif self.direction == 'right':
            self.image = any_direction_animation[math.floor(self.animation_loop)]

        # Control animation speed (for more frames)
        self.animation_loop += 0.4  # slower animation speed
        if self.animation_loop >= 2:
            self.animation_loop = 0  # Reset the animation loop after 2 frames

    def move(self):
        # Move the attack sprite based on its individual direction
        if self.direction == 'up':
            self.rect.y -= self.move_speed
        elif self.direction == 'down':
            self.rect.y += self.move_speed
        elif self.direction == 'left':
            self.rect.x -= self.move_speed
        elif self.direction == 'right':
            self.rect.x += self.move_speed

        # Track the distance traveled
        self.travelled += self.move_speed

        # Remove the attack sprite once it has moved a certain distance
        if self.travelled >= self.max_distance:
            self.kill()

class Portal(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = config.player_layer  # Define layer for rendering order
        self.groups = self.game.all_sprites, self.game.portals  # Add to appropriate groups
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.is_active = False  # Start inactive

        self.x = x * config.tile_size
        self.y = y * config.tile_size
        self.width = config.tile_size
        self.height = config.tile_size

        # Sprite image and animations
        self.image = self.game.portal_spritesheet.get_sprite(0, 0, 32, 32)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.animation_frames = [
            self.game.portal_spritesheet.get_sprite(0, 0, 32, 32),
            self.game.portal_spritesheet.get_sprite(32, 0, 32, 32),
            self.game.portal_spritesheet.get_sprite(64, 0, 32, 32),
            self.game.portal_spritesheet.get_sprite(0, 32, 32, 32),
            self.game.portal_spritesheet.get_sprite(32, 32, 32, 32),
            self.game.portal_spritesheet.get_sprite(64, 32, 32, 32)
        ]
        self.animation_index = 0
        self.animation_speed = 0.2

    def update(self):
        # Only show the portal if it is active
        if not self.is_active:
            self.image.set_alpha(0)  # Make invisible
        else:
            self.image.set_alpha(255)  # Fully visible
            self.animate()

        # Check for collision with the player
        if pygame.sprite.collide_rect(self, self.game.player):
            self.on_player_collision()

    def animate(self):
        # Cycle through portal animation frames.
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.animation_frames):
            self.animation_index = 0
        self.image = self.animation_frames[int(self.animation_index)]

    def on_player_collision(self):
        if self.is_active:
            # Do what on player collision
            print("Player entered the portal! Level Complete!")
            # Check if there's a next level
            if self.game.current_level_index + 1 < len(config.tilemaps):
                self.game.current_level_index += 1  # Increment level index
                print(f"Loading next level: {self.game.current_level_index + 1}")
                self.game.new()  # Load the next level
            else:
                print("No more levels! Congratulations, you've completed the game!")
                self.game.game_complete()  # Stop the main game loop

    def check_portal_activation(portal, enemies):
        if not enemies:  # If the enemy group is empty
            portal.is_active = True
            sounds.portal_sound.play(loops = -1)  # Start playing the portal sound loop
        else:
            # When enemies are present, deactivate the portal and stop the sound
            portal.is_active = False
            sounds.portal_sound.stop()  # Stop the portal sound when the portal is inactive

