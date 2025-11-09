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
AMARELO_DMIN = (255, 255, 0)

# --- Configurações de Asteroides ---
TIPO_ASTEROIDE = {
    3: {"nivel": "Grande", "raio": 120, "velocidade_max": 1}, # asteroid3.png
    2: {"nivel": "Medio", "raio": 60, "velocidade_max": 2}, # asteroid2.png
    1: {"nivel": "Pequeno", "raio": 20, "velocidade_max": 3} # asteroid1.png
}
ASTEROIDES_MAXIMOS_TELA = int((LARGURA_TELA / ALTURA_TELA) * 2)
MAX_ASTEROIDES_TELA = 40
NUM_ASTEROIDES_INICIAIS = 4
# 1s = 3/10 => 30%
# 2s = 4/10 => 40%
# 3s = 3/10 => 30%
PROBABILIDADE_ASTEROIDES = [1, 1, 1, 2, 2, 2, 2, 3, 3, 3]
ALERTA_COLISAO = 150  # distância para alerta de colisão

# --- Configurações das Balas ---
TAMANHO_BALA = 4
VELOCIDADE_BALA = 8
VIDA_BALA = FPS

# --- Configurações do Jogador ---
VELOCIDADE_ROTACAO = 3.5
ACELERACAO = 0.1
FRICAO = 0.99 
VELOCIDADE_MAXIMA = 6
PLAYER_ICON = "src/assets/player.png"
PLAYER_SIZE = 20
PROPULSION_OFFSET = 90
LIFE_ICON_PATH = PLAYER_ICON
LIFE_ICON_SIZE = 25
JANELA_INVULNERABILIDADE = FPS * 2

# --- Configurações de Pontuação ---
PONTUACAO_PEQUENO = 100
PONTUACAO_MEDIO = 50
PONTUACAO_GRANDE = 20
PONTUACAO_FUSAO = 200 

# --- Outras Configurações ---
INF = float('inf')
INTERVALO_CALCULO = FPS * 3
