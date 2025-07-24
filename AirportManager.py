import pygame
import random
import sys
from datetime import datetime, timedelta

pygame.init()

WIDTH, HEIGHT = 1200, 850
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gestión de Aeropuerto")

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
        self.tipo = tipo  
        self.estado = "entrando"  
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
        self.fecha_fin = fecha_fin 

    def dibujar(self, screen):
        color = YELLOW if self.seleccionado else self.color
        pygame.draw.circle(screen, color, (self.x, self.y), self.radio)
        pygame.draw.circle(screen, BLACK, (self.x, self.y), self.radio, 2)
        texto = font_small.render("E", True, BLACK)
        screen.blit(texto, (self.x - 5, self.y - 8))
        
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

    def dibujar(self, screen):
        if len(self.cola) > 5:
            color = RED
        elif len(self.cola) > 2:
            color = YELLOW
        else:
            color = GREEN
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 3)
        texto_nombre = font_small.render(f"{self.nombre}", True, BLACK)
        texto_capacidad = font_small.render(f"Cap: {len(self.empleados)}/{self.capacidad}", True, BLACK)
        screen.blit(texto_nombre, (self.x - 50, self.y - 25))
        screen.blit(texto_capacidad, (self.x - 50, self.y))
        for i, empleado in enumerate(self.empleados):
            empleado_x = self.x - 40 + i * 25
            empleado_y = self.y - 50
            pygame.draw.circle(screen, empleado.color, (empleado_x, empleado_y), 8)
            pygame.draw.circle(screen, BLACK, (empleado_x, empleado_y), 8, 1)
            if empleado.es_temporal:
                temp_texto = font_small.render("T", True, RED)
                screen.blit(temp_texto, (empleado_x - 5, empleado_y + 5))

    def puede_aceptar_pasajero(self):
        return len(self.pasajeros_atendiendo) < len(self.empleados)

    def aceptar_pasajero(self, pasajero):
        if self.puede_aceptar_pasajero():
            self.pasajeros_atendiendo.append(pasajero)
            return True
        else:
            self.cola.append(pasajero)
            return False

    def procesar_pasajeros(self, dinero, happy_hour=False):
        pasajeros_terminados = []
        for pasajero in self.pasajeros_atendiendo[:]:
            if self.nombre == "Facturación":
                if random.randint(1, 30) == 1:
                    base_amount = 250 if pasajero.tipo == "normal" else 400
                    if happy_hour:
                        dinero += base_amount * 3
                    else:
                        dinero += base_amount
                    pasajeros_terminados.append(pasajero)
                    self.pasajeros_atendiendo.remove(pasajero)
            else:
                if random.randint(1, 20) == 1:
                    pasajeros_terminados.append(pasajero)
                    self.pasajeros_atendiendo.remove(pasajero)
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

class Puerta:
    def __init__(self, nombre, x, y):
        self.nombre = nombre
        self.x = x
        self.y = y

class Tienda:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH - 200, 50, 180, 500)  
        self.precios = {
            "empleado": 500,
            "empleado_temporal": 300, 
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
        self.rect_empleado_temporal = pygame.Rect(WIDTH - 190, 150, 160, 40) 
        self.rect_estacion = pygame.Rect(WIDTH - 190, 200, 160, 40) 
        self.rect_eficiencia = pygame.Rect(WIDTH - 190, 250, 160, 40) 
        self.rect_supervisor = pygame.Rect(WIDTH - 190, 300, 160, 40) 
        self.rect_publicidad = pygame.Rect(WIDTH - 190, 350, 160, 40) 
        self.rect_puerta_entrada = pygame.Rect(WIDTH - 190, 400, 160, 40) 

    def dibujar(self, screen, dinero, empleados_actuales):
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 3)
        titulo = font.render("TIENDA", True, BLACK)
        screen.blit(titulo, (self.rect.centerx - 40, self.rect.y + 10))
        
        texto_empleados = font_small.render(f"Empleados: {len(empleados_actuales)}/15", True, BLACK)
        screen.blit(texto_empleados, (self.rect.centerx - 60, self.rect.y + 32))

        color_empleado = GRAY if len(empleados_actuales) >= 15 else WHITE
        pygame.draw.rect(screen, color_empleado, self.rect_empleado)
        pygame.draw.rect(screen, BLACK, self.rect_empleado, 2)
        texto_empleado = font_small.render(f"Empleado: ${self.precios['empleado']}", True, BLACK)
        screen.blit(texto_empleado, (self.rect_empleado.centerx - 70, self.rect_empleado.centery - 10))

        color_temporal = GRAY if len(empleados_actuales) >= 15 else WHITE
        pygame.draw.rect(screen, color_temporal, self.rect_empleado_temporal)
        pygame.draw.rect(screen, BLACK, self.rect_empleado_temporal, 2)
        texto_temporal = font_small.render(f"Empleado Temp: ${self.precios['empleado_temporal']}", True, BLACK)
        screen.blit(texto_temporal, (self.rect_empleado_temporal.centerx - 85, self.rect_empleado_temporal.centery - 10))

        pygame.draw.rect(screen, WHITE, self.rect_estacion)
        pygame.draw.rect(screen, BLACK, self.rect_estacion, 2)
        texto_estacion = font_small.render(f"Estación (+1): ${self.precios['estacion']}", True, BLACK)
        screen.blit(texto_estacion, (self.rect_estacion.centerx - 78, self.rect_estacion.centery - 10))

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

        texto_dinero = font.render(f"${dinero}", True, BLACK)
        screen.blit(texto_dinero, (WIDTH - 150, 10))

    def comprar_empleado(self, dinero, empleados_actuales):
        if dinero >= self.precios["empleado"] and len(empleados_actuales) < 15:
            dinero -= self.precios["empleado"]
            self.precios["empleado"] += 1000  
            return True, dinero
        return False, dinero

    def comprar_empleado_temporal(self, dinero, empleados_actuales):
        if dinero >= self.precios["empleado_temporal"] and len(empleados_actuales) < 15:
            dinero -= self.precios["empleado_temporal"]
            return True, dinero
        return False, dinero

    def comprar_estacion(self, dinero):
        if dinero >= self.precios["estacion"]:
            dinero -= self.precios["estacion"]
            self.precios["estacion"] += 2000  
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

def dibujar_menu(screen):
    screen.fill(WHITE)
    
    titulo = font_title.render("GESTIÓN DE AEROPUERTO", True, BLACK)
    screen.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 150))
    
    boton_jugar = pygame.Rect(WIDTH // 2 - 100, 300, 200, 50)
    pygame.draw.rect(screen, GREEN, boton_jugar)
    pygame.draw.rect(screen, BLACK, boton_jugar, 2)
    texto_jugar = font.render("JUGAR", True, BLACK)
    screen.blit(texto_jugar, (boton_jugar.centerx - texto_jugar.get_width() // 2, 
                              boton_jugar.centery - texto_jugar.get_height() // 2))
    
    boton_salir = pygame.Rect(WIDTH // 2 - 100, 400, 200, 50)
    pygame.draw.rect(screen, RED, boton_salir)
    pygame.draw.rect(screen, BLACK, boton_salir, 2)
    texto_salir = font.render("SALIR", True, BLACK)
    screen.blit(texto_salir, (boton_salir.centerx - texto_salir.get_width() // 2, 
                              boton_salir.centery - texto_salir.get_height() // 2))
    
    return boton_jugar, boton_salir

def inicializar_juego():
    
    puertas = [
        Puerta("Puerta 1", 100, 150),
        Puerta("Puerta 2", 100, 350),
        Puerta("Puerta 3", 100, 550)
    ]

    puertas_abordaje = [
        Puerta("Abordaje", WIDTH - 100, 700)
    ]

    facturacion = Estacion("Facturación", 400, 150, capacidad=1)
    seguridad = Estacion("Seguridad", 600, 350, capacidad=1)
    embarque = Estacion("Embarque", 800, 550, capacidad=1)
    estaciones = [facturacion, seguridad, embarque]

    empleados = []
    for i in range(2):
        color = COLORS_EMPLEADOS[i % len(COLORS_EMPLEADOS)]
        empleado = Empleado(300 + i * 30, 30, f"Empleado {i+1}", color)
        empleados.append(empleado)

    facturacion.agregar_empleado(empleados[0])
    seguridad.agregar_empleado(empleados[1])

    pasajeros = []

    
    dinero = 1000

    tienda = Tienda()

    hora_actual = datetime(2025, 7, 24, 6, 0)  
    intervalo_base = 1500  

    
    empleado_seleccionado = None
    ultimo_intervalo = intervalo_base
    
    return (puertas, puertas_abordaje, facturacion, seguridad, embarque, estaciones, 
            empleados, pasajeros, dinero, tienda, hora_actual, intervalo_base, 
            empleado_seleccionado, ultimo_intervalo)

def obtener_multiplicador_trafico(hora):
    hora_dia = hora.hour
    
    if (7 <= hora_dia <= 9) or (12 <= hora_dia <= 14) or (17 <= hora_dia <= 19):
        base = 4
    elif (10 <= hora_dia <= 11) or (15 <= hora_dia <= 16) or (20 <= hora_dia <= 22):
        base = 3
    else:
        base = 2
    if tienda.comprado["publicidad"]:
        base = int(base * 1.15)  
    return base, RED if base == 4 else YELLOW if base == 3 else GREEN

def es_happy_hour(hora):
    minutos_totales = hora.hour * 60 + hora.minute
    return minutos_totales % 360 == 0  

clock = pygame.time.Clock()

MENU = 0
JUGANDO = 1
estado = MENU

SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 1500)  

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
                hora_actual += timedelta(minutes=30)
                
                for empleado in empleados[:]:
                    if empleado.es_temporal and empleado.fecha_fin and hora_actual >= empleado.fecha_fin:
                        for estacion in estaciones:
                            if empleado in estacion.empleados:
                                estacion.remover_empleado(empleado)
                        empleados.remove(empleado)

                multiplicador, _ = obtener_multiplicador_trafico(hora_actual)
                for _ in range(multiplicador):
                    puerta = random.choice(puertas)
                    tipo = random.choices(["normal", "ejecutivo"], weights=[0.7, 0.3])[0]
                    pasajeros.append(Pasajero(puerta.x, puerta.y, tipo))
                nuevo_intervalo = max(500, intervalo_base // multiplicador)
                if nuevo_intervalo != ultimo_intervalo:
                    pygame.time.set_timer(SPAWN_EVENT, nuevo_intervalo)
                    ultimo_intervalo = nuevo_intervalo
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if tienda.rect_empleado.collidepoint(mouse_x, mouse_y):
                    comprado, dinero = tienda.comprar_empleado(dinero, empleados)
                    if comprado:
                        color = COLORS_EMPLEADOS[len(empleados) % len(COLORS_EMPLEADOS)]
                        nuevo_empleado = Empleado(300 + len(empleados) * 30, 30, f"Empleado {len(empleados) + 1}", color)
                        empleados.append(nuevo_empleado)
                elif tienda.rect_empleado_temporal.collidepoint(mouse_x, mouse_y):
                    comprado, dinero = tienda.comprar_empleado_temporal(dinero, empleados)
                    if comprado:
                        color = COLORS_EMPLEADOS[len(empleados) % len(COLORS_EMPLEADOS)]
                        fecha_fin = hora_actual + timedelta(weeks=1)
                        nuevo_empleado = Empleado(300 + len(empleados) * 30, 30, f"Empleado T{len(empleados) + 1}", color, es_temporal=True, fecha_fin=fecha_fin)
                        empleados.append(nuevo_empleado)
                elif tienda.rect_estacion.collidepoint(mouse_x, mouse_y):
                    comprado, dinero = tienda.comprar_estacion(dinero)
                    if comprado:
                        random.choice(estaciones).capacidad += 1
                elif tienda.rect_eficiencia.collidepoint(mouse_x, mouse_y):
                    comprado, dinero = tienda.comprar_eficiencia(dinero)
                    if comprado:
                        pass
                elif tienda.rect_supervisor.collidepoint(mouse_x, mouse_y):
                    comprado, dinero = tienda.comprar_supervisor(dinero)
                    if comprado:
                        pass
                elif tienda.rect_publicidad.collidepoint(mouse_x, mouse_y):
                    comprado, dinero = tienda.comprar_publicidad(dinero)
                    if comprado:
                        pass
                elif tienda.rect_puerta_entrada.collidepoint(mouse_x, mouse_y):
                    comprado, dinero = tienda.comprar_puerta_entrada(dinero)
                    if comprado:
                        puertas.append(Puerta("Puerta 4", 100, 750
                                              ))
                for empleado in empleados:
                    distancia = ((empleado.x - mouse_x) ** 2 + (empleado.y - mouse_y) ** 2) ** 0.5
                    if distancia <= empleado.radio:
                        if empleado_seleccionado == empleado:
                            empleado_seleccionado = None
                        else:
                            empleado_seleccionado = empleado
                        break
                if empleado_seleccionado:
                    for estacion in estaciones:
                        if estacion.rect.collidepoint(mouse_x, mouse_y):
                            if estacion.agregar_empleado(empleado_seleccionado):
                                for otra_estacion in estaciones:
                                    if empleado_seleccionado in otra_estacion.empleados and otra_estacion != estacion:
                                        otra_estacion.remover_empleado(empleado_seleccionado)
                                        break
                            empleado_seleccionado = None
                            break

        for p in puertas:
            pygame.draw.circle(screen, GRAY, (p.x, p.y), 20)
            pygame.draw.circle(screen, BLACK, (p.x, p.y), 20, 2)
            texto = font_small.render(p.nombre, True, BLACK)
            screen.blit(texto, (p.x - 30, p.y - 10))

        for p in puertas_abordaje:
            pygame.draw.circle(screen, GREEN, (p.x, p.y), 20)
            pygame.draw.circle(screen, BLACK, (p.x, p.y), 20, 2)
            texto = font_small.render(p.nombre, True, BLACK)
            screen.blit(texto, (p.x - 35, p.y - 10))

        for e in estaciones:
            e.dibujar(screen)

        happy_hour_active = es_happy_hour(hora_actual)
        for estacion in estaciones:
            dinero, pasajeros_terminados = estacion.procesar_pasajeros(dinero, happy_hour_active)
            for pasajero in pasajeros_terminados:
                if estacion == facturacion:
                    pasajero.estado = "yendo_seguridad"
                elif estacion == seguridad:
                    pasajero.estado = "yendo_embarque"
                elif estacion == embarque:
                    pasajero.estado = "saliendo"

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
                pass  
            elif p.estado == "saliendo":
                puerta_abordaje = random.choice(puertas_abordaje)
                if p.mover_a(puerta_abordaje.x, puerta_abordaje.y):
                    if p in pasajeros:
                        pasajeros.remove(p)
            p.dibujar(screen)

        for empleado in empleados:
            if empleado.destino_x != empleado.x or empleado.destino_y != empleado.y:
                empleado.mover_a(empleado.destino_x, empleado.destino_y)
            empleado.dibujar(screen)

        tienda.dibujar(screen, dinero, empleados)

        if empleado_seleccionado:
            texto_seleccion = font.render("Empleado seleccionado - Click en estación", True, BLACK)
            screen.blit(texto_seleccion, (WIDTH // 2 - 200, HEIGHT - 80))

        total_pasajeros = len(pasajeros)
        cola_total = sum(len(e.cola) for e in estaciones)
        texto_stats = font_small.render(f"Pasajeros: {total_pasajeros} | Cola: {cola_total}", True, BLACK)
        screen.blit(texto_stats, (10, 10))

        multiplicador, color_reloj = obtener_multiplicador_trafico(hora_actual)
        hora_texto = hora_actual.strftime("%H:%M")
        texto_hora = font.render(f"Hora: {hora_texto}", True, color_reloj)
        screen.blit(texto_hora, (10, 40))

        nivel_trafico = "Alto" if multiplicador == 4 else "Medio" if multiplicador == 3 else "Bajo"
        texto_trafico = font_small.render(f"Tráfico: {nivel_trafico} (x{multiplicador})", True, color_reloj)
        screen.blit(texto_trafico, (10, 70))

        if happy_hour_active:
            texto_happy = font.render("HAPPY HOUR - INGRESOS x3", True, YELLOW)
            screen.blit(texto_happy, (WIDTH // 2 - 150, 10))

        pygame.display.flip()
        clock.tick(60)

pygame.quit()
sys.exit()