from PyQt6.QtWidgets import QLabel, QSizePolicy
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt


class ImageDisplay(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setObjectName("imageDisplay")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self._image = None

    def set_image(self, image):
        if image is None:
            self._image = None
            self.clear()
            return
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        self._image = image
        qimage = QImage(
            image.tobytes("raw", "RGBA"),
            image.width,
            image.height,
            QImage.Format.Format_RGBA8888
        )
        pixmap = QPixmap.fromImage(qimage)
        pixmap = pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio)

        self.setPixmap(pixmap)

    def get_image(self):
        return self._image

    def mousePressEvent(self, event):
        if self._image is None or self.pixmap() is None:
            return
        lbl_w = self.width()
        lbl_h = self.height()
        pix_w = self.pixmap().width()
        pix_h = self.pixmap().height()
        
        offset_x = (lbl_w - pix_w) / 2
        offset_y = (lbl_h - pix_h) / 2
        
        click_x = event.pos().x() - offset_x
        click_y = event.pos().y() - offset_y
        
        if 0 <= click_x <= pix_w and 0 <= click_y <= pix_h:
            orig_w, orig_h = self._image.size
            real_x = int(click_x * orig_w / pix_w)
            real_y = int(click_y * orig_h / pix_h)
            
            if hasattr(self, 'on_click_callback') and self.on_click_callback:
                self.on_click_callback(real_x, real_y)
