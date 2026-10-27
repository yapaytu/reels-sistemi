"""Seslendirmedeki her kelimenin başlangıç/bitiş zamanını çıkarır (Whisper).
Kullanım: python3 araclar/kelimeler.py ses-kisa.wav [ciktilar/kelimeler.js]
Çıktı: window.KELIMELER = [{"w": "Bu", "s": 0.12, "e": 0.30}, ...]  (saniye)
Sahne HTML'i bunu <script src> ile yükler; altyazı ve animasyonlar kelimelere oturur.
Gerekli (biri yeter): pip install mlx-whisper (Apple Silicon, hızlı) | pip install faster-whisper | pip install openai-whisper"""
import json
import sys

if len(sys.argv) < 2:
    sys.exit(__doc__)
ses = sys.argv[1]
cikti = sys.argv[2] if len(sys.argv) > 2 else "ciktilar/kelimeler.js"
kel = []
try:
    import mlx_whisper
    r = mlx_whisper.transcribe(ses, path_or_hf_repo="mlx-community/whisper-large-v3-mlx", language="tr", word_timestamps=True)
    kel = [w for s in r["segments"] for w in s["words"]]
except ImportError:
    try:
        from faster_whisper import WhisperModel
        segs, _ = WhisperModel("large-v3", compute_type="int8").transcribe(ses, language="tr", word_timestamps=True)
        kel = [{"word": w.word, "start": w.start, "end": w.end} for s in segs for w in s.words]
    except ImportError:
        import whisper
        r = whisper.load_model("medium").transcribe(ses, language="tr", word_timestamps=True)
        kel = [w for s in r["segments"] for w in s["words"]]
out = [{"w": w["word"].strip(), "s": round(w["start"], 2), "e": round(w["end"], 2)} for w in kel if w["word"].strip()]
with open(cikti, "w", encoding="utf-8") as f:
    f.write("window.KELIMELER = " + json.dumps(out, ensure_ascii=False) + ";\n")
print(f"{len(out)} kelime → {cikti}")
print(" ".join(f"{w['w']}@{w['s']}" for w in out))
print("Yanlış yazılan kelime varsa (ör. isimler) dosyada düzelt; zamanlara dokunma.")
