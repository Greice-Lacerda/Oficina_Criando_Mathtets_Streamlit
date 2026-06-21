import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Somas de Riemann e Altíssima Descontinuidade")
st.markdown(
    r"""
Este *mathlet* explora o comportamento das Somas de Riemann ao confrontarem funções 
com infinitas descontinuidades. Analisaremos a **Função de Dirichlet Modificada** e a 
**Função de Thomae**, evidenciando o conflito entre o discreto numérico e o contínuo analítico.
"""
)

# -----------------------------------------------------------------------------
# Painel Lateral - Parâmetros
# -----------------------------------------------------------------------------
st.sidebar.header("Configurações do Experimento")
funcao_escolhida = st.sidebar.selectbox(
    "Escolha a Função:", 
    ["Dirichlet Numérica (Amostragem)", "Thomae (Popcorn Function)"]
)
n = st.sidebar.slider("Número de subintervalos (n):", min_value=10, max_value=2000, value=100, step=10)
tipo_ponto = st.sidebar.selectbox("Ponto Amostral (c_i):", ["Esquerda", "Direita", "Ponto Médio"])

# Intervalo fixo em [0, 1] para simplificar a análise de racionalidade
a, b = 0.0, 1.0
dx = (b - a) / n

# -----------------------------------------------------------------------------
# Definição das Funções Patológicas
# -----------------------------------------------------------------------------
def funcao_dirichlet_computacional(x):
    """
    Na máquina, os floats possuem precisão finita (são todos racionais).
    Para simular o conflito, introduzimos um ruído flutuante ou testamos
    a representabilidade binária aproximada.
    """
    # Como np.linspace gera floats, simulamos a descontinuidade testando se 
    # o float multiplicado por uma grande base se comporta de forma "par/ímpar" 
    # ou usamos uma aproximação senoidal de alta frequência para quebrar o padrão.
    return np.where(np.sin(1000 * np.pi * x) > 0, 1.0, 0.0)

def funcao_thomae(x):
    """
    Retorna 1/q se x = p/q (racional irredutível) e 0 se irracional.
    Aproximação numérica baseada em tolerância de denominador para float.
    """
    y = np.zeros_like(x)
    for q in range(1, 51): # Testa denominadores até 50
        # Se x * q estiver muito próximo de um inteiro, encontramos um racional p/q
        proximo_inteiro = np.round(x * q)
        mascara = np.abs(x * q - proximo_inteiro) < 1e-6
        y[mascara] = np.maximum(y[mascara], 1.0 / q)
    return y

# -----------------------------------------------------------------------------
# Cálculo da Partição e Alturas
# -----------------------------------------------------------------------------
if tipo_ponto == "Esquerda":
    c_i = np.linspace(a, b - dx, n)
elif tipo_ponto == "Direita":
    c_i = np.linspace(a + dx, b, n)
else: # Ponto Médio
    c_i = np.linspace(a + dx/2, b - dx/2, n)

# Avaliação das alturas dependendo da escolha do usuário
if funcao_escolhida == "Dirichlet Numérica (Amostragem)":
    f_c = funcao_dirichlet_computacional(c_i)
    nome_f = r"Dirichlet\text{ (Aproximada)}"
else:
    f_c = funcao_thomae(c_i)
    nome_f = r"Thomae\text{ (Popcorn)}"

# Soma de Riemann
soma_riemann = np.sum(f_c * dx)

# -----------------------------------------------------------------------------
# Renderização Gráfica
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5))

# Malha densa de fundo para "sugerir" o comportamento da função real
x_fundo = np.linspace(0, 1, 5000)
if funcao_escolhida == "Dirichlet Numérica (Amostragem)":
    y_fundo = funcao_dirichlet_computacional(x_fundo)
    ax.scatter(x_fundo, y_fundo, color="gray", s=0.5, alpha=0.3, label="Nuvem de Pontos da Função")
else:
    y_fundo = funcao_thomae(x_fundo)
    ax.scatter(x_fundo, y_fundo, color="gray", s=1, alpha=0.5, label="Pontos de Thomae (1/q)")

# Desenho dos retângulos da Soma de Riemann
for i in range(n):
    # Coordenada x inicial do retângulo depende do tipo de ponto amostral usado
    x_ret = c_i[i] - (0 if tipo_ponto == "Esquerda" else (dx if tipo_ponto == "Direita" else dx/2))
    rect = plt.Rectangle(
        (x_ret, 0), dx, f_c[i],
        edgecolor="blue", facecolor="blue", alpha=0.2, linewidth=0.5
    )
    ax.add_patch(rect)

ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.1, 1.1)
ax.set_xlabel("x")
ax.set_ylabel("f(x)")
ax.set_title(f"Soma de Riemann para ${nome_f}$ com $n = {n}$")
ax.grid(True, linestyle="--", alpha=0.3)
ax.legend()

st.pyplot(fig)

# Métrica
st.metric(label="Valor Calculado da Soma de Riemann ($S_n$)", value=f"{soma_riemann:.5f}")