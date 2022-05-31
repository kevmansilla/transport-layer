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
data = pandas.read_csv('caso1_0_1.csv')
print(data)
print(data.columns)

# 21 -> Network.nodeTx.traTx
# 22 -> q1
# 23 -> Network.nodeRx.traRx
# 24 -> q2
# 25 -> Network.nodeRx.sink
# 26 -> Network.nodeRx.traRx (no muy necesario)

### Cuento numeroo de paquetes enviados y recibidos

#Agregue en el modelo un contador de paquetes generados y paquetes consumidos
#sacando la info
packets_gen = data['vecvalue'].loc[[21]].tolist()
packets_sink = data['vecvalue'].loc[[25]].tolist()

#dividiendo en listas
packets_sink = list(map(float, packets_sink[0].split()))
packets_gen = list(map(float, packets_gen[0].split()))

print(f"Enviados {len(packets_gen)}")
print(f"Recibidos {len(packets_sink)}")


