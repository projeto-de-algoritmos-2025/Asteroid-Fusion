from models.Bullet import Bullet
from config import *
import pygame
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, x:int, y:int):
        super().__init__()
        self.raio = PLAYER_SIZE

        # começar nas coordenadas dadas
        self.x = float(x)
        self.y = float(y)

        # velocidade nos eixos
        self.vx = 0.0
        self.vy = 0.0

        # angulo inicial
        self.angle = 0.0
        self.cos_angle = 0
        self.sin_angle = 0

        self.original_image = pygame.image.load(PLAYER_ICON).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (self.raio, self.raio))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        self.rect.inflate_ip(-10, -10)  # reduz o rect para melhorar a colisão

        self.vidas = 4

    def handle_input(self, keys):
        # Rotação
        if keys[pygame.K_LEFT]:
            self.angle += VELOCIDADE_ROTACAO
        if keys[pygame.K_RIGHT]:
            self.angle -= VELOCIDADE_ROTACAO

        self.angle %= 360

        # nossa propulsão
        if keys[pygame.K_UP]:
            angle_rad = math.radians(self.angle + PROPULSION_OFFSET)
            # obtendo a aceleração nos eixos x e y
            self.vx += ACELERACAO * math.cos(angle_rad)
            self.vy -= ACELERACAO * math.sin(angle_rad)
        if keys[pygame.K_DOWN]:
            angle_rad = math.radians(self.angle + PROPULSION_OFFSET)
            # obtendo a aceleração nos eixos x e y
            self.vx -= ACELERACAO * math.cos(angle_rad)
            self.vy += ACELERACAO * math.sin(angle_rad)

    def atirar(self):
        # Calcula a direção de saída da bala
        angle_rad = math.radians(self.angle + 270)
        
        # Posição inicial da bala deve ser na ponta da nave
        pos_x_tiro = self.x - self.raio * math.cos(angle_rad + PROPULSION_OFFSET*3)
        pos_y_tiro = self.y + self.raio * math.sin(angle_rad + PROPULSION_OFFSET*3)

        return Bullet(pos_x_tiro, pos_y_tiro, angle_rad)
    
    def update(self):
        # rotacionando o player
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

        # aplicando fricção
        self.vx *= FRICAO
        self.vy *= FRICAO

        # limitando a velocidade máxima
        vel_magnitude = math.sqrt(self.vx**2 + self.vy**2)
        if vel_magnitude > VELOCIDADE_MAXIMA:
            self.vx = (self.vx / vel_magnitude) * VELOCIDADE_MAXIMA
            self.vy = (self.vy / vel_magnitude) * VELOCIDADE_MAXIMA

        self.x += self.vx
        self.y += self.vy

        # Teletransporte nas bordas da tela
        self.x %= LARGURA_TELA
        self.y %= ALTURA_TELA
