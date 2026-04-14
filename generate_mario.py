import os
import json
import urllib.request
import base64

def fetch_contributions(username, token):
    """Fetches the user's contribution graph from GitHub GraphQL API."""
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

def get_base64_image(filepath):
    """Reads a local image and converts it to a base64 data URI."""
    if os.path.exists(filepath):
        with open(filepath, "rb") as img_file:
            return "data:image/png;base64," + base64.b64encode(img_file.read()).decode('utf-8')
    return None

def generate_mario_github_svg(filename="mario_contribution.svg"):
    username = os.environ.get("GITHUB_ACTOR")
    token = os.environ.get("GITHUB_TOKEN")
    
    if not username or not token:
        print("Missing GITHUB_ACTOR or GITHUB_TOKEN environment variables.")
        return

    weeks_data = fetch_contributions(username, token)
    
    # Grid Settings
    cell_size = 10
    gap = 4
    step = cell_size + gap
    cols = len(weeks_data) if weeks_data else 53
    rows = 7
    
    width = cols * step + 16
    height = (rows + 3) * step + 16 
    
    level_map = {
        'NONE': 'empty',
        'FIRST_QUARTILE': 'lvl1',
        'SECOND_QUARTILE': 'lvl2',
        'THIRD_QUARTILE': 'lvl3',
        'FOURTH_QUARTILE': 'lvl4'
    }
    
    svg_elements = [
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">',
        '  <style>',
        '    .bg { fill: #0d1117; }',                      
        '    .empty { fill: #161b22; rx: 2; ry: 2; }',     
        '    .lvl1 { fill: #0e4429; rx: 2; ry: 2; }',      
        '    .lvl2 { fill: #006d32; rx: 2; ry: 2; }',
        '    .lvl3 { fill: #26a641; rx: 2; ry: 2; }',
        '    .lvl4 { fill: #39d353; rx: 2; ry: 2; }',      
        '    .ground { fill: #8B4513; }',                  
        '    .ground-top { fill: #5C2E0B; }',              
        '  </style>',
        f'  <rect width="100%" height="100%" class="bg" />',
        '  <g transform="translate(8, 8)">'
    ]
    
    animation_duration = 12.0  # Slightly sped up to match the energetic throwing physics
    mario_y = (rows + 1) * step 
    ground_y = mario_y + cell_size 

    # 1. Draw Ground
    svg_elements.append(f'    <!-- Game Ground -->')
    svg_elements.append(f'    <rect x="0" y="{ground_y}" width="{cols * step}" height="{cell_size * 2}" class="ground" />')
    svg_elements.append(f'    <rect x="0" y="{ground_y}" width="{cols * step}" height="2" class="ground-top" />')

    # 2. Generate Grid and Throwing Animations
    for col, week in enumerate(weeks_data):
        # Scale t_action slightly so animations finish cleanly before the loop resets
        t_action = (col / float(cols)) * 0.94 
        t_peak = t_action + 0.02  # Block shoots past the target
        t_land = t_action + 0.05  # Block drops into final place

        for row, day in enumerate(week['contributionDays']):
            lvl = level_map.get(day.get('contributionLevel', 'NONE'), 'empty')
            svg_elements.append(f'    <rect x="{col * step}" y="{row * step}" width="{cell_size}" height="{cell_size}" class="empty" />')
            
            if lvl != 'empty':
                start_y = mario_y 
                real_y = row * step 
                peak_y = real_y - 12 # Overshoot physics (flies 12px higher than it should)
                
                svg_elements.append(f'    <rect x="{col * step}" y="{start_y}" width="{cell_size}" height="{cell_size}" class="{lvl}">')
                
                # OVERSHOOT PHYSICS: Starts at bottom, shoots to peak, drops to real_y
                svg_elements.append(
                    f'      <animate attributeName="y" values="{start_y};{start_y};{peak_y};{real_y};{real_y}" '
                    f'keyTimes="0;{t_action:.3f};{t_peak:.3f};{t_land:.3f};1" dur="{animation_duration}s" '
                    f'repeatCount="indefinite" />'
                )
                
                # Opacity: Invisible until thrown
                svg_elements.append(
                    f'      <animate attributeName="opacity" values="0;0;1;1;1" '
                    f'keyTimes="0;{t_action:.3f};{t_action+0.001:.3f};{t_land:.3f};1" dur="{animation_duration}s" repeatCount="indefinite" />'
                )
                
                svg_elements.append('    </rect>')

    # 3. Embed Mario Image via Base64
    svg_elements.append('    <!-- Mario Character -->')
    mario_b64 = get_base64_image("mario.png")
    
    if mario_b64:
        # If mario.png exists, use it!
        svg_elements.append(f'    <image href="{mario_b64}" x="0" y="{mario_y - 4}" width="{cell_size + 8}" height="{cell_size + 8}">')
    else:
        # Fallback to a red square if the image is missing
        print("Warning: mario.png not found. Falling back to red square.")
        svg_elements.append(f'    <rect x="0" y="{mario_y}" width="{cell_size}" height="{cell_size}" fill="#e52521">')
    
    # Mario X-Axis Movement
    svg_elements.append(f'      <animate attributeName="x" from="-20" to="{cols * step}" dur="{animation_duration}s" repeatCount="indefinite" />')
    
    # Mario Y-Axis Running/Hopping Animation
    # This makes Mario bounce slightly as he runs across!
    svg_elements.append(f'      <animate attributeName="y" values="{mario_y - 4};{mario_y - 8};{mario_y - 4}" dur="0.25s" repeatCount="indefinite" />')
    
    if mario_b64:
        svg_elements.append('    </image>')
    else:
        svg_elements.append('    </rect>')
    
    svg_elements.append('  </g>')
    svg_elements.append('</svg>')
    
    with open(filename, "w") as f:
        f.write("\n".join(svg_elements))
    print(f"Successfully generated {filename} with Base64 image and throw physics!")

if __name__ == "__main__":
    generate_mario_github_svg()
