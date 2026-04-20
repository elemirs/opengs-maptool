import config
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QProgressBar, 
                             QStackedWidget, QLabel, QMessageBox, QFrame, QPushButton, QSizePolicy)
from logic.province_generator import generate_province_map
from logic.territory_generator import generate_territory_map
from logic.import_module import import_image, import_density_image, import_terrain_image
from logic.density_generator import normalize_density, equator_density
from logic.export_module import (export_image, export_territory_definitions,
                                 export_territory_history,
                                 export_province_definitions)
from ui.buttons import create_slider, create_button, create_checkbox
from ui.image_display import ImageDisplay

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("mainWindow")
        self.setWindowTitle(config.TITLE)
        self.setMinimumSize(1000, 700)
        
        # Start Maximized
        self.showMaximized()
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # --- SIDEBAR ---
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(280)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(20, 50, 20, 20)
        
        logo = QLabel("OpenGS\nMap Tool")
        logo.setObjectName("logo")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(logo)
        
        sidebar_layout.addSpacing(40)
        
        self.step_labels = []
        step_names = [
            "1. Temel Harita", 
            "2. Sınırlar", 
            "3. Yoğunluk (Ops.)", 
            "4. Arazi (Ops.)", 
            "5. Bölge Üretimi", 
            "6. Vilayet Üretimi"
        ]
        
        for name in step_names:
            lbl = QLabel(name)
            lbl.setObjectName("stepLabel")
            sidebar_layout.addWidget(lbl)
            self.step_labels.append(lbl)
            
        sidebar_layout.addStretch()
        
        version_lbl = QLabel(f"Sürüm: {config.VERSION}")
        version_lbl.setStyleSheet("color: rgba(255,255,255,0.4);")
        version_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(version_lbl)
        
        main_layout.addWidget(self.sidebar)
        
        # --- CONTENT AREA ---
        content_container = QFrame()
        content_container.setObjectName("contentContainer")
        content_container_layout = QVBoxLayout(content_container)
        content_container_layout.setContentsMargins(40, 40, 40, 40)
        
        self.stacked = QStackedWidget()
        content_container_layout.addWidget(self.stacked, stretch=1)
        
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        content_container_layout.addWidget(self.progress)
        content_container_layout.addSpacing(10)
        
        # Navigation Bar
        nav_bar = QHBoxLayout()
        self.btn_prev = QPushButton("Önceki Adım")
        self.btn_prev.setObjectName("navButton")
        self.btn_prev.clicked.connect(self.prev_step)
        nav_bar.addWidget(self.btn_prev)
        
        nav_bar.addStretch()
        
        self.btn_next = QPushButton("Sonraki Adım")
        self.btn_next.setObjectName("navButtonAction")
        self.btn_next.clicked.connect(self.next_step)
        nav_bar.addWidget(self.btn_next)
        
        content_container_layout.addLayout(nav_bar)
        main_layout.addWidget(content_container, stretch=1)
        
        # --- STATE ---
        self.density_image = None
        self.terrain_image = None
        
        # --- SETUP WIZARD PAGES ---
        self.setup_welcome_page()
        self.setup_land_page()
        self.setup_boundary_page()
        self.setup_density_page()
        self.setup_terrain_page()
        self.setup_territory_page()
        self.setup_province_page()
        
        self.stacked.setCurrentIndex(0)
        self.update_ui()
        
    def setup_welcome_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addStretch()
        
        title = QLabel("Yeni Bir Harita Oluştur")
        title.setObjectName("pageTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        desc = QLabel("Nasıl bir harita oluşturmak istiyorsunuz?")
        desc.setStyleSheet("font-size: 18px; color: #cbd5e1; margin-bottom: 40px;")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc)
        
        btns = QHBoxLayout()
        btn_stand = QPushButton("🌍 Su ve Kara \n(Standart Harita)")
        btn_stand.setFixedSize(280, 180)
        btn_stand.setObjectName("bigButton")
        btn_stand.clicked.connect(lambda: self.go_to_step(1))
        
        btn_land = QPushButton("⛰️ Sadece Kara \n(Denizsiz, Sınır Çizgili)")
        btn_land.setFixedSize(280, 180)
        btn_land.setObjectName("bigButton")
        btn_land.clicked.connect(lambda: self.go_to_step(2))
        
        btns.addStretch()
        btns.addWidget(btn_stand)
        btns.addSpacing(30)
        btns.addWidget(btn_land)
        btns.addStretch()
        
        layout.addLayout(btns)
        layout.addStretch()
        self.stacked.addWidget(page)
        
    def setup_land_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        self.land_image_display = ImageDisplay()
        
        inst = QLabel("🎯 Adım 1: Karaları, okyanusları ve gölleri belirten temel haritanızı yükleyin.\n(Okyanus: RGB(5,20,18), Göl: RGB(0,255,0))")
        inst.setObjectName("instructionLabel")
        layout.addWidget(inst)
        layout.addWidget(self.land_image_display)
        
        create_button(layout, "Temel Harita Yükle", lambda: import_image(self, "Temel Harita Yükle", self.land_image_display))
        self.stacked.addWidget(page)
        
    def setup_boundary_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        self.boundary_image_display = ImageDisplay()
        
        inst = QLabel("🎯 Adım 2: Varsa ülke veya eyalet sınırlarınızı belirten siyah çizgili (RGB: 0,0,0) görseli yükleyin.")
        inst.setObjectName("instructionLabel")
        layout.addWidget(inst)
        layout.addWidget(self.boundary_image_display)
        
        create_button(layout, "Sınır Görselini Yükle", lambda: import_image(self, "Sınır Görselini Yükle", self.boundary_image_display))
        self.stacked.addWidget(page)
        
    def setup_density_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        self.density_image_display = ImageDisplay()
        
        inst = QLabel("🎯 Adım 3 (Opsiyonel): Hangi alanların daha yoğun/küçük vilayetlere sahip olacağını kontrol eden yoğunluk görselini yükleyin.\nYüklemek istemiyorsanız 'Normal Dağılım' diyerek devam edebilirsiniz.")
        inst.setObjectName("instructionLabel")
        layout.addWidget(inst)
        layout.addWidget(self.density_image_display)
        
        row = QHBoxLayout()
        layout.addLayout(row)
        self.button_normalize_density = create_button(row, "Normal Dağılım", lambda: normalize_density(self))
        self.button_normalize_density.setEnabled(False)
        
        self.button_equator_density = create_button(row, "Ekvatoral Dağılım", lambda: equator_density(self))
        self.button_equator_density.setEnabled(False)
        
        create_button(layout, "Yoğunluk Görseli Yükle", lambda: import_density_image(self))
        
        self.territory_exclude_ocean_density = create_checkbox(layout, "Bölge Üretiminde Okyanusu Yoksay")
        self.province_exclude_ocean_density = create_checkbox(layout, "Vilayet Üretiminde Okyanusu Yoksay")
        self.stacked.addWidget(page)
        
    def setup_terrain_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        self.terrain_image_display = ImageDisplay()
        
        inst = QLabel("🎯 Adım 4 (Opsiyonel): Orman, dağ, çöl vb. arazileri özel renklerle atamak için arazi görselini yükleyin.")
        inst.setObjectName("instructionLabel")
        layout.addWidget(inst)
        layout.addWidget(self.terrain_image_display)
        
        create_button(layout, "Arazi Görselini Yükle", lambda: import_terrain_image(self))
        self.stacked.addWidget(page)
        
    def setup_territory_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        self.territory_image_display = ImageDisplay()
        
        inst = QLabel("🎯 Adım 5: Haritadaki temel ana bölgeleri (Territory) üretin.")
        inst.setObjectName("instructionLabel")
        layout.addWidget(inst)
        layout.addWidget(self.territory_image_display)
        
        brow = QHBoxLayout()
        layout.addLayout(brow)
        
        self.territory_land_slider = create_slider(layout, "Kara Bölgesi Sayısı:", config.LAND_TERRITORIES_MIN, config.LAND_TERRITORIES_MAX, config.LAND_TERRITORIES_DEFAULT, config.LAND_TERRITORIES_TICK, config.LAND_TERRITORIES_STEP)
        self.territory_ocean_slider = create_slider(layout, "Okyanus Bölgesi Sayısı:", config.OCEAN_TERRITORIES_MIN, config.OCEAN_TERRITORIES_MAX, config.OCEAN_TERRITORIES_DEFAULT, config.OCEAN_TERRITORIES_TICK, config.OCEAN_TERRITORIES_STEP)
        
        drow = QHBoxLayout()
        col1 = QVBoxLayout()
        self.territory_density_strength = create_slider(col1, "Yoğunluk Çarpanı:", config.DENSITY_STRENGTH_MIN, config.DENSITY_STRENGTH_MAX, config.DENSITY_STRENGTH_DEFAULT, config.DENSITY_STRENGTH_TICK, config.DENSITY_STRENGTH_STEP, display_scale=0.1)
        drow.addLayout(col1, stretch=1)
        
        col2 = QVBoxLayout()
        self.territory_jagged_land = create_checkbox(col2, "Doğal Kara Sınırları (Tırtıklı)")
        self.territory_jagged_ocean = create_checkbox(col2, "Doğal Okyanus Sınırları (Tırtıklı)")
        drow.addLayout(col2)
        layout.addLayout(drow)
        
        self.button_gen_territories = create_button(layout, "Bölgeleri Oluştur", lambda: generate_territory_map(self))
        self.button_gen_territories.setEnabled(False)
        self.button_gen_territories.setObjectName("navButtonAction")
        
        self.button_exp_terr_img = create_button(brow, "Haritayı Dışa Aktar", lambda: export_image(self, self.territory_image_display.get_image(), "Bölge Haritasını Dışa Aktar"))
        self.button_exp_terr_img.setEnabled(False)
        self.button_exp_terr_def = create_button(brow, "Verileri Dışa Aktar", lambda: export_territory_definitions(self))
        self.button_exp_terr_def.setEnabled(False)
        self.button_exp_terr_hist = create_button(brow, "Geçmişi Dışa Aktar", lambda: export_territory_history(self))
        self.button_exp_terr_hist.setEnabled(False)
        self.stacked.addWidget(page)
        
    def setup_province_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        self.province_image_display = ImageDisplay()
        
        inst = QLabel("🎯 Adım 6: Nihai adım olarak bölgeleri içerecek küçük vilayetleri (Province) üretin.")
        inst.setObjectName("instructionLabel")
        layout.addWidget(inst)
        layout.addWidget(self.province_image_display)
        
        brow = QHBoxLayout()
        layout.addLayout(brow)
        
        self.land_slider = create_slider(layout, "Kara Vilayeti Sayısı:", config.LAND_PROVINCES_MIN, config.LAND_PROVINCES_MAX, config.LAND_PROVINCES_DEFAULT, config.LAND_PROVINCES_TICK, config.LAND_PROVINCES_STEP)
        self.ocean_slider = create_slider(layout, "Okyanus Vilayeti Sayısı:", config.OCEAN_PROVINCES_MIN, config.OCEAN_PROVINCES_MAX, config.OCEAN_PROVINCES_DEFAULT, config.OCEAN_PROVINCES_TICK, config.OCEAN_PROVINCES_STEP)
        
        drow = QHBoxLayout()
        col1 = QVBoxLayout()
        self.province_density_strength = create_slider(col1, "Yoğunluk Çarpanı:", config.DENSITY_STRENGTH_MIN, config.DENSITY_STRENGTH_MAX, config.DENSITY_STRENGTH_DEFAULT, config.DENSITY_STRENGTH_TICK, config.DENSITY_STRENGTH_STEP, display_scale=0.1)
        drow.addLayout(col1, stretch=1)
        
        col2 = QVBoxLayout()
        self.province_jagged_land = create_checkbox(col2, "Doğal Kara Sınırları")
        self.province_jagged_ocean = create_checkbox(col2, "Doğal Okyanus Sınırları")
        drow.addLayout(col2)
        layout.addLayout(drow)
        
        self.button_gen_prov = create_button(layout, "Vilayetleri Oluştur", lambda: generate_province_map(self))
        self.button_gen_prov.setEnabled(False)
        self.button_gen_prov.setObjectName("navButtonAction")
        
        self.button_exp_prov_img = create_button(brow, "Haritayı Dışa Aktar", lambda: export_image(self, self.province_image_display.get_image(), "Vilayet Haritasını Dışa Aktar"))
        self.button_exp_prov_img.setEnabled(False)
        self.button_exp_prov_def = create_button(brow, "Verileri Dışa Aktar", lambda: export_province_definitions(self))
        self.button_exp_prov_def.setEnabled(False)
        self.stacked.addWidget(page)
        
    def go_to_step(self, index):
        self.stacked.setCurrentIndex(index)
        self.update_ui()
        
    def next_step(self):
        idx = self.stacked.currentIndex()
        if idx < self.stacked.count() - 1:
            self.stacked.setCurrentIndex(idx + 1)
        self.update_ui()
        
    def prev_step(self):
        idx = self.stacked.currentIndex()
        if idx > 0:
            if idx == 1 or idx == 2:
                self.stacked.setCurrentIndex(0)
            else:
                self.stacked.setCurrentIndex(idx - 1)
        self.update_ui()
        
    def update_ui(self):
        idx = self.stacked.currentIndex()
        
        if idx == 0:
            self.btn_prev.hide()
            self.btn_next.hide()
            self.sidebar.hide()
        else:
            self.btn_prev.show()
            self.sidebar.show()
            
            if idx == self.stacked.count() - 1:
                self.btn_next.hide()
            else:
                self.btn_next.show()
                self.btn_next.setText("Sonraki Adım")
            
            # highlight sidebar step
            for i, lbl in enumerate(self.step_labels):
                if i == idx - 1:
                    lbl.setStyleSheet("color: white; font-weight: bold; font-size: 17px; margin: 12px 0; border-left: 4px solid #0A84FF; padding-left: 15px;")
                else:
                    lbl.setStyleSheet("color: rgba(255,255,255,0.4); font-weight: normal; font-size: 15px; margin: 8px 0; border-left: 4px solid transparent; padding-left: 15px;")

    def check_territory_ready(self):
        land_exists = self.land_image_display.get_image() is not None
        boundary_exists = self.boundary_image_display.get_image() is not None
        density_exists = self.density_image is not None
        self.button_gen_territories.setEnabled((land_exists or boundary_exists) and density_exists)
