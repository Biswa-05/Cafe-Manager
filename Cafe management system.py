import pygame
import sys

pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (230, 230, 230)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 100, 255)
DARK_GRAY = (60, 60, 60)

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bisu's Cafe Management System")

# Fonts
font = pygame.font.SysFont("arial", 24)
title_font = pygame.font.SysFont("arial", 28, bold=True)

menu = {
    'Pizza': 40,
    'Pasta': 50,
    'Burger': 60,
    'Salad': 70,
    'Coffee': 80,
    'Sandwich': 45,
    'Fries': 35,
    'Tea': 30,
}

order_quantities = {item: 0 for item in menu}

# Layout configuration
item_buttons = []
start_y = 80
button_height = 40
row_spacing = 50
x_name = 50
x_price = 250
x_qty = 380
x_plus = 460
x_minus = 510

for i, item in enumerate(menu):
    y = start_y + i * row_spacing
    item_buttons.append({
        "item": item,
        "plus": pygame.Rect(x_plus, y, 30, button_height),
        "minus": pygame.Rect(x_minus, y, 30, button_height),
        "y": y
    })

# Control buttons
finish_btn = pygame.Rect(100, HEIGHT - 70, 180, 45)
exit_btn = pygame.Rect(320, HEIGHT - 70, 180, 45)

def draw_text(text, pos, color=BLACK, font_obj=font):
    txt = font_obj.render(text, True, color)
    screen.blit(txt, pos)

def draw_button(rect, text, color=LIGHT_GRAY, text_color=BLACK):
    pygame.draw.rect(screen, color, rect, border_radius=8)
    draw_text(text, (rect.x + 10, rect.y + 8), text_color)

def draw_menu():
    screen.fill(WHITE)
    draw_text("Bisu's Cafe - Click + or - to adjust quantity", (50, 20), DARK_GRAY, title_font)

    # Header row
    draw_text("Item", (x_name, start_y - 30), DARK_GRAY)
    draw_text("Price", (x_price, start_y - 30), DARK_GRAY)
    draw_text("Qty", (x_qty, start_y - 30), DARK_GRAY)

    for btn in item_buttons:
        item = btn["item"]
        y = btn["y"]
        qty = order_quantities[item]

        draw_text(item, (x_name, y + 8))
        draw_text(f"Rs {menu[item]}", (x_price, y + 8))
        draw_text(str(qty), (x_qty + 10, y + 8))

        draw_button(btn["plus"], "+", BLUE, WHITE)
        draw_button(btn["minus"], "-", RED, WHITE)

    draw_button(finish_btn, "Finish Order", GREEN, WHITE)
    draw_button(exit_btn, "Exit", RED, WHITE)

def show_summary():
    screen.fill(WHITE)
    draw_text("Order Summary:", (50, 30), DARK_GRAY, title_font)
    y = 80
    total = 0
    for item, qty in order_quantities.items():
        if qty > 0:
            draw_text(f"{item} x{qty} = Rs {menu[item] * qty}", (50, y))
            y += 35
            total += menu[item] * qty

    if total > 200:
        discount = int(total * 0.10)
        total -= discount
        draw_text("10% Discount Applied!", (50, y + 10), GREEN)
        draw_text(f"New Total: Rs {total}", (50, y + 40), BLACK)
    else:
        draw_text(f"Total: Rs {total}", (50, y + 20), BLACK)

    pygame.display.flip()

# Main Loop
running = True
showing_summary = False

while running:
    if not showing_summary:
        draw_menu()
        pygame.display.flip()
    else:
        show_summary()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if not showing_summary:
                for btn in item_buttons:
                    item = btn["item"]
                    if btn["plus"].collidepoint(pos):
                        order_quantities[item] += 1
                    elif btn["minus"].collidepoint(pos):
                        if order_quantities[item] > 0:
                            order_quantities[item] -= 1

                if finish_btn.collidepoint(pos):
                    showing_summary = True

                if exit_btn.collidepoint(pos):
                    running = False

pygame.quit()
sys.exit()
