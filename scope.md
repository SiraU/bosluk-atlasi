# KADİM KÜTÜPHANE × OPENAIRE — BOŞLUK ATLASI
## Proje Scope / Geliştirici Brifi (Claude'a aktarmak için)

**Tarih:** 2 Ağustos 2026 · **Teslim:** 19 Ağustos 2026 (hackathon kapanışı 20 Ağustos 23:59 CEST)

> **GÜNCELLEME — 3 Ağustos 2026 (OpenAIRE'den gelen resmî e-postalar):**
> - Kayıt **onaylandı** (Androniki Pavlidou, OpenAIRE). Kayıt e-postası: `info@sirauysal.com`
> - **Alien Intelligence daveti geldi** — MCP erişiminin önündeki engel kalktı. **Davet 17 Ağustos'ta doluyor**, hesap açılışı kullanıcı tarafından yapılmalı (davet e-postasındaki "Accept Invitation").
> - **Teslim yöntemi:** resmî şablon indirilip doldurulacak, **innovation@openaire.eu** adresine e-posta ile gönderilecek. Şablon: hackathon sayfası + Forum (`https://openaire.flarum.cloud/d/90-useful-material-for-ai-hackathon/7`)
> - **Doğrulanmış takvim:** 20 Ağu 23:59 CEST teslim · 21-29 Ağu topluluk oylaması · 20 Ağu-5 Eyl değerlendirme · **16 Eylül ödül açıklaması**
> - **Ödüller:** Büyük ödül 500 € + pilot ortaklık + OSFAIR 2027 sunumu; tema birincisi (4 adet) 12 ay Alien kredisi + vaka çalışması yayını + konuşma; ~12 finalist 3 ay kredi; topluluk seçimi 6 ay kredi + öne çıkarma yazısı
> - **Rakip alanı:** ikinci e-postadaki CC listesinde ~33 başvuran görünüyor (üniversiteler, araştırma merkezleri, bireysel geliştiriciler).
> - Forum/dokümantasyon: `https://openaire.flarum.cloud/t/ai-hackathon` (Graph community call videoları, kılavuz, Google Drive)

---

## 1. Bağlam

Kadim Kütüphane (kadimkutuphane.com), batı ezoterik geleneğinin 844+ birincil kaynağını kamu malı dijital nüshalardan (Gallica, Bodleian, Wellcome, Internet Archive…) Türkçeye çeviren, CC BY-SA 4.0 lisanslı açık erişim arşivi. Çeviriler Zenodo'ya DOI'li kayıtlar olarak yükleniyor (şu an 7 kayıt canlıda, devamı gelecek). Altyapı çok dilli; ilk hedef dil Türkçe.

**OpenAIRE AI Hackathon**'a kayıt yapıldı (Tema B — Build). Eser + 1-2 sayfalık İngilizce hikâye teslim edilecek; materyaller CC-BY olmalı.

## 2. Proje: Boşluk Atlası (Translation-Gap Atlas)

**Tek cümle:** OpenAIRE Graph'teki bilimsel literatür yoğunluğunu, birincil kaynakların dillere göre erişilebilirliğiyle çaprazlayarak "hangi eser, hangi dilde, ne kadar acil çevrilmeli" sorusunu cevaplayan ölçüm aracı + statik web vitrini.

**Skor mantığı (eser × dil):**
```
boşluk_skoru(eser, dil) = graf_yoğunluğu(eser) × (1 - dilde_erişilebilirlik(eser, dil))

graf_yoğunluğu: OpenAIRE Graph'te eserle ilgili yayın sayısı (+ MCP erişimi gelince atıf etkisi ağırlığı)
erişilebilirlik: hedef dilde kamu malı/çeviri nüsha var mı (şimdilik: Kadim Kütüphane kataloğu + manuel doğrulama; ikili 0/1 yeterli)
```

**Çıktılar:**
1. **Koleksiyon matrisi:** 17 koleksiyon × graf yoğunluğu × literatür dil dağılımı (ısı haritası)
2. **"Sıradaki Çeviriler" listesi:** boşluk skoruna göre ilk 20-50 eser — kütüphanenin çeviri önceliği artık veriye dayalı
3. **Çok dilli genelletme:** aynı skor herhangi bir hedef dil için koşulabilir (Macarca, Portekizce…) — 2-3 pilot dil gösterimi
4. **Döngü kanıtı:** Zenodo'daki çeviri kayıtları OpenAIRE Graph'e düştüğünde ekran görüntüsü/kayıt — "kütüphane grafı okumakla kalmaz, grafa yazar"

## 3. Veri kaynakları

| Kaynak | Durum | Not |
|---|---|---|
| `kaynak_katalog.csv` | ✅ hazır | 844 metin: slug, başlık, koleksiyon (ara-index.json'dan çıkarıldı) |
| OpenAIRE genel API | ✅ çalışıyor | `https://api.openaire.eu/search/publications?format=json&keywords=...` — `lang` parametresi YOK; dil dağılımı kayıt kayıt çekilip `language` alanından sayılır (bkz. `graf_olcum.py`) |
| Zenodo API | ✅ | Kadim Kütüphane kayıtları: `q="kadim kütüphane"` |
| Alien MCP (OpenAIRE Graph) | 🔑 **davet geldi (3 Ağu), hesap açılmayı bekliyor — son gün 17 Ağu** | açılınca: atıf etkisi, kronoloji, fon izleriyle derinleştirme |

**Ölçülmüş zemin (1 Ağu 2026, tekrar üretilebilir — `graf_olcum.py`):**
alchemy 9.266 yayın (%0,10 TR), gnosticism 2.402 (0 TR), western esotericism 920 (%0,65 TR), hermeticism 555, knights templar 368 (%2,72), hermetica 351 (0 TR), corpus hermeticum 311, cornelius agrippa 220 (0 TR), picatrix 140 (0 TR). Kayıtların ~%45'i dil-belirsiz; boşluk yapısal, İngilizce her kümede baskın.

## 4. Teknik kısıtlar

- **Statik site, mevcut altyapıya drop-in:** kadimkutuphane.com statik HTML/JS; build sistemi yok. Atlas tek sayfa (`/bosluk-atlasi` veya benzeri) + bir JSON veri dosyası olarak entegre edilecek. Site estetiğiyle (koyu tema, mevcut tipografi) uyumlu.
- **Veri hazırlama offline:** Python betikleri grafı sorgulayıp `atlas-veri.json` üretir; site bu dosyayı okur. Canlı API bağımlılığı yok (değerlendirici açtığında çalışması garanti).
- **Tekrar üretilebilirlik:** değerlendirme kriteri — betikler + metodoloji notu açık, lisans CC-BY.
- **Rate limit:** OpenAIRE API'ye nazik davran (istek arası ~0,4 sn; mevcut betikte örnek var).

## 5. Hikâye (submission story) omurgası

Soru → Yolculuk → İçgörü → Yeniden kullanılabilirlik. Çekirdek cümle: **"We don't just read the graph — we close the loop."** Graf boşluğu ölçer → kütüphane çevirir → çeviri DOI alıp grafa girer → graf yeniden ölçer. Türkçe bulgusu ("alan canlı ama Türkçe bilimsel çıktı ~sıfır") kanıt; çok dilli genelletme "reusability". Taslak: `basvuru-taslagi.md` §5.

## 6. İş paketleri ve sıra

1. **Atlas betiği (tam koşu):** 844 eser → kanonik eser/yazar anahtarı çıkarımı → OpenAIRE sorgusu → skor tablosu. Koleksiyon seviyesi tam, eser seviyesi önce top-100 aday.
2. **Vitrin sayfası:** ısı haritası + sıralı liste + eser kartı (tıklanınca graf özeti). Türkçe arayüz, İngilizce özet bölümü (değerlendiriciler için).
3. **Zenodo hijyeni:** mevcut 7 kaydın türü "Other" → uygun metin türüne çek; tüm kayıtlara tutarlı etiket ("Kadim Kütüphane", özgün eser adı). Yeni yüklemelerde aynı şema.
4. **MCP gelince:** atıf etkisi + kronoloji ile skoru derinleştir; hikâyedeki sayıları güncelle.
5. **Son hafta (10-18 Ağu):** vitrin canlıya, hikâye final, 19 Ağu teslim. 21-29 Ağu topluluk oylaması için kısa tanıtım metni.

## 7. Çalışma klasörü

`/Users/asumanuysal/Documents/kimi/workspace/openaire-hackathon/`
- `basvuru-taslagi.md` — başvuru + hikâye taslağı (güncel)
- `kaynak_katalog.csv` — 844 eserlik katalog
- `graf_olcum.py` / `graf_olcum_sonuc.json` — dil dağılımı ölçüm betiği + sonuç
- `ara-index.json` — site arama indeksi (ham)
- `scope.md` — bu dosya
