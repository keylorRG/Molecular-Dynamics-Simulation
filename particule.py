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