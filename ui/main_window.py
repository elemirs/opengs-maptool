import config
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QProgressBar, QTabWidget, QLabel
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

        # MAIN LAYOUT
        self.setObjectName("mainWindow")
        self.setWindowTitle(config.TITLE)
        self.setMinimumSize(800, 600)
        self.resize(config.WINDOW_SIZE_WIDTH,
                    config.WINDOW_SIZE_HEIGHT)
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs, stretch=1)

        self.progress = QProgressBar()
        self.progress.setVisible(False)
        main_layout.addWidget(self.progress)
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setValue(0)

        self.label_version = QLabel("Sürüm: "+config.VERSION)
        main_layout.addWidget(self.label_version)

        # TAB1 LAND IMAGE
        self.land_tab = QWidget()
        self.land_image_display = ImageDisplay()
        land_tab_layout = QVBoxLayout(self.land_tab)
        
        land_instruction = QLabel("🎯 Adım 1: Karaları, okyanusları ve gölleri belirten temel haritanızı yükleyin.\n(Okyanus: RGB(5,20,18), Göl: RGB(0,255,0))")
        land_instruction.setStyleSheet("color: #cbd5e1; font-weight: bold; margin-bottom: 5px;")
        land_tab_layout.addWidget(land_instruction)
        
        land_tab_layout.addWidget(self.land_image_display)
        self.tabs.addTab(self.land_tab, "1. Temel Harita")

        # Buttons
        create_button(land_tab_layout,
                      "Temel Harita Yükle",
                      lambda: import_image(self,
                                           "Temel Harita Yükle",
                                           self.land_image_display))

        # State
        self.density_image = None

        # TAB2 BOUNDARY IMAGE
        self.boundary_tab = QWidget()
        self.boundary_image_display = ImageDisplay()
        boundary_tab_layout = QVBoxLayout(self.boundary_tab)

        boundary_instruction = QLabel("🎯 Adım 2: Varsa ülke veya eyalet sınırlarınızı belirten siyah çizgili (RGB: 0,0,0) görseli yükleyin.")
        boundary_instruction.setStyleSheet("color: #cbd5e1; font-weight: bold; margin-bottom: 5px;")
        boundary_tab_layout.addWidget(boundary_instruction)

        boundary_tab_layout.addWidget(self.boundary_image_display)
        self.tabs.addTab(self.boundary_tab, "2. Sınırlar")

        # Buttons
        create_button(boundary_tab_layout,
                      "Sınır Görselini Yükle",
                      lambda: import_image(self,
                                           "Sınır Görselini Yükle",
                                           self.boundary_image_display))

        # TAB3 DENSITY IMAGE
        self.density_tab = QWidget()
        self.density_image_display = ImageDisplay()
        density_tab_layout = QVBoxLayout(self.density_tab)

        density_instruction = QLabel("🎯 Adım 3 (Opsiyonel): Hangi alanların daha yoğun/küçük vilayetlere sahip olacağını kontrol eden yoğunluk görselini yükleyin.")
        density_instruction.setStyleSheet("color: #cbd5e1; font-weight: bold; margin-bottom: 5px;")
        density_tab_layout.addWidget(density_instruction)

        density_tab_layout.addWidget(self.density_image_display)
        self.tabs.addTab(self.density_tab, "3. Yoğunluk")

        # Buttons
        density_preset_row = QHBoxLayout()
        density_tab_layout.addLayout(density_preset_row)

        self.button_normalize_density = create_button(
            density_preset_row,
            "Normal Dağılım",
            lambda: normalize_density(self))
        self.button_normalize_density.setEnabled(False)

        self.button_equator_density = create_button(
            density_preset_row,
            "Ekvatoral Dağılım",
            lambda: equator_density(self))
        self.button_equator_density.setEnabled(False)

        create_button(density_tab_layout,
                      "Yoğunluk Görseli Yükle",
                      lambda: import_density_image(self))

        self.territory_exclude_ocean_density = create_checkbox(
            density_tab_layout, "Bölge Üretiminde Okyanusu Yoksay")

        self.province_exclude_ocean_density = create_checkbox(
            density_tab_layout, "Vilayet Üretiminde Okyanusu Yoksay")

        # TAB4 TERRAIN IMAGE
        self.terrain_tab = QWidget()
        self.terrain_image_display = ImageDisplay()
        terrain_tab_layout = QVBoxLayout(self.terrain_tab)

        terrain_instruction = QLabel("🎯 Adım 4 (Opsiyonel): Orman, dağ, çöl vb. arazileri özel renklerle atamak için arazi görselini yükleyin.")
        terrain_instruction.setStyleSheet("color: #cbd5e1; font-weight: bold; margin-bottom: 5px;")
        terrain_tab_layout.addWidget(terrain_instruction)

        terrain_tab_layout.addWidget(self.terrain_image_display)
        self.tabs.addTab(self.terrain_tab, "4. Arazi")

        create_button(terrain_tab_layout,
                      "Arazi Görselini Yükle",
                      lambda: import_terrain_image(self))

        # State
        self.terrain_image = None

        # TAB5 TERRITORY IMAGE
        self.territory_tab = QWidget()
        self.territory_image_display = ImageDisplay()
        territory_tab_layout = QVBoxLayout(self.territory_tab)

        territory_instruction = QLabel("🎯 Adım 5: Haritadaki temel ana bölgeleri (Territory) üretin.")
        territory_instruction.setStyleSheet("color: #cbd5e1; font-weight: bold; margin-bottom: 5px;")
        territory_tab_layout.addWidget(territory_instruction)

        territory_tab_layout.addWidget(self.territory_image_display)
        self.tabs.addTab(self.territory_tab, "5. Bölge Üretimi")

        button_territory_row = QHBoxLayout()
        territory_tab_layout.addLayout(button_territory_row)

        # Buttons
        self.territory_land_slider = create_slider(territory_tab_layout,
                                                   "Kara Bölgesi Sayısı:",
                                                   config.LAND_TERRITORIES_MIN,
                                                   config.LAND_TERRITORIES_MAX,
                                                   config.LAND_TERRITORIES_DEFAULT,
                                                   config.LAND_TERRITORIES_TICK,
                                                   config.LAND_TERRITORIES_STEP)

        self.territory_ocean_slider = create_slider(territory_tab_layout,
                                                    "Okyanus Bölgesi Sayısı:",
                                                    config.OCEAN_TERRITORIES_MIN,
                                                    config.OCEAN_TERRITORIES_MAX,
                                                    config.OCEAN_TERRITORIES_DEFAULT,
                                                    config.OCEAN_TERRITORIES_TICK,
                                                    config.OCEAN_TERRITORIES_STEP)

        territory_density_row = QHBoxLayout()
        territory_tab_layout.addLayout(territory_density_row)

        density_slider_col = QVBoxLayout()
        territory_density_row.addLayout(density_slider_col, stretch=1)

        self.territory_density_strength = create_slider(
            density_slider_col,
            "Yoğunluk Çarpanı:",
            config.DENSITY_STRENGTH_MIN,
            config.DENSITY_STRENGTH_MAX,
            config.DENSITY_STRENGTH_DEFAULT,
            config.DENSITY_STRENGTH_TICK,
            config.DENSITY_STRENGTH_STEP,
            display_scale=0.1)

        jagged_col = QVBoxLayout()
        territory_density_row.addLayout(jagged_col)

        self.territory_jagged_land = create_checkbox(
            jagged_col, "Doğal Kara Sınırları (Tırtıklı)")
        self.territory_jagged_ocean = create_checkbox(
            jagged_col, "Doğal Okyanus Sınırları (Tırtıklı)")

        self.button_gen_territories = create_button(territory_tab_layout,
                                                    "Bölgeleri Oluştur",
                                                    lambda: generate_territory_map(self))
        self.button_gen_territories.setEnabled(False)

        self.button_exp_terr_img = create_button(button_territory_row,
                                                 "Bölge Haritasını Dışa Aktar",
                                                 lambda: export_image(self,
                                                                      self.territory_image_display.get_image(),
                                                                      "Bölge Haritasını Dışa Aktar"))
        self.button_exp_terr_img.setEnabled(False)

        self.button_exp_terr_def = create_button(button_territory_row,
                                                 "Bölge Verilerini Dışa Aktar",
                                                 lambda: export_territory_definitions(self))
        self.button_exp_terr_def.setEnabled(False)

        self.button_exp_terr_hist = create_button(button_territory_row,
                                                  "Bölge Geçmişini Dışa Aktar",
                                                  lambda: export_territory_history(self))
        self.button_exp_terr_hist.setEnabled(False)

        # TAB5 PROVINCE IMAGE
        self.province_tab = QWidget()
        self.province_image_display = ImageDisplay()
        province_tab_layout = QVBoxLayout(self.province_tab)

        province_instruction = QLabel("🎯 Adım 6: Nihai adım olarak bölgeleri içerecek küçük vilayetleri (Province) üretin.")
        province_instruction.setStyleSheet("color: #cbd5e1; font-weight: bold; margin-bottom: 5px;")
        province_tab_layout.addWidget(province_instruction)

        province_tab_layout.addWidget(self.province_image_display)
        self.tabs.addTab(self.province_tab, "6. Vilayet Üretimi")
        button_row = QHBoxLayout()
        province_tab_layout.addLayout(button_row)

        # Buttons
        self.land_slider = create_slider(province_tab_layout,
                                         "Kara Vilayeti Sayısı:",
                                         config.LAND_PROVINCES_MIN,
                                         config.LAND_PROVINCES_MAX,
                                         config.LAND_PROVINCES_DEFAULT,
                                         config.LAND_PROVINCES_TICK,
                                         config.LAND_PROVINCES_STEP)

        self.ocean_slider = create_slider(province_tab_layout,
                                          "Okyanus Vilayeti Sayısı:",
                                          config.OCEAN_PROVINCES_MIN,
                                          config.OCEAN_PROVINCES_MAX,
                                          config.OCEAN_PROVINCES_DEFAULT,
                                          config.OCEAN_PROVINCES_TICK,
                                          config.OCEAN_PROVINCES_STEP)

        province_density_row = QHBoxLayout()
        province_tab_layout.addLayout(province_density_row)

        prov_density_slider_col = QVBoxLayout()
        province_density_row.addLayout(prov_density_slider_col, stretch=1)

        self.province_density_strength = create_slider(
            prov_density_slider_col,
            "Yoğunluk Çarpanı:",
            config.DENSITY_STRENGTH_MIN,
            config.DENSITY_STRENGTH_MAX,
            config.DENSITY_STRENGTH_DEFAULT,
            config.DENSITY_STRENGTH_TICK,
            config.DENSITY_STRENGTH_STEP,
            display_scale=0.1)

        prov_jagged_col = QVBoxLayout()
        province_density_row.addLayout(prov_jagged_col)

        self.province_jagged_land = create_checkbox(
            prov_jagged_col, "Doğal Kara Sınırları (Tırtıklı)")
        self.province_jagged_ocean = create_checkbox(
            prov_jagged_col, "Doğal Okyanus Sınırları (Tırtıklı)")

        self.button_gen_prov = create_button(province_tab_layout,
                                             "Vilayetleri Oluştur",
                                             lambda: generate_province_map(self))
        self.button_gen_prov.setEnabled(False)

        self.button_exp_prov_img = create_button(button_row,
                                                 "Vilayet Haritasını Dışa Aktar",
                                                 lambda: export_image(self,
                                                                      self.province_image_display.get_image(),
                                                                      "Vilayet Haritasını Dışa Aktar"))
        self.button_exp_prov_img.setEnabled(False)

        self.button_exp_prov_def = create_button(button_row,
                                                  "Vilayet Verilerini Dışa Aktar",
                                                  lambda: export_province_definitions(self))
        self.button_exp_prov_def.setEnabled(False)

    def check_territory_ready(self):
        land_exists = self.land_image_display.get_image() is not None
        density_exists = self.density_image is not None
        self.button_gen_territories.setEnabled(land_exists and density_exists)

