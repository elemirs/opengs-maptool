translations = {
    "window_title": {"en": "OpenGS - Map Generation Tool", "tr": "OpenGS - Harita Üretim Aracı"},
    "title": {"en": "Create a New Map", "tr": "Yeni Bir Harita Oluştur"},
    "desc": {"en": "What kind of map do you want to create?", "tr": "Nasıl bir harita oluşturmak istiyorsunuz?"},
    "btn_stand": {"en": "Water & Land \n(Standard Map)", "tr": "Su ve Kara \n(Standart Harita)"},
    "btn_land": {"en": "Only Land\n(Smart Paint System)", "tr": "Sadece Kara\n(Akıllı Boyama Sistemi)"},
    
    "lbl_step1": {"en": "1. Base Map", "tr": "1. Temel Harita"},
    "lbl_step2": {"en": "2. Boundaries", "tr": "2. Sınırlar"},
    "lbl_step3": {"en": "3. Density (Opt.)", "tr": "3. Yoğunluk (Ops.)"},
    "lbl_step4": {"en": "4. Terrain (Opt.)", "tr": "4. Arazi (Ops.)"},
    "lbl_step5": {"en": "5. Territory Gen.", "tr": "5. Bölge Üretimi"},
    "lbl_step6": {"en": "6. Province Gen.", "tr": "6. Vilayet Üretimi"},
    
    "lbl_step1_b": {"en": "1. Boundaries & Sea", "tr": "1. Harita ve Deniz Boyama"},
    "lbl_step2_b": {"en": "2. Territory Gen.", "tr": "2. Bölge Üretimi"},
    "lbl_step3_b": {"en": "3. Province Gen.", "tr": "3. Vilayet Üretimi"},
    
    "inst_land": {"en": "Step 1: Upload the base image that shows Country/State and Ocean colors.\n(Ocean: RGB 5,20,18, Lake: RGB 0,255,0)", "tr": "Adım 1: Karaları, okyanusları ve gölleri belirten temel haritanızı yükleyin.\n(Okyanus: RGB 5,20,18, Göl: RGB 0,255,0)"},
    "btn_upload_land": {"en": "Upload Base Map", "tr": "Temel Harita Yükle"},
    
    "inst_bound": {"en": "Step 2: Upload the black-lined (RGB: 0,0,0) boundary image.", "tr": "Adım 2: Varsa ülke veya eyalet sınırlarınızı belirten siyah çizgili (RGB: 0,0,0) görseli yükleyin."},
    "inst_bound_b": {"en": "Step 1: Upload B/W map. Left click on the SEA areas with your mouse!", "tr": "Adım 1: Siyah-beyaz haritanızı yükleyin. Ardından farenizle DENİZ olan bölgelere bir kez sol tıklayın!"},
    "btn_upload_bound": {"en": "Upload Boundary Map", "tr": "Sınır Görselini Yükle"},
    
    "inst_density": {"en": "Step 3 (Optional): Upload a grayscale density map to control where smaller provinces appear.\nOr click 'Normal Distribution'.", "tr": "Adım 3 (Opsiyonel): Hangi alanların daha yoğun/küçük vilayetlere sahip olacağını kontrol eden yoğunluk görselini yükleyin.\nYüklemek istemiyorsanız 'Normal Dağılım' diyerek devam edebilirsiniz."},
    "btn_norm_dist": {"en": "Normal Distribution", "tr": "Normal Dağılım"},
    "btn_eq_dist": {"en": "Equatorial Distribution", "tr": "Ekvatoral Dağılım"},
    "btn_upload_dens": {"en": "Upload Density Map", "tr": "Yoğunluk Görseli Yükle"},
    "check_dens_terr": {"en": "Exclude Ocean Density (Territory)", "tr": "Bölge Üretiminde Okyanusu Yoksay"},
    "check_dens_prov": {"en": "Exclude Ocean Density (Province)", "tr": "Vilayet Üretiminde Okyanusu Yoksay"},
    
    "inst_terrain": {"en": "Step 4 (Optional): Upload an RGB terrain image mapped to terrain types.", "tr": "Adım 4 (Opsiyonel): Haritanın coğrafi yapılarını (Orman, Çöl vb.) belirten RGB görsel."},
    "btn_upload_terr": {"en": "Upload Terrain Map", "tr": "Arazi Görselini Yükle"},
    
    "inst_terr_gen": {"en": "Step 5: Generate main territories.", "tr": "Adım 5: Haritadaki temel ana bölgeleri (Territory) üretin."},
    "lbl_dens_eff": {"en": "Density Effect:", "tr": "Yoğunluk Etkisi:"},
    "check_jag_land": {"en": "Jagged Land Borders", "tr": "Kara Bölgelerini Pürüzlü Yap"},
    "check_jag_ocean": {"en": "Jagged Ocean Borders", "tr": "Okyanus Bölgelerini Pürüzlü Yap"},
    "lbl_land_count": {"en": "Land Territory Count:", "tr": "Kara Bölgesi Sayısı:"},
    "lbl_ocean_count": {"en": "Ocean Territory Count:", "tr": "Okyanus Bölgesi Sayısı:"},
    
    "btn_gen_terr": {"en": "Generate Territories", "tr": "Bölgeleri Oluştur"},
    "btn_exp_img": {"en": "Export Map", "tr": "Haritayı Dışa Aktar"},
    "btn_exp_data": {"en": "Export Data", "tr": "Verileri Dışa Aktar"},
    "btn_exp_hist": {"en": "Export History", "tr": "Geçmişi Dışa Aktar"},
    
    "inst_prov_gen": {"en": "Step 6: Subdivide territories into smaller provinces.", "tr": "Adım 6: Temel bölgelerin her birini daha küçük vilayetlere (Province) alt parçalara bölün."},
    "lbl_land_prov_num": {"en": "Land Province Count:", "tr": "Kara Vilayeti Sayısı:"},
    "lbl_ocean_prov_num": {"en": "Ocean Province Count:", "tr": "Okyanus Vilayeti Sayısı:"},
    "btn_gen_prov": {"en": "Generate Provinces", "tr": "Vilayetleri Oluştur"},
    
    "btn_prev": {"en": "Previous Step", "tr": "Önceki Adım"},
    "btn_next": {"en": "Next Step", "tr": "Sonraki Adım"},
    "btn_finish": {"en": "Finish", "tr": "Tamamla"},
    
    "modal_sea_warn_title": {"en": "No Sea Detected", "tr": "Deniz Alanı Tespit Edilmedi"},
    "modal_sea_warn_desc": {"en": "You haven't marked any sea/ocean on the map. All areas will be treated as land. Are you sure you want to continue?", "tr": "Haritada hiç deniz/okyanus işaretlemediniz. Tüm alanlar kara kabul edilecek. Devam etmek istediğinize emin misiniz?"},
    "modal_stay": {"en": "Stay Here", "tr": "Burada Kal"},
    "modal_cont": {"en": "Continue", "tr": "Devam Et"}
}

def t(lang, key):
    return translations.get(key, {}).get(lang, key)
