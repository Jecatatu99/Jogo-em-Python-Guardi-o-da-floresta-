# 🌲🔥 Guardião da Floresta

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.x-2D5F2D)
![Status](https://img.shields.io/badge/status-concluído-success)
![Licença](https://img.shields.io/badge/licença-acadêmica-blue)

## 📖 Sobre o projeto

**Guardião da Floresta** é um jogo 2D desenvolvido em **Python** com a biblioteca **Pygame**. O jogador controla um bombeiro florestal e precisa apagar todos os focos de incêndio antes que o tempo ou a água acabem.

O projeto foi desenvolvido com foco em lógica de programação, eventos de teclado, colisões, gerenciamento de estados, níveis de dificuldade, cronômetro, pontuação, imagens e efeitos sonoros.

## 🎯 Objetivo do jogo

Apague todos os focos de incêndio antes que uma das condições de derrota aconteça:

- o cronômetro chegar a `00:00`;
- a quantidade de água ficar abaixo do custo de um novo disparo;
- ainda existirem incêndios no cenário.

## ✨ Funcionalidades

- Menu inicial com imagem de fundo e elementos transparentes;
- Música exclusiva no menu;
- Quatro níveis de dificuldade;
- Movimentação em quatro direções e na diagonal;
- Sistema de disparo de água;
- Detecção de colisão entre água e incêndios;
- Barra de água dinâmica;
- Cronômetro regressivo;
- Sistema de pontuação;
- Condições de vitória e derrota;
- Efeitos sonoros de água, incêndio apagado, vitória e derrota;
- Incêndio especial no telhado da cabana no nível extremo;
- Reinício da partida e retorno ao menu;
- Executável para Windows gerado com PyInstaller.

## 🎮 Controles

| Tecla | Ação |
|---|---|
| `W` ou `↑` | Movimentar para cima |
| `S` ou `↓` | Movimentar para baixo |
| `A` ou `←` | Movimentar para a esquerda |
| `D` ou `→` | Movimentar para a direita |
| `ESPAÇO` | Lançar água |
| `R` | Reiniciar após vitória ou derrota |
| `ESC` | Voltar ao menu |
| `1`, `2`, `3`, `4` | Selecionar a dificuldade |

## 🧩 Níveis de dificuldade

| Nível | Incêndios | Água | Custo por disparo | Tempo | Pontos por incêndio |
|---|---:|---:|---:|---:|---:|
| Fácil | 3 | 100% | 2% | 02:00 | 100 |
| Médio | 4 | 80% | 3% | 01:30 | 200 |
| Difícil | 6 | 60% | 4% | 01:00 | 300 |
| Extremo | 9 | 50% | 5% | 00:45 | 500 |

> O nível **Extremo** possui um foco de incêndio especial no telhado da cabana.

## 🛠️ Tecnologias utilizadas

- Python 3;
- Pygame;
- pathlib;
- PyInstaller;
- Mermaid para os diagramas UML.

## 📁 Estrutura do projeto

```text
Guardiao_da_Floresta/
├── assets/
│   ├── imagens/
│   │   └── menu.png
│   └── sons/
│       ├── agua.wav
│       ├── fogo_apagado.wav
│       ├── vitoria.wav
│       ├── derrota.wav
│       └── musica_menu.mp3
├── executavel/
│   └── Guardiao_da_Floresta.exe
├── prints/
├── main.py
└── README.md
```

# 📐 Diagramas UML

## 1. Diagrama de casos de uso

```mermaid
flowchart LR
    Jogador([Jogador])

    subgraph Sistema[Guardião da Floresta]
        UC1((Selecionar dificuldade))
        UC2((Movimentar bombeiro))
        UC3((Lançar água))
        UC4((Apagar incêndio))
        UC5((Acompanhar água))
        UC6((Acompanhar tempo))
        UC7((Receber pontuação))
        UC8((Vencer partida))
        UC9((Perder partida))
        UC10((Reiniciar partida))
        UC11((Voltar ao menu))
    end

    Jogador --> UC1
    Jogador --> UC2
    Jogador --> UC3
    Jogador --> UC5
    Jogador --> UC6
    Jogador --> UC10
    Jogador --> UC11

    UC3 --> UC4
    UC4 --> UC7
    UC4 --> UC8
    UC5 --> UC9
    UC6 --> UC9
```

## 2. Diagrama de classes

```mermaid
classDiagram
    class Jogo {
        +String estado
        +String dificuldade
        +int pontuacao
        +float tempoRestante
        +iniciar()
        +atualizar()
        +reiniciarPartida()
        +verificarVitoria()
        +verificarDerrota()
    }

    class Menu {
        +Imagem fundo
        +Musica musicaMenu
        +desenhar()
        +selecionarDificuldade()
        +iniciarMusica()
        +pararMusica()
    }

    class Bombeiro {
        +Rect posicao
        +String direcao
        +int velocidade
        +movimentar()
        +dispararAgua()
        +desenhar()
    }

    class JatoAgua {
        +Rect retangulo
        +float velocidadeX
        +float velocidadeY
        +atualizar()
        +verificarColisao()
        +desenhar()
    }

    class Incendio {
        +Rect posicao
        +bool ativo
        +desenhar()
        +apagar()
    }

    class Dificuldade {
        +String nome
        +int quantidadeIncendios
        +int aguaMaxima
        +int custoDisparo
        +int tempoMaximo
        +int pontosPorIncendio
        +configurar()
    }

    class GerenciadorAudio {
        +Som agua
        +Som fogoApagado
        +Som vitoria
        +Som derrota
        +Musica musicaMenu
        +carregarSons()
        +reproduzirSom()
        +iniciarMusicaMenu()
        +pararMusicaMenu()
    }

    Jogo *-- Menu
    Jogo *-- Bombeiro
    Jogo *-- Dificuldade
    Jogo *-- GerenciadorAudio
    Jogo o-- Incendio
    Bombeiro --> JatoAgua : cria
    JatoAgua --> Incendio : colide e apaga
    Dificuldade --> Incendio : define quantidade
```

## 3. Diagrama de estados

```mermaid
stateDiagram-v2
    [*] --> Menu

    Menu --> Jogando : Selecionar nível 1, 2, 3 ou 4
    Jogando --> Vitoria : Todos os incêndios apagados
    Jogando --> Derrota : Tempo esgotado
    Jogando --> Derrota : Água insuficiente
    Jogando --> Menu : Pressionar ESC

    Vitoria --> Jogando : Pressionar R
    Vitoria --> Menu : Pressionar ESC

    Derrota --> Jogando : Pressionar R
    Derrota --> Menu : Pressionar ESC

    Menu --> [*] : Fechar janela
    Jogando --> [*] : Fechar janela
    Vitoria --> [*] : Fechar janela
    Derrota --> [*] : Fechar janela
```

## 4. Diagrama de atividade da partida

```mermaid
flowchart TD
    A([Início]) --> B[Exibir menu]
    B --> C{Dificuldade selecionada?}
    C -- Não --> B
    C -- Sim --> D[Configurar água, tempo e incêndios]
    D --> E[Iniciar partida]
    E --> F[Ler comandos do jogador]
    F --> G{Ação realizada}

    G -- Movimentar --> H[Atualizar posição do bombeiro]
    G -- Disparar --> I[Reduzir água e criar jato]

    H --> J[Atualizar cronômetro]
    I --> K{Jato atingiu incêndio?}
    K -- Sim --> L[Apagar incêndio e somar pontos]
    K -- Não --> J
    L --> M{Restam incêndios?}
    M -- Não --> N[Exibir vitória]
    M -- Sim --> J

    J --> O{Tempo acabou?}
    O -- Sim --> P[Exibir derrota por tempo]
    O -- Não --> Q{Água permite novo disparo?}
    Q -- Não --> R[Exibir derrota por falta de água]
    Q -- Sim --> F

    N --> S{R ou ESC?}
    P --> S
    R --> S
    S -- R --> D
    S -- ESC --> B
```

## ▶️ Como executar pelo código-fonte

### 1. Clone o repositório

```bash
git clone URL_DO_SEU_REPOSITORIO
cd Guardiao_da_Floresta
```

### 2. Instale o Pygame

```bash
python -m pip install pygame
```

### 3. Execute o jogo

```bash
python main.py
```

## 💻 Como executar no Windows

Abra a pasta `executavel` e execute:

```text
Guardiao_da_Floresta.exe
```

## 📦 Como gerar o executável

Instale o PyInstaller:

```powershell
python -m pip install --upgrade pyinstaller
```

Gere o executável incluindo a pasta `assets`:

```powershell
python -m PyInstaller --noconfirm --clean --onefile --windowed --name "Guardiao_da_Floresta" --add-data "assets;assets" main.py
```

O executável será criado em:

```text
dist/Guardiao_da_Floresta.exe
```

## 🖼️ Capturas de tela

Adicione as imagens da pasta `prints` nesta seção. Exemplo:

```markdown
![Menu inicial](prints/01_menu_inicial.png)
![Jogo em execução](prints/02_jogo_em_execucao.png)
![Nível extremo](prints/03_nivel_extremo.png)
![Tela de vitória](prints/04_vitoria.png)
![Tela de derrota](prints/05_derrota.png)
```

## 👨‍💻 Autor

**Jean Carlos Kovaliki**  
Estudante de Engenharia de Software

## 📄 Licença

Projeto desenvolvido para fins acadêmicos e educacionais.
