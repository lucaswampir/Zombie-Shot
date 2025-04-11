import pygame
import random
import os

# Inicializace
pygame.init()
#barvy
red=(183, 0, 0)
green=(91, 127, 0)
darkred=(132, 11, 27)
black=(0, 0, 0)

pygame.font.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Shot")
pygame.display.set_icon(pygame.image.load("zombie_icon.png"))
clock = pygame.time.Clock()

pismo=pygame.font.Font("HERMES.ttf",65,)

# Inicializace mixeru
pygame.mixer.init()

# Načtení hudby
pygame.mixer.music.load("anxiety.wav")

# Přehrávání hudby na pozadí stále dokola
pygame.mixer.music.play(-1)  # Argument -1 znamená nekonečné opakování


# Načtení obrázků
background = pygame.image.load("background.png")
zombie_images = [
    pygame.image.load("zombie1.png"),
    pygame.image.load("zombie2.png"),
    pygame.image.load("zombie3.png"),
]

# Nastavení velikosti
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
zombie_images = [pygame.transform.scale(img, (100, 150)) for img in zombie_images]

# Třída zombie
class Zombie:
    def __init__(self):
        self.image = random.choice(zombie_images)
        self.x = random.randint(100, WIDTH - 100)
        self.y = random.randint(300, HEIGHT - 150)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.spawn_time = pygame.time.get_ticks()

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

# Hlavní proměnné
zombies = []

# Kurzor - kříž
pygame.mouse.set_visible(False)
crosshair_img = pygame.image.load("crosshair.png")
crosshair_img = pygame.transform.scale(crosshair_img, (64, 64))  # uprav podle velikosti

spawn_delay = 1000  # ms
last_spawn = pygame.time.get_ticks()
score = 0
font = pygame.font.SysFont("verdana", 30)

# Herní smyčka
running = True
while running:



    # Initialize pygame mixer
    pygame.mixer.init()

    # Load sound effect
    click_sound = pygame.mixer.Sound("gun.wav")

    screen.blit(background, (0, 0))

    pismofont = pismo.render("Zombie Shot!", True, darkred,black )
    fontt = pismofont.get_rect()
    fontt.center = (WIDTH // 2, 32)

    current_time = pygame.time.get_ticks()

    # Spawn zombíka
    if current_time - last_spawn > spawn_delay:
        zombies.append(Zombie())
        last_spawn = current_time

    # Zobrazit zombíky a odstranit ty, co tam jsou moc dlouho
    for zombie in zombies[:]:
        if current_time - zombie.spawn_time > 1500:  # zmizí po 1,5s
            zombies.remove(zombie)
        else:
            zombie.draw(screen)

    # Události
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Kliknutí myši
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_sound.play()
            mx, my = pygame.mouse.get_pos()
            for zombie in zombies[:]:
                if zombie.rect.collidepoint(mx, my):
                    zombies.remove(zombie)
                    score += 1

    screen.blit(pismofont, fontt)
    # Zobrazit skóre
    score_text = font.render(f"Score:{score}", True, (green))
    screen.blit(score_text, (10, 10))



    # Kreslení zaměřovače
    mx, my = pygame.mouse.get_pos()
    screen.blit(crosshair_img, (mx - 16, my - 16))  # centrování obrázku


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
