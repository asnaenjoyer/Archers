from AsteroidManager import AsteroidManager
from GameObjects import *
from Menu import *
import os


def set_window_position(x, y):
    os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"


class MainProgram:
    def __init__(self):
        set_window_position(0, 0)
        pygame.init()
        self.resolution = (800, 600)
        self.window = pygame.display.set_mode(self.resolution)
        self.fullscreen = False

        self.menu = MainMenu(self.window, self)
        self.settings_menu = SettingsMenu(self.window, self)
        self.game = MainGame(self.window, self)

        self.menu.run()

    def open_menu(self):
        self.menu.run()

    def open_settings(self):
        self.settings_menu.run()

    def start_game(self):
        self.game = MainGame(self.window, self)
        self.game.run()

    def set_resolution(self, resolution):
        self.resolution = resolution
        if self.fullscreen:
            self.window = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode(resolution)

    def update_win_size(self):
        self.menu.update_buttons()
        self.settings_menu.update_buttons()

    def toggle_fullscreen(self):
        if self.fullscreen:
            self.window = pygame.display.set_mode(self.resolution)
            self.fullscreen = False
        else:
            self.window = pygame.display.set_mode(self.resolution, pygame.FULLSCREEN)
            self.fullscreen = True
        self.update_win_size()


class MainGame:
    def __init__(self, window, prog):
        self.window = window
        self.score = 0
        self.dt = 0
        self.clock = pygame.time.Clock()

        self.keys = None

        self.player = Player("Images/Player.png", self)
        self.player_s = pygame.sprite.Group()
        self.player_s.add(self.player)

        self.asteroids = AsteroidManager(self)

        self.textlayer = TextLayer("Hello", position=(0, 0))

        self.running = True
        self.prog = prog
        self.menu_b = Button("M", (0.02, 0.1), self.prog, size=(32, 32))

    def update(self):
        self.player.update(self.keys, self.dt)
        self.asteroids.update(self.dt)
        self.check_collisions()
        self.textlayer.update_text(str(self.score))
        if self.menu_b.is_clicked():
            self.running = False
            self.prog.open_menu()

    def check_collisions(self):
        if self.player.check_collision(self.asteroids.get_asteroid_group()):
            self.asteroids.stop()
            self.player.stop()
        for b in self.player.get_bullets_group():
            b.check_collision(self.asteroids.get_asteroid_group())

    def draw(self):
        self.window.fill((10, 10, 25))
        self.player_s.draw(self.window)
        self.player.bullets.draw(self.window)
        self.asteroids.draw(self.window)
        self.textlayer.draw(self.window)
        self.menu_b.draw(self.window)
        pygame.display.update()

    def run(self):
        while self.running:
            self.keys = pygame.key.get_pressed()
            self.dt = self.clock.tick(FPS) / 1000
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.update()
            self.draw()
            if pygame.key.get_pressed()[pygame.K_r]:
                self.restart()

    def restart(self):
        self.score = 0
        self.player = Player("Images/Player.png", self)

        self.player_s = pygame.sprite.Group()
        self.player_s.add(self.player)

        self.asteroids = AsteroidManager(self)


if __name__ == "__main__":
    prog_ = MainProgram()
