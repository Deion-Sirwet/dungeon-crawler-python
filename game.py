import pygame
import sprites
import config
import game_button
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.screen_width, config.screen_height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("Arial.TTF", 32)
        self.running = True

        # Loading spritesheets
        self.character_spritesheet = sprites.Spritesheet('assets/character/SpriteSheet.png')
        self.terrain_spritesheet = sprites.Spritesheet('assets/terrain/TilesetDungeon.png')
        self.floor_spritesheet = sprites.Spritesheet('assets/terrain/TilesetInteriorFloor.png')
        self.shaman_spritesheet = sprites.Spritesheet('assets/enemies/shaman.png')
        self.attack_spritesheet = sprites.Spritesheet('assets/throwable/Shuriken.png')
        self.portal_spritesheet = sprites.Spritesheet('assets/portal.png')

        # Loading start and end game background
        self.intro_background = pygame.image.load('assets/background.jpg')
        self.intro_background = pygame.transform.scale(self.intro_background, (config.screen_width, config.screen_height))

        # Default attack direction
        self.attack_direction = 'down'

        # Attack timer
        self.last_attack_time = 0  # Initialize the last attack time

        # Set default portal spawn
        self.portal_spawned = False

    def create_tilemap(self):
        for y, row in enumerate(config.tilemap):
            for x, column in enumerate(row):
                sprites.Ground(self, x, y)
                if column == "B":
                    sprites.Block(self, x, y)
                if column == "P":
                    self.player = sprites.Player(self, x, y)
                if column == "E":
                    sprites.Enemy(self, x, y)

    def new(self):
        # New game start
        self.playing = True

        # Reset portal
        self.portal_spawned = False

        # Sprite groups
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.portals = pygame.sprite.LayeredUpdates()

        # Draw tilemap
        self.create_tilemap()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.player = False
                self.running = False
                pygame.quit()

            # Update attack direction based on arrow key presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.attack_direction = 'up'
                elif event.key == pygame.K_DOWN:
                    self.attack_direction = 'down'
                elif event.key == pygame.K_LEFT:
                    self.attack_direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    self.attack_direction = 'right'

                # Set the attack direction to the player's current facing direction
                if event.key == pygame.K_SPACE:
                    self.attack_direction = self.player.facing  # Use the player's facing direction

                    current_time = pygame.time.get_ticks()  # Get current time in milliseconds
                    if current_time - self.last_attack_time > 200:  # cooldown (adjust as needed)
                        self.last_attack_time = current_time

                        # Launch an attack in the direction the player is facing
                        if self.attack_direction == 'up':
                            sprites.Attack(self, self.player.rect.x, self.player.rect.y - 16, self.attack_direction)
                        elif self.attack_direction == 'down':
                            sprites.Attack(self, self.player.rect.x, self.player.rect.y + 16, self.attack_direction)
                        elif self.attack_direction == 'left':
                            sprites.Attack(self, self.player.rect.x - 16, self.player.rect.y, self.attack_direction)
                        elif self.attack_direction == 'right':
                            sprites.Attack(self, self.player.rect.x + 16, self.player.rect.y, self.attack_direction)

    def update(self):
        # Game loop updates
        self.all_sprites.update()

        # Check if the portal needs to be spawned
        sprites.Portal.check_and_spawn(self)

    def draw(self):
        # Draw game loop
        self.screen.fill(config.black)

        # Draw all sprites
        self.all_sprites.draw(self.screen)

        # Draw health bars for each enemy
        for enemy in self.enemies:
            enemy.draw_health_bar(self.screen)
        self.clock.tick(config.fps)
        pygame.display.update()

    def main(self):
        # Game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def game_over(self):
        text = self.font.render('Game Over', True, config.white)
        text_rect = text.get_rect(x = 320, y = 200)

        restart_button = game_button.Button(360, 250, 100, 50, config.black, config.white, 'Restart', 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(config.fps)
            pygame.display.update()


    def intro_screen(self):
        intro = True

        title = self.font.render('Dungeon Crawler', True, config.white)
        title_rect = title.get_rect(x = 290, y = 200)

        play_button = game_button.Button(360, 250, 100, 50, config.black, config.white, 'Play', 32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            
            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(config.fps)
            pygame.display.update()
