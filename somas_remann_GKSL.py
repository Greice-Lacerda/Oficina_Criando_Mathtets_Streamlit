import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Cabeçalho do aplicativo
st.header("Exploração de Somas de Riemann")

# Entradas de dados interativas (Zonas de controle dos Sliders)
a = st.number_input("Limite Inferior (a):", value=0.0)
b = st.number_input("Limite Superior (b):", value=2.0) # Alterado para 2.0 para melhor visualização de x^2
n = st.slider("Número de partições (n):", min_value=2, max_value=100, value=10)

# Definição da função matemática f(x) = x^2
def f(x):
    return x ** 2

# Cálculo do espaçamento (subintervalos)
dx = (b - a) / n
x_part = np.linspace(a, b, n + 1)

# Cálculo da Soma de Riemann à Esquerda
soma_esquerda = np.sum(f(x_part[:-1]) * dx)

# --- CONSTRUÇÃO DO GRÁFICO DINÂMICO ---
fig, ax = plt.subplots(figsize=(8, 5))

# 1. Desenha a curva contínua da função f(x) com alta resolução
x_curva = np.linspace(a, b, 1000)
y_curva = f(x_curva)
ax.plot(x_curva, y_curva, color='red', label='$f(x) = x^2$', linewidth=2)

# 2. Laço para desenhar cada retângulo da partição sobre a função
for i in range(n):
    x_esq = x_part[i]  # Canto esquerdo do retângulo
    altura = f(x_esq)  # Altura definida pelo ponto esquerdo (Soma à Esquerda)
    
    # Desenha o retângulo na tela (patch geométrico)
    ax.add_patch(
        plt.Rectangle(
            (x_esq, 0),          # Ponto inicial (x, y) na base
            dx,                  # Largura do retângulo
            altura,              # Altura do retângulo
            edgecolor='blue',    # Cor da borda
            facecolor='skyblue', # Cor do preenchimento
            alpha=0.4            # Transparência para ver a curva por trás
        )
    )

# Configurações estéticas do gráfico
ax.set_xlabel('Eixo X')
ax.set_ylabel('Eixo Y')
ax.set_title(f'Refinamento da Partição com n = {n}')
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend()

# Força os limites do gráfico a se ajustarem aos dados de entrada
ax.set_xlim(a - 0.1, b + 0.1)
ax.set_ylim(0, f(b) + 0.5)

# --- EXIBIÇÃO NA INTERFACE DO STREAMLIT ---

# Exibe o gráfico gerado
st.pyplot(fig)

# Exibe o valor numérico calculado logo abaixo
st.metric("Soma de Riemann Encontrada (Esquerda)", f"{soma_esquerda:.4f}")