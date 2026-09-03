# Otimização Linear com LINDO API

Script em Python para resolver problemas de Programação Linear (PL) usando a
[LINDO API](https://www.lindo.com/), com dados de entrada lidos de um arquivo
JSON. Funciona para qualquer número de variáveis e restrições, sem precisar
alterar o código.

## Problema resolvido

```
Maximizar (ou minimizar)  Z = c1*x1 + c2*x2 + ... + cn*xn

Sujeito a restrições do tipo <=, >= ou =
```

## Pré-requisitos

- Python 3.8+
- [LINDO API](https://www.lindo.com/) instalada, com uma licença válida
- Variável de ambiente `LINDOAPI_HOME` apontando para a instalação da LINDO API

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

1. Edite `teste.json` com os dados do seu problema (veja o formato abaixo).
2. Rode o script:

```bash
python otimizacao_lindo_simples.py
```

## Formato do arquivo JSON

```json
{
    "direcao_otimizacao": -1,
    "coeficientes_objetivo": [3.0, 5.0, 4.0, 2.0, 6.0, 1.0],
    "matriz_restricoes": [
        [2.0, 1.0, 0.0, 0.0, 0.0, 0.0],
        [1.0, 3.0, 1.0, 0.0, 0.0, 0.0],
        [1.0, 0.0, 4.0, 1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 2.0, 3.0, 1.0]
    ],
    "lados_direitos": [10.0, 12.0, 15.0, 20.0],
    "tipos_restricoes": ["L", "L", "L", "L"],
    "limites_inferiores": null,
    "limites_superiores": null
}
```

| Campo                    | Descrição                                                  |
|---------------------------|-------------------------------------------------------------|
| `direcao_otimizacao`      | `-1` para maximizar, `1` para minimizar                     |
| `coeficientes_objetivo`   | Coeficientes de cada variável na função objetivo             |
| `matriz_restricoes`       | Uma linha por restrição, uma coluna por variável             |
| `lados_direitos`          | Lado direito (RHS) de cada restrição                         |
| `tipos_restricoes`        | `"L"` (<=), `"G"` (>=) ou `"E"` (=), uma por restrição        |
| `limites_inferiores`      | Opcional — padrão `0` para todas as variáveis                |
| `limites_superiores`      | Opcional — padrão infinito; use `null` para infinito por variável |

## Saída

O script imprime, nesta ordem: os dados de entrada em formato de equação, e o
resultado da otimização (valor ótimo de Z e valor de cada variável).

## Estrutura

```
.
├── otimizacao_lindo_simples.py   # script principal
├── teste.json                    # exemplo de dados de entrada
├── requirements.txt
└── README.md
```
