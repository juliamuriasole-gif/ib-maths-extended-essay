import pygame
import random
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("El viaje casual del taxista")

tablero = pygame.image.load("tablero.png")
tablero = pygame.transform.scale(tablero, (WIDTH, HEIGHT))

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

casillas = [
    (251, 367), (167, 325), (203, 276), (268, 278), (306, 317), (305, 391),
    (244, 426), (178, 426), (122, 365), (121, 288), (173, 227), (234, 231),
    (303, 231), (352, 286), (350, 353), (351, 422), (308, 476), (246, 475),
    (180, 474), (115, 474), (74, 433), (75, 363), (77, 294), (76, 222),
    (139, 180), (222, 181), (310, 181), (400, 182), (486, 184), (571, 183),
    (658, 185), (716, 227), (715, 296), (715, 363), (716, 435), (677, 478),
    (608, 477), (544, 478), (478, 477), (440, 423), (440, 354), (439, 286),
    (487, 232), (558, 233), (619, 230), (672, 294), (670, 367), (607, 430),
    (545, 427), (486, 390), (487, 322), (523, 282), (586, 282), (626, 329),
    (541, 360)
]

posiciones_finales = [0, len(casillas) - 1]

num_peons = 0
peons = []
peon_colors = []
PEON_RADIUS = 10
font = pygame.font.Font(None, 36)

def lanzar_dado():
    return random.choice(["green", "white"])

def mover_peon(peon_index, resultado):
    if resultado == "green":
        if peons[peon_index] < len(casillas) - 1:
            peons[peon_index] += 1
    else:
        if peons[peon_index] > 0:
            peons[peon_index] -= 1

def verificar_ganador():
    for i, peon_pos in enumerate(peons):
        if peon_pos in posiciones_finales:
            return i + 1
    return None

def pantalla_seleccion_jugadores():
    global num_peons, peons, peon_colors

    seleccionando = True
    while seleccionando:
        screen.fill(WHITE)
        titulo_texto = font.render("Selecciona el número de jugadores", True, BLACK)
        screen.blit(titulo_texto, (WIDTH // 2 - titulo_texto.get_width() // 2, HEIGHT // 4))

        botones = []
        for i in range(1, 5):
            boton_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + (i - 2) * 60, 100, 50)
            botones.append(boton_rect)
            pygame.draw.rect(screen, BLACK, boton_rect, 2)
            texto_boton = font.render(f"{i}", True, BLACK)
            screen.blit(texto_boton, (boton_rect.x + boton_rect.width // 2 - texto_boton.get_width() // 2,
                                      boton_rect.y + boton_rect.height // 2 - texto_boton.get_height() // 2))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, boton in enumerate(botones):
                    if boton.collidepoint(event.pos):
                        num_peons = i + 1
                        peons = [len(casillas) // 2] * num_peons
                        peon_colors = [RED, GREEN, BLUE, YELLOW][:num_peons]
                        seleccionando = False


        pygame.display.flip()

pantalla_seleccion_jugadores()

running = True
turn = 0
resultado_dado = ""
ganador = None
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and ganador is None:
                resultado_dado = lanzar_dado()
                print(f"Resultado del dado: {resultado_dado}")


                mover_peon(turn, resultado_dado)

                ganador = verificar_ganador()
                if ganador:
                    print(f"¡El jugador {ganador} ha ganado!")
                if not ganador:
                    turn = (turn + 1) % num_peons

    screen.blit(tablero, (0, 0))

    for i, peon_pos in enumerate(peons):
        pos = casillas[peon_pos]
        pygame.draw.circle(screen, peon_colors[i], pos, PEON_RADIUS)


    dado_pos = (WIDTH // 2 - 25, HEIGHT - 100)
    pygame.draw.rect(screen, BLACK, (dado_pos[0], dado_pos[1], 50, 50), 2)

    if resultado_dado == "green":
        pygame.draw.circle(screen, GREEN, (dado_pos[0] + 25, dado_pos[1] + 25), 20)
        pygame.draw.circle(screen, BLACK, (dado_pos[0] + 25, dado_pos[1] + 25), 20, 2)
    elif resultado_dado == "white":
        pygame.draw.circle(screen, WHITE, (dado_pos[0] + 25, dado_pos[1] + 25), 20)
        pygame.draw.circle(screen, BLACK, (dado_pos[0] + 25, dado_pos[1] + 25), 20, 2)

    if ganador:
        ganador_texto = font.render(f"¡El jugador {ganador} ha ganado!", True, BLACK)
        screen.blit(ganador_texto, (WIDTH // 2 - ganador_texto.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()


    clock.tick(30)

pygame.quit()

print("Gracias por jugar.")
