# ==========================================
# LICENSES / THIRD-PARTY NOTICES
# ==========================================
#
# This project uses:
#
# - Pygame (LGPL 2.1+)
#   https://www.gnu.org/licenses/lgpl-2.1.html
#
# - Python (PSF License)
#   https://docs.python.org/3/license.html
#
# - Apache License 2.0 (for referenced libraries)
#   https://www.apache.org/licenses/LICENSE-2.0
#
# This project is NOT affiliated with Microsoft or Windows.
#
# ==========================================

import pygame
import time
import webbrowser

pygame.init()

# ========================= WINDOW =========================

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Windows 11 Simulator")

clock = pygame.time.Clock()

# ========================= FONTS =========================

font = pygame.font.SysFont(None, 24)
big_font = pygame.font.SysFont(None, 40)

# ========================= COLORS =========================

BG = (32, 34, 40)
TASKBAR = (40, 42, 50)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
BLUE = (0, 120, 215)
WINDOW = (245, 245, 245)
TITLEBAR = (220, 220, 220)
GRAY = (180, 180, 180)

# ========================= STATE =========================

start_menu = False
current_app = None

calc_input = ""
notes_text = ""
paint_points = []

browser_url = "https://apps.microsoft.com/"

desktop_apps = [
    ("Calculator", 80, 120),
    ("Store", 220, 120),
    ("Notepad", 360, 120),
    ("Paint", 500, 120),
    ("Browser", 640, 120),
    ("About", 780, 120),
]

# ========================= HELPERS =========================

def draw_text(text, x, y, color=BLACK, size=font):
    img = size.render(text, True, color)
    screen.blit(img, (x, y))

def draw_window(title):
    pygame.draw.rect(screen, WINDOW, (180, 80, 920, 520), border_radius=18)
    pygame.draw.rect(screen, TITLEBAR, (180, 80, 920, 40),
                     border_top_left_radius=18,
                     border_top_right_radius=18)

    draw_text(title, 200, 90)

    pygame.draw.rect(screen, (220, 70, 70), (1040, 88, 40, 24), border_radius=8)
    draw_text("X", 1054, 91, WHITE)

# ========================= MAIN LOOP =========================

running = True

while running:

    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # CLICK
        if event.type == pygame.MOUSEBUTTONDOWN:

            # Start button
            if WIDTH//2 - 30 <= mx <= WIDTH//2 + 30 and HEIGHT-55 <= my <= HEIGHT-5:
                start_menu = not start_menu

            # Close app
            if current_app:
                if 1040 <= mx <= 1080 and 88 <= my <= 112:
                    current_app = None

            # Desktop icons
            for name, x, y in desktop_apps:
                if x <= mx <= x+60 and y <= my <= y+60:
                    current_app = name

            # STORE button opens real website
            if current_app == "Store":
                if 260 <= mx <= 580 and 240 <= my <= 300:
                    webbrowser.open("https://apps.microsoft.com/")

        # KEYBOARD INPUT
        if event.type == pygame.KEYDOWN:

            if current_app == "Calculator":
                if event.key == pygame.K_RETURN:
                    try:
                        calc_input = str(eval(calc_input))
                    except:
                        calc_input = "ERROR"
                elif event.key == pygame.K_BACKSPACE:
                    calc_input = calc_input[:-1]
                else:
                    calc_input += event.unicode

            if current_app == "Notepad":
                if event.key == pygame.K_BACKSPACE:
                    notes_text = notes_text[:-1]
                else:
                    notes_text += event.unicode

    # ========================= BACKGROUND =========================

    screen.fill(BG)

    for name, x, y in desktop_apps:
        pygame.draw.rect(screen, BLUE, (x, y, 60, 60), border_radius=14)
        draw_text(name, x-5, y+70, WHITE)

    # ========================= TASKBAR =========================

    pygame.draw.rect(screen, TASKBAR, (0, HEIGHT-60, WIDTH, 60))

    pygame.draw.rect(screen, BLUE, (WIDTH//2-30, HEIGHT-54, 60, 48), border_radius=14)
    draw_text("⊞", WIDTH//2-8, HEIGHT-46, WHITE, big_font)

    draw_text(time.strftime("%H:%M"), WIDTH-90, HEIGHT-38, WHITE)

    # ========================= START MENU =========================

    if start_menu:
        pygame.draw.rect(screen, (55, 58, 66), (WIDTH//2-180, 180, 360, 400), border_radius=20)
        draw_text("Start Menu", WIDTH//2-140, 200, WHITE, big_font)

        sy = 270
        for app in desktop_apps:
            pygame.draw.rect(screen, (80, 82, 90), (WIDTH//2-140, sy, 240, 40), border_radius=10)
            draw_text(app[0], WIDTH//2-120, sy+10, WHITE)
            sy += 50

    # ========================= WINDOWS =========================

    if current_app:

        draw_window(current_app)

        # CALCULATOR
        if current_app == "Calculator":
            pygame.draw.rect(screen, WHITE, (240, 160, 760, 70), border_radius=10)
            draw_text(calc_input, 260, 185)

        # NOTEPAD
        elif current_app == "Notepad":
            pygame.draw.rect(screen, WHITE, (220, 140, 820, 420))
            draw_text(notes_text, 240, 160)

        # PAINT
        elif current_app == "Paint":
            pygame.draw.rect(screen, WHITE, (220, 140, 820, 420))

            if pygame.mouse.get_pressed()[0]:
                if 220 <= mx <= 1040 and 140 <= my <= 560:
                    paint_points.append((mx, my))

            for p in paint_points:
                pygame.draw.circle(screen, BLACK, p, 4)

        # BROWSER
        elif current_app == "Browser":
            pygame.draw.rect(screen, WHITE, (220, 140, 820, 40), border_radius=10)
            draw_text(browser_url, 240, 150)
            draw_text("No real web engine in pygame", 240, 240)

        # STORE
        elif current_app == "Store":
            pygame.draw.rect(screen, WHITE, (220, 140, 820, 420))
            draw_text("Microsoft Store (Web Version)", 240, 160)

            pygame.draw.rect(screen, BLUE, (260, 240, 320, 60), border_radius=12)
            draw_text("OPEN STORE", 330, 260, WHITE)

        # ABOUT / LICENSES
        elif current_app == "About":
            pygame.draw.rect(screen, WHITE, (220, 140, 820, 420))

            draw_text("Windows 11 Simulator", 240, 160, size=big_font)
            draw_text("Made with Pygame", 240, 210)

            draw_text("NOT AFFILIATED WITH MICROSOFT", 240, 250, (200, 0, 0))

            draw_text("LICENSES:", 240, 300)

            draw_text("- Pygame (LGPL 2.1+)", 260, 340)
            draw_text("- Python (PSF License)", 260, 370)
            draw_text("- Apache License 2.0 (other libs)", 260, 400)

            draw_text("LINKS:", 240, 440)

            draw_text("LGPL: gnu.org/licenses/lgpl-2.1.html", 260, 470)
            draw_text("Apache: apache.org/licenses/LICENSE-2.0", 260, 500)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()