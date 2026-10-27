"""Seslendirmedeki uzun nefes boşluklarını kısaltır; video daha hızlı akar.
Kullanım: python3 araclar/kirp.py ses.mp3 [ses-kisa.wav]   (ffmpeg gerekir)
0.18 sn'den uzun sessizlikler 0.14 sn'ye iner, kesik yerleri yumuşatılır."""
import array
import math
import subprocess
import sys

if len(sys.argv) < 2:
    sys.exit(__doc__)
cikti = sys.argv[2] if len(sys.argv) > 2 else "ses-kisa.wav"
SR = 44100
ham = subprocess.run(["ffmpeg", "-v", "error", "-i", sys.argv[1], "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True, check=True).stdout
x = array.array("h", ham)
hop = SR // 100
sessiz = []
for i in range(0, len(x), hop):
    p = x[i:i + hop]
    r = math.sqrt(sum(v * v for v in p) / max(1, len(p))) / 32768
    sessiz.append(20 * math.log10(r + 1e-9) < -38)
kes, i = [], 0
while i < len(sessiz):
    if sessiz[i]:
        j = i
        while j < len(sessiz) and sessiz[j]:
            j += 1
        s, e = i / 100, j / 100
        if e - s >= 0.18 and s > 0.05 and e < len(x) / SR - 0.05:
            kes.append((s + 0.07, e - 0.07))
        i = j
    else:
        i += 1
out, son, fade = array.array("h"), 0, int(SR * 0.006)
for s, e in kes + [(len(x) / SR, None)]:
    p = x[int(son * SR):int(s * SR)]
    n = len(p)
    for k in range(n):
        g = min(1, k / fade, (n - 1 - k) / fade) if n > 2 * fade and e is not None else 1
        out.append(int(p[k] * g))
    son = e if e is not None else son
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", cikti], input=out.tobytes(), check=True)
print(f"{len(x) / SR:.1f} sn → {len(out) / SR:.1f} sn, {len(kes)} boşluk kısaldı → {cikti}")
