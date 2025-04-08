import pygame
import sys


class Button:
    def __init__(self, text, position, prog, size=(200, 50), font_size=36):
        self.text = text
        self.program = prog
        self.position = position
        self.size = size
        self.font = pygame.font.SysFont(None, font_size)
        self.color = (255, 255, 255)
        self.hover_color = (200, 200, 200)
        self.button_rect = None
        self.set_win_pos()

    def draw(self, window):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.button_rect.collidepoint(mouse_pos) else self.color

        pygame.draw.rect(window, color, self.button_rect)
        text_surf = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.button_rect.center)
        window.blit(text_surf, text_rect)

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]

    def set_win_pos(self):
        p = (self.position[0] * self.program.window.get_size()[0] - (self.size[0]/2),
             self.position[1] * self.program.window.get_size()[1] - (self.size[1]/2))
        self.button_rect = pygame.Rect(p, self.size)


class MainMenu:
    def __init__(self, window, program):
        self.window = window
        self.program = program
        self.start_button = Button("Start Game", (0.5, 0.4), self.program)
        self.settings_button = Button("Settings", (0.5, 0.5), self.program)
        self.quit_button = Button("Quit Game", (0.5, 0.6), self.program)

    def run(self):
        menu_running = True
        while menu_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.start_button.is_clicked():
                menu_running = False
                self.program.start_game()
            if self.settings_button.is_clicked():
                menu_running = False
                self.program.open_settings()
            if self.quit_button.is_clicked():
                pygame.quit()
                sys.exit()

            self.draw()
            pygame.display.update()

    def draw(self):
        self.window.fill((10, 10, 25))
        self.start_button.draw(self.window)
        self.settings_button.draw(self.window)
        self.quit_button.draw(self.window)

    def update_buttons(self):
        self.start_button.set_win_pos()
        self.quit_button.set_win_pos()
        self.settings_button.set_win_pos()


class SettingsMenu:
    def __init__(self, window, program):
        self.window = window
        self.program = program
        self.resolution_buttons = [
            Button("800x600", (0.5, 0.3), self.program),
            Button("1024x768", (0.5, 0.4), self.program),
            Button("1280x720", (0.5, 0.5), self.program),
            Button("1920x1080", (0.5, 0.6), self.program),
            Button("1536x866", (0.5, 0.7), self.program)
        ]
        self.back_button = Button("Back", (0.5, 0.8), self.program)
        self.fullscreen_button = Button("FS", (0.5, 0.2), self.program, size=(50, 50))

    def update_buttons(self):
        for but in self.resolution_buttons:
            but.set_win_pos()
        self.back_button.set_win_pos()
        self.fullscreen_button.set_win_pos()

    def run(self):
        settings_running = True
        while settings_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if self.resolution_buttons[0].is_clicked():
                self.program.set_resolution((800, 600))
                self.program.update_win_size()
            if self.resolution_buttons[1].is_clicked():
                self.program.set_resolution((1024, 768))
                self.program.update_win_size()
            if self.resolution_buttons[2].is_clicked():
                self.program.set_resolution((1280, 720))
                self.program.update_win_size()
            if self.resolution_buttons[3].is_clicked():
                self.program.set_resolution((1920, 1080))
                self.program.update_win_size()
            if self.resolution_buttons[4].is_clicked():
                self.program.set_resolution((1536, 866))
                self.program.update_win_size()
            else:
                pass

            if self.back_button.is_clicked():
                settings_running = False
                self.program.open_menu()
            if self.fullscreen_button.is_clicked():
                self.program.toggle_fullscreen()

            self.draw()
            pygame.display.update()

    def draw(self):
        self.window.fill((10, 10, 25))
        for button in self.resolution_buttons:
            button.draw(self.window)
        self.back_button.draw(self.window)
        self.fullscreen_button.draw(self.window)
