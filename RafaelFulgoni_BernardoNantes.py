# ============================================================
# OTIMIZAÇÃO LINEAR COM LINDO API — VERSÃO SIMPLIFICADA
# ============================================================
#
# Resolve um problema de programação linear:
#
#     Maximizar (ou minimizar)  Z = c1*x1 + c2*x2 + ... + cn*xn
#
#     Sujeito a restrições do tipo <=, >= ou =
#
# Os dados do problema (objetivo, restrições, etc.) vêm de um
# arquivo JSON. O código funciona para qualquer número de
# variáveis e restrições, sem precisar ser alterado.
# ============================================================

import json
import os
import numpy as np
import lindo


def resolver_lp(dados):
    """Recebe um dicionário com os dados do problema e resolve com o LINDO."""

    # --- Dados do problema -----------------------------------

    c = np.array(dados["coeficientes_objetivo"], dtype=np.double)
    A = np.array(dados["matriz_restricoes"], dtype=np.double)
    b = np.array(dados["lados_direitos"], dtype=np.double)
    tipos = np.array([t.encode() for t in dados["tipos_restricoes"]], dtype="|S1")
    direcao = dados.get("direcao_otimizacao", -1)  # -1 = maximizar, 1 = minimizar

    n_variaveis = len(c)
    n_restricoes = len(A)

    limite_inf = np.array(dados.get("limites_inferiores") or [0.0] * n_variaveis, dtype=np.double)
    limite_sup = dados.get("limites_superiores") or [lindo.LS_INFINITY] * n_variaveis
    limite_sup = np.array(
        [lindo.LS_INFINITY if v is None else v for v in limite_sup], dtype=np.double
    )

    # --- Converter a matriz (densa) para o formato que o LINDO exige (por colunas) ---

    inicio_colunas = [0]
    coef_matriz = []
    linha_coef = []

    for coluna in range(n_variaveis):
        for linha in range(n_restricoes):
            if A[linha, coluna] != 0.0:
                coef_matriz.append(A[linha, coluna])
                linha_coef.append(linha)
        inicio_colunas.append(len(coef_matriz))

    inicio_colunas = np.array(inicio_colunas, dtype=np.int32)
    coef_matriz = np.array(coef_matriz, dtype=np.double)
    linha_coef = np.array(linha_coef, dtype=np.int32)

    # --- Criar ambiente e modelo do LINDO ---------------------

    chave_licenca = np.array('', dtype='S1024')
    caminho_licenca = os.path.join(os.getenv('LINDOAPI_HOME'), 'license', 'lndapi160.lic')
    lindo.pyLSloadLicenseString(caminho_licenca, chave_licenca)

    erro = np.array([-1], dtype=np.int32)
    ambiente = lindo.pyLScreateEnv(erro, chave_licenca)
    modelo = lindo.pyLScreateModel(ambiente, erro)

    # --- Carregar o problema e resolver ------------------------

    lindo.pyLSloadLPData(
        modelo, n_restricoes, n_variaveis, direcao, 0.0,
        c, b, tipos,
        len(coef_matriz), inicio_colunas, np.asarray(None),
        coef_matriz, linha_coef,
        limite_inf, limite_sup,
    )

    status = np.array([-1], dtype=np.int32)
    lindo.pyLSoptimize(modelo, lindo.LS_METHOD_FREE, status)

    # --- Obter resultado ----------------------------------------

    z = np.array([-1.0], dtype=np.double)
    lindo.pyLSgetInfo(modelo, lindo.LS_DINFO_POBJ, z)

    solucao = np.empty(n_variaveis, dtype=np.double)
    lindo.pyLSgetPrimalSolution(modelo, solucao)

    lindo.pyLSdeleteModel(modelo)
    lindo.pyLSdeleteEnv(ambiente)

    return z[0], solucao


def mostrar_entrada(dados):
    print("=" * 55)
    print("                 DADOS DE ENTRADA")
    print("=" * 55)
    print()
    print("Direção:", "Maximizar" if dados.get("direcao_otimizacao", -1) == -1 else "Minimizar")
    print("Coeficientes da função objetivo:", dados["coeficientes_objetivo"])
    print()
    print("Matriz de restrições:")
    for linha in dados["matriz_restricoes"]:
        print("   ", linha)
    print()
    print("Lados direitos:", dados["lados_direitos"])
    print("Tipos das restrições:", dados["tipos_restricoes"])
    print("Limites inferiores:", dados.get("limites_inferiores"))
    print("Limites superiores:", dados.get("limites_superiores"))


def mostrar_resultado(z, solucao):
    print()
    print("=" * 55)
    print("                 RESULTADO DA OTIMIZAÇÃO")
    print("=" * 55)
    print()
    print(f"Valor ótimo da função objetivo: {z:.4f}")
    print()
    print("Valores das variáveis:")
    for i, v in enumerate(solucao):
        print(f"    x{i+1} = {v:.4f}")
    print()
    print("=" * 55)
    print("             PROBLEMA RESOLVIDO COM SUCESSO!")
    print("=" * 55)


if __name__ == "__main__":

    with open("dados_exemplo.json", "r", encoding="utf-8") as f:
        dados = json.load(f)

    z, solucao = resolver_lp(dados)

    mostrar_entrada(dados)
    mostrar_resultado(z, solucao)