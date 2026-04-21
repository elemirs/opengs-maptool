import config
from PIL import Image
from PyQt6.QtWidgets import QFileDialog


def import_image(layout, text, image_display):
    Image.MAX_IMAGE_PIXELS = config.MAX_IMAGE_PIXELS
    path, _ = QFileDialog.getOpenFileName(
        layout,
        text,
        "",
        "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
    )
    if not path:
        return

    imported_image = Image.open(path).convert("RGBA")
    image_display.set_image(imported_image)

    # Automatically apply uniform density so the user doesn't have to do it manually.
    from logic.density_generator import normalize_density
    normalize_density(layout)
    
    if hasattr(layout, 'button_normalize_density'):
        layout.button_normalize_density.setEnabled(True)
        layout.button_equator_density.setEnabled(True)


def import_terrain_image(layout):
    Image.MAX_IMAGE_PIXELS = config.MAX_IMAGE_PIXELS
    path, _ = QFileDialog.getOpenFileName(
        layout,
        "Import Terrain Image",
        "",
        "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
    )
    if not path:
        return

    terrain = Image.open(path).convert("RGB")
    layout.terrain_image = terrain
    layout.terrain_image_display.set_image(terrain.convert("RGBA"))


def import_density_image(layout):
    Image.MAX_IMAGE_PIXELS = config.MAX_IMAGE_PIXELS
    path, _ = QFileDialog.getOpenFileName(
        layout,
        "Import Density Image",
        "",
        "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
    )
    if not path:
        return

    density = Image.open(path).convert("L")
    layout.density_image = density

    layout.density_image_display.set_image(density.convert("RGBA"))
    layout.check_territory_ready()
