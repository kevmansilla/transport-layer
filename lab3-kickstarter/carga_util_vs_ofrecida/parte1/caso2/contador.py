# Paquetes
import matplotlib.pyplot as plt
import pandas
import seaborn as sns
import io
import requests

import numpy as np
import matplotlib.gridspec as gridspec

sns.set_style('darkgrid')
sns.set_context(context='talk', font_scale=1.2)

# Cargo base
data = pandas.read_csv('caso2_0_1.csv')
print(data)
print(data.columns)

#Agregue en el modelo un contador de paquetes generados y paquetes consumidos
#sacando la info
packets_gen = data['vecvalue'].loc[[24]].tolist()
packets_sink = data['vecvalue'].loc[[26]].tolist()

#dividiendo en listas
packets_sink = list(map(float, packets_sink[0].split()))
packets_gen = list(map(float, packets_gen[0].split()))

print(f"Enviados {len(packets_gen)}")
print(f"Recibidos {len(packets_sink)}")
