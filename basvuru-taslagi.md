# OpenAIRE AI Hackathon — Başvuru Taslağı

**Proje:** Kadim Kütüphane × OpenAIRE Graph — "Kaynaktan Bilime" Gezgini
**Tema:** B — Build
**Son teslim:** 20 Ağustos 2026, 23:59 CET (kalan: 19 gün)
**Durum:** Kayıt tamamlandı (1 Ağustos 2026) — Alien MCP erişimi bekleniyor (rolling basis)

---

## 1. Hemen yapılacaklar (kritik sıra)

1. ~~Bugün: Hackathon'a kaydol.~~ **Tamamlandı (1 Ağustos 2026).** MCP erişimi "rolling basis" veriliyor, onay bekleniyor.
2. **Bu hafta: Zenodo kayıt envanterini güçlendir** (aşağıda §4'teki bulgular).
3. **Erişim gelince: MCP üzerinden graf sorgularını doğrula** (§3'teki sorgu listesi).
4. **10–18 Ağustos: Eseri (gezgin arayüzü) kur + hikâyeyi son haline getir.**
5. **19 Ağustos: Teslim** (son güne bırakma; 20 Ağustos 23:59 CET kesin kapanış).

---

## 2. Eser konsepti: "Kaynaktan Bilime" Gezgini (From Source to Science)

**Tek cümlelik fikir:** Kadim Kütüphane'nin Zenodo'daki Türkçe birincil-kaynak çevirilerini, OpenAIRE Graph'teki uluslararası bilimsel literatüre bağlayan küçük bir web gezgini.

**Ne yapar:**
- Her çeviri kaydı (Zenodo DOI'si) için graf üzerinden ilgili yayınları, yazarları, veri setlerini ve fonları çeker.
- Kullanıcı bir metni seçer (örn. *Tapınakçı Ritüeli* çevirisi) → gezgin o metnin etrafındaki bilimsel ekosistemi gösterir: kim çalışıyor, hangi dergiler, hangi ülkeler, Türkçe literatürdeki boşluk.
- Statik, hafif bir web uygulaması — kadimkutuphane.com'un mevcut estetiğiyle uyumlu, ayrı sayfa olarak yayınlanır.

**Neden Tema B'ye tam oturuyor:** Sayfadaki tanım birebir — "a tool, an app, an agent, an integration with another data source… We want to see something that works and that others can reuse or build on." Zenodo külliyatı + OpenAIRE Graph entegrasyonu = tam istenen şey.

**Teknik yığın (basit tut):**
- Veri: Zenodo API (kendi kayıtlarınız) + OpenAIRE API / Alien MCP (graf sorguları)
- Ön yüz: tek sayfa statik site (mevcut site altyapınıza drop-in)
- Eşleştirme: çeviri başlığındaki orijinal eser adı → grafta konu/başlık sorgusu

---

## 3. Erişim gelince doğrulanacak graf sorguları

Alien MCP bağlandığında şu soruların grafta karşılığı olduğunu teyit et:

1. "Western esotericism" konulu yayın evreni: kaç yayın, hangi dergiler, yıllık eğilim?
2. Çevirisi yapılan eserlerin (Hermetica, Picatrix, Agrippa, Templar texts…) graftaki künye ve atıf izleri.
3. Türkiye merkezli / Türkçe dilli çıktılar: alanın Türkçe boşluğunun graf kanıtı (bu, hikâyenin "içgörü" kısmının bel kemiği).
4. Kendi Zenodo kayıtlarınız grafta göründü mü? (hasat gecikmesi ~birkaç hafta; temmuz ortası kayıtları ağustosta düşmeli)

---

## 4. Zenodo tarafında tespit edilen bulgular (1 Ağustos 2026)

- **7 kayıt** "kadim kütüphane" ifadesiyle indeksli; tümü 15.07.2026 tarihli, türü **"Other"**.
- Sitedeki 844 birincil kaynağın henüz çok küçük kısmı Zenodo'da görünüyor (ya da "kadim kütüphane" ifadesi tüm kayıtlarda geçmiyor).
- **Öneri 1 (yüksek etki):** Kayıt türünü "Other" yerine uygun metin türüne (literature / book section) çekmek, OpenAIRE hasadında daha doğru sınıflandırma sağlar.
- **Öneri 2:** Tüm kayıtlara tutarlı bir etiket/anahtar kelime ("Kadim Kütüphane", "Türkçe çeviri", orijinal eser adı) eklemek hem Zenodo içi keşfi hem gezginin eşleştirmesini kolaylaştırır.
- **Öneri 3:** Teslimden önce mümkünse 20–30 çeviriyi daha yüklemek, "külliyat" iddiasını graf üzerinden somutlaştırır.

---

## 5. Hikâye taslağı (1–2 sayfa, İngilizce teslim)

> Aşağıdaki metin teslim diline uygun olarak İngilizce kurgulandı. İki katman veri kullanılıyor:
> (1) **9 tematik kümenin dil dağılımı**, 1 Ağustos 2026'da OpenAIRE genel API'sinden ölçüldü
> (`graf_olcum.py` → `graf_olcum_sonuc.json`); (2) **844 eserin tek tek graf yoğunluğu**,
> 15-16 Ağustos 2026'da ölçüldü, sorgular önce otomatik üretildi, sonra LLM yardımıyla
> tek tek doğrulanıp düzeltildi (`atlas_betigi.py` → `atlas-veri.json`, bkz. `README.md`
> metodoloji notu). Canlı sonuç: kadimkutuphane.com/bosluk-atlasi.

### From Source to Science: Mapping a Turkish Primary-Source Library onto the OpenAIRE Graph

**The question.**
Kadim Kütüphane (kadimkutuphane.com) publishes Turkish translations of 844 primary sources of the Western esoteric tradition — texts like the Corpus Hermeticum, Picatrix, and Templar rituals — openly, with translations deposited on Zenodo under CC-BY-SA and DOIs. But who studies these texts scientifically? What does the international research landscape around them look like, and where does Turkish-language scholarship sit inside it? We built a small, reproducible tool — the *Boşluk Atlası* (Translation-Gap Atlas) — to ask the OpenAIRE Graph directly, work by work.

**The method.**
For each of the 844 works we built a disambiguated OpenAIRE `keywords` query identifying the work or author unambiguously, queried the public Graph API for how many publications surround it, and combined that with a topic-level heat map of Turkish-language representation across nine esotericism-adjacent research clusters (*alchemy*: 9,266 publications, *gnosticism*: 2,402, *western esotericism*: 920, *hermeticism*: 555, *hermetica*: 351, *Knights Templar*: 368, *Corpus Hermeticum*: 311, *Cornelius Agrippa*: 220, *Picatrix*: 140). Getting the per-work queries right was itself a finding: a naive, automatically generated query (raw fragments of the Turkish page slug) produces either near-total silence or wildly inflated false positives from unrelated namesakes — one early run returned 76,656 hits for a work because its query collided with a common English name. Fixing this required treating query construction as a research task in its own right — qualifying ambiguous names, using internationally recognized titles for anonymous works, and never inventing an attribution.

**The insight.**
With disambiguated queries, **534 of 844 works (63%) have at least one trace in the OpenAIRE Graph, and 310 (37%) have none at all** — a structural translation-priority signal, not noise. At the topic level the field is demonstrably active but linguistically one-sided: across ~2,700 scanned records in the nine clusters above, Turkish-language scholarly output is nearly invisible — **0 Turkish records for Picatrix, Hermetica, Cornelius Agrippa and Gnosticism; 0.65% for "western esotericism"; 0.10% for alchemy** (even accounting for the ~45% of records with undetermined language, the gap holds — English dominates every cluster). The only exception, Knights Templar at 2.7%, comes from general-history journals, not esotericism studies specifically. This is precisely the gap Kadim Kütüphane's 844-source translation project addresses: the library is not just an archive, it is infrastructure for a research field the graph shows to be internationally active but essentially silent in Turkish.

**The loop.**
Seven of the library's translations are already deposited on Zenodo with CC-BY-SA DOIs — a first, concrete instance of closing the loop the tool describes: *the graph measures the gap → the library translates the text → the translation re-enters the graph → the graph can measure again.*

**What others can reuse.**
The atlas is a small, fully static web page with no server-side component and no live API calls at view time — anyone can open it with no setup. The underlying recipe (disambiguated per-work query → OpenAIRE Graph density → gap score, cross-checked against a topic-level heat map) generalizes to any non-English source library, catalogue, or archive that wants to see its place — and its blind spots — in the global research graph. Code, data, and methodology notes are published under CC-BY.

---

## 6. Teslim paketi kontrol listesi

- [x] Eser: çalışan gezgin URL'si — https://kadimkutuphane.com/bosluk-atlasi
- [x] Açık kaynak kod deposu (CC-BY) — https://github.com/SiraU/bosluk-atlasi
- [x] Hikâye: 1–2 sayfa İngilizce write-up (yukarıda, gerçek 844-eser graf sayılarıyla güncellendi)
- [x] Lisans: repo README + LICENSE dosyasında CC-BY 4.0 belirtimi
- [ ] Resmi başvuru formunun gönderilmesi (innovation@openaire.eu)
- [ ] Topluluk oylaması hazırlığı: 21–29 Ağustos arası oy toplamak için kısa tanıtım metni (kadimkutuphane.com + kutsaladonus.com kitleleri burada avantaj)

## 7. Değerlendirme notu

Sayfada "criteria and evaluation process" dokümanı indirilebilir deniyor — kayıt sonrası indirip hikâyeyi kritere göre son kez tıraşlamakta fayda var. Ödül yapısı: 1 büyük ödül (500 € + OSFAIR 2027), tema başına 1 birinci (12 ay Alien kredisi + **OpenAIRE ile ortak vaka çalışması yayını** + eylül community call'da konuşma), ~12 final, 1 topluluk seçimi.
