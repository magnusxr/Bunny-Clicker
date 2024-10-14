import pygame
import sys

# INIT
pygame.init()

# CONSTANTS
WIDTH, HEIGHT = 800, 600
BUTTON_SIZE = 200
TEXT_COLOR = "black"
FONT_SIZE = 32
BACKGROUND_COLOR = "mistyrose"
BUILDING_COLOR = "palevioletred1"
PADDING = 10
BUILDING_WIDTH, BUILDING_HEIGHT = 200, 60  # size for upgrade buttons

# SCREEN
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bunny Clicker")

# LOAD IMAGE
button_image = pygame.image.load('./imgs/bunny.png')
button_image = pygame.transform.scale(button_image, (BUTTON_SIZE, BUTTON_SIZE))


# INIT FONT
font = pygame.font.Font(None, FONT_SIZE)

# VARIABLES
bunnies = 0
last_update_time = pygame.time.get_ticks()

# BUTTON BEHIND BUNNY
button_rect = pygame.Rect(150, (HEIGHT - BUTTON_SIZE) // 2, BUTTON_SIZE, BUTTON_SIZE)

# BUILDINGS
carrots_price = 10
spinach_price = 20
lettuce_price = 100
celery_price = 200
broccoli_price = 500
carrots_owned = 0
spinach_owned = 0
lettuce_owned = 0
celery_owned = 0
broccoli_owned = 0

def draw_button():
    screen.blit(button_image, button_rect.topleft)

def draw():
    screen.fill(BACKGROUND_COLOR)
    draw_button()

    # RENDER BUNNY COUNT
    bunny_text = font.render(f"Bunnies: {bunnies:.1f}", True, TEXT_COLOR)
    screen.blit(bunny_text, (190, 100))

    # DRAW BUILDINGS
    carrots_rect = pygame.Rect(WIDTH - 250, 100, BUILDING_WIDTH, BUILDING_HEIGHT)
    spinach_rect = pygame.Rect(WIDTH - 250, 170, BUILDING_WIDTH, BUILDING_HEIGHT)
    lettuce_rect = pygame.Rect(WIDTH - 250, 240, BUILDING_WIDTH, BUILDING_HEIGHT)
    celery_rect = pygame.Rect(WIDTH - 250, 310, BUILDING_WIDTH, BUILDING_HEIGHT)
    broccoli_rect = pygame.Rect(WIDTH - 250, 380, BUILDING_WIDTH, BUILDING_HEIGHT)

    pygame.draw.rect(screen, BUILDING_COLOR, carrots_rect, border_radius=10)
    pygame.draw.rect(screen, BUILDING_COLOR, spinach_rect, border_radius=10)
    pygame.draw.rect(screen, BUILDING_COLOR, lettuce_rect, border_radius=10)
    pygame.draw.rect(screen, BUILDING_COLOR, celery_rect, border_radius=10)
    pygame.draw.rect(screen, BUILDING_COLOR, broccoli_rect, border_radius=10)

    # RENDER BUILDINGS INFO
    carrots_text = font.render(f"Carrots: {carrots_owned} (${carrots_price})", True, TEXT_COLOR)
    spinach_text = font.render(f"Spinach: {spinach_owned} (${spinach_price})", True, TEXT_COLOR)
    lettuce_text = font.render(f"Lettuce: {lettuce_owned} (${lettuce_price})", True, TEXT_COLOR)
    celery_text = font.render(f"Celery: {celery_owned} (${celery_price})", True, TEXT_COLOR)
    broccoli_text = font.render(f"Broccoli: {broccoli_owned} (${broccoli_price})", True, TEXT_COLOR)

    # CENTER AND DRAW TEXT
    screen.blit(carrots_text, carrots_text.get_rect(center=carrots_rect.center))
    screen.blit(spinach_text, spinach_text.get_rect(center=spinach_rect.center))
    screen.blit(lettuce_text, lettuce_text.get_rect(center=lettuce_rect.center))
    screen.blit(celery_text, celery_text.get_rect(center=celery_rect.center))
    screen.blit(broccoli_text, broccoli_text.get_rect(center=broccoli_rect.center))

    # CALCULATE AND RENDER BUNNIES PER SECOND
    total_bunnies_per_second = calculate_passive_bunnies()
    passive_bunnies_text = font.render(f"Bunnies per second: {total_bunnies_per_second:.1f}", True, TEXT_COLOR)
    screen.blit(passive_bunnies_text, (130, 150))

    # UPDATE
    pygame.display.flip()

def calculate_passive_bunnies():
    passive_bunnies = 0
    passive_bunnies += carrots_owned * (0.1 if carrots_owned < 10 else 0.2)  # carrots: 1 bunny every 10s
    passive_bunnies += spinach_owned * 0.125  # spinach: 1 bunny every 8s
    passive_bunnies += lettuce_owned * 0.6  # lettuce: 3 bunnies every 5s
    passive_bunnies += celery_owned * 5  # celery: 10 bunnies every 2s
    passive_bunnies += broccoli_owned * 50  # broccoli: 50 bunnies every 1s
    return passive_bunnies

def update_passive_bunnies():
    global bunnies, last_update_time

    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - last_update_time) / 1000.0  # convert to seconds
    last_update_time = current_time

    # CALCULATE TOTAL
    total_passive_bunnies = calculate_passive_bunnies() * elapsed_time
    bunnies += total_passive_bunnies

def purchase_building(price, building):
    global bunnies, carrots_price, spinach_price, lettuce_price, celery_price, broccoli_price
    global carrots_owned, spinach_owned, lettuce_owned, celery_owned, broccoli_owned
    
    if building == "carrots" and bunnies >= price:
        bunnies -= price
        carrots_owned += 1
        carrots_price = int(carrots_price * 1.25)  # Increase price by 25%

    elif building == "spinach" and bunnies >= price:
        bunnies -= price
        spinach_owned += 1
        spinach_price = int(spinach_price * 1.25)

    elif building == "lettuce" and bunnies >= price:
        bunnies -= price
        lettuce_owned += 1
        lettuce_price = int(lettuce_price * 1.25)

    elif building == "celery" and bunnies >= price:
        bunnies -= price
        celery_owned += 1
        celery_price = int(celery_price * 1.25)

    elif building == "broccoli" and bunnies >= price:
        bunnies -= price
        broccoli_owned += 1
        broccoli_price = int(broccoli_price * 1.25)

def main():
    global bunnies

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # CHECK FOR LEFT MOUSE CLICK
                    if button_rect.collidepoint(event.pos):
                        bunnies += 1
                        
                    elif (WIDTH - 250 < event.pos[0] < WIDTH - 50 and 
                          100 < event.pos[1] < 160):  # CHECK FOR PURCHASE
                        purchase_building(carrots_price, "carrots")

                    elif (WIDTH - 250 < event.pos[0] < WIDTH - 50 and 
                          170 < event.pos[1] < 230):
                        purchase_building(spinach_price, "spinach")

                    elif (WIDTH - 250 < event.pos[0] < WIDTH - 50 and 
                          240 < event.pos[1] < 300):
                        purchase_building(lettuce_price, "lettuce")

                    elif (WIDTH - 250 < event.pos[0] < WIDTH - 50 and 
                          310 < event.pos[1] < 370):
                        purchase_building(celery_price, "celery")

                    elif (WIDTH - 250 < event.pos[0] < WIDTH - 50 and 
                          380 < event.pos[1] < 440):
                        purchase_building(broccoli_price, "broccoli")

        update_passive_bunnies()
        draw()

if __name__ == "__main__":
    main()
