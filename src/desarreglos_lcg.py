import pygame
import random
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np

matplotlib.use("Agg")

pygame.init()
WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación de Desarreglos (LCG)")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (160, 32, 240)
COLORS = [RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE]

BOLA_RADIUS = 20
user_balls = [(100 + i * 100, HEIGHT // 3) for i in range(6)]
random_balls = [(100 + i * 100, HEIGHT // 2) for i in range(6)]

def lcg(modulus, a, c, seed):
    while True:
        seed = (a * seed + c) % modulus
        yield seed / modulus # Normalizado entre 0 y 1

modulus = 2**31 - 1
a = 1103515245
c = 12345
seed = 42
lcg_generator = lcg(modulus, a, c, seed)

def generar_desarreglo():
    lista = list(range(6))
    for i in range(len(lista)):
        j = int(next(lcg_generator) * len(lista))
        lista[i], lista[j] = lista[j], lista[i]
    return lista

button_width, button_height = 150, 40
button_roll = pygame.Rect(50, HEIGHT - 60, button_width, button_height)
button_start_stop = pygame.Rect(250, HEIGHT - 60, button_width, button_height)
button_speed_up = pygame.Rect(450, HEIGHT - 60, button_width, button_height)
button_speed_down = pygame.Rect(650, HEIGHT - 60, button_width, button_height)
button_theory = pygame.Rect(850, HEIGHT - 60, button_width, button_height)

user_order = list(range(6))
random_order = []
match_counts = [0] * 7
total_rolls = 0
rolling = False
delay = 500
graph_surface = None
show_theory = False

theoretical_probs = [0.3681, 0.3667, 0.1875, 0.0556, 0.0208, 0.0, 0.0014]

font = pygame.font.SysFont(None, 28)
small_font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

def draw_balls(positions, order, colors):
    for i, pos in enumerate(positions):
        pygame.draw.circle(screen, colors[order[i]], pos, BOLA_RADIUS)

def calculate_match(user_order, random_order):
    matches = sum([1 for i in range(6) if user_order[i] == random_order[i]])
    return matches

def draw_graph():
    global graph_surface
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    x = np.arange(7)
    probabilities = [count / total_rolls if total_rolls > 0 else 0 for count in match_counts]

    bars = ax.bar(x, probabilities, color='blue')
    ax.set_ylim(0, 1)
    ax.set_xticks(x)
    ax.set_xticklabels([f'{i}' for i in range(7)], rotation=0, ha="center")
    ax.set_xlabel('Coincidencias', labelpad=5)
    ax.set_ylabel('Probabilidad')
    ax.set_title('Distribución de Coincidencias')

    for bar, count, prob in zip(bars, match_counts, probabilities):
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 0.02, f'{count}', ha='center', va='bottom', fontsize=10)
        ax.text(bar.get_x() + bar.get_width()/2, -0.07, f'{prob:.4f}', ha='center', va='top', fontsize=10)

    if show_theory:
        for i, theory_prob in enumerate(theoretical_probs):
            ax.axhline(y=theory_prob, color='red', linestyle='--')
            ax.text(i, theory_prob + 0.02, f'T{theory_prob:.4f}', color='red', ha='center', fontsize=10)

    canvas = FigureCanvas(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.buffer_rgba()
    plt.close(fig)

    graph_surface = pygame.image.frombuffer(raw_data, canvas.get_width_height(), "RGBA")
    return graph_surface

def handle_events():
    global rolling, delay, random_order, total_rolls, match_counts, graph_surface, show_theory

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_roll.collidepoint(event.pos):
                random_order = generar_desarreglo()
                matches = calculate_match(user_order, random_order)
                match_counts[matches] += 1
                total_rolls += 1
                graph_surface = draw_graph()

            elif button_start_stop.collidepoint(event.pos):
                rolling = not rolling

            elif button_speed_up.collidepoint(event.pos):
                delay = max(100, delay - 100)

            elif button_speed_down.collidepoint(event.pos):
                delay += 100

            elif button_theory.collidepoint(event.pos):
                show_theory = not show_theory
                graph_surface = draw_graph()


    return True

running = True
while running:

    screen.fill(WHITE)

    running = handle_events()

    if rolling:
        random_order = generar_desarreglo()
        matches = calculate_match(user_order, random_order)
        match_counts[matches] += 1
        total_rolls += 1
        graph_surface = draw_graph()
        pygame.time.delay(delay)

    if len(random_order) == 6:
        draw_balls(random_balls, random_order, COLORS)
    if len(user_order) == 6:
        draw_balls(user_balls, user_order, COLORS)

    pygame.draw.rect(screen, BLACK, button_roll)
    pygame.draw.rect(screen, BLACK, button_start_stop)
    pygame.draw.rect(screen, BLACK, button_speed_up)
    pygame.draw.rect(screen, BLACK, button_speed_down)
    pygame.draw.rect(screen, BLACK, button_theory)

    screen.blit(font.render("Tirar", True, WHITE), (button_roll.x + 40, button_roll.y + 8))
    screen.blit(font.render("Start/Stop", True, WHITE), (button_start_stop.x + 20, button_start_stop.y + 8))
    screen.blit(font.render("Más rápido", True, WHITE), (button_speed_up.x + 20, button_speed_up.y + 8))
    screen.blit(font.render("Más lento", True, WHITE), (button_speed_down.x + 30, button_speed_down.y + 8))
    screen.blit(font.render("Ver P. Teórica", True, WHITE), (button_theory.x + 18, button_theory.y + 8))

    screen.blit(font.render(f"Tiradas: {total_rolls}", True, BLACK), (50, 50))

    if graph_surface is not None:
        screen.blit(graph_surface, (650, 100))

    pygame.display.flip()

    clock.tick(30)
pygame.quit()
