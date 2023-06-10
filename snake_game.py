import pygame
import random

# Initiaseren van le Pygame
pygame.init()

# kleuren enzo
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# grootte van het scherm
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# grootte van de spelgrid
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Snelheid ZOOOMMM
SNAKE_SPEED = 10

# lettertype
FONT = pygame.font.Font(None, 36)

# pad naar de highscore txt file
HIGH_SCORE_FILE = "highscore.txt"

# geluid effecten cool
EAT_SOUND = pygame.mixer.Sound("eat_sound.wav")

# maak de game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")

# achtergrond muziek!
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)  # loop


# snake class maken
class Snake:
    def __init__(self):
        self.direction = "right"
        self.score = 0
        self.body = [(4, 2), (3, 2), (2, 2)]  # verschillende posities voor de snake om niet meteen dood te gaan na het starten van de game
        self.food = self.generate_food() # ok ik stop wel met commetns maken
        self.food_color = RED

    def move(self):
        x, y = self.body[0]
        if self.direction == "up":
            y -= 1
        elif self.direction == "down":
            y += 1
        elif self.direction == "left":
            x -= 1
        elif self.direction == "right":
            x += 1
        self.body.insert(0, (x, y))

        if self.body[0] == self.food:
            self.score += 10
            EAT_SOUND.play()
            self.food = self.generate_food()
        else:
            self.body.pop()

    def generate_food(self):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in self.body:
                return x, y

    def check_collision(self):
        x, y = self.body[0]
        if (
            x < 0
            or x >= GRID_WIDTH
            or y < 0
            or y >= GRID_HEIGHT
            or self.body.count((x, y)) > 1
        ):
            return True
        return False

    def change_direction(self, new_direction):
        if (
            (new_direction == "up" and self.direction != "down")
            or (new_direction == "down" and self.direction != "up")
            or (new_direction == "left" and self.direction != "right")
            or (new_direction == "right" and self.direction != "left")
        ):
            self.direction = new_direction

    def draw(self, surface):
        for x, y in self.body:
            pygame.draw.rect(
                surface, YELLOW, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            )

        pygame.draw.rect(surface, GREEN, (10, 10, 150, 50))
        score_text = FONT.render(f"Score: {self.score}", True, BLACK)
        surface.blit(score_text, (20, 20))

        pygame.draw.rect(
            surface,
            self.food_color,
            (self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE),
        )


class Game:
    def __init__(self):
        self.player_name = ""
        self.snake = Snake()
        self.high_score = self.load_high_score()

    def show_main_menu(self):
        input_box = pygame.Rect(WINDOW_WIDTH // 2 - 100, 300, 200, 50)
        active = False

        while True:
            window.fill(BLACK)
            title_text = FONT.render("Snake Game", True, YELLOW)
            instruction_text = FONT.render(
                "Enter your name and press Enter to start", True, YELLOW
            )

            pygame.draw.rect(window, (255, 255, 255), input_box, 2)
            name_text = FONT.render(self.player_name, True, YELLOW)
            window.blit(name_text, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(window, (255, 255, 255), input_box, 2)
            window.blit(
                title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, 200)
            )
            window.blit(
                instruction_text,
                (WINDOW_WIDTH // 2 - instruction_text.get_width() // 2, 250),
            )

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return self.player_name
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    else:
                        if len(self.player_name) < 12:
                            self.player_name += event.unicode
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

    def show_end_screen(self):
        while True:
            window.fill(BLACK)
            end_text = FONT.render("Game Over", True, YELLOW)
            name_text = FONT.render(f"Name: {self.player_name}", True, YELLOW)
            score_text = FONT.render(f"Score: {self.snake.score}", True, YELLOW)
            high_score_text = FONT.render(
                f"High Score: {self.high_score}", True, YELLOW
            )
            restart_text = FONT.render("Press R to Restart", True, YELLOW)
            quit_text = FONT.render("Press Q to Quit", True, YELLOW)

            window.blit(
                end_text, (WINDOW_WIDTH // 2 - end_text.get_width() // 2, 200)
            )
            window.blit(
                name_text, (WINDOW_WIDTH // 2 - name_text.get_width() // 2, 300)
            )
            window.blit(
                score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, 350)
            )
            window.blit(
                high_score_text,
                (WINDOW_WIDTH // 2 - high_score_text.get_width() // 2, 400),
            )
            window.blit(
                restart_text,
                (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, 500),
            )
            window.blit(
                quit_text, (WINDOW_WIDTH // 2 - quit_text.get_width() // 2, 550)
            )

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return "restart"
                    elif event.key == pygame.K_q:
                        return "quit"
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

    def run(self):
        clock = pygame.time.Clock()
        self.player_name = self.show_main_menu()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction("up")
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction("down")
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction("left")
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction("right")

            self.snake.move()

            if self.snake.check_collision():
                if self.snake.score > self.high_score:
                    self.high_score = self.snake.score
                    self.save_high_score()
                result = self.show_end_screen()
                if result == "restart":
                    self.restart_game()
                elif result == "quit":
                    pygame.quit()
                    quit()

            window.fill(BLACK)
            self.snake.draw(window)
            pygame.display.flip()
            clock.tick(SNAKE_SPEED)

    def load_high_score(self):
        try:
            with open(HIGH_SCORE_FILE, "r") as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    def save_high_score(self):
        with open(HIGH_SCORE_FILE, "w") as file:
            file.write(str(self.high_score))

    def restart_game(self):
        self.snake = Snake()
        self.player_name = self.show_main_menu()



game = Game()
game.run()
