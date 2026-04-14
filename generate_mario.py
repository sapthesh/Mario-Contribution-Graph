import os

def generate_mario_github_svg(filename="mario_contribution.svg"):
    # GitHub graph dimensions: 53 columns, 7 rows
    cols, rows = 53, 7
    cell_size = 10
    gap = 4
    step = cell_size + gap
    
    width = cols * step + 16
    height = rows * step + 16
    
    svg_elements = [
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">',
        '  <style>',
        '    .bg { fill: #0d1117; }',                      # GitHub Dark Mode Background
        '    .empty { fill: #161b22; rx: 2; ry: 2; }',    # Empty contribution
        '    .lvl1 { fill: #0e4429; rx: 2; ry: 2; }',     # Light green
        '    .lvl2 { fill: #006d32; rx: 2; ry: 2; }',
        '    .lvl3 { fill: #26a641; rx: 2; ry: 2; }',
        '    .lvl4 { fill: #39d353; rx: 2; ry: 2; }',     # Dark green
        '    .mario { fill: #e52521; rx: 2; ry: 2; }',    # Mario Red
        '  </style>',
        f'  <rect width="100%" height="100%" class="bg" />',
        '  <g transform="translate(8, 8)">'
    ]
    
    # 1. Generate the Grid (Mocking contribution data)
    for col in range(cols):
        for row in range(rows):
            cls = "empty"
            # Creating a mock "level": Row 6 is ground, Row 4 has floating blocks
            if row == 6:
                cls = "lvl1"
            elif col % 8 == 4 and row == 4:
                cls = "lvl3" 
            elif col % 8 == 5 and row == 4:
                cls = "lvl4" 
            
            x = col * step
            y = row * step
            svg_elements.append(f'    <rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" class="{cls}" />')
            
    # 2. Calculate Mario's Animation Path
    mario_x = []
    mario_y = []
    
    for col in range(cols + 1):
        # Default Y position (running on the ground, row 5)
        y = 5 * step
        
        # Jump logic: if a block is coming up, move Mario's Y position up to row 3
        if col % 8 in [3, 4, 5, 6]:
            y = 3 * step 
            
        mario_x.append(str((col % cols) * step))  # % cols loops it back to start
        mario_y.append(str(y))
        
    x_anim = ";".join(mario_x)
    y_anim = ";".join(mario_y)
    
    # 3. Add Mario and his Animation
    svg_elements.append('    <!-- Mario Character -->')
    svg_elements.append(f'    <rect width="{cell_size}" height="{cell_size}" class="mario">')
    # calcMode="discrete" ensures the block "snaps" to the grid just like the snake game
    svg_elements.append(f'      <animate attributeName="x" values="{x_anim}" dur="8s" repeatCount="indefinite" calcMode="discrete" />')
    svg_elements.append(f'      <animate attributeName="y" values="{y_anim}" dur="8s" repeatCount="indefinite" calcMode="discrete" />')
    svg_elements.append('    </rect>')
    
    svg_elements.append('  </g>')
    svg_elements.append('</svg>')
    
    # Write to file
    with open(filename, "w") as f:
        f.write("\n".join(svg_elements))
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    generate_mario_github_svg()
