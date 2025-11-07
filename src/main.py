from src.models.Player import Player
from src.config import *
import pygame
import sys
import random
import math 

def desenhar_texto(surface, text, font, x, y, color=BRANCO):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

def main():
    # Inicialização do Pygame
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO)

    # Taxa de Quadros (FPS)
    clock = pygame.time.Clock()

    try:
        fonte_placar = pygame.font.Font(None, 24) 
    except:
        fonte_placar = pygame.font.SysFont("monospace", 24)

    # Grupo de Sprites
    jogador = Player(LARGURA_TELA // 2, ALTURA_TELA // 2)
    balas = pygame.sprite.Group()
    asteroides = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(jogador)

    # Loop Principal do Jogo
    running = True
    while running:
        # Processando eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    projetil = jogador.atirar()
                    balas.add(projetil)
                    all_sprites.add(projetil)
        
        
        teclas = pygame.key.get_pressed()
        jogador.handle_input(teclas)

        # Atualização (movimentação, lógica do jogo e tals)
        all_sprites.update()

        # Renderização
        tela.fill(PRETO)
        all_sprites.draw(tela)

        texto_angulo = f"Ângulo: {int((jogador.angle + 90) % 360)}°"
        
        # Desenha o texto no canto superior esquerdo (ex: 10, 10)
        desenhar_texto(tela, texto_angulo, fonte_placar, 10, 10)

        # Atualiza a Tela
        pygame.display.flip()

        # Controla o FPS
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()