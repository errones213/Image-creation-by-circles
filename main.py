import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import pymunk
from pymunk.vec2d import Vec2d
from IPython.display import HTML
from PIL import Image

def setup_space(width, height, elasticity):
    space = pymunk.Space()
    space.gravity = 0, -9.820
    space.damping = 0.997  # Reduced speed over time
    static_body = space.static_body
    gap = 0.1
    static_lines = [
        pymunk.Segment(static_body, (gap, gap), (width - gap, gap), 0.01),
        pymunk.Segment(static_body, (width - gap, gap), (width - gap, height - gap), 0.01),
        pymunk.Segment(static_body, (gap, gap), (gap, height - gap), 0.01),
    ]
    for line in static_lines:
        line.elasticity = elasticity
        line.friction = 0
    space.add(*static_lines)
    return space

def mk_ball(x, y, vx, vy, radius, elasticity, color, space):
    body = pymunk.Body(0, 0)
    body.position = Vec2d(x, y)
    body.velocity = Vec2d(vx, vy)
    shape = pymunk.Circle(body, radius)
    shape.density = 1
    shape.elasticity = elasticity
    space.add(body, shape)
    body.radius = radius
    return body, color

def sim_multi_phase(space, balls, colors, T1, T2, T3, dt, height, image_positions):
    ts = np.arange(0, T1 + T2 + T3, dt)
    positions = []
    
    # Phase 1: Floating motion, no physics
    for t in ts[:int(T1 / dt)]:
        positions.append([np.array(b.position) for b in balls])
        for b in balls:
            random_offset = Vec2d(np.random.uniform(-0.01, 0.01), np.random.uniform(-0.01, 0.01))
            b.position += random_offset
        space.step(0)
    
    # Phase 2: Move to image positions
    columns = sorted(set(p.x for p in image_positions), reverse=True)
    for t in ts[int(T1 / dt):int((T1 + T2) / dt)]:
        positions.append([np.array(b.position) for b in balls])
        for col in columns:
            for i, (b, target_pos) in enumerate(zip(balls, image_positions)):
                if target_pos.x == col:
                    move_vector = target_pos - b.position
                    b.position += move_vector * 0.05
        space.step(0)

    # Phase 3: Activate physics
    for t in ts[int((T1 + T2) / dt):]:
        positions.append([np.array(b.position) for b in balls])
        space.step(dt)
        for b in balls:
            if b in space.bodies and len(list(b.shapes)) > 0:
                if b.position[1] > height + b.radius:
                    space.remove(b, list(b.shapes)[0])
        if len(space.bodies) == 0:
            break
    
    return ts[:len(positions)], positions

def load_and_pixelate_image(image_path, target_width):
    img = Image.open(image_path)
    aspect_ratio = img.height / img.width
    target_height = int(target_width * aspect_ratio)
    img = img.resize((target_width, target_height), Image.LANCZOS)
    img = img.convert("RGBA")
    return np.array(img), aspect_ratio

def initialize_with_image_positions(image_path):
    width, height = 9, 16
    elasticity = 0.90
    space = setup_space(width, height, elasticity)
    
    pixelated_img, aspect_ratio = load_and_pixelate_image(image_path, target_width=width * 50)
    pixelated_img = pixelated_img[::8, ::8]  # Increased pixelation

    new_height = width * aspect_ratio
    vertical_offset = (height - new_height) / 2

    balls = []
    colors = []
    image_positions = []
    medium_speed = 0.1
    for y in range(pixelated_img.shape[0]):
        for x in range(pixelated_img.shape[1]):
            r, g, b, a = pixelated_img[y, x]
            if a > 0:
                x_pos = (x / pixelated_img.shape[1]) * width
                y_pos = vertical_offset + new_height - (y / pixelated_img.shape[0]) * new_height + 0.5
                image_positions.append(Vec2d(x_pos, y_pos))
                init_x_pos = x_pos + np.random.uniform(-1, 1)
                init_y_pos = y_pos + np.random.uniform(-1, 1)
                vx = np.random.uniform(-medium_speed, medium_speed)
                vy = np.random.uniform(-medium_speed, medium_speed)
                radius = 0.1
                color = (r / 255, g / 255, b / 255)
                ball, color = mk_ball(init_x_pos, init_y_pos, vx, vy, radius, elasticity, color, space)
                balls.append(ball)
                colors.append(color)
    
    return width, height, space, balls, colors, image_positions

# Simulation parameters
T = 18
T1, T2, T3 = T / 4, T / 4, T / 2
dt = 1 / 30

# Initialize the simulation
image_path = 'Example_Image.png'
width, height, space, balls, colors, image_positions = initialize_with_image_positions(image_path)

# Run the simulation
ts, positions = sim_multi_phase(space, balls, colors, T1, T2, T3, dt, height, image_positions)

subsampling = 2
dpi = 96

# Set up the figure
fig, ax = plt.subplots(figsize=(9, 16), dpi=dpi)
ax.set(xlim=[0, width], ylim=[0, height])
ax.set_aspect("equal")

plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
fig.patch.set_facecolor((23 / 255, 23 / 255, 23 / 255))
ax.set_facecolor((23 / 255, 23 / 255, 23 / 255))
ax.set_xticks([])
ax.set_yticks([])

# Prepare the patches for balls
circles = [plt.Circle((0, 0), radius=b.radius, facecolor=color)
           for b, color in zip(balls, colors)]
[ax.add_patch(c) for c in circles]

# Animation function
def drawframe(p):
    for i, (c, color) in enumerate(zip(circles, colors)):
        c.set_center(p[i])
        c.set_facecolor(color)
    return circles

# Create animation
anim = animation.FuncAnimation(
    fig,
    drawframe,
    frames=positions[::subsampling],
    interval=dt * 1000,
    blit=True,
)

plt.close(fig)
HTML(anim.to_html5_video())

# Save the video
save = True
if save:
    FFwriter = animation.FFMpegWriter(fps=30, metadata=dict(artist='Me'), bitrate=1800)
    anim.save("video.mp4", writer=FFwriter)
    plt.close(fig)
