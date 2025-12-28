# Pan-Tompkins Python Implementation

Este projeto implementa o algoritmo clássico de **Pan-Tompkins** para detecção
de complexos **QRS** em sinais de ECG, utilizando a linguagem **Python** e o
banco de dados **MIT-BIH Arrhythmia Database**.

O objetivo é duplo:
1. **Praticar desenvolvimento profissional em Python** (estrutura, Git, GitHub)
2. **Reproduzir e validar cientificamente** o algoritmo Pan-Tompkins,
   servindo como base para estudos, extensões e comparação com arquiteturas
   em hardware.

---

## Referência teórica

Pan, J., & Tompkins, W. J. (1985).  
*A real-time QRS detection algorithm*.  
IEEE Transactions on Biomedical Engineering, 32(3), 230–236.

---

## Funcionalidades implementadas (até o momento)

- Leitura automática de registros do **MIT-BIH** via `wfdb`
- Pré-processamento do ECG:
  - Filtro passa-faixa Butterworth (5–15 Hz)
  - Derivada discreta (5 pontos)
  - Quadratura do sinal
  - Integração por janela móvel (MWI)
- Detecção inicial de picos:
  - Picos locais no MWI
  - Threshold adaptativo (SPKI / NPKI)
  - Período refratário
  - Refinamento do pico no sinal filtrado
- CLI simples para testes rápidos
- Projeto estruturado como **pacote Python**

---

## Estrutura do projeto

```
pan-tompkins-python/
│
├── src/
│   └── pantompkins/
│       ├── __init__.py
│       ├── io.py           # Leitura de dados (MIT-BIH / WFDB)
│       ├── filters.py      # Filtros digitais
│       ├── detector.py     # Pipeline Pan-Tompkins
│       ├── peaks.py        # Detecção de picos locais
│       └── cli.py          # Interface de linha de comando
│
├── tests/                  # Testes (em evolução)
├── notebooks/              # Análises exploratórias (opcional)
├── requirements.txt
├── pyproject.toml
├── .gitignore
└── README.md
```

## Requisitos

Python 3.10+

Bibliotecas:
numpy
scipy
wfdb
matplotlib (opcional para visualização)

## Instalação das dependências:

```
python -m pip install -r requirements.txt
```
## Instalação do projeto (modo desenvolvimento)

Na raiz do projeto:
```
python -m pip install -e .
```

Isso permite importar o pacote pantompkins diretamente durante o
desenvolvimento.

## Como executar

A partir da raiz do projeto:
```
python -m pantompkins.cli
```

O programa irá solicitar:

Record (ex: 100):

## Exemplo:

Record (ex: 100): 100
[OK] record=100 fs=360 N=650000
[OK] annotations R-peaks: 2274
[OK] predicted  R-peaks: XXXX