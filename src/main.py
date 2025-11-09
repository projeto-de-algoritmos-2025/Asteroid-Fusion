from models.Player import Player
from models.Asteroid import Asteroid
from config import *
from time import sleep
from algorithm.closest_pair import closest_pair
import pygame
import random

def desenhar_placar(surface, jogador, score, font, life_icon_img, game_over, tela, fonte_placar):
    texto_angulo = f"Ângulo: {int((jogador.angle + PROPULSION_OFFSET) % 360)}°"       
    desenhar_texto(tela, texto_angulo, fonte_placar, 10, 10)
    texto_score = f"Pontos: {score}"
    desenhar_texto(tela, texto_score, fonte_placar, LARGURA_TELA - 200, 15)
    desenhar_texto(tela, "Vidas:", fonte_placar, LARGURA_TELA - 200, 50)
    # icone pra cada vida
    start_x = LARGURA_TELA - 140
    y = 45 # Na mesma linha do rótulo "Vidas:"
    for i in range(jogador.vidas):
        x = start_x + (i * (LIFE_ICON_SIZE + 5)) # 5 pixels de espaçamento
        tela.blit(life_icon_img, (x, y))

    if game_over:
        texto_fim = "GAME OVER"
        # Fonte um pouco maior para Game Over
        fonte_game_over = pygame.font.Font(None, 64) 
        desenhar_texto(tela, texto_fim, fonte_game_over, LARGURA_TELA // 2 - 150, ALTURA_TELA // 2 - 32, VERMELHO_ALERTA)

def desenhar_texto(surface, text, font, x, y, color=BRANCO):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

def collision_detection(jogador, asteroides, balas, all_sprites, game_over, score, vulnerable):
    # Colisão: Bala vs. Asteroide 
    # True, False: Destrói a bala, mas não o asteroide para processar o split primeiro.
    colisoes_bala_ast = pygame.sprite.groupcollide(
        balas, asteroides, True, False, 
        pygame.sprite.collide_circle
    )

    # As chaves são as Balas que atingiram algo. Os valores são as listas de Asteroides atingidos.
    for bala_atingida, asteroides_atingidos in colisoes_bala_ast.items(): 
        # Itera sobre cada Asteroide atingido por esta bala
        for asteroide_atingido in asteroides_atingidos:
            if asteroide_atingido.nivel == "Pequeno":
                score += PONTUACAO_PEQUENO
            elif asteroide_atingido.nivel == "Medio":
                score += PONTUACAO_MEDIO
            elif asteroide_atingido.nivel == "Grande":
                score += PONTUACAO_GRANDE
                
            # Lógica de quebra (split)
            novos = asteroide_atingido.split()
            if novos:
                asteroides.add(novos)
                all_sprites.add(novos)
            
            # Remove o asteroide original
            asteroide_atingido.kill()
        
    # Colisão: Jogador vs. Asteroide (Game Over) 
    colisoes_jogador_ast = pygame.sprite.spritecollide(
        jogador, asteroides, False, 
        pygame.sprite.collide_circle
    )

    if colisoes_jogador_ast and jogador.vidas <= 0:
        game_over = True
        jogador.kill() 
    elif colisoes_jogador_ast and jogador.vidas > 0:
        if not vulnerable["is_vulneravel"]:
            return game_over, score  # Ignora a colisão se estiver invulnerável
        jogador.vidas -= 1
        # Reposiciona o jogador no centro da tela
        jogador.x = LARGURA_TELA // 2
        jogador.y = ALTURA_TELA // 2
        jogador.vx = 0
        jogador.vy = 0
        jogador.angle = 0
        vulnerable["is_vulneravel"] = False
        vulnerable["tempo_invulneravel"] = JANELA_INVULNERABILIDADE
    return game_over, score

def spawn_asteroids(asteroides, all_sprites, spawn_timer):
    if len(asteroides) < ASTEROIDES_MAXIMOS_TELA and spawn_timer == FPS:
        novo_asteroide = Asteroid(random.choice(PROBABILIDADE_ASTEROIDES))
        asteroides.add(novo_asteroide)
        all_sprites.add(novo_asteroide)

def start_asteroid_field(asteroides, all_sprites):
    for _ in range(NUM_ASTEROIDES_INICIAIS):
        # O construtor sem x, y gera o asteroide fora da tela
        ast = Asteroid(size=random.choice([2, 3])) # Começa com Médio e Grande
        asteroides.add(ast)
        all_sprites.add(ast)

def main():
    score = 0
    game_over = False

    # Inicialização do Pygame
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO)

    # Taxa de Quadros (FPS)
    clock = pygame.time.Clock()

    fonte_placar = pygame.font.Font(None, 24) 

    # Grupo de Sprites
    jogador = Player(LARGURA_TELA // 2, ALTURA_TELA // 2)
    balas = pygame.sprite.Group()
    asteroides = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(jogador)
    life_icon_img = pygame.image.load(LIFE_ICON_PATH).convert_alpha()
    life_icon_img = pygame.transform.scale(life_icon_img, (LIFE_ICON_SIZE, LIFE_ICON_SIZE))

    start_asteroid_field(asteroides, all_sprites)

    # Loop Principal do Jogo
    running = True
    spawn_timer = 0
    vulnerable = {"is_vulneravel": True, "tempo_invulneravel": 0}  # Jogador começa vulnerável
    while running:
        # Processando eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_SPACE:
                    projetil = jogador.atirar()
                    balas.add(projetil)
                    all_sprites.add(projetil)
            elif game_over and event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                    running = False

        if not game_over:
            # Spawn de Asteroides, limitado a uma certa quantidade na tela
            spawn_asteroids(asteroides, all_sprites, spawn_timer)
            
            teclas = pygame.key.get_pressed()
            jogador.handle_input(teclas)

            game_over, score = collision_detection(jogador, asteroides, balas, all_sprites, game_over, score, vulnerable)

            # Atualiza o estado de invulnerabilidade
            if not vulnerable["is_vulneravel"]:
                vulnerable["tempo_invulneravel"] = max(0, vulnerable["tempo_invulneravel"] - 1) # Decrementa por 1 frame
                if vulnerable["tempo_invulneravel"] == 0:
                    vulnerable["is_vulneravel"] = True

            # Atualização das nossas entidades
            all_sprites.update()

            # Renderização
            tela.fill(PRETO)
            all_sprites.draw(tela)

            # Atualiza a Tela
            pygame.display.flip()

            # Controla o FPS
            clock.tick(FPS)

            spawn_timer += 1
            spawn_timer %= FPS + 1
        
        tela.fill(PRETO)
        all_sprites.draw(tela)

        # Desenha o Placar
        desenhar_placar(tela, jogador, score, fonte_placar, life_icon_img, game_over, tela, fonte_placar)

        # Atualiza a Tela
        pygame.display.flip()

        clock.tick(FPS)
        
if __name__ == "__main__":
    main()