import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# 1. Configuração da Interface Interativa (Streamlit)
# -----------------------------------------------------------------------------
st.title("Visualizador Dinâmico: Somas de Riemann")
st.markdown(
    r"""
Este aplicativo simula o processo de partição e aproximação geométrica 
para a função $f(x) = x^2$ em um intervalo $[a, b]$, utilizando as 
**extremidades esquerdas** dos subintervalos.
"""
)

# Painel lateral para captura de parâmetros pelo usuário
st.sidebar.header("Parâmetros da Partição")
a = st.sidebar.number_input("Extremidade esquerda (a):", value=0.0, step=0.5)
b = st.sidebar.number_input("Extremidade direita (b):", value=2.0, step=0.5)
n = st.sidebar.slider("Número de subintervalos (n):", min_value=1, max_value=200, value=10)

# Validação do intervalo analítico
if a >= b:
    st.error("Erro: A extremidade 'a' deve ser estritamente menor que 'b'.")
    st.stop()

# -----------------------------------------------------------------------------
# 2. Núcleo Matemático Computacional (NumPy)
# -----------------------------------------------------------------------------
# Definição do integrando
def f(x):
    return x**2

# Cálculo da amplitude do subintervalo (dx)
dx = (b - a) / n

# Construção dos pontos amostrais da partição (extremidades esquerdas)
x_esq = np.linspace(a, b - dx, n)
y_esq = f(x_esq)

# Cálculo numérico da Soma de Riemann
soma_riemann = np.sum(y_esq * dx)
# Integral analítica exata para controle e comparação
integral_exata = (b**3 - a**3) / 3.0
erro_absoluto = abs(soma_riemann - integral_exata)

# -----------------------------------------------------------------------------
# 3. Renderização Gráfica (Matplotlib)
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))

# Malha contínua para o traçado suave da função f(x) = x^2
x_curva = np.linspace(a, b, 500)
ax.plot(x_curva, f(x_curva), color="red", label=r"$f(x) = x^2$", linewidth=2)

# Construção e plotagem dos retângulos de aproximação (Patches)
for i in range(n):
    # Coordenada da base inferior esquerda do retângulo i-ésimo: (x_esq[i], 0)
    retangulo = plt.Rectangle(
        (x_esq[i], 0), 
        dx, 
        y_esq[i], 
        edgecolor="blue", 
        facecolor="blue", 
        alpha=0.2,
        linewidth=1
    )
    ax.add_patch(retangulo)

# Configurações estéticas e limites do gráfico
ax.set_xlabel("x")
ax.set_ylabel("f(x)")
ax.set_xlim(a - 0.2, b + 0.2)
ax.set_ylim(0, f(b) * 1.1 if f(b) > 0 else 1.0)
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend()

# Exibição do gráfico na interface do Streamlit
st.pyplot(fig)

# -----------------------------------------------------------------------------
# 4. Painel de Resultados Quantitativos
# -----------------------------------------------------------------------------
col1, col2, col3 = st.columns(3)
col1.metric("Soma de Riemann (S_n)", f"{soma_riemann:.5f}")
col2.metric("Integral Exata", f"{integral_exata:.5f}")
col3.metric("Erro de Aproximação", f"{erro_absoluto:.5f}")