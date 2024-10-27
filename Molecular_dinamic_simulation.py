import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
import math

class Particula:
    def __init__(self, pos, rad, masa, rapidez, ang, color):
        self.pos = pos  # Usamos una lista en lugar de un array de NumPy
        self.rad = rad
        self.masa = masa
        self.ang = ang
        self.rapidez = rapidez
        self.v = [rapidez * np.cos(ang), rapidez * np.sin(ang)]
        self.color = color

    def mover(self, dt):
        self.pos[0] += self.v[0] * dt
        self.pos[1] += self.v[1] * dt

    def display(self, ax):
        circle = plt.Circle(self.pos, self.rad, edgecolor='k', facecolor=self.color)
        ax.add_patch(circle)
        # Longitud fija para la flecha
        arrow_length = 0.1
        # Dirección de la flecha según el ángulo de la velocidad
        direction = np.arctan2(self.v[1], self.v[0])
        end_pos = [self.pos[0] + arrow_length * np.cos(direction), self.pos[1] + arrow_length * np.sin(direction)]
        ax.quiver(self.pos[0], self.pos[1], end_pos[0] - self.pos[0], end_pos[1] - self.pos[1], angles='xy', scale_units='xy', scale=1, color='k')

    def wall_time_2d(self, size):
        tx_right = (size[0] - self.rad - self.pos[0]) / self.v[0] if self.v[0] > 0 else float('inf')
        tx_left = (self.rad - self.pos[0]) / self.v[0] if self.v[0] < 0 else float('inf')
        ty_top = (size[1] - self.rad - self.pos[1]) / self.v[1] if self.v[1] > 0 else float('inf')
        ty_bottom = (self.rad - self.pos[1]) / self.v[1] if self.v[1] < 0 else float('inf')
        return min(tx_right, tx_left, ty_top, ty_bottom)

    def pair_time(part_a, part_b):
        del_x = [part_b.pos[0] - part_a.pos[0], part_b.pos[1] - part_a.pos[1]]
        del_x_sq = del_x[0]**2 + del_x[1]**2
        del_v = [part_b.v[0] - part_a.v[0], part_b.v[1] - part_a.v[1]]
        del_v_sq = del_v[0]**2 + del_v[1]**2
        scal = del_v[0] * del_x[0] + del_v[1] * del_x[1]
        sigma = part_a.rad + part_b.rad
        Upsilon = (2 * scal)**2 - 4 * del_v_sq * (del_x_sq - sigma**2)

        if Upsilon >= 0.0 and scal < 0.0:
            sqrt_Upsilon = math.sqrt(Upsilon)
            del_t1 = ((-2 * scal) + sqrt_Upsilon) / (2 * del_v_sq)
            del_t2 = ((-2 * scal) - sqrt_Upsilon) / (2 * del_v_sq)
            
            # Seleccionar el tiempo mínimo no negativo
            del_t = float('inf')
            if del_t1 >= 0:
                del_t = del_t1
            if del_t2 >= 0 and del_t2 < del_t:
                del_t = del_t2
        else:
            del_t = float('inf')
        return del_t

def inicializar_particulas(posiciones, radios, velocidades, angulos, colores):
    particulas = []
    for i in range(len(posiciones)):
        pos = posiciones[i]
        radio = radios[i]
        rapidez = velocidades[i]
        ang = angulos[i]
        color = colores[i % len(colores)]
        masa = 1  # Asumimos masa unitaria para simplicidad
        particulas.append(Particula(pos, radio, masa, rapidez, ang, color))
    return particulas

def rebotar_pared(particula, size):
    if particula.pos[0] >= size[0] - particula.rad:
        particula.v[0] = -particula.v[0]
        particula.pos[0] = size[0] - particula.rad
    elif particula.pos[0] <= particula.rad:
        particula.v[0] = -particula.v[0]
        particula.pos[0] = particula.rad
    if particula.pos[1] >= size[1] - particula.rad:
        particula.v[1] = -particula.v[1]
        particula.pos[1] = size[1] - particula.rad
    elif particula.pos[1] <= particula.rad:
        particula.v[1] = -particula.v[1]
        particula.pos[1] = particula.rad

def choque_elastico(part1, part2):
    delta_pos = [part1.pos[0] - part2.pos[0], part1.pos[1] - part2.pos[1]]
    dist = np.linalg.norm(delta_pos)
    if dist <= (part1.rad + part2.rad):
        # Normalización del vector de diferencia de posición
        delta_pos = [delta_pos[0] / dist, delta_pos[1] / dist]
        
        # Vector unitario tangencial
        delta_tan = [-delta_pos[1], delta_pos[0]]
        
        # Proyecciones de velocidad
        v1n = part1.v[0] * delta_pos[0] + part1.v[1] * delta_pos[1]
        v1t = part1.v[0] * delta_tan[0] + part1.v[1] * delta_tan[1]
        v2n = part2.v[0] * delta_pos[0] + part2.v[1] * delta_pos[1]
        v2t = part2.v[0] * delta_tan[0] + part2.v[1] * delta_tan[1]
        
        # Nuevas velocidades normales usando colisión elástica unidimensional
        v1n_prime = (v1n * (part1.masa - part2.masa) + 2 * part2.masa * v2n) / (part1.masa + part2.masa)
        v2n_prime = (v2n * (part2.masa - part1.masa) + 2 * part1.masa * v1n) / (part2.masa + part1.masa)
        
        # Conversión a vectores
        v1n_prime_vec = [v1n_prime * delta_pos[0], v1n_prime * delta_pos[1]]
        v1t_vec = [v1t * delta_tan[0], v1t * delta_tan[1]]
        v2n_prime_vec = [v2n_prime * delta_pos[0], v2n_prime * delta_pos[1]]
        v2t_vec = [v2t * delta_tan[0], v2t * delta_tan[1]]
        
        # Nuevas velocidades
        part1.v = [v1n_prime_vec[0] + v1t_vec[0], v1n_prime_vec[1] + v1t_vec[1]]
        part2.v = [v2n_prime_vec[0] + v2t_vec[0], v2n_prime_vec[1] + v2t_vec[1]]
        
        # Mover ligeramente las partículas para evitar que se queden pegadas
        overlap = part1.rad + part2.rad - dist
        move_by = overlap / 2.0
        part1.pos[0] += delta_pos[0] * move_by
        part1.pos[1] += delta_pos[1] * move_by
        part2.pos[0] -= delta_pos[0] * move_by
        part2.pos[1] -= delta_pos[1] * move_by

def actualizar(frame, particulas, size, ax, posiciones_x,dt):
    # Limpiar el gráfico
    ax.clear()
    ax.set_xlim(0, size[0])
    ax.set_ylim(0, size[1])
    
    # Determinar el tiempo mínimo hasta el próximo evento
    tiempos_pared = [p.wall_time_2d(size) for p in particulas]
    tiempos_pareja = [Particula.pair_time(particulas[i], particulas[j]) for i in range(len(particulas)) for j in range(i+1, len(particulas))]
    all_tiempos = tiempos_pared + tiempos_pareja
    all_tiempos.sort()
    min_tiempo = next(t for t in all_tiempos if t > 1e-14 )  # Umbral de tiempo mínimo

    tiempo_mover= min(min_tiempo, dt)
    # Mover las partículas
        
    for p in particulas:
        p.mover(tiempo_mover+1e-15)
    if min_tiempo <= dt:
        # Verificar colisiones con las paredes
        for p in particulas:
            rebotar_pared(p, size)
        
        # Verificar colisiones entre partículas
        for i in range(len(particulas)):
            for j in range(i+1, len(particulas)):
                choque_elastico(particulas[i], particulas[j])
    
    # Capturar las posiciones en x de las partículas
    posiciones_x.extend([p.pos[0] for p in particulas])
    
    # Dibujar las partículas
    for p in particulas:
        p.display(ax)

def generar_densidad_probabilidad(posiciones_x):
    plt.figure(figsize=(12, 6))

    # Subplot 1: Distribución de Densidad de Probabilidad
    plt.subplot(1, 2, 1)
    sns.kdeplot(posiciones_x, bw_adjust=0.5, fill=True)
    plt.title('Distribución de Densidad de Probabilidad de las Posiciones en x')
    plt.xlabel('Posición en x')
    plt.ylabel('Densidad de Probabilidad')

    # Subplot 2: Histograma de las Posiciones en x
    plt.subplot(1, 2, 2)
    plt.hist(posiciones_x, bins=100, alpha=0.6, color='g', edgecolor='black')
    plt.title('Histograma de las Posiciones en x')
    plt.xlabel('Posición en x')
    plt.ylabel('Frecuencia')

    plt.tight_layout()
    plt.show()

# Parámetros de simulación
size = (1, 1)  # Tamaño de la caja normalizado
num_particulas = 4  # Se puede cambiar para aumentar el número de discos
radio = 0.1  # Se puede cambiar para variar el radio de los discos
dt = 0.2
velocidad_min = 0.1
velocidad_max = 0.5

# Datos conocidos
posiciones = [[0.2, 0.2], [0.4, 0.4], [0.6, 0.6], [0.8, 0.8]] #
radios = [radio] * num_particulas
velocidades = [np.random.uniform(velocidad_min, velocidad_max) for _ in range(num_particulas)]
angulos = [np.random.rand() * 2 * np.pi for _ in range(num_particulas)]
colores = ['green', 'orange', 'red', 'blue']

particulas = inicializar_particulas(posiciones, radios, velocidades, angulos, colores)
fig, ax = plt.subplots()
posiciones_x = []

# Configuración de la animación
ani = animation.FuncAnimation(fig, actualizar, frames=120000, fargs=(particulas, size, ax, posiciones_x,dt), interval=20, repeat=False)

# Mostrar la animación
plt.show()
# Generar distribución de densidad de probabilidad después de la simulación
generar_densidad_probabilidad(posiciones_x)
