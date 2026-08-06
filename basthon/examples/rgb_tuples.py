import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# Replace these grayscale RGB tuples with four colors of your choice.
color_1 = (180, 180, 180)
color_2 = (180, 180, 180)
color_3 = (180, 180, 180)
color_4 = (180, 180, 180)

rgb_colors = [color_1, color_2, color_3, color_4]
plot_colors = [
    tuple(channel / 255 for channel in color)
    for color in rgb_colors
]

figure, axis = plt.subplots()
for x_position, color in enumerate(plot_colors):
    circle = Circle((x_position, 0), 0.4, color=color)
    axis.add_patch(circle)

axis.set_xlim(-0.6, 3.6)
axis.set_ylim(-0.6, 0.6)
axis.set_aspect("equal")
axis.axis("off")
plt.show()
