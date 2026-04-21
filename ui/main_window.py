import config
from PyQt6.QtCore import QTimer, Qt
from ui.i18n import t
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
        version_lbl.setProperty("i18n", "lbl_version")
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
        self.btn_prev.setProperty("i18n", "btn_prev")
        self.btn_prev.setObjectName("navButton")
        self.btn_prev.clicked.connect(self.prev_step)
        nav_bar.addWidget(self.btn_prev)
        
        nav_bar.addStretch()
        
        self.btn_lang = QPushButton("🌐 English")
        self.btn_lang.setObjectName("navButton")
        self.btn_lang.clicked.connect(self.toggle_language)
        nav_bar.addWidget(self.btn_lang)
        
        self.btn_next = QPushButton("Sonraki Adım")
        self.btn_next.setProperty("i18n", "btn_next")
        self.btn_next.setObjectName("navButtonAction")
        self.btn_next.clicked.connect(self.next_step)
        nav_bar.addWidget(self.btn_next)
        
        content_container_layout.addLayout(nav_bar)
        main_layout.addWidget(content_container, stretch=1)
        
        # --- OVERLAY MODAL ---
        self.setup_overlay()
        
        # --- STATE ---
        self.density_image = None
        self.terrain_image = None
        self.current_language = "en"
        self.workflow_mode = "standard"
        self.active_steps = [1, 2, 3, 4, 5, 6]
        
        # --- SETUP WIZARD PAGES ---
        self.setup_welcome_page()
        self.setup_land_page()
        self.setup_boundary_page()
        self.setup_density_page()
        self.setup_terrain_page()
        self.setup_territory_page()
        self.setup_province_page()
        
        self.stacked.setCurrentIndex(0)
        self.update_texts()
        self.update_ui()
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "overlay"):
            self.overlay.resize(event.size())
            
    def setup_overlay(self):
        self.overlay = QFrame(self)
        self.overlay.setStyleSheet("QFrame#overlay { background-color: rgba(0, 0, 0, 180); }")
        self.overlay.setObjectName("overlay")
        self.overlay.hide()
        
        overlay_layout = QVBoxLayout(self.overlay)
        overlay_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.modal_box = QFrame(self.overlay)
        self.modal_box.setObjectName("instructionLabel")
        self.modal_box.setFixedWidth(500)
        self.modal_box.setStyleSheet("background-color: #1a1e2f; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1); padding: 30px;")
        
        modal_layout = QVBoxLayout(self.modal_box)
        
        self.modal_title = QLabel()
        self.modal_title.setStyleSheet("font-size: 22px; font-weight: bold; color: #ff453a; margin-bottom: 10px;")
        self.modal_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.modal_desc = QLabel()
        self.modal_desc.setStyleSheet("font-size: 16px; color: #e2e8f0; margin-bottom: 25px;")
        self.modal_desc.setWordWrap(True)
        self.modal_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        btn_row = QHBoxLayout()
        self.btn_modal_stay = QPushButton()
        self.btn_modal_stay.setObjectName("navButton")
        self.btn_modal_stay.clicked.connect(lambda: self.overlay.hide())
        
        self.btn_modal_cont = QPushButton()
        self.btn_modal_cont.setObjectName("navButtonAction")
        self.btn_modal_cont.clicked.connect(self.process_next_step)
        
        btn_row.addWidget(self.btn_modal_stay)
        btn_row.addSpacing(15)
        btn_row.addWidget(self.btn_modal_cont)
        
        modal_layout.addWidget(self.modal_title)
        modal_layout.addWidget(self.modal_desc)
        modal_layout.addLayout(btn_row)
        
        overlay_layout.addWidget(self.modal_box)

    def setup_welcome_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addStretch()
        
        title = QLabel("Yeni Bir Harita Oluştur")
        title.setProperty("i18n", "title")
        title.setObjectName("pageTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        desc = QLabel("Nasıl bir harita oluşturmak istiyorsunuz?")
        desc.setProperty("i18n", "desc")
        desc.setStyleSheet("font-size: 18px; color: #cbd5e1; margin-bottom: 40px;")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc)
        
        btns = QHBoxLayout()
        btn_stand = QPushButton("🌍 Su ve Kara \n(Standart Harita)")
        btn_stand.setProperty("i18n", "btn_stand")
        btn_stand.setFixedSize(280, 180)
        btn_stand.setObjectName("bigButton")
        btn_stand.clicked.connect(lambda: self.start_workflow("standard"))
        
        btn_land = QPushButton("⛰️ Sadece Kara\n(Akıllı Boyama Sistemi)")
        btn_land.setProperty("i18n", "btn_land")
        btn_land.setFixedSize(280, 180)
        btn_land.setObjectName("bigButton")
        btn_land.clicked.connect(lambda: self.start_workflow("boundary_only"))
        
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
        inst.setProperty("i18n", "inst_land")
        inst.setObjectName("instructionLabel")
        layout.addWidget(inst)
        layout.addWidget(self.land_image_display)
        
        btn_land_up = create_button(layout, "Temel Harita Yükle", lambda: import_image(self, "Temel Harita Yükle", self.land_image_display))
        btn_land_up.setProperty("i18n", "btn_upload_land")
        self.stacked.addWidget(page)
        
    def setup_boundary_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        self.boundary_image_display = ImageDisplay()
        self.boundary_image_display.on_click_callback = self.on_boundary_click
        
        self.boundary_inst = QLabel("🎯 Adım 2: Varsa ülke veya eyalet sınırlarınızı belirten siyah çizgili (RGB: 0,0,0) görseli yükleyin.")
        self.boundary_inst.setObjectName("instructionLabel")
        layout.addWidget(self.boundary_inst)
        layout.addWidget(self.boundary_image_display)
        
        btn_bd_up = create_button(layout, "Sınır Görselini Yükle", lambda: import_image(self, "Sınır Görselini Yükle", self.boundary_image_display))
        btn_bd_up.setProperty("i18n", "btn_upload_bound")
        self.stacked.addWidget(page)
        
    def on_boundary_click(self, x, y):
        input_image = self.boundary_image_display.get_image()
        if not input_image:
            return
        
        import numpy as np
        from scipy.ndimage import label as ndlabel
        from PIL import Image
        
        arr = np.array(input_image)
        
        r, g, b = config.BOUNDARY_COLOR
        diff = np.abs(arr[..., 0].astype(int) - r) + \
               np.abs(arr[..., 1].astype(int) - g) + \
               np.abs(arr[..., 2].astype(int) - b)
        boundary_mask = diff < 200
        if arr.shape[-1] == 4:
            boundary_mask = boundary_mask & (arr[..., 3] > 64)
            
        if boundary_mask[y, x]:
            return # Hit boundary line
        
        inv_bound = ~boundary_mask
        labeled, _ = ndlabel(inv_bound)
        click_label = labeled[y, x]
        if click_label == 0:
            return
            
        ocean_mask = labeled == click_label
        
        # Color it Ocean Blue
        arr[ocean_mask, 0] = 5
        arr[ocean_mask, 1] = 20
        arr[ocean_mask, 2] = 18
        if arr.shape[-1] == 4:
            arr[ocean_mask, 3] = 255
            
        new_img = Image.fromarray(arr)
        self.boundary_image_display.set_image(new_img)
        self.check_territory_ready()
        
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
        self.button_normalize_density.setProperty("i18n", "btn_norm_dist")
        self.button_normalize_density.setEnabled(False)
        
        self.button_equator_density = create_button(row, "Ekvatoral Dağılım", lambda: equator_density(self))
        self.button_equator_density.setProperty("i18n", "btn_eq_dist")
        self.button_equator_density.setEnabled(False)
        
        btn_up_dns = create_button(layout, "Yoğunluk Görseli Yükle", lambda: import_density_image(self))
        btn_up_dns.setProperty("i18n", "btn_upload_dens")
        
        self.territory_exclude_ocean_density = create_checkbox(layout, "Bölge Üretiminde Okyanusu Yoksay")
        self.territory_exclude_ocean_density.setProperty("i18n", "check_dens_terr")
        self.province_exclude_ocean_density = create_checkbox(layout, "Vilayet Üretiminde Okyanusu Yoksay")
        self.province_exclude_ocean_density.setProperty("i18n", "check_dens_prov")
        self.stacked.addWidget(page)
        
    def setup_terrain_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        self.terrain_image_display = ImageDisplay()
        
        inst = QLabel("🎯 Adım 4 (Opsiyonel): Orman, dağ, çöl vb. arazileri özel renklerle atamak için arazi görselini yükleyin.")
        inst.setObjectName("instructionLabel")
        layout.addWidget(inst)
        layout.addWidget(self.terrain_image_display)
        
        btn_up_ter = create_button(layout, "Arazi Görselini Yükle", lambda: import_terrain_image(self))
        btn_up_ter.setProperty("i18n", "btn_upload_terr")
        self.stacked.addWidget(page)
        
    def setup_territory_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        self.territory_image_display = ImageDisplay()
        
        inst = QLabel("🎯 Adım 5: Haritadaki temel ana bölgeleri (Territory) üretin.")
        inst.setProperty("i18n", "inst_terr_gen")
        inst.setObjectName("instructionLabel")
        layout.addWidget(inst)
        layout.addWidget(self.territory_image_display)
        
        brow = QHBoxLayout()
        layout.addLayout(brow)
        
        self.territory_land_slider = create_slider(layout, "Kara Bölgesi Sayısı:", config.LAND_TERRITORIES_MIN, config.LAND_TERRITORIES_MAX, config.LAND_TERRITORIES_DEFAULT, config.LAND_TERRITORIES_TICK, config.LAND_TERRITORIES_STEP)
        self.territory_land_slider.setProperty("i18n", "lbl_land_count")
        self.territory_ocean_slider = create_slider(layout, "Okyanus Bölgesi Sayısı:", config.OCEAN_TERRITORIES_MIN, config.OCEAN_TERRITORIES_MAX, config.OCEAN_TERRITORIES_DEFAULT, config.OCEAN_TERRITORIES_TICK, config.OCEAN_TERRITORIES_STEP)
        self.territory_ocean_slider.setProperty("i18n", "lbl_ocean_count")
        
        drow = QHBoxLayout()
        col1 = QVBoxLayout()
        self.territory_density_strength = create_slider(col1, "Yoğunluk Çarpanı:", config.DENSITY_STRENGTH_MIN, config.DENSITY_STRENGTH_MAX, config.DENSITY_STRENGTH_DEFAULT, config.DENSITY_STRENGTH_TICK, config.DENSITY_STRENGTH_STEP, display_scale=0.1)
        self.territory_density_strength.setProperty("i18n", "lbl_dens_eff")
        drow.addLayout(col1, stretch=1)
        
        col2 = QVBoxLayout()
        self.territory_jagged_land = create_checkbox(col2, "Doğal Kara Sınırları (Tırtıklı)")
        self.territory_jagged_land.setProperty("i18n", "check_jag_land")
        self.territory_jagged_ocean = create_checkbox(col2, "Doğal Okyanus Sınırları (Tırtıklı)")
        self.territory_jagged_ocean.setProperty("i18n", "check_jag_ocean")
        drow.addLayout(col2)
        layout.addLayout(drow)
        
        self.button_gen_territories = create_button(layout, "Bölgeleri Oluştur", lambda: generate_territory_map(self))
        self.button_gen_territories.setProperty("i18n", "btn_gen_terr")
        self.button_gen_territories.setEnabled(False)
        self.button_gen_territories.setObjectName("navButtonAction")
        
        self.button_exp_terr_img = create_button(brow, "Haritayı Dışa Aktar", lambda: export_image(self, self.territory_image_display.get_image(), "Bölge Haritasını Dışa Aktar"))
        self.button_exp_terr_img.setProperty("i18n", "btn_exp_img")
        self.button_exp_terr_img.setEnabled(False)
        self.button_exp_terr_def = create_button(brow, "Verileri Dışa Aktar", lambda: export_territory_definitions(self))
        self.button_exp_terr_def.setProperty("i18n", "btn_exp_data")
        self.button_exp_terr_def.setEnabled(False)
        self.button_exp_terr_hist = create_button(brow, "Geçmişi Dışa Aktar", lambda: export_territory_history(self))
        self.button_exp_terr_hist.setProperty("i18n", "btn_exp_hist")
        self.button_exp_terr_hist.setEnabled(False)
        self.stacked.addWidget(page)
        
    def setup_province_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        self.province_image_display = ImageDisplay()
        
        inst = QLabel("🎯 Adım 6: Nihai adım olarak bölgeleri içerecek küçük vilayetleri (Province) üretin.")
        inst.setProperty("i18n", "inst_prov_gen")
        inst.setObjectName("instructionLabel")
        layout.addWidget(inst)
        layout.addWidget(self.province_image_display)
        
        brow = QHBoxLayout()
        layout.addLayout(brow)
        
        self.land_slider = create_slider(layout, "Kara Vilayeti Sayısı:", config.LAND_PROVINCES_MIN, config.LAND_PROVINCES_MAX, config.LAND_PROVINCES_DEFAULT, config.LAND_PROVINCES_TICK, config.LAND_PROVINCES_STEP)
        self.land_slider.setProperty("i18n", "lbl_land_prov_num")
        self.ocean_slider = create_slider(layout, "Okyanus Vilayeti Sayısı:", config.OCEAN_PROVINCES_MIN, config.OCEAN_PROVINCES_MAX, config.OCEAN_PROVINCES_DEFAULT, config.OCEAN_PROVINCES_TICK, config.OCEAN_PROVINCES_STEP)
        self.ocean_slider.setProperty("i18n", "lbl_ocean_prov_num")
        
        drow = QHBoxLayout()
        col1 = QVBoxLayout()
        self.province_density_strength = create_slider(col1, "Yoğunluk Çarpanı:", config.DENSITY_STRENGTH_MIN, config.DENSITY_STRENGTH_MAX, config.DENSITY_STRENGTH_DEFAULT, config.DENSITY_STRENGTH_TICK, config.DENSITY_STRENGTH_STEP, display_scale=0.1)
        self.province_density_strength.setProperty("i18n", "lbl_dens_eff")
        drow.addLayout(col1, stretch=1)
        
        col2 = QVBoxLayout()
        self.province_jagged_land = create_checkbox(col2, "Doğal Kara Sınırları")
        self.province_jagged_land.setProperty("i18n", "check_jag_land")
        self.province_jagged_ocean = create_checkbox(col2, "Doğal Okyanus Sınırları")
        self.province_jagged_ocean.setProperty("i18n", "check_jag_ocean")
        drow.addLayout(col2)
        layout.addLayout(drow)
        
        self.button_gen_prov = create_button(layout, "Vilayetleri Oluştur", lambda: generate_province_map(self))
        self.button_gen_prov.setProperty("i18n", "btn_gen_prov")
        self.button_gen_prov.setEnabled(False)
        self.button_gen_prov.setObjectName("navButtonAction")
        
        self.button_exp_prov_img = create_button(brow, "Haritayı Dışa Aktar", lambda: export_image(self, self.province_image_display.get_image(), "Vilayet Haritasını Dışa Aktar"))
        self.button_exp_prov_img.setProperty("i18n", "btn_exp_img")
        self.button_exp_prov_img.setEnabled(False)
        self.button_exp_prov_def = create_button(brow, "Verileri Dışa Aktar", lambda: export_province_definitions(self))
        self.button_exp_prov_def.setProperty("i18n", "btn_exp_data")
        self.button_exp_prov_def.setEnabled(False)
        self.stacked.addWidget(page)
        
    def start_workflow(self, mode):
        self.workflow_mode = mode
        if mode == "standard":
            self.active_steps = [1, 2, 3, 4, 5, 6]
            self.stacked.setCurrentIndex(1)
        else:
            self.active_steps = [2, 5, 6]
            self.stacked.setCurrentIndex(2)
        self.update_ui()
        
    def next_step(self):
        idx = self.stacked.currentIndex()
        
        if self.workflow_mode == "boundary_only" and idx == 2:
            import numpy as np
            from logic.utils import is_sea_color
            
            b_img = self.boundary_image_display.get_image()
            if b_img is not None:
                b_arr = np.array(b_img)
                if not is_sea_color(b_arr).any():
                    self.modal_title.setText(t(self.current_language, "modal_sea_warn_title"))
                    self.modal_desc.setText(t(self.current_language, "modal_sea_warn_desc"))
                    self.btn_modal_stay.setText(t(self.current_language, "modal_stay"))
                    self.btn_modal_cont.setText(t(self.current_language, "modal_cont"))
                    
                    self.overlay.show()
                    self.overlay.raise_()
                    return
                    
        self.process_next_step()
        
    def process_next_step(self):
        if hasattr(self, "overlay"):
            self.overlay.hide()
            
        idx = self.stacked.currentIndex()
        if idx in self.active_steps:
            pos = self.active_steps.index(idx)
            if pos < len(self.active_steps) - 1:
                self.stacked.setCurrentIndex(self.active_steps[pos + 1])
        self.update_ui()
        
    def prev_step(self):
        idx = self.stacked.currentIndex()
        if idx in self.active_steps:
            pos = self.active_steps.index(idx)
            if pos > 0:
                self.stacked.setCurrentIndex(self.active_steps[pos - 1])
            else:
                self.stacked.setCurrentIndex(0)
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
            
            if idx == self.active_steps[-1]:
                self.btn_next.hide()
            else:
                self.btn_next.show()
                # Text handled by update_texts
                
            # Sidebar texts
            if self.workflow_mode == "boundary_only":
                self.step_labels[1].setProperty("i18n", "lbl_step1_b")
                self.step_labels[4].setProperty("i18n", "lbl_step2_b")
                self.step_labels[5].setProperty("i18n", "lbl_step3_b")
                self.boundary_inst.setProperty("i18n", "inst_bound_b")
            else:
                self.step_labels[0].setProperty("i18n", "lbl_step1")
                self.step_labels[1].setProperty("i18n", "lbl_step2")
                self.step_labels[2].setProperty("i18n", "lbl_step3")
                self.step_labels[3].setProperty("i18n", "lbl_step4")
                self.step_labels[4].setProperty("i18n", "lbl_step5")
                self.step_labels[5].setProperty("i18n", "lbl_step6")
                self.boundary_inst.setProperty("i18n", "inst_bound")
                
            self.update_texts()
                
            for i, lbl in enumerate(self.step_labels):
                lbl.setVisible((i + 1) in self.active_steps)
            
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

    def toggle_language(self):
        self.current_language = "tr" if self.current_language == "en" else "en"
        self.btn_lang.setText("Türkçe" if self.current_language == "tr" else "English")
        self.update_texts()
        self.update_ui()
        
    def update_texts(self):
        self.setWindowTitle(t(self.current_language, "window_title"))
        from PyQt6.QtWidgets import QLabel, QPushButton, QCheckBox, QSlider
        for lbl in self.findChildren(QLabel):
            key = lbl.property("i18n")
            if key:
                import config
                if key == "lbl_version":
                    lbl.setText(f"{t(self.current_language, key)}: {config.VERSION}")
                else:
                    lbl.setText(t(self.current_language, key))
                
        for btn in self.findChildren(QPushButton):
            key = btn.property("i18n")
            if key:
                btn.setText(t(self.current_language, key))
                
        for chk in self.findChildren(QCheckBox):
            key = chk.property("i18n")
            if key:
                chk.setText(t(self.current_language, key))
                
        for sldr in self.findChildren(QSlider):
            key = sldr.property("i18n")
            if key and hasattr(sldr, "title_label"):
                sldr.title_label.setText(t(self.current_language, key))
