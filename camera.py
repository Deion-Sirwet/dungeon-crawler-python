import pygame

class Camera:
    def __init__(self, screen_width, screen_height):
        # Display dimensions
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2(0, 0)

        # Centering variables
        self.half_w = screen_width // 2
        self.half_h = screen_height // 2

        # Optional camera box (adjustable for delayed movement)
        self.camera_borders = {'left': 300, 'right': 300, 'top': 150, 'bottom': 150}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = screen_width - (self.camera_borders['left'] + self.camera_borders['right'])
        h = screen_height - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l, t, w, h)

    def center_on_player(self, player):
        """Centers the camera directly on the player."""
        self.offset.x = player.rect.centerx - self.half_w
        self.offset.y = player.rect.centery - self.half_h

    def box_camera(self, player):
        """Uses a camera box to adjust offset only when the player moves outside it."""
        if player.rect.left < self.camera_rect.left:
            self.camera_rect.left = player.rect.left
        if player.rect.right > self.camera_rect.right:
            self.camera_rect.right = player.rect.right
        if player.rect.top < self.camera_rect.top:
            self.camera_rect.top = player.rect.top
        if player.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = player.rect.bottom

        # Update the offset based on the camera_rect position
        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']
