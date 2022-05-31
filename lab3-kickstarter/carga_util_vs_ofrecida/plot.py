# Paquetes
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import io
import requests
import xlrd

import numpy as np
import matplotlib.gridspec as gridspec

sns.set_style('darkgrid')
sns.set_context(context='talk', font_scale=1.2)

# Cargo base

parte1_caso1 = pd.read_excel('carga_util_vs_ofrecida.xlsx', sheet_name='Caso1_parte1')
parte1_caso2 = pd.read_excel('carga_util_vs_ofrecida.xlsx', sheet_name='Caso2_parte1')
parte2_caso1 = pd.read_excel('carga_util_vs_ofrecida.xlsx', sheet_name='Caso1_parte2')
parte2_caso2 = pd.read_excel('carga_util_vs_ofrecida.xlsx', sheet_name='Caso2_parte2')

print(parte1_caso1.columns)

# parte 1 #
## caso 1
c_ofrecida_p1c1 = parte1_caso1['carga_ofrecida(p/s)'].tolist()
c_util_p1c1 = parte1_caso1['carga_util(p/s)'].tolist()

## caso 2
c_ofrecida_p1c2 = parte1_caso2['carga_ofrecida(p/s)'].tolist()
c_util_p1c2 = parte1_caso2['carga_util(p/s)'].tolist()

# parte 2 #
## caso 1
c_ofrecida_p2c1 = parte2_caso1['carga_ofrecida(p/s)'].tolist()
c_util_p2c1 = parte2_caso1['carga_util(p/s)'].tolist()

## caso 2
c_ofrecida_p2c2 = parte2_caso2['carga_ofrecida(p/s)'].tolist()
c_util_p2c2 = parte2_caso2['carga_util(p/s)'].tolist()

# Plots

## Carga util vs ofrecida caso 1
plt.title("Carga útil vs Carga ofrecida (Caso 1, parte 1 vs Caso 1, parte 2)")
plt.plot(c_ofrecida_p1c1, c_util_p1c1, color="blue",
         linewidth=1.0, linestyle="-", label="Caso 1, parte 1")
plt.plot(c_ofrecida_p2c1, c_util_p1c2, color="green",
         linewidth=1.0, linestyle="-", label="Caso 1, parte 2")
plt.xlabel("Carga ofrecida (p/s)", fontsize=13)
plt.ylabel("Carga útil (p/s)", fontsize=13)
plt.legend()
plt.show()

## Carga util vs ofrecida caso 2
plt.title("Carga útil vs Carga ofrecida (Caso 2, parte 1 vs Caso 2, parte 2)")
plt.plot(c_ofrecida_p1c2, c_util_p1c2, color="blue",
         linewidth=1.0, linestyle="-", label="Caso 2, parte 1")
plt.plot(c_ofrecida_p2c2, c_util_p2c2, color="green",
         linewidth=1.0, linestyle="-", label="Caso 2, parte 2")
plt.xlabel("Carga ofrecida (p/s)", fontsize=13)
plt.ylabel("Carga útil (p/s)", fontsize=13)
plt.legend()
plt.show()
