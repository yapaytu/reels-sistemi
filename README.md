# Reels sistemi

YapayTU hesabının videolarını üreten sistemin paylaşılabilir hâli. Claude Code'a bir konu veriyorsun; hook'u ve metni yazıyor, seslendirmeyi kelime kelime zamanlıyor, her sahneyi kodla çiziyor, videoyu kare kare kontrol ediyor, açıklamayı, ilk yorumu ve yorum-DM metnini hazırlıyor.

Kamera, kurgu programı ve görüntü üreten ücretli servis yok. Çıktı dikey 1080 × 1920 MP4 (Reels, TikTok, Shorts).

## Gerekenler

- [Claude Code](https://claude.com/claude-code)
- Node.js 18 veya üstü
- ffmpeg (macOS: `brew install ffmpeg`, Windows: `winget install ffmpeg`)
- Python 3 ve bir Whisper paketi (kelime zamanları için, biri yeter):
  - Apple Silicon Mac: `pip install mlx-whisper`
  - Diğerleri: `pip install faster-whisper`
- Seslendirme: kendi sesin ya da istediğin bir seslendirme servisi

## Kurulum

```bash
git clone https://github.com/yapaytu/reels-sistemi.git
cd reels-sistemi
npm install
npx playwright install chromium
```

## Kullanım

Klasörde `claude` yaz ve konuyu söyle:

```text
reels-sistemi skill'iyle "Claude Code'a site yaptırmadan önce kurulacak 4 eklenti" konusunda reel yap. Yorum kelimesi EKLENTİ.
```

Claude önce metni gösterir. Onaylayınca metni seslendirip ses dosyasını klasöre koyarsın, gerisini o yürütür:

1. **Hook ve metin**: ilk cümle kuralları ve 30–40 saniyelik yapı
2. **Ses**: nefes boşluklarını kısaltır, her kelimenin zamanını çıkarır
3. **Sahneler**: her cümle yeni bir görüntü, vurgulu kelimelerde damga, sayaç ve sarsıntı
4. **Kontrol**: MP4'ü kaydeder, her cümleden bir kare çıkarıp hatayı düzeltir
5. **Paylaşım**: açıklama, kapak kuralları, ilk yorum
6. **Yorum → DM**: kelime ve DM metni

Önce örneği görmek istersen `ornek/ornek.html` dosyasını tarayıcıda aç ya da MP4'e çevir:

```bash
node araclar/kaydet.mjs ornek/ornek.html ciktilar/ornek.mp4
```

## Araçlar

| Dosya | Ne yapar |
|---|---|
| `araclar/kirp.py` | Seslendirmedeki uzun nefes boşluklarını kısaltır |
| `araclar/kelimeler.py` | Whisper ile her kelimenin zamanını çıkarır |
| `araclar/genlik.py` | Konuşan maskot için kare başına ağız açıklığı |
| `araclar/sablon.html` | Sahne şablonu: kelimeye bağlı zamanlama, altyazı, damga, sarsıntı |
| `araclar/kaydet.mjs` | Sahneyi kare kare MP4'e çevirir, sesi ekler |

## Nasıl çalışıyor?

Her video, kare numarasına göre kendini çizen tek bir HTML sayfası. Kayıt aracı sayfayı görünmez bir tarayıcıda açıp her kareyi tek tek çizdiriyor ve ffmpeg ile videoya diziyor. Aynı dosya her seferinde aynı videoyu verir; beğenmediğin yeri söylersin, Claude düzeltir, yeniden kaydeder.

Animasyon stilleri için kardeş repo: [claude-studyo](https://github.com/yapaytu/claude-studyo) (kil animasyon, 3D, reklam filmi, belgesel, motion grafik, çizgi film, konuşan maskot).

## Lisans

MIT. YapayTU tarafından hazırlandı. Sponsorlu değildir.
