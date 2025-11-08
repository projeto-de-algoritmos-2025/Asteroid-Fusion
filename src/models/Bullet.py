from src.config import *
import pygame
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle_rad):
        super().__init__()

        self.x = float(x)
        self.y = float(y)

        # empirismo puro, inverter o sentido do eixo x consertou tudo 
        self.vx = -VELOCIDADE_BALA * math.cos(angle_rad)
        self.vy = VELOCIDADE_BALA * math.sin(angle_rad)

        self.tamanho = 4
        self.vida = 60  

        self.image = pygame.Surface((self.tamanho, self.tamanho), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BRANCO, (self.tamanho // 2, self.tamanho // 2), self.tamanho // 2, self.tamanho // 2)
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

    def update(self):
        self.x += self.vx
        self.y += self.vy

        self.rect.center = (int(self.x), int(self.y))

        self.vida -= 1

        # para de renderizar a bala se ela sair da tela ou acabar o lifespan dela
        if self.vida <= 0 or self.x < 0 or self.x > LARGURA_TELA or self.y < 0 or self.y > ALTURA_TELA:
            self.kill()