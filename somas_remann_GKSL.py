# Cálculo da área sob a curva
2 import streamlit as st
3 import numpy as np
4
5 st. header (" E x p l o r a o de Somas de Riemann ")
6
7 a = st. number_input (" Limite Inferior (a):", value =0.0)
8 b = st. number_input (" Limite Superior (b):", value =1.0)
9 n = st. slider (" N m e r o de p a r t i e s :", 2, 100 , 10)
10
11 dx = (b - a) / n
12 x_part = np. linspace (a, b, n+1)
13
14 # Exemplo de f u n o f(x) = x^2
15 def f(x):
16 return x **2
17
18 soma_esquerda = sum(f( x_part [: -1]) * dx)
19 st. metric (" Soma de Riemann ( Esquerda )", f"{ soma_esquerda :.4f}")