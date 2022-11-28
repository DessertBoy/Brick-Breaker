import pygame
import random


pygame.init()


"""Colors"""
white = [255, 255, 255]
red = [204, 0, 0]
green = [0, 204, 0]
blue = [0, 0, 255]
black = [0, 0, 0]
orange = [255, 125, 0]
pink = [255, 204, 229]

"""Song"""
pygame.mixer.Channel(0).play(pygame.mixer.Sound('background_song.wav'), -1)

"""Dimensions"""
width = 800
height = 600

"""Surfaces"""
brick_surface_width = width
brick_surface_height = int(height / 2)
screen = pygame.display.set_mode([width, height])
background = pygame.image.load('background.png')

"""Timing"""
clock = pygame.time.Clock()
FPS = 30

"""Game text"""

"""Fonts"""
"""Search up fonts that pygame has available"""
# print(pygame.font.get_fonts())

small_font = pygame.font.SysFont('bahnschrift', 25, True)
medium_font = pygame.font.SysFont('bahnschrift', 35, True)
large_font = pygame.font.SysFont('bahnschrift', 50, True)

"""CLASSESS"""

class Bricks():

    def __init__(self):
        self.width = 80
        self.height = int(self.width / 2)
        self.bricks = []
        self.brick_seperation = 10
        self.base_color = [red, green, black, blue, orange, pink]
        self.border_color = [orange, blue, pink, green, red, black]

        """Creating bricks"""
        for x in range(0, brick_surface_width, self.width + self.brick_seperation):
            for y in range(0, brick_surface_height, self.height + self.brick_seperation):
                rect = pygame.Rect(x, y, self.width, self.height)
                self.bricks.append(rect)

    def draw_brick(self, screen):
        """Drawing bricks onto screen"""
        for brick in self.bricks:
            pygame.draw.rect(screen, orange, brick)
            pygame.draw.rect(screen, black, brick, 3)

    def won(self):
        """If all bricks are removed from self.bricks then the game has been won"""
        if len(self.bricks) == 0:
            game_won()


class Ball():
    def __init__(self, x, y):
        self.color = red
        self.radius = 5
        self.x = x
        self.y = y
        self.x_speed = 5
        self.y_speed = 5
        self.speed_max = 6
        self.start = False
        self.lose = False
        self.instructions = True
        self.cordinates = [self.x, self.y]

    def draw_ball(self, bricks, paddle):
        """Collision thresh is used to detect when an object is 5 pixels away from being detected by another 
        object. This is used for ball, brick, and paddle detection. Sometimes coliderect doesn't always work
        well. At least this way whenever we get object 1's x or y minus object's 2 x or y, a detection will occur
        when they are 5 pixels away. """
        collision_thresh = 5

        """Receive keys that are being pressed"""
        key = pygame.key.get_pressed()

        """Receives paddle direction"""
        direction = paddle[1]

        if key[pygame.K_SPACE]:
            self.start = True
            self.instructions = False

        if self.instructions:
            message_to_screen("Press Space to Start", pink, 200, 'small')
            message_to_screen("Use Left and Right Arrow Key to Move", pink, 250, 'small')


        """Once the game has begun, speed gets added to the ball cordinates, making it move"""
        if self.start:
            self.cordinates[0] += self.x_speed
            self.cordinates[1] += self.y_speed

        """Draws the outer layer for the ball"""
        pygame.draw.circle(screen, green, (self.cordinates[0], self.cordinates[1]), 10)

        """Creating a ball variable so we can access rectangle dimension that pygame.draw.circle returns"""
        self.ball = pygame.draw.circle(screen, self.color, (self.cordinates[0], self.cordinates[1]), self.radius)


        """Iterate through every brick in bricks to check if ball and brick are colliding."""
        for brick in bricks.bricks:
            if self.ball.colliderect(brick):
                pygame.mixer.music.load('brick_hit.wav')
                pygame.mixer.music.play()

                """If a collision is detected, ball changes direction"""
                if abs(self.ball.bottom - brick.top) <= collision_thresh and self.y_speed > 0:
                    self.y_speed = -self.y_speed
                # check if collision was from below
                if abs(self.ball.top - brick.bottom) <= collision_thresh and self.y_speed < 0:
                    self.y_speed = -self.y_speed
                # check if collision was from left
                if abs(self.ball.right - brick.left) <= collision_thresh and self.x_speed > 0:
                    self.x_speed = -self.x_speed
                # check if collision was from right
                if abs(self.ball.left - brick.right) <= collision_thresh and self.x_speed < 0:
                    self.x_speed = -self.x_speed

                """If collision between ball and brick is detected, brick gets removed from brick list"""
                bricks.bricks.remove(brick)


        """Detection between ball and paddle rect"""
        if self.ball.colliderect(paddle[0]):
            """If ball and paddle collide the balls y changes direction and the speed of the direction of the paddle is added to x"""
            if abs(self.ball.bottom - paddle[0].top) <= collision_thresh and self.y_speed > 0:
                self.y_speed = -self.y_speed
                self.x_speed += direction
                if self.x_speed >= self.speed_max:
                    self.x_speed = self.speed_max
                elif self.x_speed <= 0 and self.x_speed <= -self.speed_max:
                    self.x_speed = -self.speed_max
            else:
                self.x_speed = -self.x_speed
                

        if self.ball.left < 1 or self.ball.right > width - 1:
            self.x_speed = -self.x_speed

        if self.ball.top < 0 or self.ball.bottom > height:
            self.y_speed = -self.y_speed


        """If the ball falls below the screen height then the player has lost""" 
        if self.ball.y > height:
            lose_game()


class Paddle():
    def __init__(self):
        self.width = 100
        self.height = 20
        self.color = pink
        self.border_color = black
        self.x = int((width / 2) - (self.width / 2))
        self.y = int(height / 2 + 100)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = 0
        self.speed = 10

    def move(self):
        self.direction = 0
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT] and self.rect.left >= 0:
            self.rect.x -= self.speed
            self.direction = -1
        if key[pygame.K_RIGHT] and self.rect.right <= width:
            self.rect.x += self.speed
            self.direction = 1
        else:
            direction = 0

        return [self.rect, self.direction]

    def draw_paddle(self):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 5)

"""Functions"""

def game_intro():
    """Intro to the game. Allows you to quit or continue"""
    intro = True

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        screen.blit(background,[0,0])

        message_to_screen("Welcome to Brick Breaker", pink, -150, "large")
        message_to_screen('Press C to Continue or Press Q to Quit', pink, -50, "medium")
        message_to_screen('A GAME MADE BY CBASS', pink, 0, 'small')

        pygame.display.flip()
        clock.tick(FPS)


def text_object(text, color, size):
    """Function to choose the size and color of the font. Font is rendered here to be allowed to display on screen.
    The rect of the font is also returned."""
    if size == 'small':
        screen_text = small_font.render(text, True, color)
    elif size == 'medium':
        screen_text = medium_font.render(text, True, color)
    elif size == 'large':
        screen_text = large_font.render(text, True, color)
    elif size == 'border':
        screen_text = large_border_font.render(text, True, color)
    return screen_text, screen_text.get_rect()


def message_to_screen(msg, color, y_displacement=0, size='small'):
    """Function to blit the text onto the screen"""
    textSurf, textRect = text_object(msg, color, size)
    textRect.center = (width / 2), (height / 2) + y_displacement
    screen.blit(textSurf, textRect)


def lose_game():
    lost = True

    message_to_screen("YOU LOST", white, 50, 'large')
    message_to_screen("Press R to Restart", pink, 200, 'medium')
    message_to_screen("Press Q to Quit", pink, 250, 'medium')
    clock.tick(5)

    while lost:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    lost = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        pygame.display.flip()

    brick_breaker()


def pause_menu():
    pause = True
    message_to_screen('Press C to Continue or Q to Quit', pink, 50, 'medium')
    pygame.display.flip()
    clock.tick(5)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    pause = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()


def game_won():
    won = True
    message_to_screen('CONGRATULATIONS YOU WON', white, 50, 'medium')
    message_to_screen("Press R to Restart", pink, 200, 'medium')
    message_to_screen("Press Q to Quit", pink, 250, 'medium')
    pygame.display.flip()
    clock.tick(5)

    while won:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    won = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

    brick_breaker()


"""Generator"""
def brick_breaker():

    bricks = Bricks()
    paddle = Paddle()
    ball = Ball((paddle.x + (paddle.width / 2)), (paddle.y - (paddle.height / 2)))

    on = True

    while on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on = False

        key = pygame.key.get_pressed()

        if key[pygame.K_p]:
            pause_menu()

        screen.blit(background, [0, 0])

        bricks.draw_brick(screen)
        paddle.draw_paddle()
        ball.draw_ball(bricks, paddle.move())
        bricks.won()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    quit()


game_intro()
brick_breaker()
