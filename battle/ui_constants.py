# UI Constants

# Sprite sizes
SPRITE_WIDTH = 150
SPRITE_HEIGHT = 150

# Sprite positions (adjusted for HP text)
PLAYER_SPRITE_POS = (50, 128)  # Moved down a bit for HP text
ENEMY_SPRITE_POS = (550, 40)

# HP bar positions (adjusted for name/level above)
PLAYER_HP_BAR_POS = (80, 70)  # Moved down for name above
ENEMY_HP_BAR_POS = (520, 30)  # Moved down for name above

# HP bar size
HP_BAR_WIDTH = 150
HP_BAR_HEIGHT = 12

# Text box
TEXT_BOX_RECT = (50, 260, 700, 110)

# Main Battle Menu (RIGHT SIDE)
MAIN_MENU_X = 450  # Moved to right side
MAIN_MENU_Y = 300
MAIN_MENU_WIDTH = 300
MAIN_MENU_HEIGHT = 100
MAIN_MENU_OPTION_WIDTH = 150
MAIN_MENU_OPTION_HEIGHT = 40

# Move Menu (also on right side for consistency)
MOVE_MENU_RECT = (450, 240, 300, 100)  # Adjusted position
MOVE_SLOTS = [
    (470, 260),  # Top-left
    (600, 260),  # Top-right
    (470, 310),  # Bottom-left
    (600, 310),  # Bottom-right
]