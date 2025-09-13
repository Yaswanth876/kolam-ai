def create_svg(grid_size=5, symmetry="vertical"):
    cell = 60
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{grid_size*cell}" height="{grid_size*cell}" viewBox="0 0 {grid_size*cell} {grid_size*cell}">',
        '<rect width="100%" height="100%" fill="white"/>'
    ]

    # Draw dots
    for i in range(grid_size):
        for j in range(grid_size):
            x, y = i * cell + cell//2, j * cell + cell//2
            svg.append(f'<circle cx="{x}" cy="{y}" r="5" fill="black"/>')

    # Simple diagonal strokes
    for i in range(grid_size-1):
        for j in range(grid_size-1):
            x1, y1 = i * cell + cell//2, j * cell + cell//2
            x2, y2 = (i+1) * cell + cell//2, (j+1) * cell + cell//2
            svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="red" stroke-width="3"/>')

    svg.append("</svg>")
    return "\n".join(svg)
