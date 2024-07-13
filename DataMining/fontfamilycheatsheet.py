import json
import re
import logging
import os

# Dosya yolları
current_dir = os.path.dirname(os.path.abspath(__file__))
fa_file_path = os.path.join(current_dir, 'font-awesome-icons.json')
la_file_path = os.path.join(current_dir, 'line-awesome.css')

# Logger ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Font Awesome İkonları Çekme
logging.info(f"Font Awesome ikonları {fa_file_path} dosyasından çekiliyor...")
with open(fa_file_path, 'r', encoding='utf-8') as file:
    fa_icons = json.load(file)
logging.info(f"Font Awesome ikonları başarıyla çekildi. Toplam {len(fa_icons)} ikon bulundu.")

fa_cheatsheet = []
for icon, data in fa_icons.items():
    fa_cheatsheet.append({
        "FontIconKey": 'fa fa-' + icon,
        "FontIconCode": data.get("unicode"),
        "FontFamily": "Font Awesome"
    })
logging.info(f"Font Awesome ikonları işlenip listeye eklendi. Toplam {len(fa_cheatsheet)} ikon işlendi.")

# Line Awesome İkonları Çekme
logging.info(f"Line Awesome ikonları {la_file_path} dosyasından çekiliyor...")

with open(la_file_path, 'r', encoding='utf-8') as file:
    la_css = file.read()
logging.info("Line Awesome ikonları başarıyla çekildi.")

# CSS dosyasının ilk birkaç satırını loglama
logging.debug("Line Awesome CSS dosyasının ilk birkaç satırı:")
for line in la_css.split("\n")[:10]:
    logging.debug(line)

# Line Awesome ikonları ve hexode değerlerini çekme
la_cheatsheet = []
icon_count = 0
for match in re.finditer(r'\.la-([a-z0-9-]+):before\s*{\s*content:\s*"\\(f[0-9a-f]+)";\s*}', la_css):
    icon = match.group(1)
    hexode = match.group(2)
    la_cheatsheet.append({
        "FontIconKey": f"la la-{icon}",
        "FontIconCode": hexode,
        "FontFamily": "Line Awesome"
    })
    icon_count += 1

# Hata ayıklama logları için
if icon_count == 0:
    logging.warning("Line Awesome ikonları işlenemedi. Lütfen regex desenini ve CSS dosyasının içeriğini kontrol edin.")
else:
    logging.info(f"Line Awesome ikonları işlenip listeye eklendi. Toplam {icon_count} ikon işlendi.")

# Birleştirilmiş Cheatsheet
cheatsheet = fa_cheatsheet + la_cheatsheet
logging.info(f"Toplam {len(cheatsheet)} ikon içeren birleşik cheatsheet oluşturuldu.")

# Sonuçları JSON olarak kaydetme
output_file = os.path.join(current_dir, "icon_cheatsheet.json")
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(cheatsheet, f, ensure_ascii=False, indent=4)
logging.info(f"Cheatsheet JSON dosyasına kaydedildi: {output_file}")

print(f"Cheatsheet oluşturuldu ve '{output_file}' dosyasına kaydedildi.")
