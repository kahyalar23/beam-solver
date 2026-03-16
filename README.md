<div align="center">

# 🏗️ Yapı Statiği Hesaplayıcı

**Tarayıcı tabanlı kiriş ve kafes analiz uygulaması**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-009688?style=flat-square&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)
![NumPy](https://img.shields.io/badge/NumPy-1.26+-013243?style=flat-square&logo=numpy&logoColor=white)

</div>

---

## 📸 Ekran Görüntüleri

> **Kiriş Analizi** — İnteraktif canvas editörü, M/V diyagramları, reaksiyon tablosu

```
┌─────────────────────────────────────────────────────────┐
│  🔧 KİRİŞ          🔩 KAFES SİSTEMİ                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ↓P=100kN                                              │
│       │                                                 │
│  ▲────┼────────────────────────────────────⊿           │
│  x=0                  x=5m                  x=10m       │
│                                                         │
│  ━━━━━━━━━━━━ M DİYAGRAMI ━━━━━━━━━━━━━━━━━━━━        │
│              ╭──────────╮                               │
│             ╱            ╲  max|M| = 250.00 kNm        │
│  ──────────╯              ╰──────────                   │
│                                                         │
│  ━━━━━━━━━━━━ V DİYAGRAMI ━━━━━━━━━━━━━━━━━━━━        │
│  ────────────╮              ╭─────────── max|V| = 50kN │
│              ╰──────────────╯                           │
└─────────────────────────────────────────────────────────┘
```

> **Kafes Analizi** — Düğüm/çubuk editörü, kuvvet renk kodlaması (🟢 çekme / 🔴 basınç)

```
┌─────────────────────────────────────────────────────────┐
│  🔧 KİRİŞ          🔩 KAFES SİSTEMİ                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│                    C (2,3)                              │
│                   /       \                             │
│      🟢 AC=18.0  /         \  🔴 BC=-15.0              │
│                 /           \                           │
│  ▲ A (0,0) ──────────────── B (4,0) ⊿                  │
│              🟢 AB=10.0                                 │
│                                                         │
│  ┌──────────────────────────────────────────────┐      │
│  │ Çubuk │  Kuvvet  │  Durum                    │      │
│  │  AB   │  10.000  │  ✅ ÇEKİLME               │      │
│  │  AC   │  18.028  │  ✅ ÇEKİLME               │      │
│  │  BC   │ -15.000  │  🔴 BASINÇ                │      │
│  └──────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────┘
```

---

## ✨ Özellikler

### 🔧 Kiriş Analizi (Euler–Bernoulli FEM)
- **İnteraktif canvas** — tıklayarak mesnet ve yük ekleme/silme
- **4 yük tipi:** nokta yük, moment, tekdüze yayılı (UDL), üçgen/trapez
- **3 mesnet tipi:** pim (pin), rulmanlı (roller), ankastre (fixed)
- **M / V diyagramları** — hover ile değer okuma
- **Reaksiyon tablosu** — Fy ve Mz değerleri

### 🔩 Kafes Analizi (Direct Stiffness Method)
- **Görsel düğüm editörü** — grid snap ile hassas konum
- **Renkli kuvvet görselleştirmesi** — yeşil=çekme, kırmızı=basınç
- **Çubuk kuvvetleri tablosu** — kuvvet, uzunluk, EA
- **Düğüm yer değiştirmeleri** — δx, δy
- **Denge kontrolü** — ΣFx, ΣFy otomatik doğrulama
- **Örnek yükle** — tek tıkla test kafesi

---

## 🚀 Hızlı Başlangıç

### Otomatik (Windows)
`baslat (2).bat` dosyasına çift tıklayın — bağımlılıkları kurar ve tarayıcıyı açar.

### Manuel
```bash
# Bağımlılıkları yükle
pip install -r requirements.txt

# Sunucuyu başlat
uvicorn main:app --reload --port 8000
```

Tarayıcıda → **http://localhost:8000**  
API dökümantasyonu → **http://localhost:8000/docs**

---

## 🛠️ Teknoloji Yığını

| Katman | Teknoloji | Görev |
|--------|-----------|-------|
| **Backend** | FastAPI + Uvicorn | REST API sunucusu |
| **Hesap** | NumPy | Matris işlemleri (kafes) |
| **Frontend** | React 18 (CDN) | UI bileşenleri |
| **Render** | SVG | Canvas ve diyagramlar |
| **Transpiler** | Babel Standalone | JSX çalışma zamanı |

---

## 📡 API Endpointleri

| Yöntem | Yol | Açıklama |
|--------|-----|----------|
| `POST` | `/api/calculate` | Kiriş FEM hesaplama |
| `POST` | `/api/truss/calculate` | Kafes DSM hesaplama |
| `POST` | `/api/projects` | Proje kaydet |
| `GET`  | `/api/projects` | Tüm projeleri listele |
| `GET`  | `/api/projects/{id}` | Proje getir |
| `DELETE` | `/api/projects/{id}` | Proje sil |

### Kiriş İsteği
```bash
curl -X POST http://localhost:8000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "L": 10,
    "supports": [{"x": 0, "type": "pin"}, {"x": 10, "type": "roller"}],
    "loads":    [{"type": "point", "x": 5, "P": 100}]
  }'
```

### Kafes İsteği
```bash
curl -X POST http://localhost:8000/api/truss/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "nodes":    [{"id":"A","x":0,"y":0}, {"id":"B","x":4,"y":0}, {"id":"C","x":2,"y":3}],
    "members":  [{"id":"AB","n1":"A","n2":"B","EA":10000}, {"id":"AC","n1":"A","n2":"C","EA":10000}, {"id":"BC","n1":"B","n2":"C","EA":10000}],
    "supports": [{"node_id":"A","type":"pin"}, {"node_id":"B","type":"roller_h"}],
    "loads":    [{"node_id":"C","Fx":0,"Fy":-20}]
  }'
```

---

## 📐 Desteklenen Yük ve Mesnet Tipleri

### Kiriş Yükleri
| Tip | Gerekli Alanlar | Açıklama |
|-----|-----------------|----------|
| `point` | `x`, `P` (kN) | Nokta kuvvet |
| `moment` | `x`, `M` (kNm) | Saat yönü + |
| `udl` | `x1`, `x2`, `w` (kN/m) | Tekdüze yayılı |
| `triangular` | `x1`, `x2`, `w`, `w2` (kN/m) | Üçgen / trapez |

### Kiriş Mesnetleri
| Tip | Kısıt |
|-----|-------|
| `pin` | v = 0 |
| `roller` | v = 0 |
| `fixed` | v = 0, θ = 0 |

### Kafes Mesnetleri
| Tip | Kısıt |
|-----|-------|
| `pin` | u = 0, v = 0 |
| `roller_h` | v = 0 (yatay rulo) |
| `roller_v` | u = 0 (dikey rulo) |

---

## 🗂️ Proje Yapısı

```
beam-solver/
├── main.py            # FastAPI + Kiriş FEM + Kafes DSM çözücü
├── test_solver.py     # Birim testler (6 test — kiriş + kafes)
├── requirements.txt
├── projects/          # Kaydedilen projeler (JSON, otomatik oluşur)
└── static/
    └── index.html     # React frontend (tek dosya, CDN bağımlılıkları)
```

---

## 🧪 Testleri Çalıştır

```bash
python test_solver.py
```

```
[Test 1] Basit mesnetli kiriş — orta nokta yük (P=100kN, L=10m)
  ✓ Ra/Rb @x=0.0: 50.0000  ≈  50.0000
  ✓ maxM: 250.0000  ≈  250.0000

[Test 5] Kafes — basit üçgen (P=20kN)
  ✓ ΣFy reaksiyon: 20.0000  ≈  20.0000

========================================
Sonuç: 6/6 test geçti
```

---

## 📜 Lisans

MIT

