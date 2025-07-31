'''
Sundrop Caves

Name: <Your Name>
Class: <Your Class>
Date: <Date>

Description:
This program implements a text-based role-playing mining game called Sundrop Caves.
The player explores a mine, collects minerals, upgrades tools, and aims to collect 500 GP
to win. The game includes a town interface, mine map with fog of war, item upgrades,
saving/loading of game state, and additional features like a warehouse, torch, and high scores.
'''

from random import randint

game_map     = []
fog          = []
original_map = []
player       = {}

MAP_WIDTH     = 0
MAP_HEIGHT    = 0
TURNS_PER_DAY = 20
WIN_GP        = 500

minerals       = ['copper', 'silver', 'gold']
mineral_names  = {'C':'copper','S':'silver','G':'gold'}
pickaxe_price  = [50, 150]
prices         = {
    'copper': (1, 3),
    'silver': (5, 8),
    'gold':   (10,18),
}

SAVE_FILE   = 'C:/Users/doris/OneDrive/Desktop/prog/Assignment/save_file.txt'
SCORES_FILE = 'scores.txt'

def initialize_game(game_map, fog, player):
    global MAP_WIDTH, MAP_HEIGHT, original_map
    MAP_WIDTH, MAP_HEIGHT = 10, 10
    game_map.clear()
    for y in range(MAP_HEIGHT):
        row = []
        for x in range(MAP_WIDTH):
            if randint(1, 100) <= 10:
                cell = 'G'
            elif randint(1, 100) <= 20:
                cell = 'S'
            elif randint(1, 100) <= 30:
                cell = 'C'
            else:
                cell = '.'
            row.append(cell)
        game_map.append(row)
    original_map = [r.copy() for r in game_map]
    fog.clear()
    for _ in range(MAP_HEIGHT):
        fog.append(['?' for _ in range(MAP_WIDTH)])
    player.update({
        'x': 0, 'y': 0,
        'portal_x': 0, 'portal_y': 0,
        'capacity': 5,
        'pickaxe_level': 1,
        'copper': 0, 'silver': 0, 'gold': 0,
        'GP': 0, 'day': 1, 'steps': 0, 'turns': TURNS_PER_DAY,
        'torch': False,
        'warehouse': {'copper': 0, 'silver': 0, 'gold': 0},
    })
    clear_fog(fog, player)

def draw_view(game_map, fog, player):
    view_size = 2 if player['torch'] else 1
    for y in range(player['y'] - view_size, player['y'] + view_size + 1):
        row = ''
        for x in range(player['x'] - view_size, player['x'] + view_size + 1):
            if x == player['x'] and y == player['y']:
                row += '@'
            elif 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
                row += fog[y][x]
            else:
                row += ' '
        print(row)

def draw_map(game_map, fog, player):
    print("\n--- Map ---")
    for y in range(MAP_HEIGHT):
        row = ''
        for x in range(MAP_WIDTH):
            if x == player['x'] and y == player['y']:
                row += '@'
            else:
                row += fog[y][x]
        print(row)

def clear_fog(fog, player):
    radius = 2 if player['torch'] else 1
    for dy in range(-radius, radius+1):
        for dx in range(-radius, radius+1):
            nx, ny = player['x'] + dx, player['y'] + dy
            if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
                fog[ny][nx] = game_map[ny][nx]

def load_game(game_map, fog, player):
    try:
        with open(SAVE_FILE, 'r') as f:
            global MAP_WIDTH, MAP_HEIGHT, original_map
            MAP_WIDTH, MAP_HEIGHT = map(int, f.readline().split())
            game_map.clear()
            for _ in range(MAP_HEIGHT):
                game_map.append(list(f.readline().strip()))
            fog.clear()
            for _ in range(MAP_HEIGHT):
                fog.append(list(f.readline().strip()))
            fields = {}
            for line in f:
                k, v = line.strip().split(':')
                fields[k] = v
            player['name'] = fields['name']
            player['x'] = int(fields['x'])
            player['y'] = int(fields['y'])
            player['portal_x'] = int(fields['portal_x'])
            player['portal_y'] = int(fields['portal_y'])
            player['capacity'] = int(fields['capacity'])
            player['pickaxe_level'] = int(fields['pickaxe_level'])
            player['copper'] = int(fields['copper'])
            player['silver'] = int(fields['silver'])
            player['gold'] = int(fields['gold'])
            player['GP'] = int(fields['GP'])
            player['day'] = int(fields['day'])
            player['steps'] = int(fields['steps'])
            player['turns'] = int(fields['turns'])
            player['torch'] = fields['torch'] == 'True'
            player['warehouse'] = {
                'copper': int(fields['warehouse_copper']),
                'silver': int(fields['warehouse_silver']),
                'gold': int(fields['warehouse_gold'])
            }
            original_map = [r.copy() for r in game_map]
        print("Game loaded.")
        return True
    except Exception as e:
        print("Failed to load game.", e)
        return False

def show_high_scores():
    try:
        with open(SCORES_FILE, 'r') as f:
            print("\n--- High Scores ---")
            for line in f:
                print(line.strip())
    except FileNotFoundError:
        print("No high scores yet.")

def update_high_scores(player):
    score_line = f"{player['name']} - {player['GP']} GP in {player['day']} days"
    try:
        with open(SCORES_FILE, 'a') as f:
            f.write(score_line + '\n')
    except Exception as e:
        print("Failed to update high scores.", e)

# (keep all your other functions as you had them)
# show_information, save_game, replenish_nodes, shop, sell_warehouse,
# portal_return, enter_mine, show_main_menu, show_town_menu, main

if __name__ == '__main__':
    main()
