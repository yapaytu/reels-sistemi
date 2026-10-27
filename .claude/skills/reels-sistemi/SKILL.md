---
name: reels-sistemi
description: Bir konudan baştan sona Instagram Reels / TikTok / Shorts videosu üretir — hook ve metin, seslendirme sonrası kelime zamanlaması, kodla çizilen animasyonlu sahneler, kare kare kontrol, açıklama, ilk yorum ve yorum-DM metni. Kullanıcı "reel yap", "video yap", "şu konuda içerik çıkar" dediğinde kullan.
---

# Reels sistemi

Kamerasız, kurgu programsız, kodla çizilen dikey video. Her adımı sırayla yap; bir adım bitmeden sonrakine geçme. Çıktıların hepsi `ciktilar/<kısa-ad>/` klasörüne.

## 1. Hook ve metin

Önce konuyu netleştir: kime, hangi tek fikir, izleyici sonunda ne yapacak (yorum kelimesi).

**İlk cümle (hook) kuralları** — videonun kaderi ilk 1,5 saniye:
- İzleyicinin **şu anki durumunu veya kaybını** söyle: "X'i hâlâ böyle yapıyorsan…", "…yapmadan önce şu 4'ü kur", "Kurdun ama şu an 0/4 güçte".
- Ya da **büyük, somut bir rakam veya deney** ver: "17 günde 1,4 milyon izlenme", "Bin kişilik bir şehir kurdum".
- Rakam gerçek olsun. Uydurma rakam yorumlarda yakalanır, hesabı yakar.
- YAPMA: haber dili ("…çıktı", "…duyurdu"), videonun kendisini anlatan meta cümle ("bu videoyu yapay zekâ yaptı" — izleyiciye bir şey vermiyorsa), uzun giriş, selamlaşma.
- Daha önce tutmuş kendi hook'unu kelimesi kelimesine tekrar etme; aynı kalıba yeni ve daha büyük bir vaat koy.

**Metin kuralları:**
- 30–40 saniye (≈ 75–100 kelime). Kısa cümle; her cümle ekranda yeni bir görüntü demek.
- Yapı: hook → kanıt/merak → 3–7 somut madde veya adım → güçlü son cümle → çağrı: "Yoruma KELİME yaz, sana göndereyim."
- Rakamları okunduğu gibi yaz ("on yedi"), kısaltma ve sembol kullanma; seslendirme motoru doğru okusun. Yabancı isimleri okunuşuyla yaz.
- Metni `ciktilar/<ad>/metin.txt` olarak kaydet ve insana göster. Onay almadan devam etme.

## 2. Ses

İnsan metni kendi sesiyle ya da bir seslendirme servisiyle (ElevenLabs vb.) okur, dosyayı verir. Sonra:

```bash
python3 araclar/kirp.py ses.mp3 ciktilar/<ad>/ses-kisa.wav          # nefes boşluklarını kısalt
python3 araclar/kelimeler.py ciktilar/<ad>/ses-kisa.wav ciktilar/<ad>/kelimeler.js
```

`kelimeler.py` çıktısını metinle karşılaştır: yanlış yazılan kelimeyi `kelimeler.js` içinde düzelt (zamanlara dokunma). Konuşan bir maskot varsa: `python3 araclar/genlik.py ciktilar/<ad>/ses-kisa.wav ciktilar/<ad>/agiz.js`.

## 3. Sahneler

`araclar/sablon.html`'i `ciktilar/<ad>/reel.html` olarak kopyala. Sadece **AYAR** ve **SAHNELER** bölümünü değiştir; "dokunma" yazan bölümler sistemin kendisi. Çalışan örnek: `ornek/ornek.html` — başlamadan önce oku.

- `an("kelime", n)` kelimenin söylendiği kareyi verir. Aynı kelime metinde birden çok geçiyorsa **n'yi doğru say** (en sık hata: "bu", "her", "bir").
- Her cümle başında yeni sahne (`bas: an("İlkKelime") - 4`). Sahne içinde de her vurgulu kelimede bir şey olsun: damga (`damga()`), sayaç, büyüme (`nab`), sarsıntı (`SARSINTI`).
- Kanıt göster: gerçek ekran görüntüsü, gerçek rakam, gerçek ürün. Görselleri `ciktilar/<ad>/` içine koy ve `<img src="...">` ile kullan.
- Stil: beyaz zemin, kalın siyah çerçeveli kutular, sert gölge, tek vurgu rengi. Bir karede tek fikir.
- Güvenli alan: yazılar soldan/sağdan 90 px, üstten 200 px, alttan 420 px içeride (altyazı 1235 px'te, Instagram arayüzü altı kapatır).
- En küçük yazı 34 px. Büyük yazıyı SVG `<text>` ile değil HTML ile yaz.
- Her şey kareye bağlı: `Math.random`, `Date`, CSS animasyonu yok. Rastgelelik için `rnd(n)`.
- İlk kare dolu olsun (kaydırma burada durur): hook sahnesi 0. karede zaten görünür.

## 4. Kontrol

```bash
node araclar/kaydet.mjs ciktilar/<ad>/reel.html ciktilar/<ad>/reel.mp4 --ses ciktilar/<ad>/ses-kisa.wav
```

Bitti demeden önce **her cümleden bir kare** çıkar ve kendin bak:

```bash
ffmpeg -ss 3.2 -i ciktilar/<ad>/reel.mp4 -frames:v 1 ciktilar/<ad>/kare-3.2.png
```

Kontrol listesi: kesilen/taşan yazı, üst üste binen öğe, yanlış sahnede görünen görüntü (kelime eşleşmesi), boş kare, Türkçe karakter, altyazı ile ses uyumu, ilk kare. Hata varsa düzelt, tekrar kaydet, tekrar bak. Efekt sesi eklediysen konuşmanın en az 12 dB altında olsun.

## 5. Paylaşım

`ciktilar/<ad>/aciklama.txt` yaz:
- İlk satır = hook (açıklamada da "devamını gör"den önce görünen kısım).
- Videodaki maddelerin kısa listesi.
- Çağrı: "Takip et, yoruma KELİME yaz, linki DM'den göndereyim."
- 3–5 etiket. Para, kazanç, "sat" vaadi yazma (Instagram spam diye kaldırabiliyor).

Kapak: hook'un büyük yazısı + kanıt görseli. Profil ızgarası kapağı 3:4 kırpar; yazıyı dikeyde ortadaki 1440 px'e sığdır. `ilk-yorum.txt`: kelimeyi tekrar eden ve soru soran bir cümle.

Paylaşımı insan yapar (Instagram'ın kendi zamanlayıcısı ya da kullandığı araç). Saat belirsizse tam tarih ve gün yazıp onay al.

## 6. Yorum → DM

`ciktilar/<ad>/dm.txt`: yorum kelimesi, kısa selam ve link. Bir otomasyon aracında (ManyChat, Zernio vb.) "yorumda KELİME geçerse DM gönder" kuralı olarak kurulur; aracın kendi ayarını insanla birlikte yap. Gönderilen link çalışıyor olmalı — paylaşımdan önce aç ve kontrol et.

## Bitirince

İnsana: video yolu, kapak, açıklama, ilk yorum ve DM metni. Bir sonraki video için: hangi hook kalıbını kullandığını not et; yayından 24 saat sonra izlenme, kaydırıp geçme oranı ve izlenme süresine bakıp neyin tuttuğunu yaz.
