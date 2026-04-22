from PyQt6.QtWidgets import QWidget, QSizePolicy
from PyQt6.QtGui import QPainter, QImage, QPixmap
from PyQt6.QtCore import Qt, QPointF


class ImageDisplay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("imageDisplay")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMouseTracking(True)

        self._image = None
        self._pixmap = None
        
        self.scale_factor = 1.0
        self.pan_offset = QPointF(0, 0)
        
        self._is_panning = False
        self._last_mouse_pos = QPointF()
        self._dragged = False

    def set_image(self, image, reset_view=True):
        if image is None:
            self._image = None
            self._pixmap = None
            self.update()
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
        self._pixmap = QPixmap.fromImage(qimage)
        
        if reset_view or self.scale_factor == 1.0 and self.pan_offset == QPointF(0, 0):
            self._fit_to_window()
            
        self.update()

    def _fit_to_window(self):
        if self._pixmap is None:
            return
        view_rect = self.rect()
        pix_rect = self._pixmap.rect()
        
        # Avoid division by zero
        if view_rect.width() == 0 or pix_rect.width() == 0:
            return
            
        scale_x = view_rect.width() / pix_rect.width()
        scale_y = view_rect.height() / pix_rect.height()
        
        self.scale_factor = min(scale_x, scale_y)
        # Center it
        self.pan_offset.setX((view_rect.width() - pix_rect.width() * self.scale_factor) / 2)
        self.pan_offset.setY((view_rect.height() - pix_rect.height() * self.scale_factor) / 2)

    def get_image(self):
        return self._image

    def paintEvent(self, event):
        if self._pixmap is None:
            return
            
        painter = QPainter(self)
        # Smooth scaling is crucial for pixel maps to look okay when zoomed out
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        
        painter.translate(self.pan_offset)
        painter.scale(self.scale_factor, self.scale_factor)
        
        painter.drawPixmap(0, 0, self._pixmap)

    def wheelEvent(self, event):
        if self._pixmap is None:
            return
            
        zoom_in_factor = 1.15
        zoom_out_factor = 1.0 / zoom_in_factor
        
        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor
            
        old_scale = self.scale_factor
        self.scale_factor *= zoom_factor
        
        # Clamp scale between 0.05x and 50x
        self.scale_factor = max(0.05, min(self.scale_factor, 50.0))
        
        # Adjust pan_offset so we zoom into the mouse cursor
        mouse_pos = event.position()
        self.pan_offset = mouse_pos - (mouse_pos - self.pan_offset) * (self.scale_factor / old_scale)
        
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton or event.button() == Qt.MouseButton.MiddleButton:
            self._is_panning = True
            self._last_mouse_pos = event.position()
            self._dragged = False

    def mouseMoveEvent(self, event):
        if self._is_panning:
            delta = event.position() - self._last_mouse_pos
            self.pan_offset += delta
            self._last_mouse_pos = event.position()
            
            if delta.manhattanLength() > 2:
                self._dragged = True
                
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton or event.button() == Qt.MouseButton.MiddleButton:
            self._is_panning = False
            
            # If it wasn't a drag, treat it as a click
            if not self._dragged and self._image is not None and event.button() == Qt.MouseButton.LeftButton:
                click_pos = event.position()
                img_x = (click_pos.x() - self.pan_offset.x()) / self.scale_factor
                img_y = (click_pos.y() - self.pan_offset.y()) / self.scale_factor
                
                orig_w, orig_h = self._image.size
                if 0 <= img_x < orig_w and 0 <= img_y < orig_h:
                    if hasattr(self, 'on_click_callback') and self.on_click_callback:
                        self.on_click_callback(int(img_x), int(img_y))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # We only fit to window if there is no scale applied yet
        if self._pixmap is not None and self.scale_factor == 1.0 and self.pan_offset == QPointF(0, 0):
            self._fit_to_window()
            self.update()
