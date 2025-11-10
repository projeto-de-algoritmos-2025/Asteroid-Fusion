# --- Configurações de Janela e Jogo ---
LARGURA_TELA = 1200
ALTURA_TELA = 800
FPS = 60
TITULO = "Deep Impact: Asteroid Fusion"

# --- Cores (usando RGB) ---
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 100, 200)
VERMELHO_ALERTA = (255, 0, 50) 
LARANJA = (255, 165, 0)
AMARELO_DMIN = (255, 255, 0)

# --- Configurações de Asteroides ---
PONTUACAO_PEQUENO = 100
PONTUACAO_MEDIO = 50
PONTUACAO_GRANDE = 20
TIPO_ASTEROIDE = {
    3: {"nivel": "Grande", "raio": 120, "velocidade_max": 1, "pontuacao": PONTUACAO_GRANDE}, # asteroid3.png
    2: {"nivel": "Medio", "raio": 65, "velocidade_max": 2, "pontuacao": PONTUACAO_MEDIO}, # asteroid2.png
    1: {"nivel": "Pequeno", "raio": 22, "velocidade_max": 3, "pontuacao": PONTUACAO_PEQUENO} # asteroid1.png
}
ASTEROIDES_MAXIMOS_TELA = int((LARGURA_TELA / ALTURA_TELA) * 10)
MAX_ASTEROIDES_TELA = 40
PROBABILIDADE_ASTEROIDES = [1, 2, 2, 2, 2, 3, 3, 3, 3, 3] # 1's = 1/10 => 10%, 2's = 4/10 => 40%, 3's = 5/10 => 50%
ALERTA_COLISAO = 100  # distância para alerta de colisão
INTERVALO_FUSAO = FPS * 3
IMUNIDADE_FUSAO = FPS * 2  # tempo de imunidade após fusão

# --- Configurações das Balas ---
TAMANHO_BALA = 4
VELOCIDADE_BALA = 9
VIDA_BALA = FPS + 10

# --- Configurações do Jogador ---
VELOCIDADE_ROTACAO = 3.5
ACELERACAO = 0.1
FRICAO = 0.99 
VELOCIDADE_MAXIMA = 6
PLAYER_ICON = "src/assets/player.png"
PLAYER_VULNERAVEL_ICON = "src/assets/player_blue.png"
PLAYER_SIZE = 20
PROPULSION_OFFSET = 90
LIFE_ICON_PATH = PLAYER_ICON
LIFE_ICON_SIZE = 25
JANELA_INVULNERABILIDADE = FPS * 2

# --- Outras Configurações ---
INF = float('inf')
FONTE_PLACAR_TAMANHO = 24
FONTE_GAME_OVER_TAMANHO = 64
