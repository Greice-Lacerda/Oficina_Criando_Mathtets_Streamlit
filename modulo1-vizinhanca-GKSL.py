import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Interface de usuario
st.title("Visualizador de Vizinhança $V_{\delta}(a)$")

# 1. Parametros da Definicao (Widgets)
# O slider permite a exploracao dinamica dos valores de centro e raio
a = st.slider("Centro (a):", -5.0, 5.0, 0.0)
delta = st.slider("Raio (delta):", 0.1, 2.0, 0.5)

# 2. Construcao do Grafico
fig, ax = plt.subplots(figsize=(10, 2))
ax.axhline(0, color='black', linewidth=1) # Representacao da Reta Real

# 3. Traducao do Rigor para o Grafico
# Destacamos a area que satisfaz a condicao |x - a| < delta
ax.axvspan(a - delta, a + delta, color='green', alpha=0.3, label=f"Vizinhança V_{delta}({a})")

# 4. Marcacao do Ponto Central
ax.scatter([a], [0], color='red', zorder=5, label="Centro (a)")

# Ajustes de visualizacao para foco na topologia da reta
ax.set_xlim(-10, 10)
ax.set_yticks([]) # Remocao do eixo Y para analise unidimensional
ax.legend()

st.pyplot(fig)

# 5. Explicitacao da Condicao Matematica (Utilizando raw strings para LaTeX)
st.latex(rf"x \in \mathbb{{R}} : |x - {a}| < {delta}")