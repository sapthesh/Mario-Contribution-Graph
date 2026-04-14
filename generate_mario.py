import os
import json
import urllib.request

def fetch_contributions(username, token):
    query = """
    query($userName:String!) {
      user(login: $userName){
        contributionsCollection {
          contributionCalendar {
            weeks {
              contributionDays {
                contributionLevel
              }
            }
          }
        }
      }
    }
    """
    req = urllib.request.Request(
        'https://api.github.com/graphql',
        data=json.dumps({'query': query, 'variables': {'userName': username}}).encode('utf-8'),
        headers={'Authorization': f'Bearer {token}'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
    except Exception as e:
        print(f"Error fetching data from GitHub API: {e}")
        return []

def draw_sprite(name, pixels, colors, scale, is_def=True):
    svg = [f'    <g id="{name}">'] if is_def else ['    <g>']
    for y_idx, row_str in enumerate(pixels):
        for x_idx, char in enumerate(row_str):
            if char in colors:
                px = x_idx * scale
                py = y_idx * scale
                svg.append(f'      <rect x="{px:.1f}" y="{py:.1f}" width="{scale}" height="{scale}" fill="{colors[char]}" />')
    svg.append('    </g>')
    return "\n".join(svg)

def generate_mario_github_svg(filename="mario_contribution.svg"):
    username = os.environ.get("GITHUB_ACTOR", "User")
    token = os.environ.get("GITHUB_TOKEN")
    
    weeks_data = fetch_contributions(username, token) if token else []
    
    # --- LEVEL SETTINGS ---
    cell_size = 10
    gap = 4
    step = cell_size + gap
    cols = len(weeks_data) if weeks_data else 53
    rows = 7
    
    grid_x_offset = 40
    top_padding = 40
    
    flag_x = grid_x_offset + (cols * step) + 15
    castle_x = flag_x + 35
    
    width = castle_x + 80
    height = top_padding + (rows * step) + 40 
    ground_y = top_padding + (rows * step)
    
    level_map = {
        'NONE': 'empty', 'FIRST_QUARTILE': 'lvl1',
        'SECOND_QUARTILE': 'lvl2', 'THIRD_QUARTILE': 'lvl3', 'FOURTH_QUARTILE': 'lvl4'
    }
    
    # SVG Wrapper
    svg_elements = [
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">',
        '  <style>',
        '    .bg { fill: #87CEEB; }',                      
        '    .empty { fill: rgba(255,255,255,0.2); rx: 2; ry: 2; }',  
        '    .lvl1 { fill: #0e4429; rx: 2; ry: 2; stroke: #000; stroke-width: 0.5; }',      
        '    .lvl2 { fill: #006d32; rx: 2; ry: 2; stroke: #000; stroke-width: 0.5; }',
        '    .lvl3 { fill: #26a641; rx: 2; ry: 2; stroke: #000; stroke-width: 0.5; }',
        '    .lvl4 { fill: #39d353; rx: 2; ry: 2; stroke: #000; stroke-width: 0.5; }',      
        '    .ground { fill: #c84c0c; }',                  
        '    .ground-top { fill: #000000; }',              
        '  </style>',
        '  <defs>'
    ]

    # Sprite Art
    mario_pixels = [
        "  RRRRR     ", " RRRRRRRRR  ", " BBSSSO     ", " BOSSSOOOO  ",
        " BOSSSOOOO  ", "  BOOOOO    ", "  RROORR    ", " RRROORRR   ",
        " RRROORRRR  ", " SSRRRRYSS  ", " SSS  SSS   ", "BBBB  BBBB  "
    ]
    cloud_pixels = ["      WWWW      ", "   WWWWWWWWWW   ", " WWWWWWWWWWWWWW ", " WWWWWWWWWWWWWW "]
    bush_pixels = ["      GGGG      ", "   GGGGGGGGGG   ", " GGGGGGGGGGGGGG ", " GGGGGGGGGGGGGG "]
    coin_pixels = ["  YYYY  ", " YYOOYY ", " YOOOOY ", " YOOOOY ", " YYOOYY ", "  YYYY  "]
    
    mario_colors = {'R': '#e52521', 'S': '#ffcca6', 'B': '#8B4513', 'O': '#2038ec', 'Y': '#f8d820'}
    
    svg_elements.append(draw_sprite("mario", mario_pixels, mario_colors, 1.2))
    svg_elements.append(draw_sprite("cloud", cloud_pixels, {'W': '#FFFFFF'}, 2.0))
    svg_elements.append(draw_sprite("bush", bush_pixels, {'G': '#00A800'}, 2.0))
    svg_elements.append(draw_sprite("coin", coin_pixels, {'Y': '#f8d820', 'O': '#d8a000'}, 1.2))
    svg_elements.append('  </defs>')
    
    # Sky & Scenery
    svg_elements.append(f'  <rect width="100%" height="100%" class="bg" />')
    for i in range(4):
        svg_elements.append(f'  <use href="#cloud" x="0" y="{10 if i % 2 == 0 else 30}">')
        svg_elements.append(f'    <animate attributeName="x" from="{width}" to="-100" dur="{40 + (i * 5)}s" repeatCount="indefinite" />')
        svg_elements.append(f'  </use>')

    # Ground & Bushes
    svg_elements.append(f'  <rect x="0" y="{ground_y}" width="{width}" height="{height - ground_y}" class="ground" />')
    svg_elements.append(f'  <rect x="0" y="{ground_y}" width="{width}" height="2" class="ground-top" />')
    for i in range(10):
        svg_elements.append(f'  <use href="#bush" x="{i * 120 + 30}" y="{ground_y - 8}" />')

    # Start Pipe
    pipe_x, pipe_top = 10, ground_y - 30
    svg_elements.append(f'  <rect x="{pipe_x}" y="{pipe_top}" width="24" height="30" fill="#00A800" stroke="#000"/>')
    svg_elements.append(f'  <rect x="{pipe_x - 2}" y="{pipe_top}" width="28" height="10" fill="#00A800" stroke="#000"/>')

    # --- MATH & PATHFINDING ---
    mario_height = 14
    total_travel_distance = (castle_x + 25) - pipe_x # Used to calculate exactly when to collect coins
    
    path_d = f"M {pipe_x + 4} {ground_y} L {pipe_x + 4} {pipe_top - mario_height} "
    current_x, current_y = pipe_x + 4, pipe_top - mario_height
    
    empty_streak = 0
    coins_to_draw = []

    # Process Grid
    for col, week in enumerate(weeks_data):
        highest_block_row = rows 
        col_x = grid_x_offset + col * step
        is_empty_week = True
        
        for row, day in enumerate(week['contributionDays']):
            lvl = level_map.get(day.get('contributionLevel', 'NONE'), 'empty')
            block_y = top_padding + row * step
            
            svg_elements.append(f'  <rect x="{col_x}" y="{block_y}" width="{cell_size}" height="{cell_size}" class="{lvl}" />')
            
            if lvl != 'empty':
                is_empty_week = False
                if row < highest_block_row: highest_block_row = row
            
            # Level 4 Coin!
            if lvl == 'lvl4':
                coins_to_draw.append({'x': col_x, 'y': block_y - 12, 't': (col_x - pipe_x) / total_travel_distance})
        
        # Gap Logic
        if is_empty_week: empty_streak += 1
        else: empty_streak = 0
            
        target_x, target_y = col_x, (top_padding + highest_block_row * step) - mario_height
        
        # If huge gap (4 weeks), jump for a coin!
        if empty_streak == 4:
            target_y -= 25 # Jump high
            coins_to_draw.append({'x': col_x, 'y': target_y - 4, 't': (col_x - pipe_x) / total_travel_distance})
            empty_streak = 0 
            
        if target_y != current_y:
            path_d += f" Q {current_x + (target_x - current_x) / 2} {min(current_y, target_y) - 25} {target_x} {target_y}"
        else:
            path_d += f" L {target_x} {target_y}"
            
        current_x, current_y = target_x, target_y

    # End Path
    flag_top = top_padding - 10
    path_d += f" Q {current_x + 10} {current_y - 20} {flag_x - 4} {flag_top + 10} " # Jump to Flag
    path_d += f" L {flag_x - 4} {ground_y - mario_height} "                         # Slide Down
    path_d += f" L {castle_x + 15} {ground_y - mario_height} "                      # Walk into Castle

    # DRAW COINS (With collection physics!)
    for c in coins_to_draw:
        t, t_end = c['t'], min(1.0, c['t'] + 0.03) # Time to shoot up and fade
        svg_elements.append(f'  <g transform="translate({c["x"]}, {c["y"]})">')
        svg_elements.append(f'    <g>')
        # Collect Animation: Shoots up 20px and fades to 0 opacity exactly when Mario touches it
        svg_elements.append(f'      <animateTransform attributeName="transform" type="translate" values="0,0; 0,0; 0,-20; 0,-20" keyTimes="0;{t:.3f};{t_end:.3f};1" dur="20s" repeatCount="indefinite" />')
        svg_elements.append(f'      <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;{t:.3f};{t_end:.3f};1" dur="20s" repeatCount="indefinite" />')
        svg_elements.append(f'      <use href="#coin" x="0" y="0" />')
        svg_elements.append(f'    </g>')
        svg_elements.append(f'  </g>')

    # FLAGPOLE & FLAG DROP
    t_flag = min(1.0, (flag_x - pipe_x) / total_travel_distance)
    t_flag_end = min(1.0, t_flag + 0.05)
    
    svg_elements.append(f'  <rect x="{flag_x}" y="{flag_top}" width="3" height="{ground_y - flag_top}" fill="#FFF" stroke="#000" stroke-width="0.5"/>')
    svg_elements.append(f'  <circle cx="{flag_x + 1.5}" cy="{flag_top}" r="4" fill="#f8d820" stroke="#000"/>')
    
    # Animated Green Flag
    svg_elements.append(f'  <g>')
    svg_elements.append(f'    <animateTransform attributeName="transform" type="translate" values="0,0; 0,0; 0,{ground_y - flag_top - 15}; 0,{ground_y - flag_top - 15}" keyTimes="0;{t_flag:.3f};{t_flag_end:.3f};1" dur="20s" repeatCount="indefinite" />')
    svg_elements.append(f'    <polygon points="{flag_x-15},{flag_top+5} {flag_x},{flag_top+5} {flag_x},{flag_top+15}" fill="#00A800" stroke="#000"/>')
    svg_elements.append(f'  </g>')

    # ATTACH MARIO
    svg_elements.append(f'  <path id="parkour-path" d="{path_d}" fill="none" stroke="none" />')
    svg_elements.append('  <use href="#mario">')
    svg_elements.append(f'    <animateMotion dur="20s" repeatCount="indefinite"><mpath href="#parkour-path"/></animateMotion>')
    svg_elements.append('  </use>')

    # FOREGROUND CASTLE (Drawn AFTER Mario to hide him inside the door)
    castle_y = ground_y - 40
    svg_elements.append('  <!-- Castle Foreground -->')
    svg_elements.append(f'  <path d="M {castle_x} {ground_y} L {castle_x} {castle_y} L {castle_x+10} {castle_y} L {castle_x+10} {castle_y+10} L {castle_x+20} {castle_y+10} L {castle_x+20} {castle_y} L {castle_x+30} {castle_y} L {castle_x+30} {castle_y+10} L {castle_x+40} {castle_y+10} L {castle_x+40} {castle_y} L {castle_x+50} {castle_y} L {castle_x+50} {ground_y} Z" fill="#c84c0c" stroke="#000" stroke-width="1" />')
    svg_elements.append(f'  <path d="M {castle_x+15} {ground_y} L {castle_x+15} {ground_y-20} A 10 10 0 0 1 {castle_x+35} {ground_y-20} L {castle_x+35} {ground_y} Z" fill="#000" />')

    # LEVEL CLEAR TEXT (Flashes after flag goes down)
    svg_elements.append(f'  <text x="{flag_x - 70}" y="{top_padding - 10}" fill="#f8d820" font-family="monospace" font-weight="bold" font-size="16" stroke="#000" stroke-width="1" opacity="0">')
    svg_elements.append(f'    LEVEL CLEAR!')
    svg_elements.append(f'    <animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{t_flag_end:.3f};{t_flag_end+0.01:.3f};0.98;1" dur="20s" repeatCount="indefinite" />')
    svg_elements.append(f'    <animateTransform attributeName="transform" type="translate" values="0,10; 0,10; 0,0; 0,0" keyTimes="0;{t_flag_end:.3f};{t_flag_end+0.02:.3f};1" dur="20s" repeatCount="indefinite" />')
    svg_elements.append(f'  </text>')

    svg_elements.append('</svg>')
    
    with open(filename, "w") as f: f.write("\n".join(svg_elements))
    print(f"Successfully generated Interactive {filename}!")

if __name__ == "__main__": generate_mario_github_svg()
