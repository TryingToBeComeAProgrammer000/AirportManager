import pygame
import sys
import random
pygame.init()

sonido_win = None
sonido_game_over = None
try:
    sonido_win = pygame.mixer.Sound("win.wav")
    print("Sonido win.wav cargado.")
except pygame.error as e:
    print(f"Advertencia: No se pudo cargar el sonido 'win.wav'. Error: {e}")

try:
    sonido_win = pygame.mixer.Sound("normal_win.wav")
    print("Sonido win.wav cargado.")
except pygame.error as e:
    print(f"Advertencia: No se pudo cargar el sonido 'normal_win.wav'. Error: {e}")

try:
    sonido_game_over = pygame.mixer.Sound("game_over.wav")
    print("Sonido game_over.wav cargado.")
except pygame.error as e:
    print(f"Advertencia: No se pudo cargar el sonido 'game_over.wav'. Error: {e}")

ANCHO, ALTO = 1920, 1080
pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)  # Permitir redimensionar
pygame.display.set_caption("Aeropuerto Tycoon")
reloj = pygame.time.Clock()
# Colores
ROJO = (255, 0, 0)
ROJO_BONITO = (180, 9, 0)
VERDE = (0, 255, 0)
VERDE_LIMA = (109, 196, 8)
AZUL = (0, 0, 255)
GRIS = (100, 100, 100)
MORADO = (180, 0, 180)
NEGRO = (0, 0, 0)
DORADO = (255, 215, 0)
AZUL_CLARO = (150, 200, 255)
BLANCO = (255, 255, 255)
GRIS_CLARO = (200, 200, 200)
GRIS_OSCURO = (150, 150, 150)
NARANJA = (255, 165, 0)
CIAN = (0, 255, 255)
CELEST = (0, 138, 201)
# Nuevo color para el soporte técnico
ROJO_OSCURO = (200, 0, 0)
# Fuentes
fuente = pygame.font.SysFont(None, 28)
fuente_grande = pygame.font.SysFont(None, 48)
fuente_muy_grande = pygame.font.SysFont(None, 60)
fuente_pequena = pygame.font.SysFont(None, 24)
# Dimensiones del juego (ajustadas para la nueva pantalla)
# HACER LAS ESTACIONES MAS GRANDES
TAM_ESTACION = 150  # Aumentado de 60 a 100
TAM_PASAJERO = 70
ESPACIO = 30
MARGEN_DERECHO = 250
ALTURA_TOTAL_ESTACIONES = 3 * TAM_ESTACION + 2 * ESPACIO
Y_INICIO_ESTACIONES = (ALTO - ALTURA_TOTAL_ESTACIONES) // 2
X_ESTACIONES = ANCHO - TAM_ESTACION - MARGEN_DERECHO - 200
# Nueva constante para el soporte técnico
TAM_SOPORTE = 100
# --- Estados del Juego ---
ESTADO_MENU = "menu"
ESTADO_JUGANDO = "jugando"
ESTADO_RESULTADOS = "resultados"
# --- Estados del Juego (incluyendo secreto y combate) ---
ESTADO_SECRETO = "secreto"  
ESTADO_COMBATE = "combate"  
estado_juego = ESTADO_MENU
# --- Cargar Imagen de Fondo ---
imagen_fondo = None
try:
    imagen_fondo = pygame.image.load("Fondoaereopuerto.png")
    imagen_fondo = pygame.transform.scale(imagen_fondo, (1000, 700))
except pygame.error as e:
    print(
        f"Advertencia: No se pudo cargar la imagen de fondo 'Fondoaereopuerto.png'. Se usará color sólido. Error: {e}")
    # imagen_fondo seguirá siendo None
# --- Cargar Imagen de Portada del Menú ---
imagen_portada_menu = None
try:
    imagen_portada_menu = pygame.image.load("portada1.png")
    imagen_portada_menu = pygame.transform.scale(imagen_portada_menu, (1920, 1080))
    print("Imagen portada1.png cargada.")
except pygame.error as e:
    print(f"Advertencia: No se pudo cargar la imagen 'portada1.png'. Se usará color sólido. Error: {e}")
   
ANCHO_PUERTA = 150 
ALTO_PUERTA = 150  

imagen_puertas = None
try:
    imagen_puertas = pygame.image.load("entrance.png")
    # Escalar la imagen al nuevo tamaño de las puertas de entrada
    imagen_puertas = pygame.transform.scale(imagen_puertas, (ANCHO_PUERTA, ALTO_PUERTA))
    print("Imagen puertas.png cargada y escalada correctamente.")
except pygame.error as e:
    print(f"Advertencia: No se pudo cargar la imagen 'entrance.png'. Se usará color sólido. Error: {e}")
    # imagen_puertas seguirá siendo None



# --- Cargar Imágenes de Pasajeros ---
imagen_pasajero_normal = None
try:
    imagen_pasajero_normal = pygame.image.load("pasajeronormal1.png")
    # Escalar la imagen al nuevo tamaño de los pasajeros
    imagen_pasajero_normal = pygame.transform.scale(imagen_pasajero_normal, (TAM_PASAJERO, TAM_PASAJERO))
except pygame.error as e:
    print(
        f"Advertencia: No se pudo cargar la imagen del pasajero 'pasajeronormal1.png'. Se usará color sólido. Error: {e}")
    # imagen_pasajero_normal seguirá siendo None
imagen_pasajero_equipaje = None
try:
    imagen_pasajero_equipaje = pygame.image.load("pasajeromaletas1.png")
    # Escalar la imagen al nuevo tamaño de los pasajeros
    imagen_pasajero_equipaje = pygame.transform.scale(imagen_pasajero_equipaje, (TAM_PASAJERO, TAM_PASAJERO))
except pygame.error as e:
    print(
        f"Advertencia: No se pudo cargar la imagen del pasajero 'pasajeromaletas1.png'. Se usará color sólido. Error: {e}")
    # imagen_pasajero_equipaje seguirá siendo None
imagen_pasajero_vip = None
try:
    imagen_pasajero_vip = pygame.image.load("pasajerovip1.png")
    # Escalar la imagen al nuevo tamaño de los pasajeros
    imagen_pasajero_vip = pygame.transform.scale(imagen_pasajero_vip, (TAM_PASAJERO, TAM_PASAJERO))
except pygame.error as e:
    print(
        f"Advertencia: No se pudo cargar la imagen del pasajero 'pasajerovip1.png'. Se usará color sólido. Error: {e}")
    # imagen_pasajero_vip seguirá siendo None
# --- Cargar Imágenes de las Cajas para las Estaciones ---
# Cargar las imágenes de caja1.png, caja2.png y caja3.png
imagenes_cajas = []
for i in range(1, 4):  # Cargar caja1, caja2, caja3
    try:
        # Asegúrate de que las imágenes 'caja1.png', 'caja2.png', 'caja3.png' estén en la misma carpeta
        imagen_caja = pygame.image.load(f"caja{i}.png")
        # Escalar la imagen al tamaño de las estaciones (un poco más pequeña para que quepa bien)
        imagen_caja = pygame.transform.scale(imagen_caja, (TAM_ESTACION - 10, TAM_ESTACION - 10))
        imagenes_cajas.append(imagen_caja)
        print(f"Imagen caja{i} cargada y escalada correctamente.")
    except pygame.error as e:
        print(f"Advertencia: No se pudo cargar la imagen 'caja{i}.png'. Se usará color sólido. Error: {e}")
        imagenes_cajas.append(None)  # Agregar None si no se pudo cargar
# --- Cargar Imagen del Soporte Técnico ---
imagen_soporte_tecnico = None
try:
    imagen_soporte_tecnico = pygame.image.load("soporte1.png")
    # Escalar la imagen al tamaño del soporte técnico
    imagen_soporte_tecnico = pygame.transform.scale(imagen_soporte_tecnico, (TAM_SOPORTE *1.5, TAM_SOPORTE))
except pygame.error as e:
    print(
        f"Advertencia: No se pudo cargar la imagen del soporte técnico 'soporte1.png'. Se usará color sólido. Error: {e}")
    # imagen_soporte_tecnico seguirá siendo None
# --- Clases ---
class Boton:
    def __init__(self, x, y, ancho, alto, texto, accion, color_normal=GRIS_CLARO, color_hover=GRIS_OSCURO):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.accion = accion
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.color_actual = color_normal
        self.texto_renderizado = fuente.render(texto, True, NEGRO)
        self.texto_rect = self.texto_renderizado.get_rect(center=self.rect.center)
    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color_actual, self.rect, border_radius=5)
        pygame.draw.rect(pantalla, NEGRO, self.rect, 2, border_radius=5)
        pantalla.blit(self.texto_renderizado, self.texto_rect)
    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect.collidepoint(evento.pos):
                return self.accion
        return None
    def actualizar(self, pos_mouse):
        if self.rect.collidepoint(pos_mouse):
            self.color_actual = self.color_hover
        else:
            self.color_actual = self.color_normal
# Definir TIPOS_PASAJEROS antes de Pasajero para evitar "Unresolved reference"
TIPOS_PASAJEROS = {
    "normal": {"color": GRIS, "valor": 1},
    "vip": {"color": DORADO, "valor": 3},
    "equipaje": {"color": NEGRO, "valor": 2},
}
class Pasajero:
    def __init__(self, tipo, puerta_entrada):
        self.x = puerta_entrada.x
        self.y = puerta_entrada.y
        self.vel = 2
        # Asegurarse de que estaciones y puerta_salida estén definidas globalmente antes de crear un Pasajero
        self.destinos = [rect.center for rect in estaciones] + [puerta_salida.center]
        self.actual = 0
        self.esperando = False
        self.tiempo_llegada = 0
        # Nuevo atributo para rastrear el tiempo de espera
        self.tiempo_inicio_espera = 0
        self.activo = False
        self.terminado = False
        self.tipo = tipo
        self.color = TIPOS_PASAJEROS[tipo]["color"]
        self.puerta_entrada = puerta_entrada
    def posicion_en_fila(self, posicion_fila, estacion_pos):
        # Cambiar la fila para que crezca hacia la izquierda en lugar de hacia arriba
        fila_x = estacion_pos[0] - TAM_PASAJERO - 5 - (posicion_fila * (TAM_PASAJERO + 5))
        fila_y = estacion_pos[1] + (TAM_ESTACION // 2) - (TAM_PASAJERO // 2)  # Centrar verticalmente
        self.x = fila_x
        self.y = fila_y
    def mover(self):
        if not self.activo:
            return
        # Si la estación actual está dañada y esperando, no se mueve (cola visible)
        # Usar variables globales
        global falla_tecnica_activa, estaciones_danadas, estaciones_mejoras, estaciones_mejoradas
        if falla_tecnica_activa and self.actual in estaciones_danadas and self.esperando:
            return
        if self.actual >= len(self.destinos):
            self.terminado = True
            self.activo = False
            return
        if self.esperando:
            tiempo_espera = 1500
            # Aplicar mejoras de velocidad si existen
            if self.actual < 3:
                if estaciones_mejoras[self.actual]["velocidad"]:
                    tiempo_espera = 500
                elif estaciones_mejoradas[self.actual]:
                    tiempo_espera = 1000
            if falla_tecnica_activa and self.actual in estaciones_danadas:
                tiempo_espera = 5000
            if pygame.time.get_ticks() - self.tiempo_llegada >= tiempo_espera:
                self.actual += 1
                self.esperando = False
                # Resetear el tiempo de inicio de espera cuando deja de esperar
                self.tiempo_inicio_espera = 0
            return
        dx, dy = self.destinos[self.actual][0] - self.x, self.destinos[self.actual][1] - self.y
        dist = (dx ** 2 + dy ** 2) ** 0.5 or 1  # Evitar división por cero
        if dist < 2:
            if self.actual < len(self.destinos) - 1:
                self.esperando = True
                self.tiempo_llegada = pygame.time.get_ticks()
                # Registrar el inicio del tiempo de espera
                self.tiempo_inicio_espera = pygame.time.get_ticks()
            else:
                self.actual += 1
        else:
            self.x += self.vel * dx / dist
            self.y += self.vel * dy / dist
    def dibujar(self, pantalla):
        if self.activo and not self.terminado:
            # Verificar el tipo de pasajero y si la imagen correspondiente se cargó
            if self.tipo == "normal" and imagen_pasajero_normal:
                # Dibujar la imagen del pasajero normal
                pantalla.blit(imagen_pasajero_normal, (int(self.x), int(self.y)))
            elif self.tipo == "equipaje" and imagen_pasajero_equipaje:
                # Dibujar la imagen del pasajero con equipaje
                pantalla.blit(imagen_pasajero_equipaje, (int(self.x), int(self.y)))
            elif self.tipo == "vip" and imagen_pasajero_vip:
                # Dibujar la imagen del pasajero VIP
                pantalla.blit(imagen_pasajero_vip, (int(self.x), int(self.y)))
            else:
                # Dibujar el rectángulo de color como respaldo si no hay imagen o no se cargó
                pygame.draw.rect(pantalla, self.color, (int(self.x), int(self.y), TAM_PASAJERO, TAM_PASAJERO))
class SoporteTecnico:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 2
        self.destino_x = x
        self.destino_y = y
        self.activo = True  # Siempre activo, pero puede estar inactivo si no se compra
        self.reparando = False
        self.tiempo_reparacion = 0
        self.tiempo_reparacion_necesario = 3000  # 3 segundos de reparación
        self.estacion_objetivo = None  # Referencia a la estación que está reparando
        self.indice_estacion_objetivo = None  # Índice de la estación objetivo
        # Para movimiento aleatorio
        self.tiempo_ultimo_cambio_direccion = 0
        self.tiempo_cambio_direccion = random.randint(2000, 4000)  # Cambiar dirección cada 2-4 segundos
        self.margen = 50
    def comprar(self):
        pass  
    def asignar_reparacion(self, estacion_idx):
        if self.activo:  # Solo si está disponible/comprado
            # Acceder a la variable global estaciones
            global estaciones
            self.reparando = True
            self.indice_estacion_objetivo = estacion_idx
            self.estacion_objetivo = estaciones[estacion_idx]  # Guardar referencia
            # Moverse hacia el centro de la estación
            self.destino_x = self.estacion_objetivo.centerx
            self.destino_y = self.estacion_objetivo.centery
            self.tiempo_reparacion = 0
            print(f"Soporte Técnico asignado a reparar estación {estacion_idx + 1}")
    def actualizar(self, tiempo_actual):
        # Si está reparando
        if self.reparando:
            self.tiempo_reparacion += reloj.get_time()  # Sumar tiempo transcurrido en ms
        else:
            # Movimiento aleatorio cuando no está reparando
            dx, dy = self.destino_x - self.x, self.destino_y - self.y
            dist = max(1, (dx ** 2 + dy ** 2) ** 0.5)  # Evitar división por cero
            # Si está cerca del destino, cambiar dirección aleatoriamente
            if dist < 5:
                self.cambiar_direccion_aleatoria(tiempo_actual)
            else:
                # Moverse hacia el destino
                self.x += self.vel * dx / dist
                self.y += self.vel * dy / dist
            # Cambiar dirección aleatoriamente cada cierto tiempo
            if tiempo_actual - self.tiempo_ultimo_cambio_direccion > self.tiempo_cambio_direccion:
                self.cambiar_direccion_aleatoria(tiempo_actual)
    def cambiar_direccion_aleatoria(self, tiempo_actual):
        self.tiempo_ultimo_cambio_direccion = tiempo_actual
        self.tiempo_cambio_direccion = random.randint(2000, 4000)

        # Generar nuevo destino aleatorio dentro de los márgenes
        self.destino_x = random.randint(self.margen, ANCHO - self.margen)
        self.destino_y = random.randint(self.margen, ALTO - self.margen)
    def dibujar(self, pantalla):
    # Siempre se dibuja si existe, pero su comportamiento depende de si está comprado
        import math
                # --- Dibujar aura épica si está reparando ---
        if self.reparando:
            tiempo_actual = pygame.time.get_ticks()
            # Crear varias capas de aura concéntricas que pulsan
            for i in range(5, 0, -1):  # 5 capas
                # Calcular el radio del aura pulsante
                radio_base = TAM_SOPORTE + 10 + i * 5
                # Pulsación basada en el tiempo
                pulso = math.sin(tiempo_actual / 200.0 + i) * 5
                radio_pulsante = radio_base + pulso
                # Crear una superficie con transparencia para el aura
                aura_surface = pygame.Surface((radio_pulsante * 2, radio_pulsante * 2), pygame.SRCALPHA)
                # Color del aura con variación cíclica (cambia entre azul, cian, verde)
                hue_offset = (tiempo_actual / 30.0 + i * 20) % 360
                # Convertir HSV a RGB (simplificado)
                if 0 <= hue_offset < 120:  # Rojo a Verde
                    r, g, b = 255, int(255 * (hue_offset / 120)), 0
                elif 120 <= hue_offset < 240:  # Verde a Azul
                    r, g, b = int(255 * (1 - (hue_offset - 120) / 120)), 255, 0
                else:  # Azul a Rojo
                    r, g, b = 0, int(255 * (1 - (hue_offset - 240) / 120)), int(255 * ((hue_offset - 240) / 120))
                
                # Ajustar transparencia basada en la capa (más externa = más tenue)
                alpha = max(20, 100 - i * 15)
                
                # Dibujar el círculo del aura
                pygame.draw.circle(aura_surface, (r, g, b, alpha), (int(radio_pulsante), int(radio_pulsante)), int(radio_pulsante), 2 + i // 2)
                
                # Dibujar la superficie del aura en la pantalla DESPLAZADA 25 PIXELES A LA DERECHA
                pantalla.blit(aura_surface, (int(self.x - radio_pulsante + 25), int(self.y - radio_pulsante)))
            
            # Partículas de energía flotando alrededor DESPLAZADAS 25 PIXELES A LA DERECHA
            for i in range(10):
                # Posición basada en ángulo y tiempo
                angulo = (tiempo_actual / 500.0 + i) % (2 * math.pi)
                distancia = TAM_SOPORTE + 20 + math.sin(tiempo_actual / 300.0 + i) * 10
                part_x = self.x + math.cos(angulo) * distancia + 25  # Desplazamiento en X
                part_y = self.y + math.sin(angulo) * distancia
                
                # Tamaño y color de partícula variable
                tam_part = 2 + (i % 3)
                brillo = 200 + int(55 * math.sin(tiempo_actual / 100.0 + i))
                color_part = (min(255, brillo), min(255, brillo), 255)  # Blanco-azulado
                
                pygame.draw.circle(pantalla, color_part, (int(part_x), int(part_y)), tam_part)

        # --- Dibujar la imagen del soporte técnico si está cargada ---
        if imagen_soporte_tecnico:
            # Centrar la imagen en la posición del soporte técnico
            pantalla.blit(imagen_soporte_tecnico, (int(self.x - TAM_SOPORTE / 2), int(self.y - TAM_SOPORTE / 2)))
        else:
            # Dibujar el rectángulo rojo oscuro como respaldo si no hay imagen
            pygame.draw.rect(pantalla, ROJO_OSCURO,
                            (int(self.x - TAM_SOPORTE / 2), int(self.y - TAM_SOPORTE / 2), TAM_SOPORTE, TAM_SOPORTE))
        
# --- Clase para Textos Flotantes (por ejemplo, dinero perdido) ---
class TextoFlotante:
    def __init__(self, x, y, texto, color=ROJO, tiempo_vida=2000, velocidad_y=-1):
        self.x = x
        self.y = y
        self.texto = texto
        self.color = color
        self.tiempo_vida = tiempo_vida  # Milisegundos que dura el texto
        self.tiempo_creacion = pygame.time.get_ticks()
        self.velocidad_y = velocidad_y  # Velocidad de ascenso
        self.activo = True
        # Renderizar el texto una sola vez al crearlo
        self.imagen_texto = fuente.render(self.texto, True, self.color)
        self.rect = self.imagen_texto.get_rect(center=(self.x, self.y))
    def actualizar(self):
        # Actualizar posición
        self.y += self.velocidad_y
        self.rect.centery = self.y
        # Verificar si ha expirado su tiempo de vida
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_creacion > self.tiempo_vida:
            self.activo = False
    def dibujar(self, pantalla):
        if self.activo:
            pantalla.blit(self.imagen_texto, self.rect)
# --- Menú Principal del Juego ---
class MenuPrincipal:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.botones = []
        self.crear_botones()
    def crear_botones(self):
        self.botones.clear()
        # Botón Jugar
        boton_jugar = Boton(
            x=self.ancho // 2 - 100,
            y=self.alto // 2 - 25,
            ancho=200,
            alto=50,
            texto="Jugar",
            accion=self.accion_jugar
        )
        self.botones.append(boton_jugar)
        # Botón Salir
        boton_salir = Boton(
            x=self.ancho // 2 - 100,
            y=self.alto // 2 + 50,
            ancho=200,
            alto=50,
            texto="Salir",
            accion=self.accion_salir
        )
        self.botones.append(boton_salir)
    def accion_jugar(self):
        global estado_juego
        estado_juego = ESTADO_JUGANDO
        # Llamar a resetear_juego cada vez que se inicia un nuevo juego
        resetear_juego()
    def accion_salir(self):
        pygame.quit()
        sys.exit()
    def manejar_evento(self, evento):
        for boton in self.botones:
            accion = boton.manejar_evento(evento)
            if accion:
                accion()
    def actualizar(self, pos_mouse):
        for boton in self.botones:
            boton.actualizar(pos_mouse)
    def dibujar(self, pantalla):
        # Dibujar fondo del menú usando la imagen si está cargada
        if imagen_portada_menu:
            
            pantalla.blit(imagen_portada_menu, (0, 0))  # Ajusta (0, 0) si quieres centrarla o ponerla en otro lugar
        else:
            # Fallback si no se cargó la imagen de portada
            pantalla.fill(BLANCO)  # O cualquier otro color de respaldo
      
        for boton in self.botones:
            boton.dibujar(pantalla)
    def actualizar_dimensiones(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.crear_botones()
# --- Pantalla de Resultados ---
class PantallaResultados:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.botones = []
        self.datos = {
            "pasajeros_atendidos": 0,
            "pasajeros_perdidos": 0,
            "C": 0
        }
        self.crear_botones()
    def crear_botones(self):
        self.botones.clear()
        # Botón Volver al Menú
        boton_menu = Boton(
            x=self.ancho // 2 - 100,
            y=self.alto - 100,
            ancho=200,
            alto=50,
            texto="Volver al Menú",
            accion=self.accion_volver_menu
        )
        self.botones.append(boton_menu)
    def accion_volver_menu(self):
        global estado_juego
        estado_juego = ESTADO_MENU
    def establecer_datos(self, pasajeros_atendidos, pasajeros_perdidos, dinero_total):
        self.datos = {
            "pasajeros_atendidos": pasajeros_atendidos,
            "pasajeros_perdidos": pasajeros_perdidos,
            "dinero_total": dinero_total
        }
        if hasattr(self, '_sonido_victoria_reproducido'):
                delattr(self, '_sonido_victoria_reproducido')
        if hasattr(self, '_sonido_derrota_reproducido'):
                delattr(self, '_sonido_derrota_reproducido')
    def manejar_evento(self, evento):
        for boton in self.botones:
            accion = boton.manejar_evento(evento)
            if accion:
                accion()
    def actualizar(self, pos_mouse):
        for boton in self.botones:
            boton.actualizar(pos_mouse)
    def dibujar(self, pantalla):
    
        if imagen_fondo_resultados:
          
            pantalla.blit(imagen_fondo_resultados, (0, 0)) # Ajusta (0, 0) si quieres centrarla
        else:
            # Fallback si no se cargó la imagen
            pantalla.fill(BLANCO)  # O cualquier otro color de respaldo
        # Título de resultados
        titulo = fuente_muy_grande.render("RESULTADOS", True, NEGRO)
        pantalla.blit(titulo, (self.ancho // 2 - titulo.get_width() // 2, 50))

        mensaje_texto = ""
        color_mensaje = NEGRO # Color por defecto, puedes cambiarlo

        #Verificar condición de victoria/derrota por pasajeros atendidos
        pasajeros_atendidos = self.datos.get('pasajeros_atendidos', 0) # Obtener con valor por defecto
        if pasajeros_atendidos >= 70:
            mensaje_texto = "¡VICTORIA!"
            color_mensaje = VERDE
            # Reproducir sonido de victoria (solo una vez)
            if not getattr(self, '_sonido_victoria_reproducido', False):
                 if sonido_win: # Usa el sonido de victoria
                     try:
                         sonido_win.play()
                         print("Sonido de victoria (por pasajeros) reproducido.")
                     except pygame.error as e:
                         print(f"Error al reproducir sonido de victoria: {e}")
                 self._sonido_victoria_reproducido = True # Marcar como reproducido hasta que se reinicie
        else: # Menos de 70 pasajeros
            mensaje_texto = "DERROTA"
            color_mensaje = ROJO
            # Reproducir sonido de derrota (solo una vez)
            if not getattr(self, '_sonido_derrota_reproducido', False):
                if sonido_game_over: # Usa el sonido de derrota
                    try:
                        sonido_game_over.play()
                        print("Sonido de derrota (por pasajeros) reproducido.")
                    except pygame.error as e:
                        print(f"Error al reproducir sonido de derrota: {e}")
                self._sonido_derrota_reproducido = True # Marcar como reproducido hasta que se reinicie

        # --- Mostrar el mensaje de victoria/derrota ---
        if mensaje_texto:
            texto_mensaje = fuente_muy_grande.render(mensaje_texto, True, color_mensaje)
            pos_x_mensaje = self.ancho // 2 - texto_mensaje.get_width() // 2
            # Colocarlo debajo del título "RESULTADOS"
            pos_y_mensaje = 120
            pantalla.blit(texto_mensaje, (pos_x_mensaje, pos_y_mensaje))
            # Ajustar la posición Y de las estadísticas para que no se sobrepongan
            offset_y_estadisticas = 80 # Espacio adicional después del mensaje grande
        else:
            offset_y_estadisticas = 0

        # Mostrar estadísticas
        y_pos = 150
        espacio = 60
        texto_atendidos = fuente_grande.render(f"Pasajeros Atendidos: {self.datos['pasajeros_atendidos']}", True, AZUL_CLARO)
        pantalla.blit(texto_atendidos, (self.ancho // 2 - texto_atendidos.get_width() // 2, y_pos + 100))
        y_pos += espacio
        texto_perdidos = fuente_grande.render(f"Pasajeros Perdidos: {self.datos['pasajeros_perdidos']}", True, ROJO_BONITO)
        pantalla.blit(texto_perdidos, (self.ancho // 2 - texto_perdidos.get_width() // 2, y_pos + 100))
        y_pos += espacio
        texto_dinero = fuente_grande.render(f"Dinero Total: ${self.datos['dinero_total']}", True, VERDE_LIMA)
        pantalla.blit(texto_dinero, (self.ancho // 2 - texto_dinero.get_width() // 2, y_pos + 100))
        # Dibujar botones
        for boton in self.botones:
            boton.dibujar(pantalla)
    def actualizar_dimensiones(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.crear_botones()
# --- Pantalla Secreta (Shhh) ---
class PantallaSecreta:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.botones = []
        self.crear_botones()
    def crear_botones(self):
        self.botones.clear()
        # Botón para regresar al juego (ahora lleva al combate)
        boton_volver = Boton(
            x=self.ancho // 2 - 100,
            y=self.alto - 100,
            ancho=200,
            alto=50,
            texto="Volver al Juego",
            accion=self.accion_volver_juego
        )
        self.botones.append(boton_volver)
    def accion_volver_juego(self):
        global estado_juego
        # En lugar de volver directamente al juego, vamos al combate
        estado_juego = ESTADO_COMBATE
    def manejar_evento(self, evento):
        for boton in self.botones:
            accion = boton.manejar_evento(evento)
            if accion:
                accion()
    def actualizar(self, pos_mouse):
        for boton in self.botones:
            boton.actualizar(pos_mouse)
    def dibujar(self, pantalla):
        # Fondo negro 
        pantalla.fill(NEGRO)
        # Mensaje secreto
        mensaje_linea1 = "¿Te aburriste de manejar pasajeros?"
        mensaje_linea2 = "¡Eh! ¿Veamos si esto es de tu talla!"
        texto1 = fuente_muy_grande.render(mensaje_linea1, True, BLANCO)
        texto2 = fuente_muy_grande.render(mensaje_linea2, True, BLANCO)
        # Centrar ambos renglones
        pantalla.blit(texto1, (self.ancho // 2 - texto1.get_width() // 2, self.alto // 2 - 60))
        pantalla.blit(texto2, (self.ancho // 2 - texto2.get_width() // 2, self.alto // 2 + 10))
        # Dibujar botones
        for boton in self.botones:
            boton.dibujar(pantalla)
    def actualizar_dimensiones(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.crear_botones()
# --- Pantalla de Combate ---
class PantallaCombate:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.textura_fondo_estatico = None # Superficie para el fondo prerrenderizado
        self.crear_textura_fondo_estatico() # Llamar al método para crear la textura
        self.botones = []
        self.crear_botones()
        # Jugador
        self.jugador_ancho, self.jugador_alto = 40, 40
        self.jugador_x = ancho // 2 - self.jugador_ancho // 2
        self.jugador_y = alto - self.jugador_alto - 20
        self.jugador_vel = 5
        self.jugador_vidas = 3
        self.ultimo_disparo_jugador = 0
        self.cadencia_disparo_jugador = 200  # ms
        self.disparando_rayo = False
        self.inicio_rayo = 0
        self.duracion_rayo = 1000  # ms
        # --- Cambio: Daño del rayo reducido y hecho fijo ---
        self.daño_rayo = 3  # Era 1 por frame, ahora 3 por disparo
        # Jefe
        self.jefe_ancho, self.jefe_alto = 80, 80
        self.jefe_x = ancho // 2 - self.jefe_ancho // 2
        self.jefe_y = 50
        self.jefe_vel = 2
        self.jefe_direccion = 1  
        # ---
        self.jefe_vida_max = 100
        self.jefe_vida_actual = self.jefe_vida_max
        self.ultimo_disparo_jefe = 0
        self.cadencia_base_jefe = 1500  # ms
        self.tiempo_ultimo_patron = 0
        self.patron_actual = 0
        self.duracion_patron = 5000  # ms
        # Proyectiles
        self.proyectiles_jugador = []
        self.proyectiles_jefe = []
        self.vel_proyectil = 7
        self.vel_rayo = 10
        # Colores para proyectiles
        self.colores_proyectil_jefe = [ROJO, VERDE, AZUL, NARANJA, CIAN]
        # Fuentes para esta pantalla
        self.fuente_combate = pygame.font.SysFont(None, 36)
        self.fuente_pequena_combate = pygame.font.SysFont(None, 28)
    def crear_botones(self):
        self.botones.clear()
        # Botón para regresar al juego principal (por si se pierde o gana)
        boton_volver = Boton(
            x=self.ancho // 2 - 100,
            y=self.alto - 100,
            ancho=200,
            alto=50,
            texto="Volver al Juego",
            accion=self.accion_volver_juego
        )
        self.botones.append(boton_volver)
    def accion_volver_juego(self):
        global estado_juego, combate_ganado
        # Aseguramos que volvemos al estado correcto
        estado_juego = ESTADO_JUGANDO
        combate_ganado = True 
        resetear_juego()
        # No necesitamos hacer nada más aquí.
    def manejar_evento(self, evento):
        # Manejo de botones
        for boton in self.botones:
            accion = boton.manejar_evento(evento)
            if accion:
                accion()
        # Manejo de teclas de disparo
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_z:
                self.disparando_rayo = True
                self.inicio_rayo = pygame.time.get_ticks()
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_z:
                self.disparando_rayo = False
                # Disparar bala normal al soltar si no fue un ataque cargado
                tiempo_actual = pygame.time.get_ticks()
                if tiempo_actual - self.inicio_rayo < self.duracion_rayo:
                    self.disparar_jugador()
    def disparar_jugador(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_disparo_jugador > self.cadencia_disparo_jugador:
            # Crear un proyectil en el centro superior del jugador
            proyectil = {
                "x": self.jugador_x + self.jugador_ancho // 2 - 2,
                "y": self.jugador_y,
                "ancho": 4,
                "alto": 15,
                "color": AZUL_CLARO,
                "tipo": "bala"
            }
            self.proyectiles_jugador.append(proyectil)
            self.ultimo_disparo_jugador = tiempo_actual
    def disparar_rayo_jugador(self):
        # Crear un proyectil tipo rayo que se mueve hacia arriba
        rayo = {
            "x": self.jugador_x + self.jugador_ancho // 2 - 5,
            "y": self.jugador_y, # Comienza desde la parte superior del jugador
            "ancho": 10,
            "alto": 20, # Altura fija del rayo en pantalla
            "color": DORADO,
            "tipo": "rayo"
        }
        self.proyectiles_jugador.append(rayo)
        self.ultimo_disparo_jugador = pygame.time.get_ticks() # Reiniciar cadencia
    def disparar_jefe(self, tipo="normal"):
        if tipo == "normal":
            # Disparo normal aleatorio
            proyectil = {
                "x": self.jefe_x + self.jefe_ancho // 2 - 3,
                "y": self.jefe_y + self.jefe_alto,
                "ancho": 6,
                "alto": 20,
                "color": random.choice(self.colores_proyectil_jefe),
                "tipo": "bala_jefe"
            }
            self.proyectiles_jefe.append(proyectil)
        elif tipo == "barrage":
            # Disparo en ráfaga
            for i in range(-2, 3):  # 5 proyectiles
                proyectil = {
                    "x": self.jefe_x + self.jefe_ancho // 2 - 3,
                    "y": self.jefe_y + self.jefe_alto,
                    "ancho": 6,
                    "alto": 20,
                    "color": random.choice(self.colores_proyectil_jefe),
                    "tipo": "bala_jefe",
                    "vel_x": i * 1.5  # Velocidad horizontal diferente para cada uno
                }
                self.proyectiles_jefe.append(proyectil)
        elif tipo == "rain":
            # Lluvia de proyectiles desde arriba
            for _ in range(8):
                proyectil = {
                    "x": random.randint(0, self.ancho),
                    "y": 0,
                    "ancho": 6,
                    "alto": 20,
                    "color": random.choice(self.colores_proyectil_jefe),
                    "tipo": "bala_jefe_lluvia",
                    "vel_y": self.vel_proyectil + 2  # Más rápido
                }
                self.proyectiles_jefe.append(proyectil)
    def actualizar(self, pos_mouse):
        # Actualizar botones
        for boton in self.botones:
            boton.actualizar(pos_mouse)
        # Lógica del Jugador
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.jugador_x = max(0, self.jugador_x - self.jugador_vel)
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.jugador_x = min(self.ancho - self.jugador_ancho, self.jugador_x + self.jugador_vel)
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.jugador_y = max(self.alto // 2, self.jugador_y - self.jugador_vel)
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.jugador_y = min(self.alto - self.jugador_alto, self.jugador_y + self.jugador_vel)
        # Verificar si se está disparando un rayo
        tiempo_actual = pygame.time.get_ticks()
        if self.disparando_rayo:
            if tiempo_actual - self.inicio_rayo >= self.duracion_rayo:
                self.disparando_rayo = False
                self.disparar_rayo_jugador()
        self.jefe_x += self.jefe_vel * self.jefe_direccion
        # Cambiar dirección si toca un borde
        if self.jefe_x <= 0 or self.jefe_x + self.jefe_ancho >= self.ancho:
            self.jefe_direccion *= -1
        # Determinar cadencia de disparo basada en vida
        porcentaje_vida = self.jefe_vida_actual / self.jefe_vida_max
        cadencia_actual_jefe = self.cadencia_base_jefe * (0.3 + 0.7 * porcentaje_vida)  # Más rápido con menos vida
        # Patrones de ataque
        if tiempo_actual - self.tiempo_ultimo_patron > self.duracion_patron:
            self.patron_actual = (self.patron_actual + 1) % 3
            self.tiempo_ultimo_patron = tiempo_actual
        if tiempo_actual - self.ultimo_disparo_jefe > cadencia_actual_jefe:
            if self.patron_actual == 0:
                self.disparar_jefe("normal")
            elif self.patron_actual == 1:
                self.disparar_jefe("barrage")
            elif self.patron_actual == 2:
                self.disparar_jefe("rain")
            self.ultimo_disparo_jefe = tiempo_actual
        # Actualizar Proyectiles
        # Jugador
        for proyectil in self.proyectiles_jugador[:]:
            if proyectil["tipo"] == "bala":
                proyectil["y"] -= self.vel_proyectil
                # Verificar colisión con jefe
                proy_rect = pygame.Rect(proyectil["x"], proyectil["y"], proyectil["ancho"], proyectil["alto"])
                jefe_rect = pygame.Rect(self.jefe_x, self.jefe_y, self.jefe_ancho, self.jefe_alto)
                if proy_rect.colliderect(jefe_rect):
                    self.jefe_vida_actual -= 1
                    if proyectil in self.proyectiles_jugador:
                        self.proyectiles_jugador.remove(proyectil)
                    if self.jefe_vida_actual <= 0:
                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.stop() # Detener la música de fondo
                        if sonido_win:
                            sonido_win.play() # Reproducir sonido de victoria
                        # Jefe derrotado - Volver al juego o mostrar victoria
                        print("¡Jefe derrotado!")
                        self.accion_volver_juego()  # Por ahora, simplemente volvemos
            elif proyectil["tipo"] == "rayo":
                # Mover el rayo hacia arriba
                proyectil["y"] -= self.vel_rayo
                # Verificar colisión con jefe
                proy_rect = pygame.Rect(proyectil["x"], proyectil["y"], proyectil["ancho"], proyectil["alto"])
                jefe_rect = pygame.Rect(self.jefe_x, self.jefe_y, self.jefe_ancho, self.jefe_alto)
                if proy_rect.colliderect(jefe_rect):
                    self.jefe_vida_actual -= self.daño_rayo
                    if proyectil in self.proyectiles_jugador:
                        self.proyectiles_jugador.remove(proyectil)
                    if self.jefe_vida_actual <= 0:
                        print("¡Jefe derrotado!")
                        self.accion_volver_juego()
                    continue
            if proyectil["y"] + proyectil["alto"] < 0 or proyectil["y"] > self.alto:
                if proyectil in self.proyectiles_jugador:
                    self.proyectiles_jugador.remove(proyectil)
        # Jefe
        for proyectil in self.proyectiles_jefe[:]:
            if proyectil["tipo"] == "bala_jefe":
                proyectil["y"] += proyectil.get("vel_y", self.vel_proyectil)
                # Aplicar velocidad horizontal si existe
                if "vel_x" in proyectil:
                    proyectil["x"] += proyectil["vel_x"]
            elif proyectil["tipo"] == "bala_jefe_lluvia":
                proyectil["y"] += proyectil["vel_y"]
            # Verificar colisión con jugador
            proy_rect = pygame.Rect(proyectil["x"], proyectil["y"], proyectil["ancho"], proyectil["alto"])
            jugador_rect = pygame.Rect(self.jugador_x, self.jugador_y, self.jugador_ancho, self.jugador_alto)
            if proy_rect.colliderect(jugador_rect):
                self.jugador_vidas -= 1
                if proyectil in self.proyectiles_jefe:
                    self.proyectiles_jefe.remove(proyectil)
                if self.jugador_vidas <= 0:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop() 
                    if sonido_game_over:
                        sonido_game_over.play() 
                    self.manejar_derrota()
            # Eliminar proyectiles fuera de pantalla
            if proyectil["y"] > self.alto or proyectil["y"] + proyectil["alto"] < 0 or proyectil["x"] > self.ancho or \
                    proyectil["x"] + proyectil["ancho"] < 0:
                if proyectil in self.proyectiles_jefe:
                    self.proyectiles_jefe.remove(proyectil)
    def manejar_derrota(self):

        global estado_juego, pantalla_resultados, pasajeros_atendidos, pasajeros_perdidos, monedas
        # Establecer datos para la pantalla de resultados
        pantalla_resultados.establecer_datos(pasajeros_atendidos, pasajeros_perdidos, monedas)
        estado_juego = ESTADO_RESULTADOS

    def crear_textura_fondo_estatico(self):
        import math # Asegurarse de tener math disponible

        self.textura_fondo_estatico = pygame.Surface((self.ancho, self.alto))
        # Usamos esta superficie como "pantalla" destino para dibujar
        pantalla_textura = self.textura_fondo_estatico

        for y in range(0, self.alto, 4): # Dibujar líneas cada 4 píxeles para eficiencia
            factor = y / self.alto
            r = int(5 + 5 * factor)
            g = int(0 + 0 * factor)
            b = int(15 + 10 * factor)
            color = (r, g, b)
            pygame.draw.line(pantalla_textura, color, (0, y), (self.ancho, y))

        planeta_x, planeta_y = self.ancho - 350, self.alto // 2
        planeta_radio = 200

        for r in range(planeta_radio, 0, -1):
            factor = r / planeta_radio
            color_r = int(120 * factor + 80 * (1 - factor))
            color_g = int(70 * factor + 30 * (1 - factor))
            color_b = int(170 * factor + 130 * (1 - factor))
            # Asegurar que los componentes estén en el rango 0-255 
            color_r = max(0, min(255, color_r))
            color_g = max(0, min(255, color_g))
            color_b = max(0, min(255, color_b))
            color = (color_r, color_g, color_b)
            pygame.draw.circle(pantalla_textura, color, (planeta_x, planeta_y), r)

    
        for i in range(80): # Aumentado un poco el detalle
            lat = (i / 80.0) * math.pi - math.pi/2
            # Importante: Usamos un offset fijo en lugar del tiempo para que sea estático
            longitud_offset = 0 # (0 * 2 * math.pi) # Sin rotación para la textura estática
            for j in range(30):
                lon = (j / 30.0) * 2 * math.pi + longitud_offset
                # Usar un radio ligeramente menor que el del planeta principal
                r_textura = planeta_radio * 0.95
                x_textura = planeta_x + r_textura * math.cos(lon) * math.cos(lat)
                y_textura = planeta_y + r_textura * math.sin(lat) + r_textura * 0.2 * math.sin(lon) * math.cos(lat) # Aplanar un poco

                # Variar el color ligeramente para textura (estático)
                color_var = (i * j) % 50
                color_r = max(0, min(255, 100 - color_var))
                color_g = max(0, min(255, 50 - color_var//2))
                color_b = max(0, min(255, 150 - color_var))
                color = (color_r, color_g, color_b)
                pygame.draw.circle(pantalla_textura, color, (int(x_textura), int(y_textura)), 1)

        num_anillos = 5
        for i in range(num_anillos):
            radio_anillo = planeta_radio + 40 + i * 20
            # Hacer que los anillos estén inclinados
            inclinacion = 0.3
            anillo_surface = pygame.Surface((radio_anillo * 2 + 40, radio_anillo * 2 + 40), pygame.SRCALPHA)
            
            # Dibujar el anillo base como una elipse estirada
            ancho_anillo = 10 - i # Anillos más externos un poco más delgados
            # Asegurar que alpha_componente se encuentre en un rango válido
            alpha_componente = max(40, min(255, 180 - i * 25))
            color_anillo_base = (190, 170, 150, alpha_componente)
            pygame.draw.ellipse(anillo_surface, color_anillo_base,
                                (20, radio_anillo * (1 - inclinacion) + 20,
                                radio_anillo * 2, radio_anillo * 2 * inclinacion),
                                ancho_anillo)
            
            # Añadir textura de partículas al anillo (estática)
            for k in range(100):
                # Generar puntos aleatorios dentro del área del anillo
                angulo_part = (k / 100.0) * 2 * math.pi
                radio_part = radio_anillo + (k % 20) - 10 # Variación en el radio
                # Solo dibujar dentro del anillo aproximadamente
                if radio_anillo - 15 < radio_part < radio_anillo + 15:
                    x_part = radio_anillo + 20 + radio_part * math.cos(angulo_part)
                    y_part = radio_anillo * (1 - inclinacion) + 20 + radio_part * math.sin(angulo_part) * inclinacion
                    # Hacer que algunas partículas sean más brillantes (estático)
                    brillo_part = 200 + (k % 55)
                    # Asegurar que los componentes del color estén en el rango 0-255
                    color_r = min(255, brillo_part)
                    color_g = min(255, brillo_part)
                    color_b = min(255, brillo_part - 20)
                    color_part = (color_r, color_g, color_b)
                    pygame.draw.circle(anillo_surface, color_part, (int(x_part), int(y_part)), 1)

            # Dibujar la superficie del anillo prerrenderizada en la textura principal
            pantalla_textura.blit(anillo_surface, (planeta_x - radio_anillo - 20, planeta_y - radio_anillo - 20))

       
        for i in range(100): # Menos estrellas que las dinámicas para no sobrecargar
            x = (i * 53) % self.ancho
            y = (i * 37) % self.alto
            # Calcular distancia al planeta para evitar superposición
            distancia_cuadrada_planeta = (x - planeta_x)**2 + (y - planeta_y)**2
            # También evitar superposición con anillos
            distancia_cuadrada_anillos = (x - planeta_x)**2 + (y - planeta_y)**2
            if (distancia_cuadrada_planeta > (planeta_radio + 120)**2) and \
            (distancia_cuadrada_anillos > (planeta_radio + 100)**2):
                # Brillo fijo para estrella estática
                brillo = 180 + (i % 75)
                # Limitar brillo a 255
                brillo = min(255, brillo)
                # Componente azul fijo también
                componente_azul = min(255, brillo + 20)
                if i % 20 < 14: # Mayoría blancas/azules
                    color_estrella = (brillo, brillo, componente_azul)
                elif i % 20 < 18: # Algunas amarillas
                    color_estrella = (min(255, brillo + 50), brillo, brillo // 2)
                else: 
                    color_estrella = (brillo, brillo // 2, brillo // 3)

                tam = 1 # Tamaño fijo pequeño
                pygame.draw.circle(pantalla_textura, color_estrella, (x, y), tam)
    print("Textura de fondo estático de combate creada.")

    def dibujar(self, pantalla):
        # Fondo del combate
        pantalla.fill(NEGRO)
        import math
        tiempo_actual = pygame.time.get_ticks()

           #  Dibujar un planeta gigante en el fondo 
        planeta_x, planeta_y = self.ancho - 350, self.alto // 2
        planeta_radio = 200
                # Dibujar fondo prerrenderizado
        if self.textura_fondo_estatico:
            pantalla.blit(self.textura_fondo_estatico, (0, 0))
        else:
            # Fallback si por alguna razón la textura no se creó
            pantalla.fill((5, 0, 15)) # Color de fondo base
                    
        # Dibujar estrellas de fondo parpadeantes 
        for i in range(150):
            x = (i * 53) % self.ancho
            y = (i * 37) % self.alto
            distancia_cuadrada = (x - planeta_x)**2 + (y - planeta_y)**2
            if distancia_cuadrada > (planeta_radio + 120)**2:
                # Parpadeo basado en el índice y el tiempo
                brillo_base = 180 + (i % 75)
                brillo = int(brillo_base * (0.7 + 0.3 * math.sin(tiempo_actual / 300.0 + i * 0.2)))
                brillo = max(0, min(255, brillo))
                
                tam = 1 + (i % 3) // 2 # Tamaño 1 o 2
                # Colores de estrella variados
                if i % 20 < 14: # Mayoría blancas/azules
                    color_estrella = (brillo, brillo, min(255, brillo + 50))
                elif i % 20 < 18: # Algunas amarillas
                    color_estrella = (min(255, brillo + 50), brillo, brillo // 2)
                else: 
                    color_estrella = (brillo, brillo // 2, brillo // 3)
                
                pygame.draw.circle(pantalla, color_estrella, (x, y), tam)

        # Partículas de polvo cósmico 
        for i in range(200):
            x = (i * 29 + tiempo_actual // 100) % (self.ancho + 100) - 50
            y = (i * 41 + tiempo_actual // 120) % (self.alto + 100) - 50
            # Solo dibujar algunas para no saturar
            if (i + tiempo_actual // 500) % 10 < 2:
                pygame.draw.circle(pantalla, (150, 150, 180), (x, y), 1)

        # Cometas ocasionales 
        # Usar el tiempo para determinar si aparece un cometa
        if (tiempo_actual // 3000) % 17 == 0: # Aproximadamente cada 51 segundos
            cometa_offset = (tiempo_actual % 3000) / 3000.0 # De 0 a 1 durante esos 3 segundos
            if cometa_offset < 0.8: # Solo dibujar durante 2.4 segundos de ese periodo
                # Cometa desde la esquina superior derecha a la inferior izquierda
                cometa_x = int(self.ancho + 100 - cometa_offset * (self.ancho + 200))
                cometa_y = int(-50 + cometa_offset * (self.alto + 200))
                
                # Dibujar cola del cometa
                for j in range(1, 20):
                    alpha_cola = 255 - j * 15
                    if alpha_cola > 0:
                        pos_x_cola = cometa_x + j * 2
                        pos_y_cola = cometa_y - j
                        s_cola = pygame.Surface((6, 6), pygame.SRCALPHA)
                        pygame.draw.circle(s_cola, (100, 200, 255, alpha_cola), (3, 3), 3 - j//7)
                        pantalla.blit(s_cola, (pos_x_cola, pos_y_cola))
                # Dibujar cabeza del cometa
                pygame.draw.circle(pantalla, (220, 240, 255), (cometa_x, cometa_y), 4)
                pygame.draw.circle(pantalla, (255, 255, 220), (cometa_x, cometa_y), 2)

        #  Dibujar asteroides en primer plano con más variedad 
        for i in range(50):
            x = (i * 101 + tiempo_actual // (40 + i % 30)) % (self.ancho + 300) - 150
            y = (i * 71 + (i*i) // 150 + tiempo_actual // 200) % self.alto # Movimiento vertical lento
            
            tam = 3 + (i % 10)
            
            # Variar el color de los asteroides
            color_base_r = 90 + (i % 30)
            color_base_g = 80 + (i % 25)
            color_base_b = 70 + (i % 20)
            color_asteroide = (color_base_r, color_base_g, color_base_b)

            if tam > 6:
                pygame.draw.circle(pantalla, color_asteroide, (x, y), tam)
                # Cráteres
                for j in range(max(1, tam // 2)):
                    angulo_crater = (j / (tam//2)) * 2 * math.pi + (tiempo_actual / 10000.0)
                    dist_crater = (j % (tam//2)) * (tam / (tam//2))
                    crater_x = x + math.cos(angulo_crater) * dist_crater
                    crater_y = y + math.sin(angulo_crater) * dist_crater
                    if (crater_x - x)**2 + (crater_y - y)**2 < tam**2:
                        pygame.draw.circle(pantalla, (color_base_r - 20, color_base_g - 20, color_base_b - 20), (crater_x, crater_y), max(1, tam//4))
            else:
                pygame.draw.circle(pantalla, color_asteroide, (x, y), tam)
                # Para asteroides pequeños, un punto central más claro
                pygame.draw.circle(pantalla, (color_base_r + 20, color_base_g + 20, color_base_b + 20), (x, y), max(1, tam//3))

        # Dibujar jugador (cubo)
        pygame.draw.rect(pantalla, AZUL, (self.jugador_x, self.jugador_y, self.jugador_ancho, self.jugador_alto))
        pygame.draw.rect(pantalla, BLANCO, (self.jugador_x, self.jugador_y, self.jugador_ancho, self.jugador_alto), 2)
        # Dibujar jefe (cubo)
        pygame.draw.rect(pantalla, ROJO, (self.jefe_x, self.jefe_y, self.jefe_ancho, self.jefe_alto))
        pygame.draw.rect(pantalla, BLANCO, (self.jefe_x, self.jefe_y, self.jefe_ancho, self.jefe_alto), 3)
        # Dibujar ojos del jefe para darle más personalidad
        pygame.draw.circle(pantalla, BLANCO, (self.jefe_x + 20, self.jefe_y + 30), 8)
        pygame.draw.circle(pantalla, BLANCO, (self.jefe_x + self.jefe_ancho - 20, self.jefe_y + 30), 8)
        pygame.draw.circle(pantalla, NEGRO, (self.jefe_x + 20, self.jefe_y + 30), 4)
        pygame.draw.circle(pantalla, NEGRO, (self.jefe_x + self.jefe_ancho - 20, self.jefe_y + 30), 4)
        # Barra de vida del jefe
        barra_ancho = 200
        barra_alto = 20
        barra_x = self.ancho // 2 - barra_ancho // 2
        barra_y = self.jefe_y + self.jefe_alto + 10
        pygame.draw.rect(pantalla, GRIS, (barra_x, barra_y, barra_ancho, barra_alto))
        vida_proporcional = int((self.jefe_vida_actual / self.jefe_vida_max) * barra_ancho)
        pygame.draw.rect(pantalla, VERDE if self.jefe_vida_actual > 30 else ROJO,
                         (barra_x, barra_y, vida_proporcional, barra_alto))
        pygame.draw.rect(pantalla, BLANCO, (barra_x, barra_y, barra_ancho, barra_alto), 2)
        texto_vida_jefe = self.fuente_pequena_combate.render(f"JEFE: {self.jefe_vida_actual}/{self.jefe_vida_max}",
                                                             True, BLANCO)
        pantalla.blit(texto_vida_jefe, (barra_x, barra_y - 25))
        # Dibujar vidas del jugador
        texto_vidas = self.fuente_combate.render(f"VIDAS: {self.jugador_vidas}", True, BLANCO)
        pantalla.blit(texto_vidas, (20, 20))
        # Dibujar indicador de rayo cargando
        if self.disparando_rayo:
            tiempo_carga = pygame.time.get_ticks() - self.inicio_rayo
            porcentaje_carga = min(1.0, tiempo_carga / self.duracion_rayo)
            carga_ancho = int(100 * porcentaje_carga)
            pygame.draw.rect(pantalla, GRIS, (20, 60, 100, 15))
            pygame.draw.rect(pantalla, DORADO, (20, 60, carga_ancho, 15))
            pygame.draw.rect(pantalla, BLANCO, (20, 60, 100, 15), 2)
            texto_carga = self.fuente_pequena_combate.render("RAYO", True, BLANCO)
            pantalla.blit(texto_carga, (20, 75))
        # Dibujar proyectiles del jugador
        for proyectil in self.proyectiles_jugador:
            pygame.draw.rect(pantalla, proyectil["color"],
                             (proyectil["x"], proyectil["y"], proyectil["ancho"], proyectil["alto"]))
            if proyectil["tipo"] == "rayo":
                # Añadir un efecto de brillo al rayo
                pygame.draw.rect(pantalla, BLANCO,
                                 (proyectil["x"], proyectil["y"], proyectil["ancho"], proyectil["alto"]), 1)
        # Dibujar proyectiles del jefe
        for proyectil in self.proyectiles_jefe:
            pygame.draw.rect(pantalla, proyectil["color"],
                             (proyectil["x"], proyectil["y"], proyectil["ancho"], proyectil["alto"]))
            # Añadir un pequeño círculo para hacerlos más visibles
            pygame.draw.circle(pantalla, BLANCO,
                               (proyectil["x"] + proyectil["ancho"] // 2, proyectil["y"] + proyectil["alto"] // 2), 2)
        # Dibujar botones si es necesario (Game Over o Victoria)
        if self.jugador_vidas <= 0 or self.jefe_vida_actual <= 0:
            for boton in self.botones:
                boton.dibujar(pantalla)
            # Mensaje de Victoria o Derrota
            if self.jefe_vida_actual <= 0:
                texto_victoria = fuente_muy_grande.render("¡VICTORIA!", True, VERDE)
                pantalla.blit(texto_victoria, (self.ancho // 2 - texto_victoria.get_width() // 2, self.alto // 2 - 50))
            elif self.jugador_vidas <= 0:
                texto_derrota = fuente_muy_grande.render("DERROTA", True, ROJO)
                pantalla.blit(texto_derrota, (self.ancho // 2 - texto_derrota.get_width() // 2, self.alto // 2 - 50))
    def actualizar_dimensiones(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.crear_botones()
        # Reajustar posiciones si es necesario
        self.jugador_x = ancho // 2 - self.jugador_ancho // 2
        
estaciones = [
    pygame.Rect(X_ESTACIONES, Y_INICIO_ESTACIONES + i * (TAM_ESTACION + ESPACIO), TAM_ESTACION, TAM_ESTACION)
    for i in range(3)
]
colores_estaciones = [ROJO, VERDE, AZUL]
# Ahora cada estación tiene un diccionario de mejoras
estaciones_mejoras = [
    {"basica": False, "velocidad": False, "capacidad": False},
    {"basica": False, "velocidad": False, "capacidad": False},
    {"basica": False, "velocidad": False, "capacidad": False}
]
# Mantener estaciones_mejoradas para compatibilidad con código existente
estaciones_mejoradas = [False, False, False]
# Puertas de entrada (a la izquierda) - Más grandes
puertas_entrada = [
    pygame.Rect(885, -50, ANCHO_PUERTA, ALTO_PUERTA),
    pygame.Rect(20, 455, ANCHO_PUERTA, ALTO_PUERTA),
    pygame.Rect(20, 520, ANCHO_PUERTA, ALTO_PUERTA),
    pygame.Rect(885, 967, ANCHO_PUERTA, ALTO_PUERTA)
]
# Puerta de salida (a la derecha)
puerta_salida = pygame.Rect(ANCHO - 100, ALTO // 2 - 25, 60, 200)
# Otros elementos del juego
decoracion_rect = pygame.Rect(ANCHO - 100, ALTO - 80, 40, 40)
publicidad_rect = pygame.Rect(ANCHO - 160, ALTO - 80, 40, 40)  # Nuevo elemento de publicidad

#  Cargar Imagen de Fondo para Resultados
imagen_fondo_resultados = None
try:
    
    imagen_fondo_resultados = pygame.image.load("fin_del_juego.png")
    imagen_fondo_resultados = pygame.transform.scale(imagen_fondo_resultados, (ANCHO, ALTO)) # Si quieres escalarla
    print("Imagen fin_del_juego.png cargada.")
except pygame.error as e:
    print(f"Advertencia: No se pudo cargar la imagen 'fin_del_juego.png'. Se usará color sólido. Error: {e}")
    # imagen_fondo_resultados seguirá siendo None

# Variables globales que definen el estado del juego
global pasajeros_atendidos, pasajeros_perdidos, monedas
global falla_tecnica_activa, hora_pico_activa, DURACION_JUEGO
global soporte_tecnico_comprado, ambiente_mejorado, publicidad_mejorada

# Inicialización de algunas variables
pasajeros_atendidos = 0
pasajeros_perdidos = 0
monedas = 15  # Monedas iniciales
DURACION_JUEGO = 120000  # 2 minutos en milisegundos
falla_tecnica_activa = False
hora_pico_activa = False
soporte_tecnico_comprado = False
ambiente_mejorado = False
publicidad_mejorada = False

soporte_tecnico = None
soporte_tecnico_comprado = False  # Variable para saber si el soporte técnico ha sido comprado
# Rectángulo para el ícono del soporte técnico
soporte_tecnico_rect = pygame.Rect(ANCHO - 220, ALTO - 80, 40, 40)  # Al lado de decoración y publicidad
# Estado del juego (inicializado en resetear_juego)
ambiente_mejorado = False
publicidad_mejorada = False  # Nueva mejora de publicidad
monedas = 0
# Crear pasajeros iniciales
pasajeros = []
espacio_entre_fila = 30
# Eventos 
falla_tecnica_activa = False
falla_tecnica_inicio = 0
falla_tecnica_duracion = 30000
proximo_evento_falla_tecnica = 0  # Se inicializa en resetear_juego
estaciones_danadas = []
estacion_actual_danada = None
max_danadas = 3
tiempo_inicio_estacion_danada = 0
tiempo_max_reparacion = 5000
hora_pico_activa = False
hora_pico_inicio = 0
hora_pico_duracion = 10000
proximo_evento_hora_pico = 0  # Se inicializa en resetear_juego
hora_pico_generados = 0
max_pasajeros_hora_pico = 20
hora_pico_tiempo_ultimo_spawn = 0
hora_pico_spawn_intervalo = 300
# Variables para el menú contextual de mejoras
menu_mejoras_visible = False
menu_mejoras_estacion_idx = None
menu_mejoras_botones = []
#  Temporizador 
tiempo_inicio_juego = 0
DURACION_JUEGO = 120000  # 2 minutos en milisegundos
# Estadísticas
# Estas variables se definen aquí pero se reinician en resetear_juego
pasajeros_atendidos = 0
pasajeros_perdidos = 0
# Variables globales adicionales 
# Lista para almacenar textos flotantes
textos_flotantes = []
pantalla_secreta_activa = False
tiempo_para_secreto = 0
punto_secreto_rect = pygame.Rect(10, 10, 20, 20)  # Esquina superior izquierda, por ejemplo
punto_secreto_visible = True
ultimo_parpadeo = 0
intervalo_parpadeo = 500  # Milisegundos
# Variable para indicar si se ganó el combate 
combate_ganado = False
# Funciones del Juego
def evento_activo():
    # Asegurarse de usar las variables globales
    global falla_tecnica_activa, hora_pico_activa
    return falla_tecnica_activa or hora_pico_activa
def iniciar_evento_falla():
    # Declarar variables globales que se modifican
    global falla_tecnica_activa, falla_tecnica_inicio, estaciones_danadas, estacion_actual_danada, tiempo_inicio_estacion_danada
    global soporte_tecnico  # Acceder a la variable global
    falla_tecnica_activa = True
    falla_tecnica_inicio = pygame.time.get_ticks()
    estaciones_danadas = random.sample([0, 1, 2], max_danadas)
    estacion_actual_danada = estaciones_danadas[0]
    tiempo_inicio_estacion_danada = pygame.time.get_ticks()
    # Activar el soporte técnico SOLO SI HA SIDO COMPRADO
    if soporte_tecnico and soporte_tecnico_comprado:
        # Asignar la primera estación dañada al soporte técnico
        if estaciones_danadas:
            soporte_tecnico.asignar_reparacion(estaciones_danadas[0])
            print(f"Iniciar falla: Asignando soporte a estación {estaciones_danadas[0] + 1}")
def accion_mejorar(index, tipo_mejora):
    # Declarar variables globales que se modifican
    global monedas, menu_mejoras_visible, menu_mejoras_estacion_idx, estaciones_mejoras, estaciones_mejoradas
    costos = {"basica": 5, "velocidad": 8, "capacidad": 10}
    costo = costos[tipo_mejora]
    if not estaciones_mejoras[index][tipo_mejora] and monedas >= costo:
        estaciones_mejoras[index][tipo_mejora] = True
        monedas -= costo
        # Actualizar estaciones_mejoradas para compatibilidad
        if tipo_mejora == "basica":
            estaciones_mejoradas[index] = True
    # Cerrar el menú después de la acción
    menu_mejoras_visible = False
    menu_mejoras_estacion_idx = None
def accion_mejorar_ambiente():
    # Declarar variables globales que se modifican
    global monedas, ambiente_mejorado
    costo = 10
    if not ambiente_mejorado and monedas >= costo:
        ambiente_mejorado = True
        monedas -= costo
def accion_mejorar_publicidad():
    # Declarar variables globales que se modifican
    global monedas, publicidad_mejorada
    costo = 15
    if not publicidad_mejorada and monedas >= costo:
        publicidad_mejorada = True
        monedas -= costo
def accion_comprar_soporte_tecnico():
    global monedas, soporte_tecnico_comprado
    costo = 20  # Costo del soporte técnico
    if not soporte_tecnico_comprado and monedas >= costo:
        soporte_tecnico_comprado = True
        monedas -= costo
        # Activar el soporte técnico para que comience a chambear
        if soporte_tecnico:
            soporte_tecnico.comprar()
        print("¡Soporte Técnico comprado y activo!")
def accion_reparar():
    # Declarar variables globales que se modifican
    global monedas, estaciones_danadas, estacion_actual_danada, tiempo_inicio_estacion_danada, falla_tecnica_activa, proximo_evento_falla_tecnica
    costo_reparacion = 10
    
    # Solo permitir la reparación si hay una falla activa, hay una estación dañada, no se ha comprado el soporte técnico y hay suficientes monedas
    if falla_tecnica_activa and estacion_actual_danada is not None and not soporte_tecnico_comprado and monedas >= costo_reparacion:
        monedas -= costo_reparacion
        # Reparar estación actual
        estaciones_danadas.remove(estacion_actual_danada)
        if estaciones_danadas:
            estacion_actual_danada = estaciones_danadas[0]
            tiempo_inicio_estacion_danada = pygame.time.get_ticks()
            # Asignar la siguiente estación al soporte técnico si está disponible
            if soporte_tecnico and soporte_tecnico_comprado:
                # Asignar la nueva estación actual dañada
                if estaciones_danadas:
                    soporte_tecnico.asignar_reparacion(estaciones_danadas[0])
        else:
            falla_tecnica_activa = False
            estacion_actual_danada = None
            proximo_evento_falla_tecnica = pygame.time.get_ticks() + random.randint(30000, 60000)
def mostrar_menu_mejoras(estacion_idx):
    # Declarar variables globales que se modifican
    global menu_mejoras_visible, menu_mejoras_estacion_idx, menu_mejoras_botones, estaciones_mejoras
    menu_mejoras_visible = True
    menu_mejoras_estacion_idx = estacion_idx
    menu_mejoras_botones.clear()
    # Crear botones para las mejoras de esta estación
    x = estaciones[estacion_idx].x - 200
    y = estaciones[estacion_idx].y
    # Botón de mejora básica
    if not estaciones_mejoras[estacion_idx]["basica"]:
        boton_basica = Boton(x, y, 180, 35, f"Básica (5)", lambda idx=estacion_idx: accion_mejorar(idx, "basica"))
        menu_mejoras_botones.append(boton_basica)
        y += 40
    # Botón de mejora de velocidad
    if not estaciones_mejoras[estacion_idx]["velocidad"]:
        boton_velocidad = Boton(x, y, 180, 35, f"Velocidad (8)",
                                lambda idx=estacion_idx: accion_mejorar(idx, "velocidad"))
        menu_mejoras_botones.append(boton_velocidad)
        y += 40
    # Botón de mejora de capacidad
    if not estaciones_mejoras[estacion_idx]["capacidad"]:
        boton_capacidad = Boton(x, y, 180, 35, f"Capacidad (10)",
                                lambda idx=estacion_idx: accion_mejorar(idx, "capacidad"))
        menu_mejoras_botones.append(boton_capacidad)
def resetear_juego():
    #  Declarar todas las variables globales que se van a modificar
    global ambiente_mejorado, publicidad_mejorada, monedas, pasajeros, falla_tecnica_activa, falla_tecnica_inicio
    global proximo_evento_falla_tecnica, estaciones_danadas, estacion_actual_danada, tiempo_inicio_estacion_danada
    global hora_pico_activa, hora_pico_inicio, proximo_evento_hora_pico, hora_pico_generados, hora_pico_tiempo_ultimo_spawn
    global estaciones_mejoras, estaciones_mejoradas, ANCHO, ALTO, estaciones, Y_INICIO_ESTACIONES, X_ESTACIONES
    global puerta_salida, decoracion_rect, publicidad_rect  # MODIFICAR objetos existentes, no reasignar
    global menu_mejoras_visible, menu_mejoras_estacion_idx, menu_mejoras_botones
    global tiempo_inicio_juego, pasajeros_atendidos, pasajeros_perdidos
    global soporte_tecnico, soporte_tecnico_comprado, textos_flotantes  # Acceder a las variables globales
    global pantalla_secreta_activa, tiempo_para_secreto, punto_secreto_visible, ultimo_parpadeo  # Secreto shhh
    global combate_ganado, DURACION_JUEGO  # Variable para el combate y duración del juego
    global pantalla_combate
    # Recalcular posiciones basadas en el tamaño actual de la pantalla
    ALTURA_TOTAL_ESTACIONES = 3 * TAM_ESTACION + 2 * ESPACIO
    Y_INICIO_ESTACIONES = (ALTO - ALTURA_TOTAL_ESTACIONES) // 2
    X_ESTACIONES = ANCHO - TAM_ESTACION - MARGEN_DERECHO - 100

    pygame.mixer.music.stop()
    try:
        # Cargar e iniciar la música normal
        pygame.mixer.music.load("musica chill.mp3")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1) # Repetir infinitamente
        print("🎵 Música normal 'musica chill.mp3' reiniciada en resetear_juego.")
        # Accedemos a la variable global pantalla_combate que ya declaramos arriba
        if pantalla_combate and hasattr(pantalla_combate, 'musica_iniciada'):
             pantalla_combate.musica_iniciada = False
    except pygame.error as e:
        print(f"⚠️ No se pudo cargar o reproducir 'musica chill.mp3' en resetear_juego. Error: {e}")

    for i in range(3):
        estaciones[i].x = X_ESTACIONES
        estaciones[i].y = Y_INICIO_ESTACIONES + i * (TAM_ESTACION + ESPACIO)
        # width y height ya son TAM_ESTACION
    # Actualizar puerta de salida (MODIFICAR el objeto global existente)
    puerta_salida.x = ANCHO - 50
    puerta_salida.y = ALTO // 2 - 25
    # puerta_salida.width y height ya son 30, 50
    # Actualizar otros elementos (MODIFICAR los objetos globales existentes)
    decoracion_rect.x = ANCHO - 100
    decoracion_rect.y = ALTO - 80
    # decoracion_rect.width y height ya son 40, 40
    publicidad_rect.x = ANCHO - 160
    publicidad_rect.y = ALTO - 80
    # publicidad_rect.width y height ya son 40, 40
    # Reiniciar estado del juego
    ambiente_mejorado = False
    publicidad_mejorada = False  # Reiniciar mejora de publicidad
    
    #  Cambio: Si se ganó el combate, dar bonificaciones
    if combate_ganado:
        monedas = 50  # Empezar con más monedas
        # Extender la duración del juego
        DURACION_JUEGO = 180000  # 3 minutos en milisegundos (en lugar de 2)
        combate_ganado = False  # Resetear la bandera
        print("¡Bonificación por ganar el combate! +30 monedas y +1 minuto de juego.")
    else:
        monedas = 15  # Empezar con algunas monedas normales
        DURACION_JUEGO = 120000  # Duración normal de 2 minutos
    # ---
    # Reiniciar mejoras de estaciones
    estaciones_mejoras = [
        {"basica": False, "velocidad": False, "capacidad": False},
        {"basica": False, "velocidad": False, "capacidad": False},
        {"basica": False, "velocidad": False, "capacidad": False}
    ]
    estaciones_mejoradas = [False, False, False]
    # Reiniciar pasajeros
    pasajeros.clear()
    for i in range(5):
        tipo = random.choice(list(TIPOS_PASAJEROS.keys()))
        puerta_entrada = random.choice(puertas_entrada)
        p = Pasajero(tipo, puerta_entrada)
        p.x = puerta_entrada.x + puerta_entrada.width // 2
        p.y = puerta_entrada.y + puerta_entrada.height // 2
        p.activo = False
        pasajeros.append(p)
    if pasajeros:
        pasajeros[0].activo = True
    # Reiniciar eventos
    falla_tecnica_activa = False
    falla_tecnica_inicio = 0
    proximo_evento_falla_tecnica = pygame.time.get_ticks() + random.randint(20000, 40000)
    estaciones_danadas = []
    estacion_actual_danada = None
    tiempo_inicio_estacion_danada = 0
    hora_pico_activa = False
    hora_pico_inicio = 0
    proximo_evento_hora_pico = pygame.time.get_ticks() + random.randint(10000, 30000)
    hora_pico_generados = 0
    hora_pico_tiempo_ultimo_spawn = 0
    # Reiniciar menú de mejoras
    menu_mejoras_visible = False
    menu_mejoras_estacion_idx = None
    menu_mejoras_botones.clear()
    # Reiniciar temporizador y estadísticas
    tiempo_inicio_juego = pygame.time.get_ticks()
    pasajeros_atendidos = 0
    pasajeros_perdidos = 0
    # Reiniciar textos flotantes
    textos_flotantes.clear()
    # Reiniciar o crear el Soporte Técnico 
    soporte_tecnico_comprado = False  # El soporte técnico no está comprado al reiniciar
    if soporte_tecnico is None:
        # Crear la instancia si no existe (primera vez)
        soporte_tecnico = SoporteTecnico(ANCHO // 2, ALTO // 2)  # Comienza en el centro
    else:
      
        pass
# - Reiniciar variables secretas -
pantalla_secreta_activa = False

if not combate_ganado:
    # Programar el secreto entre 30 y 90 segundos después del inicio
    tiempo_para_secreto = tiempo_inicio_juego + random.randint(30000, 90000)
    punto_secreto_visible = True # Solo se hace visible si no se ha ganado
else:
    # Si ya se ganó, asegurarse de que esté desactivado
    punto_secreto_visible = False
    tiempo_para_secreto = float('inf') # O un tiempo muy grande, para que nunca se active

ultimo_parpadeo = pygame.time.get_ticks()

# Botón de reparación (aparece solo durante Falla Técnica)
boton_reparar = Boton(
    x=0, y=0, ancho=200, alto=50,
    texto=f"Reparar (10)",
    accion=accion_reparar,
    color_normal=VERDE,
    color_hover=(0, 200, 0)
)
# Crear Menú Principal y Pantalla de Resultados 
menu_principal = MenuPrincipal(ANCHO, ALTO)
pantalla_resultados = PantallaResultados(ANCHO, ALTO)
# Crear Pantalla Secreta 
pantalla_secreta = PantallaSecreta(ANCHO, ALTO)
# Crear Pantalla de Combate
pantalla_combate = PantallaCombate(ANCHO, ALTO)  

resetear_juego()
while True:
    tiempo_actual = pygame.time.get_ticks()
    pos_mouse = pygame.mouse.get_pos()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

                     #  Manejo de eventos de teclado
        if evento.type == pygame.KEYDOWN:
            
      
            if evento.key == pygame.K_o:
              
                if estado_juego != ESTADO_MENU and estado_juego != ESTADO_SECRETO:
                   
                    print("Tecla 'o' presionada, yendo a resultados...")
                   
                    pantalla_resultados.establecer_datos(pasajeros_atendidos, pasajeros_perdidos, monedas)
                    estado_juego = ESTADO_RESULTADOS 
                    continue
           
        if evento.type == pygame.VIDEORESIZE:
            # Manejar el redimensionamiento de la ventana
            ANCHO, ALTO = evento.size
            pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
            # Recalcular posiciones
            resetear_juego()
            # Actualizar menú principal y pantalla de resultados
            menu_principal.actualizar_dimensiones(ANCHO, ALTO)
            pantalla_resultados.actualizar_dimensiones(ANCHO, ALTO)
            pantalla_secreta.actualizar_dimensiones(ANCHO, ALTO)  
            pantalla_combate.actualizar_dimensiones(ANCHO, ALTO)  
        if estado_juego == ESTADO_MENU:
            menu_principal.manejar_evento(evento)
        elif estado_juego == ESTADO_JUGANDO:
            
            
            if menu_mejoras_visible:
                for boton in menu_mejoras_botones:
                    accion = boton.manejar_evento(evento)
                    if accion:
                        accion()
                # Cerrar menú si se hace clic fuera
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    # Verificar si el clic está fuera del menú
                    clic_fuera = True
                    for boton in menu_mejoras_botones:
                        if boton.rect.collidepoint(evento.pos):
                            clic_fuera = False
                            break
                    # También verificar si se hizo clic en una estación
                    for i, estacion in enumerate(estaciones):
                        if estacion.collidepoint(evento.pos):
                            clic_fuera = False
                            break
                    if clic_fuera:
                        menu_mejoras_visible = False
                        menu_mejoras_estacion_idx = None
                        menu_mejoras_botones.clear()
            # Manejar botón de reparación si está visible
            if falla_tecnica_activa:
                accion_reparar_boton = boton_reparar.manejar_evento(evento)
                if accion_reparar_boton:
                    accion_reparar_boton()
            # Manejo de clics en estaciones y otros elementos
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                #  Secreto shhh 
                if not pantalla_secreta_activa and punto_secreto_rect.collidepoint(
                        evento.pos) and punto_secreto_visible:
                    print("¡Has encontrado el secreto!")  # Para debugging
                    pantalla_secreta_activa = True
                    estado_juego = ESTADO_SECRETO  # Nuevo estado
                    continue  # Salir temprano del manejo de eventos para esta iteración
                
                for i, estacion in enumerate(estaciones):
                    if estacion.collidepoint(evento.pos):
                        mostrar_menu_mejoras(i)
                        break
                # Verificar si se hace clic en la decoración
                if decoracion_rect.collidepoint(evento.pos):
                    accion_mejorar_ambiente()
                # Verificar si se hace clic en la publicidad
                if publicidad_rect.collidepoint(evento.pos):
                    accion_mejorar_publicidad()
                # Verificar si se hace clic en el ícono del soporte técnico para comprarlo
                if soporte_tecnico_rect.collidepoint(evento.pos):
                    accion_comprar_soporte_tecnico()
            # Manejo de teclas
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    # Cerrar menú de mejoras con ESC
                    menu_mejoras_visible = False
                    menu_mejoras_estacion_idx = None
                    menu_mejoras_botones.clear()
                # Las teclas 1-3 y R se mantienen para compatibilidad
                if evento.key == pygame.K_1 and monedas >= 5 and not estaciones_mejoras[0]["basica"]:
                    accion_mejorar(0, "basica")
                if evento.key == pygame.K_2 and monedas >= 5 and not estaciones_mejoras[1]["basica"]:
                    accion_mejorar(1, "basica")
                if evento.key == pygame.K_3 and monedas >= 5 and not estaciones_mejoras[2]["basica"]:
                    accion_mejorar(2, "basica")
                if evento.key == pygame.K_r and falla_tecnica_activa and estacion_actual_danada is not None:
                    accion_reparar()
        elif estado_juego == ESTADO_RESULTADOS:
            pantalla_resultados.manejar_evento(evento)
        elif estado_juego == ESTADO_SECRETO:  
            pantalla_secreta.manejar_evento(evento)
        elif estado_juego == ESTADO_COMBATE:  
            pantalla_combate.manejar_evento(evento)
           
            if estado_juego == ESTADO_COMBATE and not getattr(pantalla_combate, 'musica_iniciada', False):
                try:
                    pygame.mixer.music.stop()  # Detener cualquier otra música
                    pygame.mixer.music.load("temaboss.mp3")  # Nombre de tu archivo
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)  # Repetir infinitamente
                    pantalla_combate.musica_iniciada = True
                    print("🎵 Música del jefe iniciada.")
                except pygame.error as e:
                    print(f"⚠️ No se pudo cargar 'musica boss.mp3'. Error: {e}")
        
    # Lógica del Juego 
    if estado_juego == ESTADO_JUGANDO:
        
        tiempo_transcurrido = tiempo_actual - tiempo_inicio_juego
        if tiempo_transcurrido >= DURACION_JUEGO:
            
            print("¡Tiempo agotado! Evaluando condición de victoria en pantalla de resultados...")
           
            # Detener la música de fondo si aún suena
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
           
            # Pasar los datos a la pantalla de resultados
            pantalla_resultados.establecer_datos(pasajeros_atendidos, pasajeros_perdidos, monedas)
            # Cambiar al estado de resultados
            estado_juego = ESTADO_RESULTADOS
            continue
      
        if soporte_tecnico:
            soporte_tecnico.actualizar(tiempo_actual)
        # Control evento falla técnica (inicio)
        if not falla_tecnica_activa and not evento_activo() and tiempo_actual >= proximo_evento_falla_tecnica:
            iniciar_evento_falla()  
        if falla_tecnica_activa and soporte_tecnico and soporte_tecnico_comprado:
            
            if (soporte_tecnico.reparando and
                    soporte_tecnico.tiempo_reparacion >= soporte_tecnico.tiempo_reparacion_necesario):
                # Verificar que la estación objetivo aún está registrada como dañada
                if (soporte_tecnico.indice_estacion_objetivo is not None and
                        soporte_tecnico.indice_estacion_objetivo in estaciones_danadas):
                    # Reparar la estación: eliminarla de la lista de dañadas
                    idx_estacion_reparada = soporte_tecnico.indice_estacion_objetivo
                    estaciones_danadas.remove(idx_estacion_reparada)
                    print(f"Estación {idx_estacion_reparada + 1} reparada automáticamente por el Soporte Técnico.")
                    # Si era la estación actual del evento, actualizar el evento
                    if estacion_actual_danada == idx_estacion_reparada:
                        if estaciones_danadas:
                            # Si hay más, la siguiente en la lista es la nueva "actual"
                            estacion_actual_danada = estaciones_danadas[0]
                            tiempo_inicio_estacion_danada = pygame.time.get_ticks()
                            # Asignar la siguiente estación al soporte técnico
                            soporte_tecnico.asignar_reparacion(estaciones_danadas[0])
                            print(f"Asignando soporte a siguiente estación {estaciones_danadas[0] + 1}")
                        else:
                            # Si no quedan estaciones dañadas, terminar la falla
                            falla_tecnica_activa = False
                            estacion_actual_danada = None
                            proximo_evento_falla_tecnica = tiempo_actual + random.randint(30000, 60000)
                            print("Falla técnica terminada por reparación automática.")
                            # El soporte técnico dejará de reparar y volverá a patrullar
                            soporte_tecnico.reparando = False
                            soporte_tecnico.estacion_objetivo = None
                            soporte_tecnico.indice_estacion_objetivo = None
                            soporte_tecnico.tiempo_reparacion = 0
                            # Reiniciar movimiento aleatorio
                            soporte_tecnico.tiempo_ultimo_cambio_direccion = tiempo_actual
          
                if not estaciones_danadas or (
                        estacion_actual_danada is not None and estacion_actual_danada != soporte_tecnico.indice_estacion_objetivo):
                    soporte_tecnico.reparando = False
                    soporte_tecnico.estacion_objetivo = None
                    soporte_tecnico.indice_estacion_objetivo = None
                    soporte_tecnico.tiempo_reparacion = 0
                    # Reiniciar movimiento aleatorio
                    soporte_tecnico.tiempo_ultimo_cambio_direccion = tiempo_actual
        # Si evento falla activa, verificar tiempo para auto reparar estación actual (por tiempo límite)
        if falla_tecnica_activa and estacion_actual_danada is not None:
            if tiempo_actual - tiempo_inicio_estacion_danada > tiempo_max_reparacion:
                # Auto reparar estación que no se reparó a tiempo
                estaciones_danadas.remove(estacion_actual_danada)
                if estaciones_danadas:
                    estacion_actual_danada = estaciones_danadas[0]
                    tiempo_inicio_estacion_danada = pygame.time.get_ticks()
                    # Asignar la siguiente estación al soporte técnico
                    if soporte_tecnico and soporte_tecnico_comprado and estaciones_danadas:
                        soporte_tecnico.asignar_reparacion(estaciones_danadas[0])
                else:
                    falla_tecnica_activa = False
                    estacion_actual_danada = None
                    proximo_evento_falla_tecnica = tiempo_actual + random.randint(30000, 60000)
        # Control evento hora pico (inicio)
        if not hora_pico_activa and not evento_activo() and tiempo_actual >= proximo_evento_hora_pico:
            hora_pico_activa = True
            hora_pico_inicio = tiempo_actual
            hora_pico_generados = 0
            hora_pico_tiempo_ultimo_spawn = tiempo_actual
        # Control evento hora pico (duración y generación limitada en fila)
        if hora_pico_activa:
            if tiempo_actual - hora_pico_inicio >= hora_pico_duracion:
                hora_pico_activa = False
                proximo_evento_hora_pico = tiempo_actual + random.randint(30000, 60000)
            else:
                # Generar pasajeros uno por uno separados en fila con intervalo
                # Si la publicidad está mejorada, generar más pasajeros a la vez
                num_pasajeros_grupo = 2 if publicidad_mejorada else 1
                if hora_pico_generados < max_pasajeros_hora_pico and tiempo_actual - hora_pico_tiempo_ultimo_spawn >= hora_pico_spawn_intervalo:
                    for _ in range(num_pasajeros_grupo):
                        tipo = random.choice(list(TIPOS_PASAJEROS.keys()))
                        puerta_entrada = random.choice(puertas_entrada)
                        nuevo = Pasajero(tipo, puerta_entrada)
                        nuevo.activo = True
                        # Posición inicial en la puerta
                        nuevo.x = puerta_entrada.x + puerta_entrada.width // 2
                        nuevo.y = puerta_entrada.y + puerta_entrada.height // 2
                        pasajeros.append(nuevo)
                        hora_pico_generados += 1
                    hora_pico_tiempo_ultimo_spawn = tiempo_actual
        if falla_tecnica_activa:
            boton_reparar.actualizar(pos_mouse)
        # Actualizar botones del menú contextual
        if menu_mejoras_visible:
            for boton in menu_mejoras_botones:
                boton.actualizar(pos_mouse)
        
        for p in pasajeros[:]:  
            if p.activo and not p.terminado and p.esperando and p.tiempo_inicio_espera > 0:
                tiempo_espera_actual = tiempo_actual - p.tiempo_inicio_espera
                # Si ha estado esperando más de 10 segundos (10000 milisegundos)
                if tiempo_espera_actual > 10000:  # 10 segundos
                    # El pasajero se va
                    print(
                        f"Pasajero tipo {p.tipo} se fue por espera excesiva. Tiempo: {tiempo_espera_actual / 1000:.1f}s")
                    # Restar dinero 
                    costo_pasajero_perdido = 2
                    monedas_anterior = monedas
                    monedas = max(-100, monedas - costo_pasajero_perdido)  # Evitar que las monedas sean negativas 
                    monedas_perdidas = monedas_anterior - monedas  # Calcular monedas realmente perdidas
                    # Marcar al pasajero como terminado para que se elimine
                    p.terminado = True
                    p.activo = False
                    # Incrementar contador de pasajeros perdidos
                    pasajeros_perdidos += 1
                    #  Crear texto flotante
                    # Posición inicial: donde estaba el pasajero
                    pos_x = int(p.x)
                    pos_y = int(p.y)
                    # Crear el texto indicando la pérdida
                    texto_perdida = f"-${monedas_perdidas}"
                    # Crear la instancia del texto flotante
                    texto_flotante = TextoFlotante(pos_x, pos_y, texto_perdida, ROJO, 2000, -1)
                    # Agregarlo a la lista global
                    textos_flotantes.append(texto_flotante)
                    
        if not pantalla_secreta_activa:
            # Verificar si es hora de mostrar el secreto
            if tiempo_actual >= tiempo_para_secreto:
                # Lógica de parpadeo
                if tiempo_actual - ultimo_parpadeo > intervalo_parpadeo:
                    punto_secreto_visible = not punto_secreto_visible
                    ultimo_parpadeo = tiempo_actual
            else:
                # Asegurarse de que no sea visible antes de tiempo
                punto_secreto_visible = False
    if estado_juego == ESTADO_MENU:
        menu_principal.actualizar(pos_mouse)
        menu_principal.dibujar(pantalla)
    elif estado_juego == ESTADO_JUGANDO:
        pantalla.fill(BLANCO)

        # Dibujar fondo
        if imagen_fondo:
            # Redimensionar la imagen de fondo si el tamaño de la pantalla cambia
            fondo_escalado = pygame.transform.scale(imagen_fondo, (ANCHO, ALTO))
            pantalla.blit(fondo_escalado, (0, 0))
        else:
            # Fallback si no se cargó la imagen
            pantalla.fill(BLANCO)  # O cualquier otro color de respaldo
        
        for i, puerta in enumerate(puertas_entrada):
            if imagen_puertas:
                # Dibujar la imagen de la puerta
                pantalla.blit(imagen_puertas, (puerta.x, puerta.y))
            else:
                # Dibujar rectángulo gris como respaldo si no se cargó la imagen
                pygame.draw.rect(pantalla, GRIS, puerta)
                pygame.draw.rect(pantalla, NEGRO, puerta, 2)
            # Opcional: Mantener el texto de la puerta encima (centrado horizontalmente)
            texto_puerta = fuente_pequena.render(f"", True, BLANCO)
            pos_texto_x = puerta.x + (puerta.width - texto_puerta.get_width()) // 2  # Centrar horizontalmente
            pos_texto_y = puerta.y + 15  # Mantener el margen superior
            pantalla.blit(texto_puerta, (pos_texto_x, pos_texto_y))
                 # Dibujar puerta de salida
        
    
        texto_salida = fuente_pequena.render("", True, BLANCO)
        pantalla.blit(texto_salida, (puerta_salida.x - 10, puerta_salida.y + 15))
        for i, estacion in enumerate(estaciones):
            color = colores_estaciones[i]
            # Cambiar color si tiene mejoras
            if estaciones_mejoras[i]["basica"]:
                color = DORADO
            if estaciones_mejoras[i]["velocidad"]:
                color = CIAN
            # Si tiene ambas mejoras, priorizar velocidad visualmente
            if estaciones_mejoras[i]["basica"] and estaciones_mejoras[i]["velocidad"]:
                color = (0, 255, 150)  # Verde azulado
            if falla_tecnica_activa and i == estacion_actual_danada:
                color = (150, 150, 150)  # Gris apagado para estación dañada actual
            # Dibujar la imagen de caja encima de la estación si está disponible
            if i < len(imagenes_cajas) and imagenes_cajas[i]:
                # Centrar la imagen de caja en la estación
                imagen_caja = imagenes_cajas[i]
                pos_x = estacion.x + (estacion.width - imagen_caja.get_width()) // 2
                pos_y = estacion.y + (estacion.height - imagen_caja.get_height()) // 2
                pantalla.blit(imagen_caja, (pos_x, pos_y))
            import math
            if falla_tecnica_activa and i in estaciones_danadas:
                offset_x = 10
                centro_x = estacion.x + estacion.width + offset_x
                centro_y = estacion.y + estacion.height // 2
                tamano = 45
                tiempo = pygame.time.get_ticks() / 180.0

                # Dibujar un marco rectangular que parpadea
                marco_ancho = tamano * 1.2
                marco_alto = tamano * 0.8
                if (int(tiempo * 2.5) % 4) < 3: # Parpadeo del marco
                    pygame.draw.rect(pantalla, (100, 200, 255), 
                                    (centro_x - marco_ancho/2, centro_y - marco_alto/2, marco_ancho, marco_alto), 2)

                # Núcleo central de advertencia (triángulo invertido)
                tamano_nucleo = tamano * 0.4
                puntos_nucleo = [
                    (centro_x, centro_y + tamano_nucleo),  # Abajo (punta)
                    (centro_x - tamano_nucleo, centro_y - tamano_nucleo * 0.5),  # Arriba izquierda
                    (centro_x + tamano_nucleo, centro_y - tamano_nucleo * 0.5)   # Arriba derecha
                ]
                # Color que parpadea entre rojo y amarillo
                if math.sin(tiempo * 4) > 0:
                    color_nucleo = (255, 50, 50) # Rojo
                else:
                    color_nucleo = (255, 255, 0) # Amarillo
                pygame.draw.polygon(pantalla, color_nucleo, puntos_nucleo)
                pygame.draw.polygon(pantalla, (255, 255, 255), puntos_nucleo, 1) # Borde blanco

                # Líneas de datos corrompidos (líneas diagonales que parpadean)
                for k in range(6):
                    if (int(tiempo * 3 + k)) % 5 < 3: # Parpadeo irregular
                        offset_linea_x = (k % 3 - 1) * tamano * 0.3
                        offset_linea_y = (k // 3 - 0.5) * tamano * 0.3
                        x_inicio = centro_x + offset_linea_x - tamano * 0.2
                        y_inicio = centro_y + offset_linea_y - tamano * 0.2
                        x_fin = centro_x + offset_linea_x + tamano * 0.2
                        y_fin = centro_y + offset_linea_y + tamano * 0.2
                        pygame.draw.line(pantalla, (100, 255, 100), (x_inicio, y_inicio), (x_fin, y_fin), 2)

                # Medidor de sobrecarga estilo barra
                barra_ancho = tamano * 0.8
                barra_alto = tamano * 0.15
                barra_x = centro_x - barra_ancho / 2
                barra_y = centro_y + tamano * 0.5
                
                # Fondo del medidor
                pygame.draw.rect(pantalla, (50, 50, 50), (barra_x, barra_y, barra_ancho, barra_alto))
                # Nivel de sobrecarga 
                nivel_sobrecarga = 0.3 + 0.7 * abs(math.sin(tiempo * 2.5)) # De 30% a 100%
                ancho_nivel = barra_ancho * nivel_sobrecarga
                # Color del nivel (verde a rojo según nivel)
                color_r = int(255 * nivel_sobrecarga)
                color_g = int(255 * (1 - nivel_sobrecarga))
                pygame.draw.rect(pantalla, (color_r, color_g, 50), (barra_x, barra_y + 2, ancho_nivel, barra_alto - 4))
                pygame.draw.rect(pantalla, (150, 150, 150), (barra_x, barra_y, barra_ancho, barra_alto), 1)

            # Dibujar indicadores de mejoras
            if estaciones_mejoras[i]["basica"]:
                pygame.draw.rect(pantalla, (255, 215, 0),
                                 pygame.Rect(estacion.x, estacion.y, estacion.width, 5))
            if estaciones_mejoras[i]["velocidad"]:
                pygame.draw.rect(pantalla, (0, 255, 255),
                                 pygame.Rect(estacion.x, estacion.y + 5, estacion.width, 5))
            if estaciones_mejoras[i]["capacidad"]:
                pygame.draw.rect(pantalla, (255, 0, 255),
                                 pygame.Rect(estacion.x, estacion.y + 10, estacion.width, 5))
        # Dibujar decoración (círculo azul claro o dorado si mejorado)
        pygame.draw.circle(pantalla, AZUL_CLARO if not ambiente_mejorado else DORADO, decoracion_rect.center, 20)
        pygame.draw.rect(pantalla, NEGRO, decoracion_rect, 2)
        texto_decor = fuente_pequena.render("DEC", True, NEGRO)
        pantalla.blit(texto_decor, (decoracion_rect.centerx - 15, decoracion_rect.centery - 10))
        # Dibujar publicidad (círculo rojo o verde si mejorado)
        pygame.draw.circle(pantalla, ROJO if not publicidad_mejorada else VERDE, publicidad_rect.center, 20)
        pygame.draw.rect(pantalla, NEGRO, publicidad_rect, 2)
        texto_pub = fuente_pequena.render("PUB", True, BLANCO)
        pantalla.blit(texto_pub, (publicidad_rect.centerx - 15, publicidad_rect.centery - 10))
        
        color_soporte_icono = ROJO_OSCURO if soporte_tecnico_comprado else GRIS_OSCURO
        pygame.draw.rect(pantalla, color_soporte_icono, soporte_tecnico_rect)
        pygame.draw.rect(pantalla, NEGRO, soporte_tecnico_rect, 2)
        # Siempre mostrar "SUP"
        texto_soporte = fuente_pequena.render("SUP", True, BLANCO)
        # Centrar el texto dentro del rectángulo
        pantalla.blit(texto_soporte, (soporte_tecnico_rect.centerx - texto_soporte.get_width() // 2,
                                      soporte_tecnico_rect.centery - texto_soporte.get_height() // 2))
        # Dibujar el Soporte Técnico móvil (siempre se dibuja si existe) 
        if soporte_tecnico:
            soporte_tecnico.dibujar(pantalla)
        # Mostrar textos eventos (centrados)
        if falla_tecnica_activa:
            texto_falla = fuente_muy_grande.render("¡FALLA TÉCNICA!", True, ROJO)
            pantalla.blit(texto_falla, (ANCHO // 2 - texto_falla.get_width() // 2, 125))
            # Mostrar mensaje de soporte técnico activo si ha sido comprado
            if soporte_tecnico_comprado:
                texto_soporte_activo = fuente.render("Soporte Técnico en camino...", True, ROJO_OSCURO)
                pantalla.blit(texto_soporte_activo,
                              (ANCHO // 2 - texto_soporte_activo.get_width() // 2, 125 + texto_falla.get_height() + 5))
        if hora_pico_activa:
            texto_pico = fuente_muy_grande.render("¡HORA PICO!", True, (255, 165, 0))
            pantalla.blit(texto_pico, (ANCHO // 2 - texto_pico.get_width() // 2, 145))
        # Pasajeros en fila delante de estación dañada actual
        if falla_tecnica_activa and estacion_actual_danada is not None:
            pasajeros_en_fila = [p for p in pasajeros if
                                 p.activo and not p.terminado and p.actual == estacion_actual_danada and p.esperando]
            pasajeros_en_fila.sort(key=lambda p: p.tiempo_llegada)
            for idx, pasajero in enumerate(pasajeros_en_fila):
                pasajero.posicion_en_fila(idx, estaciones[estacion_actual_danada].center)
        # Mover pasajeros (los que no están esperando en estación dañada)
        for p in pasajeros:
            if falla_tecnica_activa and p.actual == estacion_actual_danada and p.esperando:
                continue
            p.mover()
        # Dibujar pasajeros
        for p in pasajeros:
            p.dibujar(pantalla)
        for texto in textos_flotantes[:]:
            texto.actualizar()
            texto.dibujar(pantalla)
            # Eliminar textos que ya no están activos
            if not texto.activo:
                textos_flotantes.remove(texto)
        for i, p in enumerate(pasajeros):
            if p.terminado:
                #Verifica si llego al final/puerta de salida
                if p.actual >= len(p.destinos): # Llegó al final
                    valor_base = TIPOS_PASAJEROS[p.tipo]["valor"]
                    bonificacion = 2 if ambiente_mejorado else 1
                    monedas_ganadas = valor_base * bonificacion
                    monedas_anteriores = monedas 
                    monedas += monedas_ganadas
                    pasajeros_atendidos += 1

                    pos_x = int(p.x)
                    pos_y = int(p.y)
                    # Crear y mostrar el texto indicando la ganancia
                    texto_ganancia = f"+${monedas_ganadas}" 
                    texto_flotante_ganado = TextoFlotante(pos_x, pos_y, texto_ganancia, VERDE_LIMA, 2000, -1) # "Y" negativa para subir lentamente
                    textos_flotantes.append(texto_flotante_ganado)
                    
                p.terminado = False
                p.actual = 0
                puerta_entrada = random.choice(puertas_entrada)
                p.x = puerta_entrada.x + puerta_entrada.width // 2
                p.y = puerta_entrada.y + puerta_entrada.height // 2
                p.esperando = False
                p.activo = False
                p.tiempo_inicio_espera = 0 # Resetear tiempo de espera
                # Activar siguiente pasajero en la cola
                siguiente = None
                for j in range(i + 1, len(pasajeros)):
                    if not pasajeros[j].terminado:
                        siguiente = pasajeros[j]
                        break
                if siguiente:
                    siguiente.activo = True
                else:
                    if pasajeros:
                        pasajeros[0].activo = True
                    # Fin if p.terminado
                # Reiniciar el pasajero
                p.terminado = False
                p.actual = 0
                puerta_entrada = random.choice(puertas_entrada)
                p.x = puerta_entrada.x + puerta_entrada.width // 2
                p.y = puerta_entrada.y + puerta_entrada.height // 2
                p.esperando = False
                p.activo = False
                p.tiempo_inicio_espera = 0  # Resetear tiempo de espera
                siguiente = None
                for j in range(i + 1, len(pasajeros)):
                    if not pasajeros[j].terminado:
                        siguiente = pasajeros[j]
                        break
                if siguiente:
                    siguiente.activo = True
                else:
                    if pasajeros:
                        pasajeros[0].activo = True
        # Mostrar monedas en el centro arriba de la pantalla
        texto_monedas = fuente_grande.render(f"${monedas}", True, NEGRO)
        pantalla.blit(texto_monedas, (ANCHO // 1.5 - texto_monedas.get_width() // 2, 20))
        # Mostrar temporizador en la esquina superior derecha
        tiempo_restante = max(0, DURACION_JUEGO - tiempo_transcurrido)
        segundos_restantes = tiempo_restante // 1000
        texto_temporizador = fuente_grande.render(f"Tiempo: {segundos_restantes}s", True, NEGRO)
        pantalla.blit(texto_temporizador, (ANCHO - texto_temporizador.get_width() - 20, 20))
       
        if falla_tecnica_activa and estacion_actual_danada is not None and not soporte_tecnico_comprado:
            
            boton_reparar.rect.center = (ANCHO // 2, ALTO - 60)
           
            tiempo_restante_reparacion = max(0, tiempo_max_reparacion - (
                    tiempo_actual - tiempo_inicio_estacion_danada)) // 1000
            boton_reparar.texto = f"Reparar Est. {estacion_actual_danada + 1} ({tiempo_restante_reparacion}s) (10)"
            boton_reparar.texto_renderizado = fuente.render(boton_reparar.texto, True, NEGRO)
            boton_reparar.texto_rect = boton_reparar.texto_renderizado.get_rect(center=boton_reparar.rect.center)
            boton_reparar.dibujar(pantalla)
        if falla_tecnica_activa and estacion_actual_danada is not None and not soporte_tecnico_comprado:
            accion_reparar_boton = boton_reparar.manejar_evento(evento)
            if accion_reparar_boton:
                accion_reparar_boton()
        if menu_mejoras_visible:
            for boton in menu_mejoras_botones:
                boton.dibujar(pantalla)

        
        if not pantalla_secreta_activa and tiempo_actual >= tiempo_para_secreto and punto_secreto_visible:
           
            pygame.draw.circle(pantalla, ROJO, punto_secreto_rect.center, punto_secreto_rect.width // 2)
            
            pygame.draw.circle(pantalla, NEGRO, punto_secreto_rect.center, punto_secreto_rect.width // 2, 2)
      
    elif estado_juego == ESTADO_RESULTADOS:
        pantalla_resultados.actualizar(pos_mouse)
        pantalla_resultados.dibujar(pantalla)
    elif estado_juego == ESTADO_SECRETO:  
        pantalla_secreta.actualizar(pos_mouse)
        pantalla_secreta.dibujar(pantalla)
    elif estado_juego == ESTADO_COMBATE:  
        pantalla_combate.actualizar(pos_mouse)  
        pantalla_combate.dibujar(pantalla)
    pygame.display.flip()
    reloj.tick(60)