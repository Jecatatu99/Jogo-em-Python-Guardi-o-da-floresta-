import math
import sys
from pathlib import Path

import pygame


# ==================================================
# CONFIGURAÇÃO DO ÁUDIO
# ==================================================

pygame.mixer.pre_init(
    frequency=44100,
    size=-16,
    channels=2,
    buffer=512
)


# ==================================================
# INICIALIZAÇÃO DO PYGAME
# ==================================================

pygame.init()

LARGURA = 1000
ALTURA = 650
FPS = 60

tela = pygame.display.set_mode(
    (LARGURA, ALTURA)
)

pygame.display.set_caption(
    "Guardião da Floresta"
)

relogio = pygame.time.Clock()


# ==================================================
# CAMINHO COMPATÍVEL COM PYINSTALLER
# ==================================================

def caminho_recurso(caminho_relativo):
    """
    Retorna o caminho correto de imagens e sons.

    Funciona tanto ao executar pelo VS Code quanto
    dentro do executável criado pelo PyInstaller.
    """

    if hasattr(sys, "_MEIPASS"):
        pasta_base = Path(sys._MEIPASS)
    else:
        pasta_base = Path(__file__).resolve().parent

    return pasta_base / caminho_relativo


# ==================================================
# CAMINHOS DOS ARQUIVOS
# ==================================================

PASTA_ASSETS = caminho_recurso("assets")
PASTA_IMAGENS = PASTA_ASSETS / "imagens"
PASTA_SONS = PASTA_ASSETS / "sons"

CAMINHO_FUNDO_MENU = (
    PASTA_IMAGENS / "menu.png"
)

CAMINHO_MUSICA_MENU = (
    PASTA_SONS / "musica_menu.mp3"
)


# ==================================================
# CORES
# ==================================================

BRANCO = (255, 255, 255)
PRETO = (20, 20, 20)

CEU = (105, 190, 245)

VERDE_ESCURO = (25, 90, 45)
VERDE_CAMPO = (80, 175, 70)
VERDE_CLARO = (105, 195, 85)
VERDE_FOLHA = (40, 135, 60)

MARROM = (110, 70, 40)
MARROM_CLARO = (160, 105, 55)
MARROM_ESCURO = (75, 45, 30)

CINZA = (110, 120, 120)
CINZA_CLARO = (160, 170, 175)

AMARELO = (255, 215, 55)
LARANJA = (255, 125, 25)

VERMELHO = (210, 60, 45)
VERMELHO_ESCURO = (145, 35, 30)

AZUL = (45, 135, 220)
AZUL_CLARO = (120, 215, 255)

ROXO = (90, 25, 110)

COR_PELE = (235, 180, 135)
COR_CAMINHO = (185, 145, 90)


# ==================================================
# FONTES
# ==================================================

fonte_titulo = pygame.font.SysFont(
    "arial",
    39,
    bold=True
)

fonte_normal = pygame.font.SysFont(
    "arial",
    24,
    bold=True
)

fonte_pequena = pygame.font.SysFont(
    "arial",
    18
)

fonte_resultado = pygame.font.SysFont(
    "arial",
    62,
    bold=True
)


# ==================================================
# FUNÇÕES DE TEXTO E TEMPO
# ==================================================

def escrever_texto(
    texto,
    fonte,
    cor,
    x,
    y,
    centralizado=True
):
    imagem = fonte.render(
        texto,
        True,
        cor
    )

    retangulo = imagem.get_rect()

    if centralizado:
        retangulo.center = (x, y)
    else:
        retangulo.topleft = (x, y)

    tela.blit(
        imagem,
        retangulo
    )


def formatar_tempo(segundos):
    segundos = max(
        0,
        math.ceil(segundos)
    )

    minutos = segundos // 60
    segundos_restantes = segundos % 60

    return (
        f"{minutos:02d}:"
        f"{segundos_restantes:02d}"
    )


# ==================================================
# FUNDO ALTERNATIVO
# ==================================================

def criar_fundo_alternativo():
    """
    Cria um fundo simples caso menu.png
    não possa ser carregado.
    """

    fundo = pygame.Surface(
        (LARGURA, ALTURA)
    )

    fundo.fill(
        VERDE_ESCURO
    )

    pygame.draw.circle(
        fundo,
        AMARELO,
        (850, 100),
        55
    )

    pygame.draw.polygon(
        fundo,
        CINZA_CLARO,
        [
            (0, 360),
            (220, 110),
            (440, 360)
        ]
    )

    pygame.draw.polygon(
        fundo,
        CINZA,
        [
            (300, 360),
            (570, 130),
            (800, 360)
        ]
    )

    pygame.draw.polygon(
        fundo,
        CINZA_CLARO,
        [
            (600, 360),
            (820, 120),
            (1000, 360)
        ]
    )

    pygame.draw.rect(
        fundo,
        VERDE_CAMPO,
        (
            0,
            330,
            LARGURA,
            ALTURA - 330
        )
    )

    return fundo


# ==================================================
# CARREGAMENTO DA IMAGEM
# ==================================================

def carregar_fundo_menu():
    try:
        imagem = pygame.image.load(
            str(CAMINHO_FUNDO_MENU)
        ).convert()

        imagem = pygame.transform.smoothscale(
            imagem,
            (LARGURA, ALTURA)
        )

        print(
            "Imagem do menu carregada:",
            CAMINHO_FUNDO_MENU
        )

        return imagem

    except Exception as erro:
        print(
            "AVISO: não foi possível carregar menu.png."
        )

        print(
            "Caminho:",
            CAMINHO_FUNDO_MENU
        )

        print(
            "Erro:",
            erro
        )

        return criar_fundo_alternativo()


# ==================================================
# CARREGAMENTO DOS EFEITOS SONOROS
# ==================================================

def carregar_som(nome_arquivo, volume):
    caminho = PASTA_SONS / nome_arquivo

    if not caminho.exists():
        print(
            f"AVISO: som não encontrado: {caminho}"
        )

        return None

    try:
        som = pygame.mixer.Sound(
            str(caminho)
        )

        som.set_volume(
            volume
        )

        print(
            f"Som carregado: {nome_arquivo}"
        )

        return som

    except pygame.error as erro:
        print(
            f"ERRO ao carregar {nome_arquivo}: {erro}"
        )

        return None


def reproduzir_som(som):
    if som is not None:
        som.play()


fundo_menu = carregar_fundo_menu()

som_agua = carregar_som(
    "agua.wav",
    0.35
)

som_fogo_apagado = carregar_som(
    "fogo_apagado.wav",
    0.55
)

som_vitoria = carregar_som(
    "vitoria.wav",
    0.65
)

som_derrota = carregar_som(
    "derrota.wav",
    0.65
)


# ==================================================
# MÚSICA DO MENU
# ==================================================

musica_menu_disponivel = False


def carregar_musica_menu():
    global musica_menu_disponivel

    if not CAMINHO_MUSICA_MENU.exists():
        print(
            "AVISO: música do menu não encontrada:"
        )

        print(
            CAMINHO_MUSICA_MENU
        )

        musica_menu_disponivel = False
        return

    try:
        pygame.mixer.music.load(
            str(CAMINHO_MUSICA_MENU)
        )

        pygame.mixer.music.set_volume(
            0.20
        )

        musica_menu_disponivel = True

        print(
            "Música do menu carregada com sucesso!"
        )

    except pygame.error as erro:
        musica_menu_disponivel = False

        print(
            "ERRO ao carregar música do menu:"
        )

        print(erro)


def iniciar_musica_menu():
    if not musica_menu_disponivel:
        return

    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(-1)


def parar_musica_menu():
    if musica_menu_disponivel:
        pygame.mixer.music.fadeout(400)


def voltar_musica_menu():
    if not musica_menu_disponivel:
        return

    try:
        pygame.mixer.music.load(
            str(CAMINHO_MUSICA_MENU)
        )

        pygame.mixer.music.set_volume(
            0.20
        )

        pygame.mixer.music.play(-1)

    except pygame.error as erro:
        print(
            "Erro ao reiniciar música:"
        )

        print(erro)


carregar_musica_menu()


# ==================================================
# ESTADOS DO JOGO
# ==================================================

MENU = "menu"
JOGANDO = "jogando"
VITORIA = "vitoria"
DERROTA = "derrota"

estado_jogo = MENU


# ==================================================
# CONFIGURAÇÕES INICIAIS
# ==================================================

dificuldade = "medio"
nome_dificuldade = "MÉDIO"

agua_maxima = 80
agua_disponivel = 80
custo_disparo = 3

tempo_maximo = 90
tempo_restante = 90

pontuacao = 0
motivo_derrota = ""


# ==================================================
# CONFIGURAÇÕES DO BOMBEIRO
# ==================================================

LARGURA_BOMBEIRO = 44
ALTURA_BOMBEIRO = 70
VELOCIDADE_BOMBEIRO = 250

bombeiro = pygame.Rect(
    LARGURA // 2 - LARGURA_BOMBEIRO // 2,
    ALTURA - 140,
    LARGURA_BOMBEIRO,
    ALTURA_BOMBEIRO
)

direcao_bombeiro = "direita"


# ==================================================
# SISTEMA DE ÁGUA
# ==================================================

VELOCIDADE_AGUA = 500
TEMPO_ENTRE_DISPAROS = 250

jatos_agua = []
ultimo_disparo = 0


# ==================================================
# INCÊNDIOS POR DIFICULDADE
# ==================================================

def criar_incendios(nivel):
    if nivel == "facil":
        return [
            pygame.Rect(150, 420, 55, 65),
            pygame.Rect(420, 520, 55, 65),
            pygame.Rect(710, 430, 55, 65)
        ]

    if nivel == "medio":
        return [
            pygame.Rect(135, 410, 45, 55),
            pygame.Rect(340, 520, 45, 55),
            pygame.Rect(620, 430, 45, 55),
            pygame.Rect(800, 555, 45, 55)
        ]

    if nivel == "dificil":
        return [
            pygame.Rect(120, 410, 38, 48),
            pygame.Rect(260, 530, 38, 48),
            pygame.Rect(400, 430, 38, 48),
            pygame.Rect(550, 555, 38, 48),
            pygame.Rect(700, 415, 38, 48),
            pygame.Rect(835, 545, 38, 48)
        ]

    if nivel == "extremo":
        return [
            pygame.Rect(105, 415, 34, 44),
            pygame.Rect(215, 535, 34, 44),
            pygame.Rect(325, 440, 34, 44),
            pygame.Rect(440, 555, 34, 44),
            pygame.Rect(560, 420, 34, 44),
            pygame.Rect(665, 545, 34, 44),
            pygame.Rect(755, 475, 34, 44),
            pygame.Rect(875, 560, 34, 44),

            # Fogo no telhado da cabana
            pygame.Rect(842, 325, 42, 52)
        ]

    return []


incendios = criar_incendios(
    dificuldade
)


def configurar_dificuldade(nivel):
    global dificuldade
    global nome_dificuldade
    global agua_maxima
    global custo_disparo
    global tempo_maximo

    dificuldade = nivel

    if nivel == "facil":
        nome_dificuldade = "FÁCIL"
        agua_maxima = 100
        custo_disparo = 2
        tempo_maximo = 120

    elif nivel == "medio":
        nome_dificuldade = "MÉDIO"
        agua_maxima = 80
        custo_disparo = 3
        tempo_maximo = 90

    elif nivel == "dificil":
        nome_dificuldade = "DIFÍCIL"
        agua_maxima = 60
        custo_disparo = 4
        tempo_maximo = 60

    elif nivel == "extremo":
        nome_dificuldade = "EXTREMO"
        agua_maxima = 50
        custo_disparo = 5
        tempo_maximo = 45

    parar_musica_menu()
    reiniciar_partida()


# ==================================================
# ELEMENTOS DO CENÁRIO
# ==================================================

def desenhar_nuvem(x, y, escala=1):
    pygame.draw.circle(
        tela,
        BRANCO,
        (x, y),
        int(22 * escala)
    )

    pygame.draw.circle(
        tela,
        BRANCO,
        (
            x + int(27 * escala),
            y - int(10 * escala)
        ),
        int(28 * escala)
    )

    pygame.draw.circle(
        tela,
        BRANCO,
        (
            x + int(58 * escala),
            y
        ),
        int(22 * escala)
    )

    pygame.draw.ellipse(
        tela,
        BRANCO,
        (
            x - int(5 * escala),
            y,
            int(85 * escala),
            int(28 * escala)
        )
    )


def desenhar_arvore(x, y, escala=1):
    largura_tronco = int(
        24 * escala
    )

    altura_tronco = int(
        75 * escala
    )

    pygame.draw.rect(
        tela,
        MARROM,
        (
            x - largura_tronco // 2,
            y - altura_tronco,
            largura_tronco,
            altura_tronco
        ),
        border_radius=4
    )

    pygame.draw.circle(
        tela,
        VERDE_FOLHA,
        (
            x,
            y - int(105 * escala)
        ),
        int(44 * escala)
    )

    pygame.draw.circle(
        tela,
        VERDE_CLARO,
        (
            x - int(30 * escala),
            y - int(90 * escala)
        ),
        int(32 * escala)
    )

    pygame.draw.circle(
        tela,
        VERDE_FOLHA,
        (
            x + int(30 * escala),
            y - int(90 * escala)
        ),
        int(32 * escala)
    )


def desenhar_pedra(x, y):
    pygame.draw.ellipse(
        tela,
        CINZA,
        (x, y, 50, 28)
    )

    pygame.draw.ellipse(
        tela,
        CINZA_CLARO,
        (x + 8, y + 4, 25, 10)
    )


def desenhar_capim(x, y):
    pygame.draw.line(
        tela,
        VERDE_ESCURO,
        (x, y),
        (x - 7, y - 15),
        3
    )

    pygame.draw.line(
        tela,
        VERDE_ESCURO,
        (x, y),
        (x, y - 18),
        3
    )

    pygame.draw.line(
        tela,
        VERDE_ESCURO,
        (x, y),
        (x + 8, y - 14),
        3
    )


def desenhar_cabana(x, y):
    pygame.draw.rect(
        tela,
        MARROM_CLARO,
        (x, y, 140, 95)
    )

    for linha_y in range(
        y + 12,
        y + 90,
        18
    ):
        pygame.draw.line(
            tela,
            MARROM,
            (x, linha_y),
            (x + 140, linha_y),
            2
        )

    pygame.draw.polygon(
        tela,
        VERMELHO_ESCURO,
        [
            (x - 20, y),
            (x + 70, y - 65),
            (x + 160, y)
        ]
    )

    pygame.draw.rect(
        tela,
        MARROM_ESCURO,
        (x + 54, y + 40, 38, 55)
    )

    pygame.draw.circle(
        tela,
        AMARELO,
        (x + 84, y + 68),
        3
    )

    pygame.draw.rect(
        tela,
        BRANCO,
        (x + 12, y + 25, 34, 28),
        border_radius=3
    )

    pygame.draw.rect(
        tela,
        AZUL,
        (x + 16, y + 29, 26, 20)
    )

    pygame.draw.line(
        tela,
        BRANCO,
        (x + 29, y + 29),
        (x + 29, y + 49),
        2
    )

    pygame.draw.line(
        tela,
        BRANCO,
        (x + 16, y + 39),
        (x + 42, y + 39),
        2
    )

    pygame.draw.rect(
        tela,
        MARROM_ESCURO,
        (x + 108, y - 48, 22, 40)
    )


def desenhar_cenario():
    tela.fill(CEU)

    pygame.draw.circle(
        tela,
        AMARELO,
        (880, 85),
        43
    )

    desenhar_nuvem(90, 75, 0.9)
    desenhar_nuvem(480, 65, 0.7)

    pygame.draw.polygon(
        tela,
        CINZA_CLARO,
        [
            (0, 300),
            (170, 110),
            (350, 300)
        ]
    )

    pygame.draw.polygon(
        tela,
        CINZA,
        [
            (250, 300),
            (480, 130),
            (700, 300)
        ]
    )

    pygame.draw.polygon(
        tela,
        CINZA_CLARO,
        [
            (580, 300),
            (800, 100),
            (1000, 300)
        ]
    )

    pygame.draw.polygon(
        tela,
        BRANCO,
        [
            (170, 110),
            (135, 150),
            (170, 140),
            (200, 155)
        ]
    )

    pygame.draw.polygon(
        tela,
        BRANCO,
        [
            (480, 130),
            (445, 165),
            (480, 155),
            (510, 170)
        ]
    )

    pygame.draw.polygon(
        tela,
        BRANCO,
        [
            (800, 100),
            (760, 145),
            (800, 130),
            (840, 150)
        ]
    )

    pygame.draw.rect(
        tela,
        VERDE_CAMPO,
        (
            0,
            280,
            LARGURA,
            ALTURA - 280
        )
    )

    pygame.draw.ellipse(
        tela,
        VERDE_CLARO,
        (
            -200,
            300,
            1400,
            500
        )
    )

    pygame.draw.polygon(
        tela,
        COR_CAMINHO,
        [
            (755, 650),
            (960, 650),
            (895, 530),
            (850, 470),
            (805, 470),
            (820, 550)
        ]
    )

    desenhar_cabana(790, 375)

    desenhar_arvore(70, 390, 0.8)
    desenhar_arvore(210, 390, 0.75)
    desenhar_arvore(680, 390, 0.8)
    desenhar_arvore(970, 390, 0.75)

    desenhar_arvore(70, 620, 1.1)
    desenhar_arvore(940, 620, 1.1)

    desenhar_pedra(270, 470)
    desenhar_pedra(590, 550)
    desenhar_pedra(430, 600)

    posicoes_capim = [
        (120, 475),
        (225, 590),
        (305, 540),
        (405, 630),
        (470, 455),
        (525, 510),
        (610, 620),
        (710, 480),
        (765, 580),
        (885, 590)
    ]

    for x, y in posicoes_capim:
        desenhar_capim(x, y)


# ==================================================
# INCÊNDIO
# ==================================================

def desenhar_incendio(incendio):
    x = incendio.x
    y = incendio.y

    largura = incendio.width
    altura = incendio.height

    pygame.draw.ellipse(
        tela,
        (70, 85, 45),
        (
            x - 4,
            y + altura - 10,
            largura + 8,
            16
        )
    )

    pygame.draw.polygon(
        tela,
        VERMELHO,
        [
            (x + largura // 2, y),
            (
                x + largura - 5,
                y + altura // 2
            ),
            (
                x + largura,
                y + altura - 5
            ),
            (
                x + largura // 2,
                y + altura
            ),
            (
                x,
                y + altura - 5
            ),
            (
                x + 5,
                y + altura // 2
            )
        ]
    )

    pygame.draw.polygon(
        tela,
        LARANJA,
        [
            (
                x + largura // 2,
                y + altura // 4
            ),
            (
                x + largura - 10,
                y + altura // 2
            ),
            (
                x + largura - 8,
                y + altura - 6
            ),
            (
                x + largura // 2,
                y + altura - 2
            ),
            (
                x + 8,
                y + altura - 6
            ),
            (
                x + 11,
                y + altura // 2
            )
        ]
    )

    pygame.draw.polygon(
        tela,
        AMARELO,
        [
            (
                x + largura // 2,
                y + altura // 2
            ),
            (
                x + largura - 14,
                y + altura - 12
            ),
            (
                x + largura // 2,
                y + altura - 4
            ),
            (
                x + 14,
                y + altura - 12
            )
        ]
    )


# ==================================================
# BOMBEIRO
# ==================================================

def desenhar_bombeiro():
    x = bombeiro.x
    y = bombeiro.y

    pygame.draw.ellipse(
        tela,
        (55, 115, 55),
        (x - 5, y + 62, 54, 15)
    )

    pygame.draw.rect(
        tela,
        AZUL,
        (x + 34, y + 28, 12, 29),
        border_radius=5
    )

    pygame.draw.rect(
        tela,
        PRETO,
        (x + 8, y + 46, 11, 20),
        border_radius=4
    )

    pygame.draw.rect(
        tela,
        PRETO,
        (x + 25, y + 46, 11, 20),
        border_radius=4
    )

    pygame.draw.rect(
        tela,
        PRETO,
        (x + 4, y + 61, 17, 8),
        border_radius=3
    )

    pygame.draw.rect(
        tela,
        PRETO,
        (x + 23, y + 61, 17, 8),
        border_radius=3
    )

    pygame.draw.rect(
        tela,
        VERMELHO,
        (x + 5, y + 25, 34, 29),
        border_radius=8
    )

    pygame.draw.rect(
        tela,
        AMARELO,
        (x + 6, y + 42, 32, 5)
    )

    pygame.draw.rect(
        tela,
        VERMELHO,
        (x, y + 29, 10, 26),
        border_radius=5
    )

    pygame.draw.rect(
        tela,
        VERMELHO,
        (x + 34, y + 29, 10, 26),
        border_radius=5
    )

    pygame.draw.circle(
        tela,
        COR_PELE,
        (x + 5, y + 54),
        5
    )

    pygame.draw.circle(
        tela,
        COR_PELE,
        (x + 39, y + 54),
        5
    )

    pygame.draw.circle(
        tela,
        COR_PELE,
        (x + 22, y + 20),
        14
    )

    pygame.draw.circle(
        tela,
        AMARELO,
        (x + 22, y + 11),
        13
    )

    pygame.draw.rect(
        tela,
        AMARELO,
        (x + 5, y + 10, 34, 11),
        border_radius=5
    )

    pygame.draw.circle(
        tela,
        VERMELHO,
        (x + 22, y + 10),
        5
    )

    pygame.draw.circle(
        tela,
        PRETO,
        (x + 18, y + 22),
        2
    )

    pygame.draw.circle(
        tela,
        PRETO,
        (x + 26, y + 22),
        2
    )


def movimentar_bombeiro(tempo_segundos):
    global direcao_bombeiro

    teclas = pygame.key.get_pressed()

    movimento_x = 0
    movimento_y = 0

    if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
        movimento_x = -VELOCIDADE_BOMBEIRO
        direcao_bombeiro = "esquerda"

    if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
        movimento_x = VELOCIDADE_BOMBEIRO
        direcao_bombeiro = "direita"

    if teclas[pygame.K_w] or teclas[pygame.K_UP]:
        movimento_y = -VELOCIDADE_BOMBEIRO
        direcao_bombeiro = "cima"

    if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
        movimento_y = VELOCIDADE_BOMBEIRO
        direcao_bombeiro = "baixo"

    if movimento_x != 0 and movimento_y != 0:
        movimento_x *= 0.7071
        movimento_y *= 0.7071

    bombeiro.x += int(
        movimento_x * tempo_segundos
    )

    bombeiro.y += int(
        movimento_y * tempo_segundos
    )

    if bombeiro.left < 0:
        bombeiro.left = 0

    if bombeiro.right > LARGURA:
        bombeiro.right = LARGURA

    if bombeiro.top < 290:
        bombeiro.top = 290

    if bombeiro.bottom > ALTURA:
        bombeiro.bottom = ALTURA


# ==================================================
# SISTEMA DE ÁGUA
# ==================================================

def disparar_agua():
    global agua_disponivel
    global ultimo_disparo

    if agua_disponivel < custo_disparo:
        return

    tempo_atual = pygame.time.get_ticks()

    if (
        tempo_atual - ultimo_disparo
        < TEMPO_ENTRE_DISPAROS
    ):
        return

    centro_x = bombeiro.centerx
    centro_y = bombeiro.centery

    velocidade_x = 0
    velocidade_y = 0

    if direcao_bombeiro == "direita":
        retangulo_agua = pygame.Rect(
            bombeiro.right,
            centro_y - 5,
            18,
            10
        )

        velocidade_x = VELOCIDADE_AGUA

    elif direcao_bombeiro == "esquerda":
        retangulo_agua = pygame.Rect(
            bombeiro.left - 18,
            centro_y - 5,
            18,
            10
        )

        velocidade_x = -VELOCIDADE_AGUA

    elif direcao_bombeiro == "cima":
        retangulo_agua = pygame.Rect(
            centro_x - 5,
            bombeiro.top - 18,
            10,
            18
        )

        velocidade_y = -VELOCIDADE_AGUA

    else:
        retangulo_agua = pygame.Rect(
            centro_x - 5,
            bombeiro.bottom,
            10,
            18
        )

        velocidade_y = VELOCIDADE_AGUA

    novo_jato = {
        "retangulo": retangulo_agua,
        "x": float(retangulo_agua.x),
        "y": float(retangulo_agua.y),
        "velocidade_x": velocidade_x,
        "velocidade_y": velocidade_y
    }

    jatos_agua.append(
        novo_jato
    )

    reproduzir_som(
        som_agua
    )

    agua_disponivel -= custo_disparo

    agua_disponivel = max(
        0,
        agua_disponivel
    )

    ultimo_disparo = tempo_atual


def atualizar_jatos_agua(tempo_segundos):
    global estado_jogo
    global pontuacao

    pontos_por_incendio = {
        "facil": 100,
        "medio": 200,
        "dificil": 300,
        "extremo": 500
    }

    for jato in jatos_agua[:]:

        jato["x"] += (
            jato["velocidade_x"]
            * tempo_segundos
        )

        jato["y"] += (
            jato["velocidade_y"]
            * tempo_segundos
        )

        jato["retangulo"].x = int(
            jato["x"]
        )

        jato["retangulo"].y = int(
            jato["y"]
        )

        retangulo_agua = jato["retangulo"]
        acertou = False

        for incendio in incendios[:]:

            if retangulo_agua.colliderect(
                incendio
            ):
                incendios.remove(
                    incendio
                )

                reproduzir_som(
                    som_fogo_apagado
                )

                pontuacao += (
                    pontos_por_incendio[
                        dificuldade
                    ]
                )

                acertou = True
                break

        if acertou:

            if jato in jatos_agua:
                jatos_agua.remove(
                    jato
                )

            if len(incendios) == 0:
                estado_jogo = VITORIA

                jatos_agua.clear()

                reproduzir_som(
                    som_vitoria
                )

                return

            continue

        saiu_da_tela = (
            retangulo_agua.right < 0
            or retangulo_agua.left > LARGURA
            or retangulo_agua.bottom < 0
            or retangulo_agua.top > ALTURA
        )

        if saiu_da_tela and jato in jatos_agua:
            jatos_agua.remove(
                jato
            )


def desenhar_jatos_agua():
    for jato in jatos_agua:
        retangulo = jato["retangulo"]

        pygame.draw.ellipse(
            tela,
            BRANCO,
            retangulo.inflate(4, 4)
        )

        pygame.draw.ellipse(
            tela,
            AZUL_CLARO,
            retangulo
        )


# ==================================================
# CRONÔMETRO E DERROTA
# ==================================================

def atualizar_cronometro(tempo_segundos):
    global tempo_restante
    global estado_jogo
    global motivo_derrota

    tempo_restante -= tempo_segundos

    if tempo_restante <= 0:
        tempo_restante = 0

        if len(incendios) > 0:
            motivo_derrota = "O tempo acabou!"
            estado_jogo = DERROTA

            jatos_agua.clear()

            reproduzir_som(
                som_derrota
            )


def verificar_derrota_agua():
    global estado_jogo
    global motivo_derrota

    if (
        agua_disponivel < custo_disparo
        and len(jatos_agua) == 0
        and len(incendios) > 0
    ):
        motivo_derrota = (
            "Você ficou sem água suficiente!"
        )

        estado_jogo = DERROTA

        reproduzir_som(
            som_derrota
        )


def reiniciar_partida():
    global agua_disponivel
    global direcao_bombeiro
    global ultimo_disparo
    global incendios
    global estado_jogo
    global tempo_restante
    global motivo_derrota
    global pontuacao

    bombeiro.x = (
        LARGURA // 2
        - LARGURA_BOMBEIRO // 2
    )

    bombeiro.y = ALTURA - 140

    direcao_bombeiro = "direita"

    agua_disponivel = agua_maxima
    tempo_restante = tempo_maximo

    ultimo_disparo = 0
    motivo_derrota = ""
    pontuacao = 0

    jatos_agua.clear()

    incendios = criar_incendios(
        dificuldade
    )

    estado_jogo = JOGANDO


# ==================================================
# MENU TRANSPARENTE
# ==================================================

def desenhar_opcao_menu(
    y,
    cor,
    titulo,
    descricao,
    cor_borda=BRANCO
):
    largura_botao = 535
    altura_botao = 67

    botao = pygame.Surface(
        (
            largura_botao,
            altura_botao
        ),
        pygame.SRCALPHA
    )

    cor_transparente = (
        cor[0],
        cor[1],
        cor[2],
        115
    )

    pygame.draw.rect(
        botao,
        cor_transparente,
        (
            0,
            0,
            largura_botao,
            altura_botao
        ),
        border_radius=14
    )

    tela.blit(
        botao,
        (55, y)
    )

    pygame.draw.rect(
        tela,
        cor_borda,
        (
            55,
            y,
            largura_botao,
            altura_botao
        ),
        width=2,
        border_radius=14
    )

    escrever_texto(
        titulo,
        fonte_normal,
        BRANCO,
        322,
        y + 20
    )

    escrever_texto(
        descricao,
        fonte_pequena,
        BRANCO,
        322,
        y + 48
    )


def desenhar_menu():
    tela.blit(
        fundo_menu,
        (0, 0)
    )

    painel = pygame.Surface(
        (610, 620),
        pygame.SRCALPHA
    )

    painel.fill(
        (5, 25, 15, 80)
    )

    tela.blit(
        painel,
        (18, 15)
    )

    pygame.draw.rect(
        tela,
        BRANCO,
        (18, 15, 610, 620),
        width=2,
        border_radius=20
    )

    escrever_texto(
        "GUARDIÃO DA FLORESTA",
        fonte_titulo,
        PRETO,
        325,
        55
    )

    escrever_texto(
        "GUARDIÃO DA FLORESTA",
        fonte_titulo,
        AMARELO,
        323,
        53
    )

    escrever_texto(
        "Escolha uma dificuldade",
        fonte_normal,
        BRANCO,
        323,
        95
    )

    desenhar_opcao_menu(
        125,
        (25, 115, 55),
        "1 - FÁCIL",
        "3 incêndios | Água: 100% | Tempo: 02:00"
    )

    desenhar_opcao_menu(
        200,
        (145, 110, 25),
        "2 - MÉDIO",
        "4 incêndios | Água: 80% | Tempo: 01:30"
    )

    desenhar_opcao_menu(
        275,
        (145, 45, 35),
        "3 - DIFÍCIL",
        "6 incêndios | Água: 60% | Tempo: 01:00"
    )

    desenhar_opcao_menu(
        350,
        ROXO,
        "4 - EXTREMO",
        "9 incêndios | Água: 50% | Tempo: 00:45",
        AMARELO
    )

    escrever_texto(
        "O nível extremo possui fogo na cabana!",
        fonte_pequena,
        LARANJA,
        323,
        438
    )

    escrever_texto(
        "CONTROLES",
        fonte_normal,
        AMARELO,
        323,
        478
    )

    escrever_texto(
        "WASD ou setas: movimentar",
        fonte_pequena,
        BRANCO,
        323,
        515
    )

    escrever_texto(
        "ESPAÇO: lançar água",
        fonte_pequena,
        BRANCO,
        323,
        545
    )

    escrever_texto(
        "ESC: voltar ao menu",
        fonte_pequena,
        BRANCO,
        323,
        575
    )

    escrever_texto(
        "Pressione 1, 2, 3 ou 4 para começar",
        fonte_pequena,
        AMARELO,
        323,
        610
    )


# ==================================================
# INTERFACE DA PARTIDA
# ==================================================

def desenhar_interface():
    pygame.draw.rect(
        tela,
        (20, 65, 35),
        (15, 15, 810, 72),
        border_radius=12
    )

    pygame.draw.rect(
        tela,
        BRANCO,
        (15, 15, 810, 72),
        width=2,
        border_radius=12
    )

    escrever_texto(
        f"Incêndios: {len(incendios)}",
        fonte_pequena,
        BRANCO,
        30,
        25,
        centralizado=False
    )

    escrever_texto(
        f"Água: {agua_disponivel}%",
        fonte_pequena,
        AZUL_CLARO,
        165,
        25,
        centralizado=False
    )

    escrever_texto(
        f"Nível: {nome_dificuldade}",
        fonte_pequena,
        AMARELO,
        295,
        25,
        centralizado=False
    )

    if tempo_restante <= 10:
        cor_tempo = VERMELHO

    elif tempo_restante <= 30:
        cor_tempo = AMARELO

    else:
        cor_tempo = BRANCO

    escrever_texto(
        f"Tempo: {formatar_tempo(tempo_restante)}",
        fonte_pequena,
        cor_tempo,
        470,
        25,
        centralizado=False
    )

    escrever_texto(
        f"Pontos: {pontuacao}",
        fonte_pequena,
        AMARELO,
        650,
        25,
        centralizado=False
    )

    pygame.draw.rect(
        tela,
        CINZA,
        (30, 59, 765, 12),
        border_radius=6
    )

    porcentagem = (
        agua_disponivel / agua_maxima
    )

    largura_barra = int(
        765 * porcentagem
    )

    if agua_disponivel <= custo_disparo * 2:
        cor_barra = VERMELHO
    else:
        cor_barra = AZUL

    if largura_barra > 0:
        pygame.draw.rect(
            tela,
            cor_barra,
            (
                30,
                59,
                largura_barra,
                12
            ),
            border_radius=6
        )


def desenhar_jogo():
    desenhar_cenario()

    for incendio in incendios:
        desenhar_incendio(
            incendio
        )

    desenhar_jatos_agua()
    desenhar_bombeiro()
    desenhar_interface()


# ==================================================
# TELAS DE RESULTADO
# ==================================================

def desenhar_fundo_resultado():
    desenhar_cenario()

    for incendio in incendios:
        desenhar_incendio(
            incendio
        )

    desenhar_bombeiro()

    camada = pygame.Surface(
        (LARGURA, ALTURA),
        pygame.SRCALPHA
    )

    camada.fill(
        (0, 0, 0, 175)
    )

    tela.blit(
        camada,
        (0, 0)
    )


def desenhar_vitoria():
    desenhar_fundo_resultado()

    pygame.draw.rect(
        tela,
        (20, 90, 50),
        (185, 90, 630, 480),
        border_radius=25
    )

    pygame.draw.rect(
        tela,
        AMARELO,
        (185, 90, 630, 480),
        width=4,
        border_radius=25
    )

    escrever_texto(
        "VITÓRIA!",
        fonte_resultado,
        AMARELO,
        LARGURA // 2,
        165
    )

    escrever_texto(
        "Você apagou todos os incêndios!",
        fonte_normal,
        BRANCO,
        LARGURA // 2,
        245
    )

    escrever_texto(
        f"Dificuldade: {nome_dificuldade}",
        fonte_normal,
        LARANJA,
        LARGURA // 2,
        300
    )

    escrever_texto(
        f"Pontuação: {pontuacao}",
        fonte_normal,
        AMARELO,
        LARGURA // 2,
        345
    )

    escrever_texto(
        f"Tempo restante: {formatar_tempo(tempo_restante)}",
        fonte_normal,
        BRANCO,
        LARGURA // 2,
        390
    )

    escrever_texto(
        f"Água restante: {agua_disponivel}%",
        fonte_normal,
        AZUL_CLARO,
        LARGURA // 2,
        435
    )

    escrever_texto(
        "R: jogar novamente | ESC: menu",
        fonte_pequena,
        BRANCO,
        LARGURA // 2,
        515
    )


def desenhar_derrota():
    desenhar_fundo_resultado()

    pygame.draw.rect(
        tela,
        (90, 28, 25),
        (185, 100, 630, 455),
        border_radius=25
    )

    pygame.draw.rect(
        tela,
        VERMELHO,
        (185, 100, 630, 455),
        width=4,
        border_radius=25
    )

    escrever_texto(
        "DERROTA",
        fonte_resultado,
        VERMELHO,
        LARGURA // 2,
        175
    )

    escrever_texto(
        motivo_derrota,
        fonte_normal,
        BRANCO,
        LARGURA // 2,
        260
    )

    escrever_texto(
        f"Dificuldade: {nome_dificuldade}",
        fonte_normal,
        LARANJA,
        LARGURA // 2,
        315
    )

    escrever_texto(
        f"Incêndios restantes: {len(incendios)}",
        fonte_normal,
        AMARELO,
        LARGURA // 2,
        365
    )

    escrever_texto(
        f"Pontuação: {pontuacao}",
        fonte_normal,
        BRANCO,
        LARGURA // 2,
        410
    )

    escrever_texto(
        "R: tentar novamente | ESC: menu",
        fonte_pequena,
        BRANCO,
        LARGURA // 2,
        500
    )


# ==================================================
# LAÇO PRINCIPAL
# ==================================================

iniciar_musica_menu()

executando = True

while executando:
    tempo_segundos = (
        relogio.tick(FPS) / 1000
    )

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            executando = False

        if evento.type == pygame.KEYDOWN:

            if estado_jogo == MENU:

                if evento.key == pygame.K_1:
                    configurar_dificuldade(
                        "facil"
                    )

                elif evento.key == pygame.K_2:
                    configurar_dificuldade(
                        "medio"
                    )

                elif evento.key == pygame.K_3:
                    configurar_dificuldade(
                        "dificil"
                    )

                elif evento.key == pygame.K_4:
                    configurar_dificuldade(
                        "extremo"
                    )

            elif (
                estado_jogo == JOGANDO
                and evento.key == pygame.K_SPACE
            ):
                disparar_agua()

            elif (
                estado_jogo in [VITORIA, DERROTA]
                and evento.key == pygame.K_r
            ):
                reiniciar_partida()

            elif (
                estado_jogo
                in [
                    JOGANDO,
                    VITORIA,
                    DERROTA
                ]
                and evento.key == pygame.K_ESCAPE
            ):
                estado_jogo = MENU

                voltar_musica_menu()

    if estado_jogo == MENU:
        desenhar_menu()

    elif estado_jogo == JOGANDO:
        movimentar_bombeiro(
            tempo_segundos
        )

        atualizar_jatos_agua(
            tempo_segundos
        )

        if estado_jogo == JOGANDO:
            atualizar_cronometro(
                tempo_segundos
            )

        if estado_jogo == JOGANDO:
            verificar_derrota_agua()

        if estado_jogo == JOGANDO:
            desenhar_jogo()

        elif estado_jogo == VITORIA:
            desenhar_vitoria()

        elif estado_jogo == DERROTA:
            desenhar_derrota()

    elif estado_jogo == VITORIA:
        desenhar_vitoria()

    elif estado_jogo == DERROTA:
        desenhar_derrota()

    pygame.display.flip()


# ==================================================
# ENCERRAMENTO
# ==================================================

pygame.mixer.music.stop()
pygame.quit()
sys.exit()