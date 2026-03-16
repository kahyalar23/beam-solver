# Yapı Statiği Hesaplayıcı — Backend

FastAPI tabanlı yapı analiz servisi.  
- **Kiriş:** Euler–Bernoulli FEM (100 eleman) + Gauss eliminasyonu ile **moment (M)**, **kesme kuvveti (V)** ve **reaksiyon** hesabı.  
- **Kafes:** Direct Stiffness Method ile 2-D düzlem kafes analizi — çubuk kuvvetleri, reaksiyonlar, yer değiştirmeler.

---

## Kurulum

```bash
# 1. Bağımlılıkları yükle
pip install -r requirements.txt

# 2. Sunucuyu başlat
uvicorn main:app --reload --port 8000
```

Tarayıcıda `http://localhost:8000` → `static/index.html` dosyasını sunar.  
API dökümantasyonu: `http://localhost:8000/docs`

---

## API Endpointleri

| Yöntem | Yol | Açıklama |
|--------|-----|----------|
| `POST` | `/api/calculate` | Kiriş FEM hesaplama |
| `POST` | `/api/truss/calculate` | Kafes hesaplama |
| `POST` | `/api/projects` | Proje kaydet |
| `GET`  | `/api/projects` | Tüm projeleri listele |
| `GET`  | `/api/projects/{id}` | Proje getir |
| `DELETE` | `/api/projects/{id}` | Proje sil |

---

## Kiriş Örnek İsteği

```bash
curl -X POST http://localhost:8000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "L": 10,
    "n_elem": 100,
    "supports": [
      {"x": 0,  "type": "pin"},
      {"x": 10, "type": "roller"}
    ],
    "loads": [
      {"type": "point", "x": 5, "P": 100}
    ]
  }'
```

## Kafes Örnek İsteği

```bash
curl -X POST http://localhost:8000/api/truss/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "nodes": [
      {"id":"A","x":0,"y":0},
      {"id":"B","x":4,"y":0},
      {"id":"C","x":2,"y":3}
    ],
    "members": [
      {"id":"AB","n1":"A","n2":"B","EA":10000},
      {"id":"AC","n1":"A","n2":"C","EA":10000},
      {"id":"BC","n1":"B","n2":"C","EA":10000}
    ],
    "supports": [
      {"node_id":"A","type":"pin"},
      {"node_id":"B","type":"roller_h"}
    ],
    "loads": [
      {"node_id":"C","Fx":0,"Fy":-20}
    ]
  }'
```

### Yanıt

```json
{
  "xs":       [0.0, 0.0167, ...],
  "Ms":       [0.0, 0.833, ...],
  "Vs":       [50.0, 50.0, ...],
  "Ns":       [0.0, 0.0, ...],
  "maxM":     250.0,
  "maxV":     50.0,
  "maxN":     0.0,
  "reactions": [
    {"x": 0.0,  "Fy":  50.0, "Mz": 0.0},
    {"x": 10.0, "Fy":  50.0, "Mz": 0.0}
  ],
  "L": 10,
  "n_elem": 100,
  "elapsed_ms": 12.4
}
```

---

## Yük Tipleri

| `type` | Gerekli Alanlar |
|--------|-----------------|
| `point` | `x`, `P` (kN) |
| `moment` | `x`, `M` (kNm) |
| `udl` | `x1`, `x2`, `w` (kN/m) |
| `triangular` | `x1`, `x2`, `w` (başlangıç kN/m), `w2` (bitiş kN/m) |

## Kiriş Mesnet Tipleri

| `type` | Kısıt |
|--------|-------|
| `pin` | Düşey yerdeğiştirme = 0 |
| `roller` | Düşey yerdeğiştirme = 0 |
| `fixed` | Düşey yerdeğiştirme + dönme = 0 |

## Kafes Mesnet Tipleri

| `type` | Kısıt |
|--------|-------|
| `pin` | x ve y sabit |
| `roller_h` | y sabit, x serbest (yatay rulo) |
| `roller_v` | x sabit, y serbest (dikey rulo) |

---

## Proje Dosyaları

Projeler `projects/` klasöründe JSON formatında saklanır.

---

## Mimari

```
beam-solver/
├── main.py            # FastAPI uygulaması + Kiriş FEM + Kafes DSM çözücü
├── test_solver.py     # Birim testler (kiriş + kafes)
├── requirements.txt
├── projects/          # Kaydedilen projeler (otomatik oluşur)
└── static/
    └── index.html     # Frontend (Kiriş + Kafes sekmeli arayüz)
```
