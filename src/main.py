from models.Player import Player
from models.Asteroid import Asteroid
from config import *
from time import sleep
from algorithm.closest_pair import closest_pair
import pygame
import random

# TODO
# colocar um timer pra poder fazer a fusão dos asteroides
# tá uma putaria misturando inglês com português, tlvz escolher um só ou fdse
# botar sons? acho q seria trampo dmais
# colocar o número de asteroides na tela? 
# a quantidade de asteroides na tela tá boa?
# lógica do tiro tá boa? atirar mais balas? e se deixar a tecla espaço pressionada?

def desenhar_placar(tela, jogador, score, fonte_placar, vida_icon, game_over, d_min_atual, closest_pair_timer):
    # ----- LADO DIREITO -----
    ALTURA_INICIAL_DIREITA = 15
    OFFSET_DIREITA = 200
    desenhar_texto(tela, f"Ângulo: {int((jogador.angle + PROPULSION_OFFSET) % 360)}°", fonte_placar, LARGURA_TELA - OFFSET_DIREITA, ALTURA_INICIAL_DIREITA)
    desenhar_texto(tela, f"Pontos: {score}", fonte_placar, LARGURA_TELA - OFFSET_DIREITA, ALTURA_INICIAL_DIREITA + 35)
    desenhar_texto(tela, "Vidas:", fonte_placar, LARGURA_TELA - OFFSET_DIREITA, ALTURA_INICIAL_DIREITA + 65)
    # icone pra cada vida
    start_x = LARGURA_TELA - 140
    y = ALTURA_INICIAL_DIREITA + 60 # Na mesma linha do rótulo "Vidas:"
    for i in range(jogador.vidas):
        x = start_x + (i * (LIFE_ICON_SIZE + 5)) # 5px de espaçamento
        tela.blit(vida_icon, (x, y))
    # ----------------------
    
    # ----- LADO ESQUERDO -----
    ALTURA_INICIAL_ESQUERDA = 40
    OFFSET_ESQUERDA = 10
    # distancia entre o par de asteroides mais proximos
    if d_min_atual != INF:
        texto_dmin = f"Distância: {d_min_atual:.2f}"
        desenhar_texto(tela, texto_dmin, fonte_placar, OFFSET_ESQUERDA, ALTURA_INICIAL_ESQUERDA, AMARELO_DMIN)
    else:
        desenhar_texto(tela, "D_min: N/A", fonte_placar, OFFSET_ESQUERDA, ALTURA_INICIAL_ESQUERDA)
    # timer para a próxima fusão
    tempo_restante = (INTERVALO_CALCULO_PARES - closest_pair_timer) / FPS
    desenhar_texto(tela, f"Próxima Fusão em: {tempo_restante:.1f}s", fonte_placar, OFFSET_ESQUERDA, ALTURA_INICIAL_ESQUERDA + 30, AZUL)
    # ----------------------

    if game_over:
        texto_fim = "GAME OVER"
        # Fonte um pouco maior para Game Over
        fonte_game_over = pygame.font.Font(None, FONTE_GAME_OVER_TAMANHO) 
        desenhar_texto(tela, texto_fim, fonte_game_over, LARGURA_TELA // 2 - 150, ALTURA_TELA // 2 - 32, VERMELHO_ALERTA)

def desenhar_texto(surface, text, font, x, y, color=BRANCO):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

def player_collision(jogador, asteroides, game_over, vulneravel):
    # Colisão: Jogador vs. Asteroide 
    colisoes_jogador_ast = pygame.sprite.spritecollide(
        jogador, asteroides, False, 
        pygame.sprite.collide_circle
    )

    if colisoes_jogador_ast and jogador.vidas <= 0:
        return True  # Game Over
    elif colisoes_jogador_ast and jogador.vidas > 0:
        if not vulneravel["is_vulneravel"]:
            return None  # Ignora a colisão se estiver invulnerável
        jogador.vidas -= 1
        # Reposiciona o jogador no centro da tela
        jogador.x = LARGURA_TELA // 2
        jogador.y = ALTURA_TELA // 2
        jogador.vx = 0
        jogador.vy = 0
        jogador.angle = 0
        vulneravel["is_vulneravel"] = False
        vulneravel["janela_invulneravel"] = JANELA_INVULNERABILIDADE
        return False

def bullet_collision(balas, asteroides, all_sprites, score):
    # Colisão: Bala vs. Asteroide 
    # True, False: Destrói a bala, mas não o asteroide pq a gnt vai processar ele no split primeiro.
    colisoes_bala_ast = pygame.sprite.groupcollide(
        balas, asteroides, True, False, 
        pygame.sprite.collide_circle
    )

    # As chaves são as Balas que atingiram algo. Os valores são as listas de Asteroides atingidos.
    for bala_atingida, asteroides_atingidos in colisoes_bala_ast.items(): 
        # Itera sobre cada Asteroide atingido por esta bala
        for asteroide_atingido in asteroides_atingidos:
            score += asteroide_atingido.pontuacao
                
            # Lógica de quebra (split)
            novos = asteroide_atingido.split()
            if novos:
                asteroides.add(novos)
                all_sprites.add(novos)
            
            # Remove o asteroide original
            asteroide_atingido.kill()

    return score

def asteroid_collision(asteroides, asteroide_a, asteroide_b, all_sprites):
    # se os asteroides do par mais próximo colidiram, faz a lógica de fusão
    if asteroide_a and asteroide_b:
        if asteroide_a.immune_to_fusion_timer == 0 and asteroide_b.immune_to_fusion_timer == 0:
            # verificar colisão entre os dois asteroides mais próximos
            if pygame.sprite.collide_circle(asteroide_a, asteroide_b):
                # Lógica de fusão
                novo_asteroide = asteroide_a.fusion(asteroide_b)
                if novo_asteroide:
                    asteroides.add(novo_asteroide)
                    all_sprites.add(novo_asteroide)
                    # O PROBLEMA TÁ AQUI
                    asteroide_a.kill()
                    asteroide_b.kill()

    return asteroides, all_sprites

def collision_detection(jogador, asteroides, balas, all_sprites, game_over, score, vulneravel, asteroide_a, asteroide_b):

    score = bullet_collision(balas, asteroides, all_sprites, score)

    asteroid_collision(asteroides, asteroide_a, asteroide_b, all_sprites)

    if player_collision(jogador, asteroides, game_over, vulneravel):
        game_over = True

    return game_over, score

def spawn_asteroides(asteroides, all_sprites, spawn_timer):
    if len(asteroides) < ASTEROIDES_MAXIMOS_TELA and spawn_timer == FPS:
        novo_asteroide = Asteroid(random.choice(PROBABILIDADE_ASTEROIDES))
        asteroides.add(novo_asteroide)
        all_sprites.add(novo_asteroide)

def main():
    # Inicialização do Pygame
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO)
    clock = pygame.time.Clock()

    fonte_placar = pygame.font.Font(None, FONTE_PLACAR_TAMANHO)

    # Grupo de Sprites
    jogador = Player(LARGURA_TELA // 2, ALTURA_TELA // 2)
    balas = pygame.sprite.Group()
    asteroides = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(jogador)
    vida_icon = pygame.image.load(LIFE_ICON_PATH).convert_alpha()
    vida_icon = pygame.transform.scale(vida_icon, (LIFE_ICON_SIZE, LIFE_ICON_SIZE))
    jogador_invuln_img = pygame.image.load(PLAYER_VULNERAVEL_ICON).convert_alpha()
    jogador_invuln_img = pygame.transform.scale(jogador_invuln_img, (PLAYER_SIZE, PLAYER_SIZE))

    # Variáveis do Jogo
    asteroide_a = None
    asteroide_b = None
    d_min_atual = INF
    game_over = False
    running = True
    score = 0
    closest_pair_timer = 0
    spawn_timer = 0
    vulneravel = {"is_vulneravel": True, "janela_invulneravel": 0}  

    # Loop Principal do Jogo
    while running:
        # Processando eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and not game_over and vulneravel["is_vulneravel"]:
                if event.key == pygame.K_SPACE:
                    projetil = jogador.atirar()
                    balas.add(projetil)
                    all_sprites.add(projetil)
            elif game_over and event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                    running = False

        if not game_over:
            # Spawn de Asteroides, limitado a uma certa quantidade na tela
            spawn_asteroides(asteroides, all_sprites, spawn_timer)
            
            teclas = pygame.key.get_pressed()
            jogador.handle_input(teclas)

            # calcula o par de asteroides mais proximos
            asteroides_ativos = list(asteroides)
            if len(asteroides_ativos) >= 2:
                d_min_atual, asteroide_a, asteroide_b = closest_pair(asteroides_ativos)
            else:
                d_min_atual = INF
                asteroide_a = None
                asteroide_b = None

            game_over, score = collision_detection(jogador, asteroides, balas, all_sprites, game_over, score, vulneravel, asteroide_a, asteroide_b)

            # Atualiza o estado de invulnerabilidade se o jogador colidiu com um asteroide
            if not vulneravel["is_vulneravel"]:
                vulneravel["janela_invulneravel"] = max(0, vulneravel["janela_invulneravel"] - 1) # Decrementa por 1 frame
                if vulneravel["janela_invulneravel"] == 0:
                    vulneravel["is_vulneravel"] = True

            # Chamando o update de todos os sprites
            all_sprites.update()

            # redesenhando as sprites
            tela.fill(PRETO)
            all_sprites.draw(tela)

            # Controla o FPS
            #clock.tick(FPS)

            closest_pair_timer += 1
            spawn_timer += 1
            spawn_timer %= FPS + 1
        
        tela.fill(PRETO)

        # desenha o status de proximidade dos asteroides
        if asteroide_a and asteroide_b:
            p1 = (int(asteroide_a.x), int(asteroide_a.y))
            p2 = (int(asteroide_b.x), int(asteroide_b.y))
            
            # a gnt muda a cor dependendo da disancia entre os asteroides
            if d_min_atual <= ALERTA_COLISAO:
                linha_cor = VERMELHO_ALERTA
            else:
                linha_cor = AMARELO_DMIN

            # linha entre os dois asteroides mais próximos
            pygame.draw.line(tela, linha_cor, p1, p2, 2)

            # circulo de alerta ao redor dos asteroides
            pygame.draw.circle(tela, linha_cor, p1, asteroide_a.raio, 2)
            pygame.draw.circle(tela, linha_cor, p2, asteroide_b.raio, 2)

        # mudando imagem do jogador quando invulnerável
        if vulneravel["is_vulneravel"]:
            jogador.original_image = pygame.image.load(PLAYER_ICON).convert_alpha()
            jogador.original_image = pygame.transform.scale(jogador.original_image, (jogador.raio, jogador.raio))
        else:
            jogador.original_image = jogador_invuln_img

        all_sprites.draw(tela)

        desenhar_placar(tela, jogador, score, fonte_placar, vida_icon, game_over, d_min_atual, closest_pair_timer)

        # limpa o buffer e atualiza a tela com as sprites atualizadas
        pygame.display.flip()

        clock.tick(FPS)
        
if __name__ == "__main__":
    main()