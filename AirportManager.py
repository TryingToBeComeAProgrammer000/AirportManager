import pygame
import random
import sys
from datetime import datetime, timedelta

# Inicialización de Pygame
pygame.init()

# Dimensiones de la pantalla
WIDTH, HEIGHT = 1200, 850
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gestión de Aeropuerto")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
BROWN = (139, 69, 19)
PINK = (255, 192, 203)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)
DARK_RED = (139, 0, 0)
LIGHT_GRAY = (211, 211, 211)
COLORS_EMPLEADOS = [ORANGE, PINK, LIGHT_BLUE, LIGHT_GREEN, CYAN, YELLOW, PURPLE]

# Fuentes
font = pygame.font.SysFont(None, 30)
font_small = pygame.font.SysFont(None, 24)
font_large = pygame.font.SysFont(None, 40)
font_title = pygame.font.SysFont(None, 60)

# Clases
class Pasajero:
    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.tipo = tipo  # "normal" o "ejecutivo"
        self.estado = "entrando"  # entrando -> facturacion -> seguridad -> embarque -> saliendo
        self.estacion_actual = None
        self.velocidad = 2 if tipo == "normal" else 3
        self.radio = 10 if tipo == "normal" else 15
        self.color = BLUE if tipo == "normal" else PURPLE
        self.tiempo_espera = 0

    def dibujar(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radio)
        tipo_texto = "E" if self.tipo == "ejecutivo" else "N"
        texto = font_small.render(tipo_texto, True, WHITE)
        screen.blit(texto, (self.x - 5, self.y - 10))

    def mover_a(self, destino_x, destino_y):
        dx = destino_x - self.x
        dy = destino_y - self.y
        distancia = max(1, (dx ** 2 + dy ** 2) ** 0.5)
        if distancia < self.velocidad:
            self.x, self.y = destino_x, destino_y
            return True
        else:
            self.x += int(dx / distancia * self.velocidad)
            self.y += int(dy / distancia * self.velocidad)
            return False

class Empleado:
    def __init__(self, x, y, nombre, color, es_temporal=False, fecha_fin=None):
        self.x = x
        self.y = y
        self.nombre = nombre
        self.destino_x = x
        self.destino_y = y
        self.velocidad = 3
        self.radio = 12
        self.color = color
        self.seleccionado = False
        self.es_temporal = es_temporal
        self.fecha_fin = fecha_fin # datetime cuando el contrato termina

    def dibujar(self, screen):
        color = YELLOW if self.seleccionado else self.color
        pygame.draw.circle(screen, color, (self.x, self.y), self.radio)
        pygame.draw.circle(screen, BLACK, (self.x, self.y), self.radio, 2)
        texto = font_small.render("E", True, BLACK)
        screen.blit(texto, (self.x - 5, self.y - 8))
        # Indicador de temporal
        if self.es_temporal:
            temp_texto = font_small.render("T", True, RED)
            screen.blit(temp_texto, (self.x - 5, self.y + 5))

    def mover_a(self, destino_x, destino_y):
        self.destino_x = destino_x
        self.destino_y = destino_y
        dx = destino_x - self.x
        dy = destino_y - self.y
        distancia = max(1, (dx ** 2 + dy ** 2) ** 0.5)
        if distancia < self.velocidad:
            self.x, self.y = destino_x, destino_y
            return True
        else:
            self.x += int(dx / distancia * self.velocidad)
            self.y += int(dy / distancia * self.velocidad)
            return False

    def ir_a_estacion(self, estacion):
        return self.mover_a(estacion.x, estacion.y - 50)

class Estacion:
    def __init__(self, nombre, x, y, capacidad=1):
        self.nombre = nombre
        self.x = x
        self.y = y
        self.capacidad = capacidad
        self.empleados = []
        self.pasajeros_atendiendo = []
        self.cola = []
        self.rect = pygame.Rect(x - 60, y - 30, 120, 60)
        self.tiempo_procesamiento = 0
        self.averiada = False
        self.rect_reparar = pygame.Rect(x + 70, y - 15, 100, 30)  # Botón de reparar

    def dibujar(self, screen):
        # Color según congestión o avería
        if self.averiada:
            color = BLACK
        elif len(self.cola) > 5:
            color = RED
        elif len(self.cola) > 2:
            color = YELLOW
        else:
            color = GREEN
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 3)
        # Mostrar capacidad y empleados
        texto_nombre = font_small.render(f"{self.nombre}", True, BLACK)
        texto_capacidad = font_small.render(f"Cap: {len(self.empleados)}/{self.capacidad}", True, BLACK)
        screen.blit(texto_nombre, (self.x - 50, self.y - 25))
        screen.blit(texto_capacidad, (self.x - 50, self.y))
        # Dibujar empleados en la estación
        for i, empleado in enumerate(self.empleados):
            empleado_x = self.x - 40 + i * 25
            empleado_y = self.y - 50
            pygame.draw.circle(screen, empleado.color, (empleado_x, empleado_y), 8)
            pygame.draw.circle(screen, BLACK, (empleado_x, empleado_y), 8, 1)
            # Indicador de temporal
            if empleado.es_temporal:
                temp_texto = font_small.render("T", True, RED)
                screen.blit(temp_texto, (empleado_x - 5, empleado_y + 5))
        
        # Dibujar botón de reparar si está averiada
        if self.averiada:
            pygame.draw.rect(screen, RED, self.rect_reparar)
            pygame.draw.rect(screen, BLACK, self.rect_reparar, 2)
            texto_reparar = font_small.render("Reparar ($1000)", True, WHITE)
            screen.blit(texto_reparar, (self.rect_reparar.centerx - texto_reparar.get_width() // 2, 
                                       self.rect_reparar.centery - texto_reparar.get_height() // 2))

    def puede_aceptar_pasajero(self):
        return len(self.pasajeros_atendiendo) < len(self.empleados) and not self.averiada

    def aceptar_pasajero(self, pasajero):
        if self.puede_aceptar_pasajero():
            self.pasajeros_atendiendo.append(pasajero)
            return True
        else:
            self.cola.append(pasajero)
            return False

    def procesar_pasajeros(self, dinero, happy_hour=False):
        # Procesar pasajeros que están siendo atendidos
        pasajeros_terminados = []
        for pasajero in self.pasajeros_atendiendo[:]:
            if self.nombre == "Facturación":
                # Tiempo de procesamiento más largo para facturación
                if random.randint(1, 30) == 1:
                    # Cobrar dinero
                    base_amount = 250 if pasajero.tipo == "normal" else 400
                    if happy_hour:
                        dinero += base_amount * 3
                    else:
                        dinero += base_amount
                    pasajeros_terminados.append(pasajero)
                    self.pasajeros_atendiendo.remove(pasajero)
            else:
                # Seguridad y embarque más rápidos
                if random.randint(1, 20) == 1:
                    pasajeros_terminados.append(pasajero)
                    self.pasajeros_atendiendo.remove(pasajero)
        # Mover pasajeros de la cola a atención si hay espacio
        while self.cola and self.puede_aceptar_pasajero():
            pasajero = self.cola.pop(0)
            self.pasajeros_atendiendo.append(pasajero)
        return dinero, pasajeros_terminados

    def agregar_empleado(self, empleado):
        if len(self.empleados) < self.capacidad:
            self.empleados.append(empleado)
            return True
        return False

    def remover_empleado(self, empleado):
        if empleado in self.empleados:
            self.empleados.remove(empleado)
            return True
        return False

    def reparar(self, dinero):
        if self.averiada and dinero >= 1000:
            self.averiada = False
            dinero -= 1000
            return True, dinero
        return False, dinero

class Puerta:
    def __init__(self, nombre, x, y):
        self.nombre = nombre
        self.x = x
        self.y = y

class Tienda:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH - 200, 50, 180, 500)  # Aumentamos altura
        self.precios = {
            "empleado": 500,
            "empleado_temporal": 300, # Precio para empleado temporal
            "estacion": 1000,
            "eficiencia": 4000,
            "supervisor": 4000,
            "publicidad": 3000,
            "puerta_entrada": 5000
        }
        self.comprado = {
            "eficiencia": False,
            "supervisor": False,
            "publicidad": False,
            "puerta_entrada": False
        }
        # Rectángulos para las opciones
        self.rect_empleado = pygame.Rect(WIDTH - 190, 100, 160, 40)
        self.rect_empleado_temporal = pygame.Rect(WIDTH - 190, 150, 160, 40) # Nuevo rectángulo
        self.rect_estacion = pygame.Rect(WIDTH - 190, 200, 160, 40) # Ajustar posición
        self.rect_eficiencia = pygame.Rect(WIDTH - 190, 250, 160, 40) # Ajustar posición
        self.rect_supervisor = pygame.Rect(WIDTH - 190, 300, 160, 40) # Ajustar posición
        self.rect_publicidad = pygame.Rect(WIDTH - 190, 350, 160, 40) # Ajustar posición
        self.rect_puerta_entrada = pygame.Rect(WIDTH - 190, 400, 160, 40) # Ajustar posición

    def dibujar(self, screen, dinero, empleados_actuales):
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 3)
        titulo = font.render("TIENDA", True, BLACK)
        screen.blit(titulo, (self.rect.centerx - 40, self.rect.y + 10))
        
        # Mostrar cantidad de empleados
        texto_empleados = font_small.render(f"Empleados: {len(empleados_actuales)}/15", True, BLACK)
        screen.blit(texto_empleados, (self.rect.centerx - 60, self.rect.y + 32))

        # Opciones de compra con rectángulos
        color_empleado = GRAY if len(empleados_actuales) >= 15 else WHITE
        pygame.draw.rect(screen, color_empleado, self.rect_empleado)
        pygame.draw.rect(screen, BLACK, self.rect_empleado, 2)
        texto_empleado = font_small.render(f"Empleado: ${self.precios['empleado']}", True, BLACK)
        screen.blit(texto_empleado, (self.rect_empleado.centerx - 70, self.rect_empleado.centery - 10))

        # Empleado temporal
        color_temporal = GRAY if len(empleados_actuales) >= 15 else WHITE
        pygame.draw.rect(screen, color_temporal, self.rect_empleado_temporal)
        pygame.draw.rect(screen, BLACK, self.rect_empleado_temporal, 2)
        texto_temporal = font_small.render(f"Empleado Temp: ${self.precios['empleado_temporal']}", True, BLACK)
        screen.blit(texto_temporal, (self.rect_empleado_temporal.centerx - 85, self.rect_empleado_temporal.centery - 10))

        pygame.draw.rect(screen, WHITE, self.rect_estacion)
        pygame.draw.rect(screen, BLACK, self.rect_estacion, 2)
        texto_estacion = font_small.render(f"Estación (+1): ${self.precios['estacion']}", True, BLACK)
        screen.blit(texto_estacion, (self.rect_estacion.centerx - 78, self.rect_estacion.centery - 10))

        # Mejoras únicas
        color_eficiencia = GRAY if self.comprado["eficiencia"] else WHITE
        pygame.draw.rect(screen, color_eficiencia, self.rect_eficiencia)
        pygame.draw.rect(screen, BLACK, self.rect_eficiencia, 2)
        texto_eficiencia = font_small.render("Eficiencia: $4000", True, BLACK)
        screen.blit(texto_eficiencia, (self.rect_eficiencia.centerx - 75, self.rect_eficiencia.centery - 10))

        color_supervisor = GRAY if self.comprado["supervisor"] else WHITE
        pygame.draw.rect(screen, color_supervisor, self.rect_supervisor)
        pygame.draw.rect(screen, BLACK, self.rect_supervisor, 2)
        texto_supervisor = font_small.render("Supervisor: $4000", True, BLACK)
        screen.blit(texto_supervisor, (self.rect_supervisor.centerx - 75, self.rect_supervisor.centery - 10))

        color_publicidad = GRAY if self.comprado["publicidad"] else WHITE
        pygame.draw.rect(screen, color_publicidad, self.rect_publicidad)
        pygame.draw.rect(screen, BLACK, self.rect_publicidad, 2)
        texto_publicidad = font_small.render("Publicidad: $3000", True, BLACK)
        screen.blit(texto_publicidad, (self.rect_publicidad.centerx - 70, self.rect_publicidad.centery - 10))

        color_puerta = GRAY if self.comprado["puerta_entrada"] else WHITE
        pygame.draw.rect(screen, color_puerta, self.rect_puerta_entrada)
        pygame.draw.rect(screen, BLACK, self.rect_puerta_entrada, 2)
        texto_puerta = font_small.render("Puerta Entrada: $5000", True, BLACK)
        screen.blit(texto_puerta, (self.rect_puerta_entrada.centerx - 85, self.rect_puerta_entrada.centery - 10))

        # Dinero
        texto_dinero = font.render(f"${dinero}", True, BLACK)
        screen.blit(texto_dinero, (WIDTH - 150, 10))

    def comprar_empleado(self, dinero, empleados_actuales):
        if dinero >= self.precios["empleado"] and len(empleados_actuales) < 15:
            dinero -= self.precios["empleado"]
            self.precios["empleado"] += 1000  # Aumentar precio para la próxima compra
            return True, dinero
        return False, dinero

    def comprar_empleado_temporal(self, dinero, empleados_actuales):
        if dinero >= self.precios["empleado_temporal"] and len(empleados_actuales) < 15:
            dinero -= self.precios["empleado_temporal"]
            # El precio del temporal no aumenta
            return True, dinero
        return False, dinero

    def comprar_estacion(self, dinero):
        if dinero >= self.precios["estacion"]:
            dinero -= self.precios["estacion"]
            self.precios["estacion"] += 2000  # Aumentar precio para la próxima compra
            return True, dinero
        return False, dinero

    def comprar_eficiencia(self, dinero):
        if not self.comprado["eficiencia"] and dinero >= self.precios["eficiencia"]:
            dinero -= self.precios["eficiencia"]
            self.comprado["eficiencia"] = True
            return True, dinero
        return False, dinero

    def comprar_supervisor(self, dinero):
        if not self.comprado["supervisor"] and dinero >= self.precios["supervisor"]:
            dinero -= self.precios["supervisor"]
            self.comprado["supervisor"] = True
            return True, dinero
        return False, dinero

    def comprar_publicidad(self, dinero):
        if not self.comprado["publicidad"] and dinero >= self.precios["publicidad"]:
            dinero -= self.precios["publicidad"]
            self.comprado["publicidad"] = True
            return True, dinero
        return False, dinero

    def comprar_puerta_entrada(self, dinero):
        if not self.comprado["puerta_entrada"] and dinero >= self.precios["puerta_entrada"]:
            dinero -= self.precios["puerta_entrada"]
            self.comprado["puerta_entrada"] = True
            return True, dinero
        return False, dinero

# Funciones para el menú
def dibujar_menu(screen):
    screen.fill(WHITE)
    
    # Título del juego
    titulo = font_title.render("GESTIÓN DE AEROPUERTO", True, BLACK)
    screen.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 150))
    
    # Botón Jugar
    boton_jugar = pygame.Rect(WIDTH // 2 - 100, 300, 200, 50)
    pygame.draw.rect(screen, GREEN, boton_jugar)
    pygame.draw.rect(screen, BLACK, boton_jugar, 2)
    texto_jugar = font.render("JUGAR", True, BLACK)
    screen.blit(texto_jugar, (boton_jugar.centerx - texto_jugar.get_width() // 2, 
                              boton_jugar.centery - texto_jugar.get_height() // 2))
    
    # Botón Salir
    boton_salir = pygame.Rect(WIDTH // 2 - 100, 400, 200, 50)
    pygame.draw.rect(screen, RED, boton_salir)
    pygame.draw.rect(screen, BLACK, boton_salir, 2)
    texto_salir = font.render("SALIR", True, BLACK)
    screen.blit(texto_salir, (boton_salir.centerx - texto_salir.get_width() // 2, 
                              boton_salir.centery - texto_salir.get_height() // 2))
    
    return boton_jugar, boton_salir

# Inicializar variables del juego
def inicializar_juego():
    # Crear puertas de entrada
    puertas = [
        Puerta("Puerta 1", 100, 150),
        Puerta("Puerta 2", 100, 350),
        Puerta("Puerta 3", 100, 550)
    ]

    # Crear puertas de abordaje (salida)
    puertas_abordaje = [
        Puerta("Abordaje", WIDTH - 100, 700)
    ]

    # Crear estaciones iniciales
    facturacion = Estacion("Facturación", 400, 150, capacidad=1)
    seguridad = Estacion("Seguridad", 600, 350, capacidad=1)
    embarque = Estacion("Embarque", 800, 550, capacidad=1)
    estaciones = [facturacion, seguridad, embarque]

    # Crear empleados iniciales con colores diferentes
    empleados = []
    for i in range(2):
        color = COLORS_EMPLEADOS[i % len(COLORS_EMPLEADOS)]
        empleado = Empleado(300 + i * 30, 30, f"Empleado {i+1}", color)
        empleados.append(empleado)

    # Asignar empleados a estaciones iniciales
    facturacion.agregar_empleado(empleados[0])
    seguridad.agregar_empleado(empleados[1])

    # Lista de pasajeros
    pasajeros = []

    # Dinero
    dinero = 1000

    # Tienda
    tienda = Tienda()

    # Reloj y tiempo
    hora_actual = datetime(2025, 7, 24, 6, 0)  # Comenzar a las 6:00 AM
    intervalo_base = 1500  # Intervalo base en milisegundos

    # Variables de juego
    empleado_seleccionado = None
    ultimo_intervalo = intervalo_base
    
    return (puertas, puertas_abordaje, facturacion, seguridad, embarque, estaciones, 
            empleados, pasajeros, dinero, tienda, hora_actual, intervalo_base, 
            empleado_seleccionado, ultimo_intervalo)

# Función para obtener multiplicador de tráfico según la hora
def obtener_multiplicador_trafico(hora):
    hora_dia = hora.hour
    # Horas pico: 7-9 AM, 12-2 PM, 5-7 PM
    if (7 <= hora_dia <= 9) or (12 <= hora_dia <= 14) or (17 <= hora_dia <= 19):
        base = 4
    # Horas moderadas: 10-11 AM, 3-4 PM, 8-10 PM
    elif (10 <= hora_dia <= 11) or (15 <= hora_dia <= 16) or (20 <= hora_dia <= 22):
        base = 3
    # Horas bajas: resto del día
    else:
        base = 2
    # Aplicar publicidad si está comprada
    if tienda.comprado["publicidad"]:
        base = int(base * 1.15)  # 15% más de tráfico
    return base, RED if base == 4 else YELLOW if base == 3 else GREEN

# Verificar si es happy hour
def es_happy_hour(hora):
    # Happy hour cada 6 horas: 00:00, 06:00, 12:00, 18:00
    minutos_totales = hora.hour * 60 + hora.minute
    return minutos_totales % 360 == 0  # 360 minutos = 6 horas

# Reloj
clock = pygame.time.Clock()

# Estado del juego
MENU = 0
JUGANDO = 1
estado = MENU

# Generación de nuevos pasajeros
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 1500)  # Valor inicial, se actualizará dinámicamente

# Evento de avería
AVERIA_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(AVERIA_EVENT, random.randint(10000, 30000))  # Primera avería entre 10 y 30 segundos

# Bucle principal
running = True
while running:
    if estado == MENU:
        boton_jugar, boton_salir = dibujar_menu(screen)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if boton_jugar.collidepoint(mouse_x, mouse_y):
                    estado = JUGANDO
                    # Inicializar variables del juego
                    (puertas, puertas_abordaje, facturacion, seguridad, embarque, estaciones, 
                     empleados, pasajeros, dinero, tienda, hora_actual, intervalo_base, 
                     empleado_seleccionado, ultimo_intervalo) = inicializar_juego()
                elif boton_salir.collidepoint(mouse_x, mouse_y):
                    running = False
                    
    elif estado == JUGANDO:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == SPAWN_EVENT:
                # Actualizar hora (avanzar 30 minutos por cada evento de spawn)
                hora_actual += timedelta(minutes=30)
                
                # Verificar y remover empleados temporales que hayan expirado
                for empleado in empleados[:]:
                    if empleado.es_temporal and empleado.fecha_fin and hora_actual >= empleado.fecha_fin:
                        # Remover de cualquier estación donde esté
                        for estacion in estaciones:
                            if empleado in estacion.empleados:
                                estacion.remover_empleado(empleado)
                        empleados.remove(empleado)

                # Obtener multiplicador de tráfico
                multiplicador, _ = obtener_multiplicador_trafico(hora_actual)
                # Generar pasajeros según el multiplicador
                for _ in range(multiplicador):
                    puerta = random.choice(puertas)
                    tipo = random.choices(["normal", "ejecutivo"], weights=[0.7, 0.3])[0]
                    pasajeros.append(Pasajero(puerta.x, puerta.y, tipo))
                # Actualizar intervalo de generación (más frecuente en horas pico)
                nuevo_intervalo = max(500, intervalo_base // multiplicador)
                if nuevo_intervalo != ultimo_intervalo:
                    pygame.time.set_timer(SPAWN_EVENT, nuevo_intervalo)
                    ultimo_intervalo = nuevo_intervalo
            elif event.type == AVERIA_EVENT:
                # Generar una avería aleatoria en una estación
                if estaciones:  # Solo si hay estaciones
                    estacion_averiada = random.choice(estaciones)
                    estacion_averiada.averiada = True
                # Programar la próxima avería
                pygame.time.set_timer(AVERIA_EVENT, random.randint(10000, 30000))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Click en tienda
                if tienda.rect_empleado.collidepoint(mouse_x, mouse_y):
                    # Comprar empleado
                    comprado, dinero = tienda.comprar_empleado(dinero, empleados)
                    if comprado:
                        color = COLORS_EMPLEADOS[len(empleados) % len(COLORS_EMPLEADOS)]
                        nuevo_empleado = Empleado(300 + len(empleados) * 30, 30, f"Empleado {len(empleados) + 1}", color)
                        empleados.append(nuevo_empleado)
                elif tienda.rect_empleado_temporal.collidepoint(mouse_x, mouse_y):
                    # Comprar empleado temporal
                    comprado, dinero = tienda.comprar_empleado_temporal(dinero, empleados)
                    if comprado:
                        color = COLORS_EMPLEADOS[len(empleados) % len(COLORS_EMPLEADOS)]
                        # Calcular fecha de finalización (una semana después)
                        fecha_fin = hora_actual + timedelta(weeks=1)
                        nuevo_empleado = Empleado(300 + len(empleados) * 30, 30, f"Empleado T{len(empleados) + 1}", color, es_temporal=True, fecha_fin=fecha_fin)
                        empleados.append(nuevo_empleado)
                elif tienda.rect_estacion.collidepoint(mouse_x, mouse_y):
                    # Comprar capacidad de estación
                    comprado, dinero = tienda.comprar_estacion(dinero)
                    if comprado:
                        # Aumentar capacidad de una estación aleatoria
                        random.choice(estaciones).capacidad += 1
                elif tienda.rect_eficiencia.collidepoint(mouse_x, mouse_y):
                    # Comprar mejora de eficiencia
                    comprado, dinero = tienda.comprar_eficiencia(dinero)
                    if comprado:
                        # Aplicar mejora (se aplica en la lógica de procesamiento)
                        pass
                elif tienda.rect_supervisor.collidepoint(mouse_x, mouse_y):
                    # Comprar supervisor
                    comprado, dinero = tienda.comprar_supervisor(dinero)
                    if comprado:
                        # Aplicar mejora (se aplica en la lógica de procesamiento)
                        pass
                elif tienda.rect_publicidad.collidepoint(mouse_x, mouse_y):
                    # Comprar publicidad
                    comprado, dinero = tienda.comprar_publicidad(dinero)
                    if comprado:
                        # La mejora se aplica automáticamente en obtener_multiplicador_trafico
                        pass
                elif tienda.rect_puerta_entrada.collidepoint(mouse_x, mouse_y):
                    # Comprar cuarta puerta de entrada
                    comprado, dinero = tienda.comprar_puerta_entrada(dinero)
                    if comprado:
                        puertas.append(Puerta("Puerta 4", 100, 250))
                # Click en empleados
                for empleado in empleados:
                    distancia = ((empleado.x - mouse_x) ** 2 + (empleado.y - mouse_y) ** 2) ** 0.5
                    if distancia <= empleado.radio:
                        # Seleccionar/deseleccionar empleado
                        if empleado_seleccionado == empleado:
                            empleado_seleccionado = None
                        else:
                            empleado_seleccionado = empleado
                        break
                # Click en estaciones (para mover empleado seleccionado)
                if empleado_seleccionado:
                    for estacion in estaciones:
                        if estacion.rect.collidepoint(mouse_x, mouse_y):
                            # Mover empleado a esta estación
                            if estacion.agregar_empleado(empleado_seleccionado):
                                # Remover de estación anterior
                                for otra_estacion in estaciones:
                                    if empleado_seleccionado in otra_estacion.empleados and otra_estacion != estacion:
                                        otra_estacion.remover_empleado(empleado_seleccionado)
                                        break
                            empleado_seleccionado = None
                            break
                # Click en botones de reparar
                for estacion in estaciones:
                    if estacion.averiada and estacion.rect_reparar.collidepoint(mouse_x, mouse_y):
                        reparado, dinero = estacion.reparar(dinero)
                        if reparado:
                            pass  # La estación ya no está averiada

        # Dibujar puertas de entrada
        for p in puertas:
            pygame.draw.circle(screen, GRAY, (p.x, p.y), 20)
            pygame.draw.circle(screen, BLACK, (p.x, p.y), 20, 2)
            texto = font_small.render(p.nombre, True, BLACK)
            screen.blit(texto, (p.x - 30, p.y - 10))

        # Dibujar puertas de abordaje
        for p in puertas_abordaje:
            pygame.draw.circle(screen, GREEN, (p.x, p.y), 20)
            pygame.draw.circle(screen, BLACK, (p.x, p.y), 20, 2)
            texto = font_small.render(p.nombre, True, BLACK)
            screen.blit(texto, (p.x - 35, p.y - 10))

        # Dibujar estaciones
        for e in estaciones:
            e.dibujar(screen)

        # Procesar estaciones
        happy_hour_active = es_happy_hour(hora_actual)
        for estacion in estaciones:
            dinero, pasajeros_terminados = estacion.procesar_pasajeros(dinero, happy_hour_active)
            # Liberar pasajeros terminados
            for pasajero in pasajeros_terminados:
                if estacion == facturacion:
                    pasajero.estado = "yendo_seguridad"
                elif estacion == seguridad:
                    pasajero.estado = "yendo_embarque"
                elif estacion == embarque:
                    pasajero.estado = "saliendo"

        # Actualizar pasajeros
        for p in pasajeros[:]:
            if p.estado == "entrando":
                if p.mover_a(facturacion.x, facturacion.y):
                    p.estado = "en_facturacion"
                    if not facturacion.aceptar_pasajero(p):
                        p.estado = "esperando_facturacion"
            elif p.estado == "esperando_facturacion":
                if facturacion.puede_aceptar_pasajero():
                    if facturacion.aceptar_pasajero(p):
                        p.estado = "en_facturacion"
            elif p.estado == "yendo_seguridad":
                if p.mover_a(seguridad.x, seguridad.y):
                    p.estado = "en_seguridad"
                    if not seguridad.aceptar_pasajero(p):
                        p.estado = "esperando_seguridad"
            elif p.estado == "esperando_seguridad":
                if seguridad.puede_aceptar_pasajero():
                    if seguridad.aceptar_pasajero(p):
                        p.estado = "en_seguridad"
            elif p.estado == "yendo_embarque":
                if p.mover_a(embarque.x, embarque.y):
                    p.estado = "en_embarque"
                    if not embarque.aceptar_pasajero(p):
                        p.estado = "esperando_embarque"
            elif p.estado == "esperando_embarque":
                if embarque.puede_aceptar_pasajero():
                    if embarque.aceptar_pasajero(p):
                        p.estado = "en_embarque"
            elif p.estado == "en_embarque":
                pass  # Se maneja en procesar_pasajeros
            elif p.estado == "saliendo":
                # Elegir una puerta de abordaje aleatoria
                puerta_abordaje = random.choice(puertas_abordaje)
                if p.mover_a(puerta_abordaje.x, puerta_abordaje.y):
                    if p in pasajeros:
                        pasajeros.remove(p)
            p.dibujar(screen)

        # Actualizar empleados
        for empleado in empleados:
            if empleado.destino_x != empleado.x or empleado.destino_y != empleado.y:
                empleado.mover_a(empleado.destino_x, empleado.destino_y)
            empleado.dibujar(screen)

        # Dibujar tienda
        tienda.dibujar(screen, dinero, empleados)

        # Mostrar empleado seleccionado
        if empleado_seleccionado:
            texto_seleccion = font.render("Empleado seleccionado - Click en estación", True, BLACK)
            screen.blit(texto_seleccion, (WIDTH // 2 - 200, HEIGHT - 80))

        # Mostrar estadísticas
        total_pasajeros = len(pasajeros)
        cola_total = sum(len(e.cola) for e in estaciones)
        texto_stats = font_small.render(f"Pasajeros: {total_pasajeros} | Cola: {cola_total}", True, BLACK)
        screen.blit(texto_stats, (10, 10))

        # Mostrar reloj y hora
        multiplicador, color_reloj = obtener_multiplicador_trafico(hora_actual)
        hora_texto = hora_actual.strftime("%H:%M")
        texto_hora = font.render(f"Hora: {hora_texto}", True, color_reloj)
        screen.blit(texto_hora, (10, 40))

        # Mostrar nivel de tráfico
        nivel_trafico = "Alto" if multiplicador == 4 else "Medio" if multiplicador == 3 else "Bajo"
        texto_trafico = font_small.render(f"Tráfico: {nivel_trafico} (x{multiplicador})", True, color_reloj)
        screen.blit(texto_trafico, (10, 70))

        # Mostrar happy hour si está activa
        if happy_hour_active:
            texto_happy = font.render("HAPPY HOUR - INGRESOS x3", True, YELLOW)
            screen.blit(texto_happy, (WIDTH // 2 - 150, 10))

        pygame.display.flip()
        clock.tick(60)

pygame.quit()
sys.exit()