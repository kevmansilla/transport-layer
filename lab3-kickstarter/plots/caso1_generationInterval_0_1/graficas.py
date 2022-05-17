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
data = pandas.read_csv('caso1_1.csv')
print(data)
print(data.columns)

#Omnet guarda los valores de nuestro "vector" (lista de valores) en una celda, por lo que tengo que esxtraer estos valores
time_gen = data['vectime'].loc[[24]].tolist()
buffer_gen = data['vecvalue'].loc[[24]].tolist()

time_queue = data['vectime'].loc[[25]].tolist()
buffer_queue = data['vecvalue'].loc[[25]].tolist()

time_sink = data['vectime'].loc[[26]].tolist()
buffer_sink = data['vecvalue'].loc[[26]].tolist()

# print(time_gen)
# print(buffer_gen)
# print(time_queue)
# print(buffer_queue)
# print(time_sink)
# print(buffer_sink)

# Los valores que sacamos estan como un solostring separados por comas por lo que tengo que convertirlos a listas para poder graficarlos
time_gen = list(map(float, time_gen[0].split()))
time_queue = list(map(float, time_queue[0].split()))
time_sink = list(map(float, time_sink[0].split()))
buffer_gen = list(map(float, buffer_gen[0].split()))
buffer_queue = list(map(float, buffer_queue[0].split()))
buffer_sink = list(map(float, buffer_sink[0].split()))

# Graficando
# Dibuja el sistema de coordenadas (subgrafo) de la fila 0 y la columna 1, ir significa círculo verde, punto verde

ax1 = plt.subplot(212)
plt.suptitle("Caso 1 (generationInterval = 0.1): Ocupacion de buffers en el sistema")
ax1.plot(82, 33, marker="o", color="gray", label='(82,33)')
ax1.plot(time_gen, buffer_gen, color='gray')
plt.legend()
ax1.set_title('NodeTx')

ax2 = plt.subplot(221)
ax2.plot(time_queue, buffer_queue, color='blue')
ax2.set_title('Queue')

ax3 = plt.subplot(222)
ax3.plot(42, 200, marker="o", color="green", label='(42,200)')
ax3.plot(time_sink, buffer_sink, color='green')
ax3.set_title('NodeRx')
plt.grid()

ax1.set_xlabel('tiempo de simulacion')
ax2.set_ylabel('Cantidad de paquetes en el buffer')
plt.grid()
plt.legend()
plt.show()

#Agregue en el modelo un contador de paquetes generados y paquetes consumidos
#sacando la info
time_gen = data['vectime'].loc[[24]].tolist()
packets_gen = data['vecvalue'].loc[[24]].tolist()
time_sink = data['vectime'].loc[[26]].tolist()
packets_sink = data['vecvalue'].loc[[26]].tolist()

#dividiendo en listas
time_gen = list(map(float, time_gen[0].split()))
packets_sink = list(map(float, packets_sink[0].split()))
time_sink = list(map(float, time_sink[0].split()))
packets_gen = list(map(float, packets_gen[0].split()))

plt.figure(figsize=(10, 6))
plt.suptitle("Caso 1 (generationInterval = 0.1): Paquetes enviados y recibidos")
sns.barplot(
    x=['Enviados', 'Recibidos'],
    y=[len(packets_gen), len(packets_sink)])
print(len(packets_gen)) #1979
print(len(packets_sink)) #1199
plt.show()
