import pygame, sys
import random, time

pygame.init()

WIDTH, HEIGHT = 800, 600
FONT = pygame.font.SysFont("Consolas", 24)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kamen - Škare - Papir")

pygame_icon = pygame.image.load("kamen.png")
pygame.display.set_icon(pygame_icon)

# postavljanje boja
BLACK = (35, 39, 35)
WHITE = (215, 224, 215)
RED = (231, 181, 250)
GREEN = (148, 232, 231)
YELLOW = (237, 226, 144)

#inicijalizacija slika
kamen_img = pygame.image.load("kamen.png")
skare_img = pygame.image.load("škare.png")
papir_img = pygame.image.load("papir.png")

#scale-anje slika
img_size = (270, 270)
kamen_img = pygame.transform.scale(kamen_img, img_size)
skare_img = pygame.transform.scale(skare_img, img_size)
papir_img = pygame.transform.scale(papir_img, img_size)

def output_text(text, font, color, x, y):
    img = font.render(text, True, color)
    text_rect = img.get_rect(center = (x, y))
    SCREEN.blit(img, text_rect)

def draw_button(text, x, y, w, h, inactive_clr, active_clr):
    mouse = pygame.mouse.get_pos()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(SCREEN, active_clr, (x, y, w, h))
    else:
        pygame.draw.rect(SCREEN, inactive_clr, (x, y, w, h))

    text_surf = FONT.render(text, True, BLACK)
    text_rect = text_surf.get_rect()
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    SCREEN.blit(text_surf, text_rect)

    return x + w > mouse[0] > x and y + h > mouse[1] > y #vratit će boolean

def game_loop():
    user = 0
    computer = 0
    u_score = 0
    c_score = 0
    result = 0
    choices = ["kamen", "škare", "papir"]    

    animation = [kamen_img, skare_img, papir_img]
    animation_index = 0
    last_anim_time = time.time()
    round_in_progress = False
    next_round_hover = False

    click_handled = False

    running = True
    while running:
        current_time = time.time()
        mouse_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click = True
        SCREEN.fill(WHITE)

        if not round_in_progress:
            if current_time - last_anim_time >= 1:
                animation_index = (animation_index + 1) % 3
                last_anim_time = current_time
            
            animation_rect = animation[animation_index].get_rect(center=(WIDTH // 2, HEIGHT // 2.5))
            SCREEN.blit(animation[animation_index], animation_rect)

            kamen_hover = draw_button("Kamen", 50, 450, 200, 100, RED, (242, 201, 241))
            skare_hover = draw_button("Škare", 300, 450, 200, 100, GREEN, (176, 232, 213))
            papir_hover = draw_button("Papir", 550, 450, 200, 100, YELLOW, (241, 233, 174))

            if mouse_click and not click_handled:
                if kamen_hover:
                    user = "kamen"
                    round_in_progress = True
                elif skare_hover:
                    user = "škare"
                    round_in_progress = True
                elif papir_hover:
                    user = "papir"
                    round_in_progress = True
                
                if round_in_progress:
                    computer = random.choice(choices)
                    click_handled = True

                    if computer == user:
                        result = "Izjednačeno!!"
                    elif (computer == "škare" and user == "papir") or (computer == "kamen" and user == "škare") or (computer == "papir" and user == "kamen"):
                        result = "Komp je pobjedio!!"
                        c_score += 1
                    elif (user == "škare" and computer == "papir") or (user == "kamen" and computer == "škare") or (user == "papir" and computer == "kamen"):
                        result = "Korisnik je pobjedio!!"
                        u_score += 1
                    else: 
                        result = "Došlo je do greške :( "


        if round_in_progress:
            user_img = kamen_img if user == "kamen" else papir_img if user == "papir" else skare_img
            user_rect = user_img.get_rect(center=(WIDTH // 3, HEIGHT // 2))
            SCREEN.blit(user_img, user_rect)
            
            computer_img = kamen_img if computer == "kamen" else papir_img if computer == "papir" else skare_img
            computer_rect = computer_img.get_rect(center=(2 * WIDTH // 3, HEIGHT // 2))
            SCREEN.blit(computer_img, computer_rect)

            output_text(result, FONT, BLACK, WIDTH // 2, 100)

            next_round_hover = draw_button("Iduća runda", 300, 500, 200, 70, (200, 200, 200), (150, 150, 150))

        if next_round_hover and mouse_click and not click_handled:
            user = None
            computer = None
            result = None 
            round_in_progress = False
            click_handled = True 

        #rezultati
        output_text(f'Korisnik: {u_score}', FONT, BLACK, WIDTH - 120, 50)
        output_text(f'Komp: {c_score}', FONT, BLACK, WIDTH - 120, 100)

        pygame.display.update()

        if not mouse_click:
            click_handled = False

    pygame.quit()

game_loop()







