# Simple Pokemon Battle using Pygame
# Name - ADITYA BHARDWAJ
# Section - D2
# Roll No - 08
# Course – B TECH
# Branch – CSE

import pygame
import sys
import random

from config import *
from colors import *
from paths import *
from ui_constants import *
from battle_constants import *
from Pokemon_Data import charmander, squirtle

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

clock = pygame.time.Clock()
font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
small_font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_SMALL)

# ========== LOAD ASSETS ==========
charmander_img = pygame.image.load(POKEMON_IMAGE_DIR + "4.png").convert_alpha()
squirtle_img = pygame.image.load(POKEMON_IMAGE_DIR + "7.png").convert_alpha()

charmander_img = pygame.transform.scale(charmander_img, (SPRITE_WIDTH, SPRITE_HEIGHT))
squirtle_img = pygame.transform.scale(squirtle_img, (SPRITE_WIDTH, SPRITE_HEIGHT))

# Load win/lose images
try:
    win_image = pygame.image.load("New folder/WON.jpg").convert()
    lose_image = pygame.image.load("New folder/Lost.jpg").convert()
    # Scale images to fit screen
    win_image = pygame.transform.scale(win_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    lose_image = pygame.transform.scale(lose_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except:
    print("Warning: Win/Lose images not found. Using colored screens instead.")
    win_image = None
    lose_image = None

# ========== LOAD SOUNDS ==========
try:
    # Menu and interface sounds
    blip_sound = pygame.mixer.Sound(SOUND_DIR + "blip.wav")
    
    # Pokemon cries
    charmander_cry = pygame.mixer.Sound(SOUND_DIR + "Charmander.ogg")
    squirtle_cry = pygame.mixer.Sound(SOUND_DIR + "Squirtle.ogg")
    
    # Attack sounds
    scratch_sound = pygame.mixer.Sound(SOUND_DIR + "Attacks/Scratch.mp3")
    growl_sound = pygame.mixer.Sound(SOUND_DIR + "Attacks/Growl.mp3")
    tackle_sound = pygame.mixer.Sound(SOUND_DIR + "Attacks/Tackle.mp3")
    
    # Battle sounds
    win_sound = pygame.mixer.Sound(SOUND_DIR + "BattleWInSound.mp3")
    
    # Background music
    theme_sound = pygame.mixer.Sound(SOUND_DIR + "theme.mp3")
    
    # Set volumes
    blip_sound.set_volume(0.3)
    charmander_cry.set_volume(0.5)
    squirtle_cry.set_volume(0.5)
    scratch_sound.set_volume(0.4)
    growl_sound.set_volume(0.4)
    tackle_sound.set_volume(0.4)
    win_sound.set_volume(0.5)
    theme_sound.set_volume(0.3)
    
except Exception as e:
    print(f"Warning: Some sound files not found. Sounds disabled. Error: {e}")
    blip_sound = None
    charmander_cry = None
    squirtle_cry = None
    scratch_sound = None
    growl_sound = None
    tackle_sound = None
    win_sound = None
    theme_sound = None

# Play Pokemon cries at the start of battle
def play_starting_cries():
    if charmander_cry:
        charmander_cry.play()
        pygame.time.delay(500)  # Wait half a second
    if squirtle_cry:
        squirtle_cry.play()

# Play blip sound for button presses
def play_blip_sound():
    if blip_sound:
        blip_sound.play()

# Start background music
def start_background_music():
    if theme_sound:
        theme_sound.play(-1)  # -1 means loop forever

# Stop background music
def stop_background_music():
    if theme_sound:
        theme_sound.stop()

# Play win sound and stop background music
def play_win_sound():
    stop_background_music()
    if win_sound:
        win_sound.play()

# Play attack sounds
def play_attack_sound(move_name):
    if move_name == "Scratch" and scratch_sound:
        scratch_sound.play()
    elif move_name == "Growl" and growl_sound:
        growl_sound.play()
    elif move_name == "Tackle" and tackle_sound:
        tackle_sound.play()

# ========== VIBRATION SYSTEM ==========
class VibrationEffect:
    def __init__(self):
        self.active = False
        self.duration = 0
        self.intensity = 5
        self.timer = 0
        
    def start(self, duration=300):  # 300ms vibration
        self.active = True
        self.duration = duration
        self.timer = 0
        
    def update(self, dt):
        if self.active:
            self.timer += dt
            if self.timer >= self.duration:
                self.active = False
                
    def get_offset(self):
        if not self.active:
            return (0, 0)
        
        # Calculate vibration offset (oscillating pattern)
        progress = self.timer / self.duration
        if progress < 0.25:
            return (random.randint(-self.intensity, self.intensity), 0)
        elif progress < 0.5:
            return (0, random.randint(-self.intensity, self.intensity))
        elif progress < 0.75:
            return (random.randint(-self.intensity, self.intensity), 
                    random.randint(-self.intensity, self.intensity))
        else:
            return (-random.randint(-self.intensity, self.intensity), 
                    -random.randint(-self.intensity, self.intensity))

# Create vibration effects for both Pokemon
player_vibration = VibrationEffect()
enemy_vibration = VibrationEffect()

# ========== MESSAGE SYSTEM ==========
message_queue = []
current_message = ""
typed_message = ""
char_index = 0
text_animating = False
last_char_time = 0

# Track pending damage
pending_player_damage = None
pending_enemy_damage = None
player_turn_complete = False
enemy_turn_complete = False
just_took_damage = {"player": False, "enemy": False}  # Track who just took damage

def start_next_message():
    global current_message, typed_message, char_index
    global text_animating, pending_player_damage, pending_enemy_damage
    global player_turn_complete, enemy_turn_complete, just_took_damage

    # Apply pending damage
    if pending_player_damage is not None:
        dmg = pending_player_damage
        squirtle["current_hp"] -= dmg
        if squirtle["current_hp"] < 0:
            squirtle["current_hp"] = 0
        pending_player_damage = None
        player_turn_complete = True
        # Start enemy vibration when they take damage
        if dmg > 0:
            enemy_vibration.start()
            just_took_damage["enemy"] = True

    if pending_enemy_damage is not None:
        dmg = pending_enemy_damage
        charmander["current_hp"] -= dmg
        if charmander["current_hp"] < 0:
            charmander["current_hp"] = 0
        pending_enemy_damage = None
        enemy_turn_complete = True
        # Start player vibration when they take damage
        if dmg > 0:
            player_vibration.start()
            just_took_damage["player"] = True

    # Start next message
    if message_queue:
        current_message = message_queue.pop(0)
        typed_message = ""
        char_index = 0
        text_animating = True


def update_text_animation():
    global typed_message, char_index, text_animating, last_char_time

    if not text_animating:
        return

    now = pygame.time.get_ticks()
    if now - last_char_time >= TEXT_SPEED:
        last_char_time = now

        if char_index < len(current_message):
            typed_message += current_message[char_index]
            char_index += 1
        else:
            text_animating = False


def draw_text_box():
    x, y, w, h = TEXT_BOX_RECT
    pygame.draw.rect(screen, WHITE, (x, y, w, h))
    pygame.draw.rect(screen, BLACK, (x, y, w, h), 3)
    
    # Draw text with word wrapping
    words = typed_message.split(' ')
    lines = []
    current_line = ''
    
    for word in words:
        test_line = current_line + word + ' '
        if font.size(test_line)[0] <= w - 40:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + ' '
    
    if current_line:
        lines.append(current_line)
    
    for i, line in enumerate(lines[:3]):
        screen.blit(font.render(line, True, BLACK), (x + 20, y + 20 + i * 25))


# ========== HP ==========
def animate_hp(pokemon):
    if pokemon["display_hp"] > pokemon["current_hp"]:
        pokemon["display_hp"] -= HP_ANIMATION_SPEED


def get_hp_color(current, max_hp):
    ratio = current / max_hp
    if ratio > HP_GREEN_THRESHOLD:
        return GREEN
    elif ratio > HP_YELLOW_THRESHOLD:
        return YELLOW
    return RED


def draw_hp_bar(pos, pokemon, is_player=True):
    x, y = pos
    ratio = pokemon["display_hp"] / pokemon["max_hp"]
    width = int(HP_BAR_WIDTH * ratio)

    # Draw name and level (above HP bar)
    name_text = f"{pokemon['name']}"
    
    # Get level safely (default to 5 if not found)
    level = pokemon.get('level', 5)
    level_text = f"Lv{level}"
    
    if is_player:
        # For player (left side)
        screen.blit(font.render(name_text, True, BLACK), (x, y - 30))
        screen.blit(font.render(level_text, True, BLACK), (x + 100, y - 30))
    else:
        # For enemy (right side)
        screen.blit(font.render(name_text, True, BLACK), (x, y - 30))
        screen.blit(font.render(level_text, True, BLACK), (x + 100, y - 30))

    # Draw HP bar
    pygame.draw.rect(screen, GRAY, (x, y, HP_BAR_WIDTH, HP_BAR_HEIGHT))
    pygame.draw.rect(screen, get_hp_color(pokemon["display_hp"], pokemon["max_hp"]), (x, y, width, HP_BAR_HEIGHT))
    pygame.draw.rect(screen, BLACK, (x, y, HP_BAR_WIDTH, HP_BAR_HEIGHT), 2)
    
    # Draw HP text (below HP bar) - Only for player
    if is_player:
        hp_text = f"HP: {int(pokemon['display_hp'])}/{pokemon['max_hp']}"
        screen.blit(small_font.render(hp_text, True, BLACK), (x, y + HP_BAR_HEIGHT + 5))


# ========== BATTLE MENU SYSTEM ==========
class BattleMenu:
    def __init__(self):
        self.options = ["FIGHT", "BAG", "POKÉMON", "RUN"]
        self.cursor_pos = 0
        self.active = True  # Start active
        self.move_menu_active = False
        self.selected_move_index = 0
        
    def draw(self):
        if not self.active:
            return
            
        # Draw main menu on right side
        menu_rect = pygame.Rect(MAIN_MENU_X, MAIN_MENU_Y, MAIN_MENU_WIDTH, MAIN_MENU_HEIGHT)
        pygame.draw.rect(screen, WHITE, menu_rect)
        pygame.draw.rect(screen, BLACK, menu_rect, 3)
        
        # Draw options
        for i, option in enumerate(self.options):
            col = i % 2
            row = i // 2
            
            x = MAIN_MENU_X + 20 + (col * MAIN_MENU_OPTION_WIDTH)
            y = MAIN_MENU_Y + 15 + (row * MAIN_MENU_OPTION_HEIGHT)
            
            # Only FIGHT is selectable
            color = BLACK if i == 0 else DARK_GRAY
            screen.blit(font.render(option, True, color), (x, y))
            
            # Draw cursor
            if i == self.cursor_pos:
                cursor_x = x - 20
                cursor_y = y + 10
                pygame.draw.polygon(screen, BLACK, [
                    (cursor_x, cursor_y), 
                    (cursor_x + 10, cursor_y + 5), 
                    (cursor_x, cursor_y + 10)
                ])


# ========== MOVE SELECTION ==========
def get_player_moves(pokemon):
    return list(pokemon["moves"].keys())

def draw_move_menu(pokemon):
    pygame.draw.rect(screen, WHITE, MOVE_MENU_RECT)
    pygame.draw.rect(screen, BLACK, MOVE_MENU_RECT, 3)

    moves = get_player_moves(pokemon)
    
    for i, move in enumerate(moves):
        x, y = MOVE_SLOTS[i]
        screen.blit(font.render(move.upper(), True, BLACK), (x, y))

    # Draw cursor
    cx, cy = MOVE_SLOTS[menu.selected_move_index]
    pygame.draw.polygon(screen, BLACK, [
        (cx - 15, cy + 5), 
        (cx - 5, cy + 10), 
        (cx - 15, cy + 15)
    ])


# ========== GAME STATE ==========
running = True
battle_over = False
game_won = False
game_lost = False
current_turn = "player"
menu = BattleMenu()
background_music_started = False

def reset_game():
    global battle_over, game_won, game_lost, current_turn
    global menu, background_music_started
    global message_queue, current_message, typed_message, char_index
    global text_animating, last_char_time
    global pending_player_damage, pending_enemy_damage
    global player_turn_complete, enemy_turn_complete, just_took_damage
    global player_vibration, enemy_vibration
    
    # Reset Pokemon data
    charmander["current_hp"] = charmander["max_hp"]
    charmander["display_hp"] = charmander["max_hp"]
    squirtle["current_hp"] = squirtle["max_hp"]
    squirtle["display_hp"] = squirtle["max_hp"]
    
    # Reset game state
    battle_over = False
    game_won = False
    game_lost = False
    current_turn = "player"
    
    # Reset message system
    message_queue = []
    current_message = ""
    typed_message = ""
    char_index = 0
    text_animating = False
    last_char_time = 0
    
    # Reset damage tracking
    pending_player_damage = None
    pending_enemy_damage = None
    player_turn_complete = False
    enemy_turn_complete = False
    just_took_damage = {"player": False, "enemy": False}
    
    # Reset vibration
    player_vibration = VibrationEffect()
    enemy_vibration = VibrationEffect()
    
    # Reset menu
    menu = BattleMenu()
    
    # Play starting cries
    play_starting_cries()
    
    # Reset background music flag
    background_music_started = False

def start_enemy_turn():
    global message_queue, pending_enemy_damage, current_turn
    
    current_turn = "enemy"
    message_queue.append("Squirtle used Tackle!")
    play_attack_sound("Tackle")
    dmg = random.randint(4, 8)
    message_queue.append(f"It dealt {dmg} damage!")
    pending_enemy_damage = dmg
    
    if not text_animating:
        start_next_message()

def select_move(move_name):
    global message_queue, pending_player_damage, player_turn_complete, menu
    
    message_queue.append(f"Charmander used {move_name}!")
    play_attack_sound(move_name)
    
    if move_name == "Scratch":
        dmg = random.randint(5, 10)
        message_queue.append(f"It dealt {dmg} damage!")
        pending_player_damage = dmg
    else:  # Growl
        message_queue.append("But it did no damage!")
        player_turn_complete = True
        
    menu.move_menu_active = False
    menu.active = False
    
    if not text_animating:
        start_next_message()

def handle_enter_key():
    global current_turn, player_turn_complete, enemy_turn_complete
    global game_won, game_lost, battle_over
    
    if text_animating:
        return
    
    # If battle is over and ENTER is pressed, restart the game
    if battle_over:
        reset_game()
        return
    
    if message_queue:
        start_next_message()
        return
    
    if not message_queue and not text_animating:
        # Main menu selection
        if menu.active and not menu.move_menu_active:
            selected_option = menu.options[menu.cursor_pos]
            
            if selected_option == "FIGHT":
                menu.move_menu_active = True
                menu.selected_move_index = 0
                play_blip_sound()
            elif selected_option == "BAG":
                message_queue.append("You don't have any items in your bag!")
                play_blip_sound()
                start_next_message()
            elif selected_option == "POKÉMON":
                message_queue.append("You don't have any other Pokémon!")
                play_blip_sound()
                start_next_message()
            elif selected_option == "RUN":
                message_queue.append("Can't escape!")
                play_blip_sound()
                start_next_message()
            return
        
        # Move selection
        elif menu.move_menu_active:
            move = get_player_moves(charmander)[menu.selected_move_index]
            select_move(move)
            play_blip_sound()
            return
        
        # Turn transitions
        elif not menu.active and not menu.move_menu_active:
            if player_turn_complete and current_turn == "player":
                start_enemy_turn()
            elif enemy_turn_complete and current_turn == "enemy":
                current_turn = "player"
                player_turn_complete = False
                enemy_turn_complete = False
                menu.active = True
                menu.cursor_pos = 0

# ========== MAIN LOOP ==========
# Play starting cries at the beginning
play_starting_cries()

while running:
    dt = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # ESC key to quit
            if event.key == pygame.K_ESCAPE:
                running = False
            
            # Play blip sound for other key presses
            elif event.key != pygame.K_ESCAPE:
                play_blip_sound()
            
            # Start background music on first key press if not started
            if not background_music_started and theme_sound and not battle_over:
                start_background_music()
                background_music_started = True
            
            # ENTER key
            if event.key == pygame.K_RETURN:
                handle_enter_key()
            
            # ARROW keys (only work during battle)
            elif event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                if text_animating or battle_over:
                    continue
                
                # Main menu navigation
                if menu.active and not menu.move_menu_active:
                    if event.key == pygame.K_UP:
                        if menu.cursor_pos in [2, 3]:
                            menu.cursor_pos -= 2
                    elif event.key == pygame.K_DOWN:
                        if menu.cursor_pos in [0, 1]:
                            menu.cursor_pos += 2
                    elif event.key == pygame.K_LEFT:
                        if menu.cursor_pos in [1, 3]:
                            menu.cursor_pos -= 1
                    elif event.key == pygame.K_RIGHT:
                        if menu.cursor_pos in [0, 2]:
                            menu.cursor_pos += 1
                
                # Move menu navigation
                elif menu.move_menu_active:
                    if event.key == pygame.K_DOWN:
                        if menu.selected_move_index < 2:
                            menu.selected_move_index += 2
                    elif event.key == pygame.K_UP:
                        if menu.selected_move_index >= 2:
                            menu.selected_move_index -= 2
                    elif event.key == pygame.K_LEFT:
                        if menu.selected_move_index % 2 == 1:
                            menu.selected_move_index -= 1
                    elif event.key == pygame.K_RIGHT:
                        if menu.selected_move_index % 2 == 0:
                            menu.selected_move_index += 1

    # Update vibration effects
    player_vibration.update(dt)
    enemy_vibration.update(dt)
    
    # Reset damage flags after vibration ends
    if just_took_damage["player"] and not player_vibration.active:
        just_took_damage["player"] = False
    if just_took_damage["enemy"] and not enemy_vibration.active:
        just_took_damage["enemy"] = False

    # Automatic turn transitions
    if (not text_animating and not message_queue and 
        player_turn_complete and current_turn == "player" and not battle_over):
        start_enemy_turn()
    
    if (not text_animating and not message_queue and 
        enemy_turn_complete and current_turn == "enemy" and not battle_over):
        current_turn = "player"
        player_turn_complete = False
        enemy_turn_complete = False
        menu.active = True
        menu.cursor_pos = 0

    # Battle end conditions
    if charmander["current_hp"] <= 0 and not battle_over:
        battle_over = True
        game_lost = True
        menu.active = False
        menu.move_menu_active = False
        message_queue.clear()
        message_queue.append("Charmander fainted!")
        message_queue.append("You lost the battle!")
        stop_background_music()
        if not text_animating:
            start_next_message()
    
    if squirtle["current_hp"] <= 0 and not battle_over:
        battle_over = True
        game_won = True
        menu.active = False
        menu.move_menu_active = False
        message_queue.clear()
        message_queue.append("Squirtle fainted!")
        message_queue.append("You won the battle!")
        play_win_sound()
        if not text_animating:
            start_next_message()

    # Update animations
    animate_hp(charmander)
    animate_hp(squirtle)
    update_text_animation()

    # ========== DRAW EVERYTHING ==========
    if battle_over:
        # Show win/lose image after battle ends
        if game_won and win_image:
            screen.blit(win_image, (0, 0))
        elif game_lost and lose_image:
            screen.blit(lose_image, (0, 0))
        else:
            # Fallback if images not found
            if game_won:
                screen.fill(GREEN)
            elif game_lost:
                screen.fill(RED)
    else:
        # Normal battle screen
        screen.fill(WHITE)
        
        # Draw Pokemon with vibration offset
        player_offset = player_vibration.get_offset()
        enemy_offset = enemy_vibration.get_offset()
        
        screen.blit(charmander_img, (PLAYER_SPRITE_POS[0] + player_offset[0], 
                                     PLAYER_SPRITE_POS[1] + player_offset[1]))
        screen.blit(squirtle_img, (ENEMY_SPRITE_POS[0] + enemy_offset[0], 
                                   ENEMY_SPRITE_POS[1] + enemy_offset[1]))
        
        # Draw HP bars with names, levels, and HP text
        draw_hp_bar(PLAYER_HP_BAR_POS, charmander, is_player=True)
        draw_hp_bar(ENEMY_HP_BAR_POS, squirtle, is_player=False)
        
        draw_text_box()
        
        if menu.active and not battle_over:
            menu.draw()
        if menu.move_menu_active and not battle_over:
            draw_move_menu(charmander)

    pygame.display.flip()

pygame.quit()
sys.exit()