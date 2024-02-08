import pygame
import random
import sys

# Inicialización de PyGame
pygame.init()

# Definición de constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Función para mostrar texto en la pantalla
def draw_text(surface, text, size, x, y, color):
    font = pygame.font.Font(pygame.font.match_font('arial'), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# Función para mostrar el menú principal
def show_menu(screen):
    screen.fill(BLACK)
    draw_text(screen, "Space Shooter", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, WHITE)
    draw_text(screen, "Presiona una tecla para comenzar", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, WHITE)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                waiting = False

# Función para mostrar la pantalla de game over
def show_game_over(screen, score):
    screen.fill(BLACK)
    draw_text(screen, "Game Over", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, WHITE)
    draw_text(screen, f"Puntuación: {score}", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, WHITE)
    draw_text(screen, "Presiona una tecla para intentarlo de nuevo", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4, WHITE)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                waiting = False

# Clase para la nave espacial del jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/player.png").convert_alpha()  
        self.image = pygame.transform.scale(self.image, (50, 38))  
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.centery = SCREEN_HEIGHT // 2
        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        self.speed_x = 0
        self.speed_y = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed_x = -5
        if keys[pygame.K_RIGHT]:
            self.speed_x = 5
        if keys[pygame.K_UP]:
            self.speed_y = -5
        if keys[pygame.K_DOWN]:
            self.speed_y = 5
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Clase para los enemigos
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/enemy.png").convert_alpha()  
        self.image = pygame.transform.scale(self.image, (30, 30))  
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(1, 3)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(1, 3)

    def shoot(self, all_sprites, bullets):
        bullet = EnemyBullet(self.rect.centerx, self.rect.bottom, "down")
        all_sprites.add(bullet)
        bullets.add(bullet)

# Clase para los disparos del jugador
class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10 if direction == "up" else 10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Clase para los disparos de los enemigos
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = 3  # Velocidad más lenta para las balas de los enemigos

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Función principal del juego
def main():
    # Configuración de la pantalla
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Shooter")
    clock = pygame.time.Clock()

    # Cargar la música de fondo
    pygame.mixer.music.load("assets/background_music.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(loops=-1)

    # Mostrar menú principal
    show_menu(screen)

    # Creación de la imagen de fondo
    background = pygame.image.load("assets/galaxy_background.jpg").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Creación de los sprites
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    player_bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)

    # Creación de los enemigos
    for _ in range(8):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Puntuación
    score = 0

    # Bucle principal del juego
    running = True
    while running:
        # Procesamiento de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = PlayerBullet(player.rect.centerx, player.rect.top, "up")
                    all_sprites.add(bullet)
                    player_bullets.add(bullet)

        # Actualización de los sprites
        all_sprites.update()

        # Colisiones entre balas del jugador y enemigos
        for bullet in player_bullets:
            enemy_hits = pygame.sprite.spritecollide(bullet, enemies, True)
            for enemy_hit in enemy_hits:
                bullet.kill()
                score += 1

        # Colisiones entre balas de enemigos y el jugador
        for bullet in enemy_bullets:
            player_hits = pygame.sprite.spritecollide(bullet, [player], False)
            for player_hit in player_hits:
                # Mostrar pantalla de Game Over
                show_game_over(screen, score)
                # Reiniciar el juego
                main()

        # Hacer que los enemigos disparen automáticamente
        for enemy in enemies:
            if random.random() < 0.01:  # Controla la frecuencia de disparo
                enemy.shoot(all_sprites, enemy_bullets)

        # Dibujado en pantalla
        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()

        # Control de la velocidad de fotogramas
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
