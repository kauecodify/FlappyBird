import pygame
import sys
import random

# Inicialização do Pygame
pygame.init()

# Definições Globais
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BIRD_SIZE = 30
GRAVITY = 0.5
JUMP = 8
PIPE_WIDTH = 50
PIPE_HEIGHT = 300
PIPE_GAP = 100

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configurações da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy ball")

# Carregando imagens
bird_image = pygame.Surface((BIRD_SIZE, BIRD_SIZE))
bird_image.fill(WHITE)
pipe_image = pygame.Surface((PIPE_WIDTH, PIPE_HEIGHT))
pipe_image.fill(WHITE)

# Inicialização do jogador
bird_rect = bird_image.get_rect()
bird_rect.center = (100, SCREEN_HEIGHT // 2)
bird_velocity = 0

# Lista para armazenar os canos
pipes = []

# Relógio para controlar a taxa de quadros por segundo
clock = pygame.time.Clock()

# Função para reiniciar o jogo
def reset_game():
    bird_rect.center = (100, SCREEN_HEIGHT // 2)
    bird_velocity = 0
    pipes.clear()

# Loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = -JUMP  # Configurando a velocidade vertical para cima ao pressionar espaço

    # Atualizando a posição do pássaro
    bird_velocity += GRAVITY
    bird_rect.y += bird_velocity

    # Verificando colisões com as bordas da tela
    if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT:
        reset_game()

    # Geração de canos
    if len(pipes) == 0 or pipes[-1]["x"] < SCREEN_WIDTH - 200:
        pipe_height = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)
        pipes.append({"x": SCREEN_WIDTH, "height": pipe_height})

    # Atualizando a posição dos canos
    for pipe in pipes:
        pipe["x"] -= 5

    # Verificando colisões com os canos
    for pipe in pipes:
        if (
            bird_rect.colliderect(
                pygame.Rect(pipe["x"], 0, PIPE_WIDTH, pipe["height"])
            )
            or bird_rect.colliderect(
                pygame.Rect(
                    pipe["x"], pipe["height"] + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT
                )
            )
        ):
            reset_game()

    # Removendo os canos fora da tela
    pipes = [pipe for pipe in pipes if pipe["x"] + PIPE_WIDTH > 0]

    # Desenhando na tela
    screen.fill(BLACK)
    for pipe in pipes:
        pygame.draw.rect(screen, WHITE, (pipe["x"], 0, PIPE_WIDTH, pipe["height"]))
        pygame.draw.rect(
            screen,
            WHITE,
            (
                pipe["x"],
                pipe["height"] + PIPE_GAP,
                PIPE_WIDTH,
                SCREEN_HEIGHT,
            ),
        )
    pygame.draw.ellipse(screen, WHITE, bird_rect)

    # Atualizando a tela
    pygame.display.flip()

    # Controlando a taxa de quadros por segundo
    clock.tick(30)
