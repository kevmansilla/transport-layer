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
data = pandas.read_csv('caso1_2.csv')
print(data)
print(data.columns)

#Omnet guarda los valores de nuestro "vector" (lista de valores) en una celda, por lo que tengo que esxtraer estos valores
time_tratx = data['vectime'].loc[[21]].tolist()
buffer_tratx = data['vecvalue'].loc[[21]].tolist()

time_q1 = data['vectime'].loc[[22]].tolist()
buffer_q1 = data['vecvalue'].loc[[22]].tolist()

time_trarx = data['vectime'].loc[[23]].tolist()
buffer_trarx = data['vecvalue'].loc[[23]].tolist()

time_q2 = data['vectime'].loc[[24]].tolist()
buffer_q2 = data['vecvalue'].loc[[24]].tolist()

time_sink = data['vectime'].loc[[25]].tolist()
buffer_sink = data['vecvalue'].loc[[25]].tolist()

# Los valores que sacamos estan como un solostring separados por comas por lo que tengo que convertirlos a listas para poder graficarlos
time_trarx = list(map(float, time_trarx[0].split()))
time_tratx = list(map(float, time_tratx[0].split()))
time_sink = list(map(float, time_sink[0].split()))
time_q1 = list(map(float, time_q1[0].split()))
time_q2 = list(map(float, time_q2[0].split()))

buffer_trarx = list(map(float, buffer_trarx[0].split()))
buffer_tratx = list(map(float, buffer_tratx[0].split()))
buffer_sink = list(map(float, buffer_sink[0].split()))
buffer_q1 = list(map(float, buffer_q1[0].split()))
buffer_q2 = list(map(float, buffer_q2[0].split()))

# Graficando
# Dibuja el sistema de coordenadas (subgrafo) de la fila 0 y la columna 1, ir significa círculo verde, punto verde

ax1 = plt.subplot(212)
plt.suptitle("Caso 1 (generationInterval = 1): Ocupacion de buffers en el sistema")
ax1.plot(time_trarx, buffer_trarx, color='gray')
ax1.set_title('traRx')

ax2 = plt.subplot(221)
ax2.plot(time_tratx, buffer_tratx, color='blue')
ax2.set_title('traTx')

ax3 = plt.subplot(222)
ax3.plot(time_sink, buffer_sink, color='green')
ax3.set_title('Sink')
plt.grid()
ax1.set_xlabel('tiempo de simulacion en segundos')
ax2.set_ylabel('Cantidad de paquetes en el buffer')
plt.grid()
plt.show()

### 2
ax1 = plt.subplot(121)
plt.suptitle("Caso 1 (generationInterval = 1): Ocupacion de buffers en el sistema")
ax1.plot(time_q1, buffer_q1, color='gray')
ax1.set_title('Queue1')
ax1.set_xlabel('tiempo de simulacion en segundos')
ax1.set_ylabel('Cantidad de paquetes en el buffer')

ax2 = plt.subplot(122)
ax2.plot(time_q2, buffer_q2, color='blue')
ax2.set_title('Queue2')
ax2.set_xlabel('tiempo de simulacion en segundos')
ax2.set_ylabel('Cantidad de paquetes en el buffer')

plt.grid()
plt.show()

#Agregue en el modelo un contador de paquetes generados y paquetes consumidos
#sacando la info
time_gen = data['vectime'].loc[[21]].tolist()
packets_gen = data['vecvalue'].loc[[21]].tolist()
time_sink = data['vectime'].loc[[25]].tolist()
packets_sink = data['vecvalue'].loc[[25]].tolist()

#dividiendo en listas
time_gen = list(map(float, time_gen[0].split()))
packets_sink = list(map(float, packets_sink[0].split()))
time_sink = list(map(float, time_sink[0].split()))
packets_gen = list(map(float, packets_gen[0].split()))

plt.figure(figsize=(10, 6))
plt.suptitle("Caso 1 (generationInterval = 1): Paquetes enviados y recibidos")
sns.barplot(
    x=['Enviados', 'Recibidos'],
    y=[len(packets_gen), len(packets_sink)])
plt.text(1.25, 1.25, len(packets_sink), horizontalalignment='right',
         verticalalignment='top', fontsize=15)
plt.text(.25, .25, len(packets_gen), horizontalalignment='left',
         verticalalignment='top', fontsize=15)
plt.ylabel("Número de paquetes")
plt.show()
