import pygame
import random

# Initialize Pygame
pygame.init()

# Play background music
pygame.mixer.init()
pygame.mixer.music.load("catchy_music.mp3")  # Place your catchy music file in the same directory
pygame.mixer.music.play(-1)  # Loop indefinitely

# Window settings
width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

# Player class
class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.vel = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, win):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # Draw frog body (ellipse)
        body_rect = pygame.Rect(self.x, self.y + self.height//4, self.width, self.height//2)
        pygame.draw.ellipse(win, (0, 200, 0), body_rect)  # dark green body
        # Draw frog head (circle)
        head_center = (self.x + self.width//2, self.y + self.height//4)
        pygame.draw.circle(win, (0, 255, 0), head_center, self.width//4)
        # Draw eyes (white circles)
        eye_radius = self.width//10
        left_eye = (self.x + self.width//3, self.y + self.height//6)
        right_eye = (self.x + 2*self.width//3, self.y + self.height//6)
        pygame.draw.circle(win, (255,255,255), left_eye, eye_radius)
        pygame.draw.circle(win, (255,255,255), right_eye, eye_radius)
        # Draw pupils (black)
        pupil_radius = self.width//20
        pygame.draw.circle(win, (0,0,0), left_eye, pupil_radius)
        pygame.draw.circle(win, (0,0,0), right_eye, pupil_radius)

    def move(self, obstacles):
        keys = pygame.key.get_pressed()
        old_x, old_y = self.x, self.y
        if keys[pygame.K_LEFT]:
            self.x -= self.vel
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
        if keys[pygame.K_UP]:
            self.y -= self.vel
        if keys[pygame.K_DOWN]:
            self.y += self.vel
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        for obs in obstacles:
            if self.rect.colliderect(obs):
                self.x, self.y = old_x, old_y
                self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
                break

    def draw_tongue(self, win):
        # Draw tongue stretching out from frog's mouth
        mouth_x = self.x + self.width//2
        mouth_y = self.y + self.height//4 + self.width//8
        pygame.draw.rect(win, (255, 0, 100), (mouth_x-5, mouth_y, 10, -80))  # tongue

    def draw_poop(self, win):
        # Draw poop below the frog
        poop_rect = pygame.Rect(self.x + self.width//2 - 10, self.y + self.height, 20, 15)
        pygame.draw.ellipse(win, (139, 69, 19), poop_rect)

class Fly():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 16, 16)
    def draw(self, win):
        # Draw a simple fly (circle with wings)
        pygame.draw.circle(win, (50, 50, 50), (self.x+8, self.y+8), 8)
        pygame.draw.ellipse(win, (200, 200, 200), (self.x, self.y+2, 8, 6))
        pygame.draw.ellipse(win, (200, 200, 200), (self.x+8, self.y+2, 8, 6))

class Bullet():
    def __init__(self, x, y, width, height, color, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.y += self.speed
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, win):
        # Draw golden bullet body (ellipse)
        body_rect = pygame.Rect(self.x, self.y + self.height//6, self.width, self.height*2//3)
        pygame.draw.ellipse(win, (212, 175, 55), body_rect)  # golden color
        # Draw bullet tip (triangle)
        tip_points = [
            (self.x + self.width//2, self.y),  # top center
            (self.x, self.y + self.height//6),  # bottom left
            (self.x + self.width, self.y + self.height//6)  # bottom right
        ]
        pygame.draw.polygon(win, (255, 223, 90), tip_points)  # lighter gold tip
        # Draw outline for effect
        pygame.draw.ellipse(win, (160, 130, 40), body_rect, 2)
        pygame.draw.polygon(win, (160, 130, 40), tip_points, 2)

def draw_heart(win, x, y, size, color):
    # Draw a heart shape using two circles and a triangle
    radius = size // 2
    # Left circle
    pygame.draw.circle(win, color, (x + radius//2, y + radius//2), radius//2)
    # Right circle
    pygame.draw.circle(win, color, (x + radius + radius//2, y + radius//2), radius//2)
    # Bottom triangle
    points = [
        (x, y + radius//2),
        (x + size, y + radius//2),
        (x + size//2, y + size)
    ]
    pygame.draw.polygon(win, color, points)

def draw_pond_background(win, plants):
    # Draw blue pond background
    win.fill((30, 144, 255))
    # Draw some water ripples
    for i in range(5):
        pygame.draw.ellipse(win, (135, 206, 250), (50 + i*80, 350 + (i%2)*20, 100, 30), 2)
    # Draw lily pads (plants)
    for plant in plants:
        pygame.draw.ellipse(win, (34, 139, 34), plant)
        pygame.draw.ellipse(win, (0, 100, 0), plant, 2)

# Redraw the window
def redrawWindow(win, player, bullets, score, lives, fly=None):
    win.fill((30, 144, 255))
    # Draw hearts (lives)
    heart_color = (255, 0, 0)
    for i in range(lives):
        draw_heart(win, 10 + i*35, 10, 30, heart_color)
    # Draw bullets
    for bullet in bullets:
        bullet.draw(win)
    # Draw fly
    if fly:
        fly.draw(win)
    # Draw player
    player.draw(win)
    # Draw score
    font = pygame.font.SysFont('Arial', 30)
    score_text = font.render(f"Score: {score}", True, (255,255,255))
    win.blit(score_text, (10, 50))
    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()
    player = Player(200, 400, 60, 60, (0, 255, 0))
    score = 0
    lives = 3
    bullets = []
    bullet_timer = 0
    # Spawn the first fly
    fly = Fly(random.randint(0, 500-16), random.randint(0, 500-16))

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        player.move([])

        # Spawn bullets at intervals
        bullet_timer += 1
        if bullet_timer > 30:
            bullet_x = random.randint(0, width-20)
            bullets.append(Bullet(bullet_x, 0, 20, 20, (255,0,0), 7))
            bullet_timer = 0

        # Move bullets and check for collision
        for bullet in bullets[:]:
            bullet.move()
            if bullet.rect.colliderect(player.rect):
                bullets.remove(bullet)
                lives -= 1
                if lives == 0:
                    run = False
            elif bullet.y > height:
                bullets.remove(bullet)

        # Check collision with fly
        if player.rect.colliderect(fly.rect):
            score += 1
            fly = Fly(random.randint(0, 500-16), random.randint(0, 500-16))

        redrawWindow(win, player, bullets, score, lives, fly=fly)

    pygame.quit()
    print(f"Game Over! Final Score: {score}")

main()