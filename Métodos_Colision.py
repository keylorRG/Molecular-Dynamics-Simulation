# def inicializar_particulas(posiciones, radios, velocidades, angulos, colores):
#     particulas = []
#     for i in range(len(posiciones)):
#         pos = posiciones[i]
#         radio = radios[i]
#         rapidez = velocidades[i]
#         ang = angulos[i]
#         color = colores[i % len(colores)]
#         masa = 1  # Asumimos masa unitaria para simplicidad
#         particulas.append(Particula(pos, radio, masa, rapidez, ang, color))
#     return particulas

# def rebotar_pared(particula, size):
#     if particula.pos[0] >= size[0] - particula.rad:
#         particula.v[0] = -particula.v[0]
#         particula.pos[0] = size[0] - particula.rad
#     elif particula.pos[0] <= particula.rad:
#         particula.v[0] = -particula.v[0]
#         particula.pos[0] = particula.rad
#     if particula.pos[1] >= size[1] - particula.rad:
#         particula.v[1] = -particula.v[1]
#         particula.pos[1] = size[1] - particula.rad
#     elif particula.pos[1] <= particula.rad:
#         particula.v[1] = -particula.v[1]
#         particula.pos[1] = particula.rad

# def choque_elastico(part1, part2):
#     delta_pos = [part1.pos[0] - part2.pos[0], part1.pos[1] - part2.pos[1]]
#     dist = np.linalg.norm(delta_pos)
#     if dist <= (part1.rad + part2.rad):
#         # Normalización del vector de diferencia de posición
#         delta_pos = [delta_pos[0] / dist, delta_pos[1] / dist]
        
#         # Vector unitario tangencial
#         delta_tan = [-delta_pos[1], delta_pos[0]]
        
#         # Proyecciones de velocidad
#         v1n = part1.v[0] * delta_pos[0] + part1.v[1] * delta_pos[1]
#         v1t = part1.v[0] * delta_tan[0] + part1.v[1] * delta_tan[1]
#         v2n = part2.v[0] * delta_pos[0] + part2.v[1] * delta_pos[1]
#         v2t = part2.v[0] * delta_tan[0] + part2.v[1] * delta_tan[1]
        
#         # Nuevas velocidades normales usando colisión elástica unidimensional
#         v1n_prime = (v1n * (part1.masa - part2.masa) + 2 * part2.masa * v2n) / (part1.masa + part2.masa)
#         v2n_prime = (v2n * (part2.masa - part1.masa) + 2 * part1.masa * v1n) / (part2.masa + part1.masa)
        
#         # Conversión a vectores
#         v1n_prime_vec = [v1n_prime * delta_pos[0], v1n_prime * delta_pos[1]]
#         v1t_vec = [v1t * delta_tan[0], v1t * delta_tan[1]]
#         v2n_prime_vec = [v2n_prime * delta_pos[0], v2n_prime * delta_pos[1]]
#         v2t_vec = [v2t * delta_tan[0], v2t * delta_tan[1]]
        
#         # Nuevas velocidades
#         part1.v = [v1n_prime_vec[0] + v1t_vec[0], v1n_prime_vec[1] + v1t_vec[1]]
#         part2.v = [v2n_prime_vec[0] + v2t_vec[0], v2n_prime_vec[1] + v2t_vec[1]]
        
#         # Mover ligeramente las partículas para evitar que se queden pegadas
#         overlap = part1.rad + part2.rad - dist
#         move_by = overlap / 2.0
#         part1.pos[0] += delta_pos[0] * move_by
#         part1.pos[1] += delta_pos[1] * move_by
#         part2.pos[0] -= delta_pos[0] * move_by
#         part2.pos[1] -= delta_pos[1] * move_by

# def actualizar(frame, particulas, size, ax, posiciones_x,dt):
#     # Limpiar el gráfico
#     ax.clear()
#     ax.set_xlim(0, size[0])
#     ax.set_ylim(0, size[1])
    
#     # Determinar el tiempo mínimo hasta el próximo evento
#     tiempos_pared = [p.wall_time_2d(size) for p in particulas]
#     tiempos_pareja = [Particula.pair_time(particulas[i], particulas[j]) for i in range(len(particulas)) for j in range(i+1, len(particulas))]
#     all_tiempos = tiempos_pared + tiempos_pareja
#     all_tiempos.sort()
#     min_tiempo = next(t for t in all_tiempos if t > 1e-14 )  # Umbral de tiempo mínimo

#     tiempo_mover= min(min_tiempo, dt)
#     # Mover las partículas
        
#     for p in particulas:
#         p.mover(tiempo_mover+1e-15)
#     if min_tiempo <= dt:
#         # Verificar colisiones con las paredes
#         for p in particulas:
#             rebotar_pared(p, size)
        
#         # Verificar colisiones entre partículas
#         for i in range(len(particulas)):
#             for j in range(i+1, len(particulas)):
#                 choque_elastico(particulas[i], particulas[j])
    
#     # Capturar las posiciones en x de las partículas
#     posiciones_x.extend([p.pos[0] for p in particulas])
    
#     # Dibujar las partículas
#     for p in particulas:
#         p.display(ax)