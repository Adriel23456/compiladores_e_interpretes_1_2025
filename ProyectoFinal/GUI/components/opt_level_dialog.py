import pygame
from GUI.components.button import Button

class OptLevelDialog:
    def __init__(self, screen):
        self.screen = screen
        self.rect = pygame.Rect(0, 0, 400, 200)
        self.rect.center = screen.get_rect().center
        self.selected = None

        # Botones con texto explícito
        labels = ["O0", "O1", "O2", "O3"]
        btn_w, btn_h, gap = 70, 40, 20
        start_x = self.rect.centerx - (2 * btn_w + 1.5 * gap)
        y = self.rect.centery + 20

        self.buttons = []
        for i, label in enumerate(labels):
            rect = pygame.Rect(start_x + i * (btn_w + gap), y, btn_w, btn_h)
            self.buttons.append(Button(rect, label, fixed_width=btn_w))

    def handle_events(self, events):
        for ev in events:
            for i, b in enumerate(self.buttons):
                if b.handle_event(ev):
                    self.selected = i  # nivel seleccionado (0 = O0, ..., 3 = O3)

    def render(self):
        pygame.draw.rect(self.screen, (240, 240, 240), self.rect)
        pygame.draw.rect(self.screen, (100, 100, 100), self.rect, 2)

        title_font = pygame.font.SysFont("sans", 20)
        text = title_font.render("Seleccione nivel de optimización:", True, (0, 0, 0))
        self.screen.blit(text, (self.rect.centerx - text.get_width() // 2, self.rect.top + 25))

        for b in self.buttons:
            b.render(self.screen)
