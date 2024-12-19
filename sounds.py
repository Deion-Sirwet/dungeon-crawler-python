import pygame

pygame.mixer.init()

# Initialize music
def play_music(track_path, volume = 0.05, loops = -1):
    pygame.mixer.music.load(track_path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(loops=loops)

# Initialize sound effects
def load_sound_effect(file_path, volume = 0.25):
    sound = pygame.mixer.Sound(file_path)
    sound.set_volume(volume)
    return sound

# Load intro screen sound
intro_sound = load_sound_effect("assets/sounds/gamestart.mp3")

# Initialize Attack Sound
attack_sound = load_sound_effect("assets/sounds/Shuriken.mp3")

# Load death sound
death_sound = load_sound_effect("assets/sounds/death.mp3")

# Load portal sound
portal_sound = load_sound_effect("assets/sounds/portal.mp3", volume = 0.05)

# Load game over screen sound
game_over_sound = load_sound_effect("assets/sounds/gameover.mp3", volume = 0.05)