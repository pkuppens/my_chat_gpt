"""
RGB Color Blender.

This script blends a given RGB color with white at specified percentages
and displays the blended colors in a table format with their hex values.
The original color is a shade of green (68, 170, 0) and the blending color is white (255, 255, 255).
"""

from matplotlib import patches
from matplotlib import pyplot as plt

# Original color
orig_rgb = (68, 170, 0)
white_rgb = (255, 255, 255)

# Blend percentages
percentages = [0.15, 0.25, 0.33, 0.40]


def blend_colors(c1, c2, percent):
    """
    Blend two RGB colors based on a percentage.

    :param c1: First color (RGB tuple)
    :param c2: Second color (RGB tuple)
    :param percent: Percentage to blend (0 to 1)

    :return: Blended color (RGB tuple)
    """
    return tuple(int(c1[i] + (c2[i] - c1[i]) * percent) for i in range(3))


# Generate blended colors and hex values
blended_colors = [blend_colors(orig_rgb, white_rgb, p) for p in percentages]
hex_colors = ["#%02x%02x%02x" % c for c in blended_colors]

# Create a color swatch table
fig, ax = plt.subplots(figsize=(8, 2))
ax.set_xlim(0, len(percentages))
ax.set_ylim(0, 1)
ax.axis("off")

for i, (hex_code, pct) in enumerate(zip(hex_colors, percentages, strict=False)):
    rect = patches.Rectangle((i, 0), 1, 1, linewidth=1, edgecolor="none", facecolor=hex_code)
    ax.add_patch(rect)
    ax.text(i + 0.5, 0.5, f"{int(pct * 100)}%\n{hex_code}", color="black", ha="center", va="center", fontsize=12)

plt.tight_layout()
plt.show()
