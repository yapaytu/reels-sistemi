"""Bir ses dosyasından kare başına ağız açıklığı (0-1) çıkarır; konuşan maskotun ağzı bununla oynar.
Kullanım: python3 araclar/genlik.py ses.mp3 [ornekler/ses.js]   (ffmpeg gerekir)
Çıktı: window.AGIZ = [0.0, 0.42, ...]  (30 fps, sahne HTML'ine <script src> ile eklenir)"""
import array
import math
import subprocess
import sys

if len(sys.argv) < 2:
    sys.exit(__doc__)
cikti = sys.argv[2] if len(sys.argv) > 2 else "ses.js"
ham = subprocess.run(["ffmpeg", "-v", "error", "-i", sys.argv[1], "-ac", "1", "-ar", "24000", "-f", "s16le", "-"], capture_output=True, check=True).stdout
x = array.array("h", ham)
adim = 24000 // 30
rms = [math.sqrt(sum(v * v for v in x[i:i + adim]) / max(1, len(x[i:i + adim]))) / 32768 for i in range(0, len(x), adim)]
tepe = sorted(rms)[int(len(rms) * 0.95)] or 1
agiz = [round(min(1, max(0, (r / tepe - 0.08) * 1.1)), 2) for r in rms]
with open(cikti, "w", encoding="utf-8") as f:
    f.write("window.AGIZ = " + str(agiz) + ";\nwindow.SES_SURE = " + str(round(len(agiz) / 30, 2)) + ";\n")
print(f"{len(agiz)} kare ({len(agiz) / 30:.1f} sn) → {cikti}")
