import pygame
import sprites
import config
import game_button
import camera
import sounds

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((config.screen_width, config.screen_height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("Arial.TTF", 60)
        self.running = True
        self.camera = camera.Camera(config.screen_width, config.screen_height)
        pygame.display.set_caption("Void Step")


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

        self.game_over_bg = pygame.image.load('assets/game_over.jpg')
        self.game_over_bg = pygame.transform.scale(self.game_over_bg, (config.screen_width, config.screen_height))

        # Game complete background
        self.game_complete_bg = pygame.image.load('assets/game_complete.jpg')
        self.game_complete_bg = pygame.transform.scale(self.game_complete_bg, (config.screen_width, config.screen_height))

        # Create a button for toggling music
        self.music_button = game_button.Button(10, 10, 100, 50, config.black, config.white, "ToggleMusic", 16)
        self.music_playing = True

        # Pause button
        self.pause_button = game_button.Button(690, 10, 100, 50, config.black, config.white, "Pause", 16)
        self.game_paused = False

        # Default attack direction
        self.attack_direction = 'down'

        # Attack timer
        self.last_attack_time = 0  # Initialize the last attack time

        # Current/Start level
        self.current_level_index = 0

    def create_tilemap(self):
        tilemap = config.tilemaps[self.current_level_index]
        for y, row in enumerate(tilemap):
            for x, column in enumerate(row):
                sprites.Ground(self, x, y)
                if column == "B":
                    sprites.Block(self, x, y)
                if column == "P":
                    self.player = sprites.Player(self, x, y)
                if column == "E":
                    sprites.Enemy(self, x, y)
                if column == "L":
                    self.portal = sprites.Portal(self, x, y)

    def new(self):
        # Calculate the map size
        self.map_width = len(config.tilemaps[self.current_level_index][0]) * config.tile_size
        self.map_height = len(config.tilemaps[self.current_level_index]) * config.tile_size

        # Initialize the camera
        self.camera = camera.Camera(self.map_width, self.map_height)

        # Reset vars
        self.game_over_sound_played = False
        self.game_complete_sound_played = False
        self.playing = True

        # Sprite groups
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.portals = pygame.sprite.LayeredUpdates()

        # Initialize Game Music
        if self.music_playing:
            sounds.play_music("assets/sounds/background_music.mp3")

        # Draw tilemap
        self.create_tilemap()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.player = False
                self.running = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                # Update attack direction based on arrow key presses
                # if event.key == pygame.K_UP:
                #     self.attack_direction = 'up'
                # elif event.key == pygame.K_DOWN:
                #     self.attack_direction = 'down'
                # elif event.key == pygame.K_LEFT:
                #     self.attack_direction = 'left'
                # elif event.key == pygame.K_RIGHT:
                #     self.attack_direction = 'right'

                # Set the attack direction to the player's current facing direction
                if event.key == pygame.K_SPACE:
                    direction = self.player.facing  # Use the player's facing direction

                    current_time = pygame.time.get_ticks()  # Get current time in milliseconds
                    if current_time - self.last_attack_time > 200:  # cooldown (adjust as needed)
                        self.last_attack_time = current_time

                        # Launch an attack in the direction the player is facing
                        if direction == 'up':
                            sprites.Attack(self, self.player.rect.x, self.player.rect.y - 16, direction)
                            sounds.attack_sound.play()
                        elif direction == 'down':
                            sprites.Attack(self, self.player.rect.x, self.player.rect.y + 16, direction)
                            sounds.attack_sound.play()
                        elif direction == 'left':
                            sprites.Attack(self, self.player.rect.x - 16, self.player.rect.y, direction)
                            sounds.attack_sound.play()
                        elif direction == 'right':
                            sprites.Attack(self, self.player.rect.x + 16, self.player.rect.y, direction)
                            sounds.attack_sound.play()

            # Get mouse input for music button
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            # Check if the music button is pressed
            if self.music_button.is_pressed(mouse_pos, mouse_pressed):
                if self.music_playing:
                    pygame.mixer.music.stop()
                    self.music_playing = False
                else:
                    pygame.mixer.music.play()
                    self.music_playing = True

            # Check if pause button is pressed
            if self.pause_button.is_pressed(mouse_pos, mouse_pressed):
                self.game_paused = not self.game_paused  # Toggle the pause state

    def update(self):
        # Game loop updates
        self.all_sprites.update()

        # Game events and updates
        sprites.Portal.check_portal_activation(self.portal, self.enemies)

        # Update camera on player
        self.camera.center_on_player(self.player)  # Or use box_camera(self.player)


    def draw(self):
        # Clear the screen
        self.screen.fill(config.black)

        # Draw all sprites with the camera offset
        for sprite in self.all_sprites:
            offset_pos = sprite.rect.topleft - self.camera.offset
            self.screen.blit(sprite.image, offset_pos)

        # Draw health bars for each enemy (apply camera offset)
        for enemy in self.enemies:
            enemy.draw_health_bar(self.screen, self.camera.offset)

        # Draw the toggle music button
        self.screen.blit(self.music_button.image, self.music_button.rect)

        # Draw the pause button
        self.screen.blit(self.pause_button.image, self.pause_button.rect)

        # Limit FPS and update the display
        self.clock.tick(config.fps)
        pygame.display.update()

    def main(self):
        # Game loop
        while self.playing:
            self.events()  # Check for pause button click

            # If the game is paused
            if self.game_paused:
                # Create a semi-transparent grey overlay (RGBA with alpha set to 5 for opacity)
                overlay = pygame.Surface((config.screen_width, config.screen_height))
                overlay.set_alpha(5)  # Set opacity (0 is fully transparent, 255 is fully opaque)
                overlay.fill((128, 128, 128))  # Fill the overlay with grey color (RGB)

                # Draw the overlay
                self.screen.blit(overlay, (0, 0))

                # Render the "Paused" text in the center of the screen
                paused_text = self.font.render("Paused", True, (255, 255, 255))  # White text
                paused_text_rect = paused_text.get_rect(center=(config.screen_width // 2, config.screen_height // 2))

                # Draw the "Paused" text
                self.screen.blit(paused_text, paused_text_rect)

                # Draw the pause button
                self.screen.blit(self.pause_button.image, self.pause_button.rect)

                pygame.display.update()  # Update display to show pause screen

                # Pause the music when the game is paused
                pygame.mixer.music.pause()

                continue  # Skip the rest of the loop (no updates, no drawing)

            # Normal game updates (only happens when not paused)
            self.update()
            self.draw()

            # If the game is not paused, resume the music if it's not already playing
            if not self.game_paused:
                pygame.mixer.music.unpause()

    def game_over(self):
        # text = self.font.render('Game Over', True, config.white)
        # text_rect = text.get_rect(x = 325, y = 200)

        restart_button = game_button.Button(360, 350, 100, 50, config.black, config.white, 'Restart', 32)

        for sprite in self.all_sprites:
            sprite.kill()

        # Add a flag to check if the game over sound has been played
        self.game_over_sound_played = False

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            # Pause background music and play game over music
            if not self.game_over_sound_played:
                pygame.mixer.music.stop()
                sounds.game_over_sound.play()
                self.game_over_sound_played = True

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            self.screen.blit(self.game_over_bg, (0, 0))
            # self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(config.fps)
            pygame.display.update()


    def intro_screen(self):
        intro = True

        # Call intro sound
        sounds.intro_sound.play()

        title = self.font.render('Void Step', True, config.white)
        title_rect = title.get_rect(x = 280, y = 200)

        play_button = game_button.Button(360, 350, 100, 50, config.black, config.white, 'Play', 32)

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

    def game_complete(self):
        # Clear all active sprites
        for sprite in self.all_sprites:
            sprite.kill()

        # Game complete background (ensure `self.game_complete_bg` exists and loads correctly)
        self.screen.blit(self.game_complete_bg, (0, 0))

        # Render "Game Complete!" message
        message = self.font.render("Game Complete!", True, (255, 255, 255))  # White text
        message_rect = message.get_rect(x = 200, y = 200)
        self.screen.blit(message, message_rect)

        # Init game complete var
        self.game_complete_sound_played = False

        # Create a button for replaying the game
        replay_game = game_button.Button(325, 350, 200, 50, config.black, config.white, 'Play Again', 32)

        # Main loop for the "Game Complete" screen
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()

            # Pause music and play game is complete sound
            if not self.game_complete_sound_played:
                pygame.mixer.music.stop()
                sounds.portal_sound.stop()
                # sounds.game_complete_sound.play()
                self.game_complete_sound_played = True

            # Get mouse input
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            # Check if the "Play Again" button is pressed
            if replay_game.is_pressed(mouse_pos, mouse_pressed):
                self.current_level_index = 0  # Reset to the first level
                self.new()  # Reset the game state
                return  # Exit the `game_complete` method and go back to the main game loop

            # Redraw the screen
            self.screen.blit(self.game_complete_bg, (0, 0))  # Redraw the background
            self.screen.blit(message, message_rect)  # Redraw the "Game Complete!" text
            self.screen.blit(replay_game.image, replay_game.rect)  # Redraw the button

            # Update the display
            pygame.display.update()
            self.clock.tick(config.fps)
