# def generar_densidad_probabilidad(posiciones_x):
#     plt.figure(figsize=(12, 6))

#     # Subplot 1: Distribución de Densidad de Probabilidad
#     plt.subplot(1, 2, 1)
#     sns.kdeplot(posiciones_x, bw_adjust=0.5, fill=True)
#     plt.title('Distribución de Densidad de Probabilidad de las Posiciones en x')
#     plt.xlabel('Posición en x')
#     plt.ylabel('Densidad de Probabilidad')

#     # Subplot 2: Histograma de las Posiciones en x
#     plt.subplot(1, 2, 2)
#     plt.hist(posiciones_x, bins=100, alpha=0.6, color='g', edgecolor='black')
#     plt.title('Histograma de las Posiciones en x')
#     plt.xlabel('Posición en x')
#     plt.ylabel('Frecuencia')

#     plt.tight_layout()
#     plt.show()

# # Parámetros de simulación
# size = (1, 1)  # Tamaño de la caja normalizado
# num_particulas = 4  # Se puede cambiar para aumentar el número de discos
# radio = 0.1  # Se puede cambiar para variar el radio de los discos
# dt = 0.2
# velocidad_min = 0.1
# velocidad_max = 0.5

# # Datos conocidos
# posiciones = [[0.2, 0.2], [0.4, 0.4], [0.6, 0.6], [0.8, 0.8]] #
# radios = [radio] * num_particulas
# velocidades = [np.random.uniform(velocidad_min, velocidad_max) for _ in range(num_particulas)]
# angulos = [np.random.rand() * 2 * np.pi for _ in range(num_particulas)]
# colores = ['green', 'orange', 'red', 'blue']

# particulas = inicializar_particulas(posiciones, radios, velocidades, angulos, colores)
# fig, ax = plt.subplots()
# posiciones_x = []

# # Configuración de la animación
# ani = animation.FuncAnimation(fig, actualizar, frames=120000, fargs=(particulas, size, ax, posiciones_x,dt), interval=20, repeat=False)

# # Mostrar la animación
# plt.show()
# # Generar distribución de densidad de probabilidad después de la simulación
# generar_densidad_probabilidad(posiciones_x)
