import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuração inicial com layout amplo
st.set_page_config(page_title="Mathlet: Detetive de Patologias", layout="wide")

# Redução de margens nativas do Streamlit via CSS para economizar espaço vertical
st.markdown(
    """
    <style>
        .block-container {padding-top: 1rem; padding-bottom: 0rem;}
        h1 {margin-bottom: 0rem; padding-bottom: 0rem; font-size: 2rem !important;}
    </style>
    """, 
    unsafe_allow_html=True
)

st.title("Laboratório de Análise Real: Investigando Descontinuidades")

# --- BARRA LATERAL DE CONTROLES ---
st.sidebar.header("1. Seleção da Patologia")
funcao_escolhida = st.sidebar.selectbox(
    "Escolha a função para análise:",
    [
        "Oscilação Infinita: sin(1/x)",
        "Função Degrau (Salto)",
        "Descontinuidade Removível (Ponto Deslocado)",
        "Descontinuidade Infinita: 1/x"
    ]
)

st.sidebar.markdown("---")
st.sidebar.header("2. Parâmetros Métricos")

# Ajustado os sliders do ponto 'a' para permitir varredura condizente com a nova escala [-2.5, 2.5]
if funcao_escolhida in ["Função Degrau (Salto)", "Descontinuidade Removível (Ponto Deslocado)"]:
    ponto_a = st.sidebar.slider("Ponto de análise (a)", min_value=-2.5, max_value=2.5, value=0.0, step=0.01)
else:
    ponto_a = st.sidebar.slider("Ponto de análise (a)", min_value=-1.0, max_value=1.0, value=0.0, step=0.01)

epsilon = st.sidebar.slider("Raio Epsilon (ε)", min_value=0.05, max_value=1.5, value=0.4, step=0.05)
delta = st.sidebar.slider("Raio Delta (δ)", min_value=0.005, max_value=0.6, value=0.1, step=0.005)

st.sidebar.markdown("---")
st.sidebar.header("3. Vigilância Tecnológica")
num_pontos = st.sidebar.slider("Resolução (np.linspace)", min_value=50, max_value=3000, value=1200, step=50)

# --- MODELAGEM DAS FUNÇÕES ---
def calcular_funcao(x, tipo):
    with np.errstate(divide='ignore', invalid='ignore'):
        if tipo == "Oscilação Infinita: sin(1/x)":
            return np.where(x == 0, 0.0, np.sin(1.0 / x))
        elif tipo == "Função Degrau (Salto)":
            return np.where(x < 0, 0.0, 1.0)
        elif tipo == "Descontinuidade Removível (Ponto Deslocado)":
            return np.where(x == 0, 0.7, x**2)
        elif tipo == "Descontinuidade Infinita: 1/x":
            return np.where(x == 0, np.nan, 1.0 / x)

# --- PROCESSAMENTO MATEMÁTICO ---
fa = calcular_funcao(np.array([ponto_a]), funcao_escolhida)[0]

# Alterado o intervalo do linspace para abranger de -2.5 a 2.5
x_valores = np.linspace(-2.5, 2.5, num_pontos)
x_valores = np.sort(np.unique(np.concatenate([x_valores, [ponto_a, ponto_a - delta, ponto_a + delta]])))
y_valores = calcular_funcao(x_valores, funcao_escolhida)

x_vizinhanca = x_valores[(x_valores >= ponto_a - delta) & (x_valores <= ponto_a + delta)]
y_vizinhanca = calcular_funcao(x_vizinhanca, funcao_escolhida)

# Blindagem conceitual para garantir o veredito correto nos pontos críticos
if ponto_a == 0.0 and funcao_escolhida in ["Oscilação Infinita: sin(1/x)", "Função Degrau (Salto)", "Descontinuidade Infinita: 1/x"]:
    condicao_satisfeita = False
elif funcao_escolhida == "Descontinuidade Infinita: 1/x" and np.any(np.isnan(y_vizinhanca)):
    condicao_satisfeita = False
else:
    condicao_satisfeita = np.all(np.abs(y_vizinhanca - fa) < epsilon)

# --- CONSTRUÇÃO DO GRÁFICO (TAMANHO REDUZIDO) ---
fig, ax = plt.subplots(figsize=(8, 3.2))

ax.scatter(x_valores, y_valores, color="black", s=1.2, label="Amostra")

# Faixas de vizinhança
ax.axhspan(fa - epsilon, fa + epsilon, color="blue", alpha=0.12, label=r"$V_\epsilon(f(a))$")
ax.axhline(fa, color="blue", linestyle="--", alpha=0.4, linewidth=1)

ax.axvspan(ponto_a - delta, ponto_a + delta, color="green", alpha=0.12, label=r"$V_\delta(a)$")
ax.axvline(ponto_a, color="green", linestyle="--", alpha=0.4, linewidth=1)

ax.scatter([ponto_a], [fa], color="red", s=40, zorder=5, label=r"$(a, f(a))$")

# Ajustado os limites dos eixos X e Y fixados em [-2.5, 2.5]
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-2.5, 2.5)

ax.axhline(0, color='gray', linewidth=0.5)
ax.axvline(0, color='gray', linewidth=0.5)
ax.legend(loc="upper right", fontsize="x-small")
ax.grid(True, linestyle=":", alpha=0.4)

# Ajuste estrito de margens internas do gráfico
fig.tight_layout()

# Exibição do gráfico centralizado
st.pyplot(fig)

# --- FEEDBACK PEDAGÓGICO COMPACTO ---
if condicao_satisfeita:
    st.success(f"Satisfeita! Para ε = {epsilon}, δ = {delta} prende as imagens na faixa azul.")
else:
    st.error(f"Violada! Há pontos na faixa verde cuja imagem escapou da faixa azul.")

# Nota rápida de diagnóstico
if ponto_a == 0.0:
    if funcao_escolhida == "Oscilação Infinita: sin(1/x)":
        st.info("💡 **Análise:** O comportamento oscilatório impede o limite na origem. Nenhum δ funciona se ε < 1.")
    elif funcao_escolhida == "Função Degrau (Salto)":
        st.info("💡 **Análise:** Limites laterais existem, mas são diferentes ($0$ e $1$). Descontinuidade de salto.")
    elif funcao_escolhida == "Descontinuidade Removível (Ponto Deslocado)":
        st.info("💡 **Análise:** O limite existe ($0$), mas difere do ponto isolado $f(0) = 0.7$.")
    elif funcao_escolhida == "Descontinuidade Infinita: 1/x":
        st.info("💡 **Análise:** O ponto explode para assíntotas verticais, violando a limitação métrica.")