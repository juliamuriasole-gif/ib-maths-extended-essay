"""Run the essay's Pygame programs headless by feeding them synthetic events.

Usage (from the repo root):
    SDL_VIDEODRIVER=dummy python tools/headless_check.py
The original programs in src/ are not modified; this script only drives them.
"""
import os
import runpy
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
import pygame

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
_real_get = pygame.event.get


def drive(script, events_per_frame, frames=None):
    """events_per_frame: list of event lists, one per frame; then QUIT."""
    queue = list(events_per_frame)

    def fake_get(*a, **k):
        _real_get()
        if queue:
            return queue.pop(0)
        return [pygame.event.Event(pygame.QUIT)]

    pygame.event.get = fake_get
    cwd = os.getcwd()
    os.chdir(SRC)
    try:
        g = runpy.run_path(script, run_name="__main__")
    except SystemExit:
        g = {}
    finally:
        os.chdir(cwd)
        pygame.event.get = _real_get
    return g


def click(x, y):
    return pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(x, y), button=1)


def run_derangements(script, n):
    # "Tirar" button is at Rect(50, HEIGHT-60, 150, 40) with HEIGHT=700
    g = drive(script, [[click(60, 650)] for _ in range(n)])
    return g["match_counts"], g["total_rolls"]


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
    for name in ("desarreglos_mersenne.py", "desarreglos_lcg.py"):
        counts, total = run_derangements(name, n)
        print(name, total, counts, [round(c / total, 4) for c in counts])
    # Taxi: pick 2 players, then press space until someone wins
    space = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
    g = drive("taxista.py", [[click(400, 300)]] + [[space]] * 3000)
    print("taxista ganador:", g.get("ganador"))
    # Urn: start simulation, then draw 5 balls without replacement
    g = drive("urnas.py", [[click(310, 610)], [click(510, 610)]] + [[click(10, 10)]] * 4)
    print("urnas extraidas:", len(g["extraidas"]), "restantes:", len(g["bolas_en_urna"]))
