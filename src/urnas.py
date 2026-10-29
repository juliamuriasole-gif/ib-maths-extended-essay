import pygame
import random

pygame.init()

screen_width, screen_height = 800, 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Modelo de Urna Personalizable")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (100, 100, 255)
RED = (255, 100, 100)

color_nombres = {
    (255, 0, 0): "Rojo",
    (0, 255, 0): "Verde",
    (0, 0, 255): "Azul",
    (255, 255, 0): "Amarillo",
    (0, 255, 255): "Cian",
    (255, 0, 255): "Magenta"
}

font = pygame.font.SysFont(None, 36)

config_urnas = {
    "Rojo": 3,
    "Verde": 3,
    "Azul": 3,
    "Amarillo": 2,
    "Cian": 2,
    "Magenta": 2,
}

bolas_en_urna = []
extraidas = []
simulacion_iniciada = False
modo_con_reemplazo = True


def generar_urna_config():
    global bolas_en_urna
    bolas_en_urna = []
    bolas_en_urna += [(255, 0, 0)] * config_urnas["Rojo"]
    bolas_en_urna += [(0, 255, 0)] * config_urnas["Verde"]
    bolas_en_urna += [(0, 0, 255)] * config_urnas["Azul"]
    bolas_en_urna += [(255, 255, 0)] * config_urnas["Amarillo"]
    bolas_en_urna += [(0, 255, 255)] * config_urnas["Cian"]
    bolas_en_urna += [(255, 0, 255)] * config_urnas["Magenta"]
    extraidas.clear()

def draw_text(text, x, y, color=BLACK):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def draw_button(text, rect, active):
    color = BLUE if active else GRAY
    pygame.draw.rect(screen, color, rect)
    draw_text(text, rect.x + 10, rect.y + 5, WHITE)

def extraer_bola():
    if bolas_en_urna:
        bola = random.choice(bolas_en_urna)
        extraidas.append(bola)
        if not modo_con_reemplazo:
            bolas_en_urna.remove(bola)

def reiniciar_experimento():
    generar_urna_config()

def draw_config():
    y_start = 100
    for i, (color, cantidad) in enumerate(config_urnas.items()):
        draw_text(f"{color}: {cantidad}", 100, y_start + i * 60)

        rect_mas = pygame.Rect(300, y_start + i * 60, 50, 40)
        rect_menos = pygame.Rect(360, y_start + i * 60, 50, 40)
        draw_button("+", rect_mas, True)
        draw_button("-", rect_menos, True)
        config_buttons[color] = (rect_mas, rect_menos)

def draw_simulacion():
    screen.fill(WHITE)

    draw_urna()

    for i, color in enumerate(extraidas):
        nombre_color = color_nombres.get(color, "Desconocido")
        draw_text(f"{nombre_color}", 50, 100 + i * 50, color)

    draw_text("Historial de colores extraídos:", 500, 50)
    draw_text(f"Bolas restantes: {len(bolas_en_urna)}", 150, 400)
    draw_text(f"Bolas extraídas: {len(extraidas)}", 150, 450)
    draw_button("Con Reemplazo", rect_con_reemplazo, modo_con_reemplazo)
    draw_button("Sin Reemplazo", rect_sin_reemplazo, not modo_con_reemplazo)
    draw_button("Reiniciar", rect_reset, False)

def draw_urna():
    pygame.draw.rect(screen, BLACK, urna_rect, 2)
    for i, color in enumerate(bolas_en_urna):
        x = 170 + (i * 50) % 280
        y = 150 + (i // 5) * 50
        pygame.draw.circle(screen, color, (x, y), 20)

urna_rect = pygame.Rect(150, 100, 300, 200)
config_buttons = {}

rect_con_reemplazo = pygame.Rect(500, 550, 200, 40)
rect_sin_reemplazo = pygame.Rect(500, 600, 200, 40)
rect_reset = pygame.Rect(500, 650, 200, 40)

running = True
while running:
    screen.fill(WHITE)
    if simulacion_iniciada:

        draw_simulacion()
    else:

        draw_text("Configura la Urna:", 300, 50)
        draw_config()

        rect_iniciar = pygame.Rect(300, 600, 200, 50)
        draw_button("Iniciar Simulación", rect_iniciar, True)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not simulacion_iniciada:

                for color, (rect_mas, rect_menos) in config_buttons.items():
                    if rect_mas.collidepoint(event.pos):
                        config_urnas[color] += 1
                    elif rect_menos.collidepoint(event.pos) and config_urnas[color] > 0:
                        config_urnas[color] -= 1

                if rect_iniciar.collidepoint(event.pos):
                    generar_urna_config()
                    simulacion_iniciada = True
            else:

                if rect_con_reemplazo.collidepoint(event.pos):
                    modo_con_reemplazo = True
                elif rect_sin_reemplazo.collidepoint(event.pos):
                    modo_con_reemplazo = False
                elif rect_reset.collidepoint(event.pos):
                    reiniciar_experimento()

                extraer_bola()


    pygame.display.flip()

pygame.quit()
