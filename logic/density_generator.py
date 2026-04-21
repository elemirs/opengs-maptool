import config
import numpy as np
from PIL import Image


def normalize_density(layout):
    base_image = layout.land_image_display.get_image()
    if base_image is None:
        base_image = layout.boundary_image_display.get_image()
    if base_image is None:
        return

    w, h = base_image.size
    density = Image.new("L", (w, h), config.DEFAULT_DENSITY_GREY)
    layout.density_image = density

    layout.density_image_display.set_image(density.convert("RGBA"))
    layout.check_territory_ready()


def equator_density(layout):
    base_image = layout.land_image_display.get_image()
    if base_image is None:
        base_image = layout.boundary_image_display.get_image()
    if base_image is None:
        return

    w, h = base_image.size
    # Black (0) at equator (middle row), white (255) at top/bottom poles
    rows = np.linspace(0, 1, h)
    gradient = np.abs(rows - 0.5) * 2.0  # 0 at center, 1 at edges
    pixel_values = (gradient * 255).astype(np.uint8)
    arr = np.tile(pixel_values[:, np.newaxis], (1, w))

    density = Image.fromarray(arr, mode="L")
    layout.density_image = density
    layout.density_image_display.set_image(density.convert("RGBA"))
    layout.check_territory_ready()
