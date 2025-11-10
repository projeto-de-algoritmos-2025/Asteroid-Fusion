# Deep Impact: Asteroid Fusion

**Conteúdo da Disciplina**: Dividir e Conquistar

## Alunos

<table>
  <tr>
    <td align="center"><a href="https://github.com/luanasoares0901"><img style="border-radius: 60%;" src="https://github.com/luanasoares0901.png" width="200px;" alt=""/><br /><sub><b>Luana Ribeiro Soares<br>(202016720)</br></b></sub></a><br/></td>
    <td align="center"><a href="https://github.com/MMcLovin"><img style="border-radius: 60%;" src="https://github.com/MMcLovin.png" width="200px;" alt=""/><br /><sub><b>Gabriel Fernando de Jesus Silva<br>(222022162)</br></b></sub></a><br/></td>
  </tr>
</table>

## Sobre

O projeto foi desenvolvido em Python com a biblioteca Pygame, que implementa e disponibiliza uma série de métodos e classes que auxiliam na construção de jogos 2D. Escolhemos replicar o clássico jogo [Asteroids](https://pt.wikipedia.org/wiki/Asteroids) da atari, porém, com a uma mecânica de colisão e fusão dos asteróides e é justamente nessa mecânica em que usamos o algoritmo de Dividir e Conquistar Par Mais Próximo (Closest Pair of Points), para detectar e alertar sobre potenciais fusões de asteroides.

### Linguagem e Bibliotecas

* **Linguagem**: Python
* **Principais Bibliotecas utilizadas**: Pygame

### Estrutura do Projeto

```
  Deep Impact: Asteroid Fusion/
  └── src/
      ├── algorithm/
      │   └── closest_pair.py  # Implementação do algoritmo de Par Mais Próximo (Closest Pair of Points).
      │
      ├── assets/
      │   └── Imagens para os asteroides e nave do jogador.
      │
      ├── models/
      │   ├── Asteroid.py      # Classe do Asteroide, que inclui lógica de movimento, divisão (split) e fusão (fusion).
      │   ├── Bullet.py        # Classe do Projétil disparado pelo jogador, incluindo lógica de movimento e tempo de vida.
      │   └── Player.py        # Classe do Jogador, incluindo física e manuseio de inputs.
      │
      ├── config.py            # Contém todas as constantes e configurações globais do jogo (tamanhos, velocidades, cores, pontuações, etc.).
      └── main.py              # Arquivo principal que inicializa o Pygame, contém o loop do jogo, e gerencia a detecção de colisões e o placar.
```

### Funcionalidades

* **Controle da Nave**: é possível rotacionar, acelerar e aplicar propulsão para frente e para trás.

* **Física da Nave**: Implementa fricção e limitação de velocidade máxima. A nave se "teletransporta" para a borda oposta da tela caso ultrapasse os limites da tela.

* **Sistema de Vidas**: O jogador possui um número limitado de vidas (4) e entra em um estado de invulnerabilidade temporária (JANELA_INVULNERABILIDADE = 120 frames) após colidir com um asteroide, reaparecendo no centro da tela.

* **Asteroides**: Os asteroides são gerados aleatoriamente em tamanhos Grande (tamanho = 3 e pontuação = 100), Médio (tamanho = 2 e pontuação = 50) e Pequeno (tamanho = 1 e pontuação = 20) a partir das bordas da tela.

* **Mecânica de Divisão (Split)**: Ao ser atingido por uma bala, um asteroide se divide em dois asteroides de um nível de tamanho menor, caso o tamanho seja maior que 1.

* **Mecânica de Fusão (Fusion)**: Se dois asteroides colidirem, e ambos não estiverem com o temporizador de imunidade à fusão ativo (isso é necessário para que os asterroides não se fundam imediatamente após serem divididos por um tiro do jogador), eles se fundem em um asteroide de um nível de tamanho maior, com a média de suas posições e velocidades e pontuação somada dos asteroides que colidiram. Colisão entre asteroides Grandes (3) é ignorada.

* **Algoritmo de Par Mais Próximo**: O algoritmo de Closest Pair of Points é executado para encontrar o par de asteroides mais próximos na tela a cada frame.

* **Alerta Visual de Fusão**: Uma linha e círculos de alerta são desenhados em torno do par de asteroides mais próximos obtidos pelo algoritmo de dividir e conquistar, mudando de cor para alertar se a distância mínima (D_min) for menor ou igual ao ALERTA_COLISAO (100 pixels).

### Controles

| Ação | Tecla |
| --- | --- |
| Rotacionar Esquerda | Seta Esquerda (`pygame.K_LEFT`) |
| Rotacionar Direita | Seta Direita (`pygame.K_RIGHT`) |
| Propulsão (Acelerar) | Seta Cima (`pygame.K_UP`) |
| Propulsão Reversa | Seta Baixo (`pygame.K_DOWN`) |
| Atirar | Espaço (`pygame.K_SPACE`) |
| Sair (Tela de Game Over) | Enter (`pygame.K_RETURN` ou `pygame.K_KP_ENTER`) |

### Configurações do Jogo
As principais configurações do jogo podem ser ajustadas em src/config.py:
| Constante | Valor | Descrição |
| --------- | :---: | --------- |
| LARGURA_TELA      | 1200  | Largura da janela do jogo. |
| ALTURA_TELA       | 800   | Altura da janela do jogo. |
| FPS               | 60    | Taxa de quadros por segundo. |
| TITULO            | "Deep Impact: Asteroid Fusion" | Título da janela do jogo. |
| VELOCIDADE_MAXIMA | 6     | Velocidade máxima da nave do jogador. |
| ALERTA_COLISAO    | 100   | Distância para ativar o alerta visual de colisão (vermelho). |
| IMUNIDADE_FUSAO   | 120   | Tempo (em frames) que um asteroide recém-dividido/criado fica imune à fusão. |

## Apresentação

A apresentação do projeto pode ser acessada [aqui]().

## Guia de Instalação

### Pré-requisitos

- Git (versão 2.40 ou superior);
- Python (versão 3.12 ou superior);

### Clonando o repositório

- O primeiro passo é clonar o repositório do projeto do GitHub.

```bash
git clone https://github.com/projeto-de-algoritmos-2025/Asteroid-Fusion.git

cd Asteroid-Fusion
```

### Executando o projeto

- Recomendamos criar e ativar um ambiente virtual novo para o projeto. Para isso, utilize os comandos abaixo:

```bash
python -m venv env
.\env\Scripts\activate
```

- Em seguida, instale as dependências:

```bash
pip install -r requirements.txt
```

- Após instalar as dependências, execute o comando a partir da raiz do projeto:

```bash
python .\src\main.py
```
