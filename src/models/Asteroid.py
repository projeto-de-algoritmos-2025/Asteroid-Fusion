import pygame
import random
import math
from config import *

class Asteroid(pygame.sprite.Sprite):
    # Mapeamento do número (tamanho) aos atributos de nível
    TAMANHOS = {
        3: {"nivel": "Grande", "raio": 120, "velocidade_max": 1}, # asteroid3.png
        2: {"nivel": "Medio", "raio": 60, "velocidade_max": 2}, # asteroid2.png
        1: {"nivel": "Pequeno", "raio": 20, "velocidade_max": 3} # asteroid1.png
    }

    def __init__(self, size:int, x=None, y=None, vx=None, vy=None):
        super().__init__()
        
        # Definindo atributos com base no tamanho
        self.size = size
        props = self.TAMANHOS.get(size, self.TAMANHOS[3]) 
        self.nivel = props["nivel"]
        self.raio = props["raio"]
        self.velocidade_max = props["velocidade_max"]

        # gerando posição inicial
        if x is None or y is None:
            self.x, self.y = self._generate_initial_coordinates() # Posição inicial fora da tela
        else:
            self.x = float(x) # Começa na posição da colisão
            self.y = float(y)

        # gerando velocidade inicial
        if vx is None or vy is None:
            self.vx, self.vy = self._generate_initial_velocity() # Velocidade inicial aleatória
        else:
            self.vx = float(vx) # Usa a velocidade calculada pelo split
            self.vy = float(vy)

        # Angulação inicial e velocidade de rotação do asteroide
        self.angle = random.uniform(0, 360) 
        self.rot_speed = random.uniform(-1, 1) # Velocidade de rotação visual
        
        # Escolhendo a imagem do asteroide
        self.original_image = pygame.image.load(f"src/assets/asteroid{size}.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (self.raio, self.raio))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))
    
    def _generate_initial_velocity(self):
        angle_rad = random.uniform(0, 2 * math.pi)
        velocidade = random.uniform(0.5, self.velocidade_max)

        vx = velocidade * math.cos(angle_rad)
        vy = velocidade * math.sin(angle_rad)
        return vx, vy

    def _generate_initial_coordinates(self):
        side = random.choice(['top', 'bottom', 'left', 'right'])
        
        # A posição inicial é calculado pra fora da borda, para garantir que 
        # o asteroide inteiro comece fora e entre na tela gradualmente.
        if side == 'top':
            # y = 0 - tamanho do asteroide
            # x varia entre 0 e LARGURA_TELA
            x = random.randint(0, LARGURA_TELA)
            y = -self.raio 
        elif side == 'bottom':
            # y = ALTURA_TELA + tamanho do asteroide
            # x varia entre 0 e LARGURA_TELA
            x = random.randint(0, LARGURA_TELA)
            y = ALTURA_TELA + self.raio
        elif side == 'left':
            # x = 0 - tamanho do asteroide
            # y varia entre 0 e ALTURA_TELA
            x = -self.raio
            y = random.randint(0, ALTURA_TELA)
        else: # 'right'
            # x = LARGURA_TELA + tamanho do asteroide
            # y varia entre 0 e ALTURA_TELA
            x = LARGURA_TELA + self.raio
            y = random.randint(0, ALTURA_TELA)

        return float(x), float(y)

    def split(self):
        novos_asteroides = []
        # 1 asteroide grande se divide em 2 médios
        # 1 asteroide médio se divide em 2 pequenos
        new_size = self.size - 1

        if new_size < 1:
            return novos_asteroides
        
        props_new = self.TAMANHOS[new_size]
        novo_raio = props_new["raio"]
        base_vel = self.velocidade_max + 1

        # depois de destruido, ele vai para uma direção aleatória
        base_angle_rad = random.uniform(0, 2 * math.pi)
        push_angle_rad = base_angle_rad

        for _ in range(2):
            vx = base_vel * math.cos(push_angle_rad)
            vy = base_vel * math.sin(push_angle_rad)
            novos_asteroides.append(Asteroid(new_size, x=self.x, y=self.y, vx=vx, vy=vy))
            push_angle_rad += math.pi # varia 180 graus para o próximo asteroide

        return novos_asteroides

    def update(self):
        # Atualiza a Posição (Movimento)
        self.x += self.vx
        self.y += self.vy

        # Teletransporte nas bordas da tela
        # O asteroide desaparece quando o centro dele passa mais de um raio para fora da tela.
        # Ele reaparece no lado oposto com a mesma distância para dentro.
        if self.x > LARGURA_TELA + self.raio:
            self.x = -self.raio
        elif self.x < -self.raio:
            self.x = LARGURA_TELA + self.raio
            
        if self.y > ALTURA_TELA + self.raio:
            self.y = -self.raio
        elif self.y < -self.raio:
            self.y = ALTURA_TELA + self.raio
        
        # Atualiza a rotação, dentro entre 0 e 360 graus
        self.angle += self.rot_speed
        self.angle %= 360
        
        # Atualiza a imagem rotacionada e o retângulo de colisão
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))