"""
Yapı Statiği Hesaplayıcı — FastAPI Backend
============================================
Kiriş: Euler–Bernoulli kiriş teorisi, FEM çözücü (100 eleman), Gauss eliminasyonu.
Kafes: Direct Stiffness Method, 2-D düzlem kafes sistemi.

Endpoints:
  POST /api/calculate          → Kiriş FEM hesaplama
  POST /api/truss/calculate    → Kafes hesaplama
  POST /api/projects           → Proje kaydet
  GET  /api/projects           → Tüm projeleri listele
  GET  /api/projects/{pid}     → Proje getir
  DELETE /api/projects/{pid}   → Proje sil
  GET  /                       → Sağlık kontrolü
"""

from __future__ import annotations

import json
import math
import time
import uuid
from pathlib import Path
from typing import Literal, Optional

import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, Field, field_validator

# ─────────────────────────────────────────────
# UYGULAMA
# ─────────────────────────────────────────────

app = FastAPI(
    title="Kiriş Hesaplayıcı API",
    description="Euler–Bernoulli FEM kiriş analiz servisi",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Üretimde kısıtlayın
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Projeleri JSON dosyalarında sakla
PROJECTS_DIR = Path("projects")
PROJECTS_DIR.mkdir(exist_ok=True)


# ─────────────────────────────────────────────
# PYDANTIC MODELLERİ
# ─────────────────────────────────────────────

class Support(BaseModel):
    x: float = Field(..., ge=0, description="Mesnet konumu (m)")
    type: Literal["pin", "roller", "fixed"] = Field(..., description="Mesnet tipi")


class Load(BaseModel):
    type: Literal["point", "moment", "udl", "triangular"]
    # Nokta yük / moment
    x:  Optional[float] = None
    P:  Optional[float] = None   # kN
    M:  Optional[float] = None   # kNm
    # Yayılı / üçgen yük
    x1: Optional[float] = None
    x2: Optional[float] = None
    w:  Optional[float] = None   # kN/m (başlangıç)
    w2: Optional[float] = None   # kN/m (bitiş, üçgen için)

    @field_validator("type")
    @classmethod
    def validate_fields(cls, v):
        return v


class BeamRequest(BaseModel):
    L:        float   = Field(..., gt=0, le=500, description="Kiriş uzunluğu (m)")
    supports: list[Support] = Field(..., min_length=1)
    loads:    list[Load]    = Field(..., min_length=1)
    n_elem:   int     = Field(default=100, ge=20, le=500, description="FEM eleman sayısı")


class ProjectSaveRequest(BaseModel):
    name:     str = Field(..., min_length=1, max_length=100)
    beam:     BeamRequest
    results:  Optional[dict] = None


class ProjectMeta(BaseModel):
    id:         str
    name:       str
    created_at: float
    L:          float
    n_supports: int
    n_loads:    int


# ── Kafes (Truss) modelleri ──────────────────
class TrussNode(BaseModel):
    id: str
    x:  float
    y:  float


class TrussMember(BaseModel):
    id: str
    n1: str
    n2: str
    EA: float = Field(default=1.0, gt=0, description="EA (kN)")


class TrussSupport(BaseModel):
    node_id: str
    type: Literal["pin", "roller_h", "roller_v"]
    # pin      → x ve y sabit
    # roller_h → y sabit, x serbest (yatay rulo)
    # roller_v → x sabit, y serbest (dikey rulo)


class TrussLoad(BaseModel):
    node_id: str
    Fx: float = 0.0   # kN  (+→ sağ)
    Fy: float = 0.0   # kN  (+↑ yukarı)


class TrussRequest(BaseModel):
    nodes:    list[TrussNode]   = Field(..., min_length=2)
    members:  list[TrussMember] = Field(..., min_length=1)
    supports: list[TrussSupport]= Field(..., min_length=1)
    loads:    list[TrussLoad]   = Field(..., min_length=1)


# ─────────────────────────────────────────────
# FEM ÇÖZÜCÜ
# ─────────────────────────────────────────────

def _get_w(load: Load, x: float) -> float:
    """Yayılı yükte x noktasındaki yoğunluğu döndür."""
    if load.type == "udl":
        return load.w
    span = max(load.x2 - load.x1, 1e-10)
    w2 = load.w2 if load.w2 is not None else load.w
    return load.w + (w2 - load.w) * (x - load.x1) / span


def compute_beam(L: float, supports: list[Support], loads: list[Load], n_elem: int = 100) -> dict:
    """
    Euler–Bernoulli kiriş FEM çözümü.

    Döndürür:
        xs, Ms, Vs, Ns : diyagram noktaları
        reactions       : [{"x", "Fy", "Mz"}, ...]
        maxM, maxV, maxN
    """
    t0 = time.perf_counter()

    n_nodes = n_elem + 1
    le = L / n_elem
    n_dof = 2 * n_nodes
    EI  = 1.0
    PEN = 1e12

    def node_of(x: float) -> int:
        return int(max(0, min(n_elem, round(x / L * n_elem))))

    # ── Rijitlik matrisi ──────────────────────
    K = np.zeros((n_dof, n_dof))

    for e in range(n_elem):
        c   = EI / le**3
        le2 = le * le
        ke = np.array([
            [ 12*c,     6*le*c,  -12*c,     6*le*c ],
            [  6*le*c,  4*le2*c,  -6*le*c,  2*le2*c],
            [-12*c,    -6*le*c,   12*c,    -6*le*c ],
            [  6*le*c,  2*le2*c,  -6*le*c,  4*le2*c],
        ])
        dofs = [2*e, 2*e+1, 2*e+2, 2*e+3]
        for i, di in enumerate(dofs):
            for j, dj in enumerate(dofs):
                K[di, dj] += ke[i, j]

    # ── Yük vektörü ──────────────────────────
    F = np.zeros(n_dof)

    for ld in loads:
        if ld.type == "point":
            F[2 * node_of(ld.x)] -= ld.P
        elif ld.type == "moment":
            F[2 * node_of(ld.x) + 1] -= ld.M
        else:  # udl / triangular
            for e in range(n_elem):
                xe1, xe2 = e * le, (e + 1) * le
                a = max(ld.x1, xe1)
                b = min(ld.x2, xe2)
                if b - a < 1e-12:
                    continue
                wa = _get_w(ld, a)
                wb = _get_w(ld, b)
                R  = (wa + wb) / 2 * (b - a)
                if abs(wa - wb) < 1e-10:
                    cg = (a + b) / 2
                else:
                    cg = a + (b - a) * (wa + 2*wb) / (3 * (wa + wb + 1e-15))
                r2 = (cg - xe1) / le
                F[2*e]       -= R * (1 - r2)
                F[2*(e+1)]   -= R * r2

    # Orijinal K ve F'yi sakla (reaksiyon hesabı için)
    K0 = K.copy()
    F0 = F.copy()

    # ── Sınır koşulları (ceza yöntemi) ───────
    for s in supports:
        n0 = node_of(s.x)
        K[2*n0, 2*n0] += PEN
        if s.type == "fixed":
            K[2*n0+1, 2*n0+1] += PEN

    # ── Çöz ──────────────────────────────────
    try:
        d = np.linalg.solve(K, F)
    except np.linalg.LinAlgError:
        raise ValueError("Rijitlik matrisi tekil — mesnet konfigürasyonunu kontrol edin.")

    # ── Reaksiyonlar ─────────────────────────
    rx_map: dict[float, dict] = {}
    for s in supports:
        n0  = node_of(s.x)
        xk  = round(n0 * le, 8)
        if xk not in rx_map:
            rx_map[xk] = {"Fy": 0.0, "Mz": 0.0}

        Fy = float(-F0[2*n0] + K0[2*n0] @ d)
        rx_map[xk]["Fy"] += Fy

        if s.type == "fixed":
            Mz = float(-F0[2*n0+1] + K0[2*n0+1] @ d)
            rx_map[xk]["Mz"] += Mz

    reactions = sorted(
        [{"x": x, "Fy": v["Fy"], "Mz": v["Mz"]} for x, v in rx_map.items()],
        key=lambda r: r["x"],
    )

    # ── Diyagramlar (denge yöntemi) ───────────
    n_pts = 600
    xs, Ms, Vs = [], [], []

    sorted_rx = sorted(rx_map.items())

    for i in range(n_pts + 1):
        x = i * L / n_pts
        V = 0.0
        M = 0.0

        for rx_x, rv in sorted_rx:
            if rx_x <= x + 1e-9:
                V += rv["Fy"]
                M += rv["Fy"] * (x - rx_x) + rv["Mz"]

        for ld in loads:
            if ld.type == "point" and ld.x <= x + 1e-9:
                V -= ld.P
                M -= ld.P * (x - ld.x)
            elif ld.type == "moment" and ld.x <= x + 1e-9:
                M -= ld.M
            elif ld.type in ("udl", "triangular") and ld.x1 < x + 1e-9:
                x2c   = min(ld.x2, x)
                delta = x2c - ld.x1
                if delta > 1e-9:
                    w1  = ld.w
                    w2c = _get_w(ld, x2c)
                    R   = (w1 + w2c) / 2 * delta
                    if abs(w1 - w2c) < 1e-10:
                        cg = ld.x1 + delta / 2
                    else:
                        cg = ld.x1 + delta * (w1 + 2*w2c) / (3 * (w1 + w2c + 1e-15))
                    V -= R
                    M -= R * (x - cg)

        xs.append(round(x, 6))
        Ms.append(round(M, 6))
        Vs.append(round(V, 6))

    Ns = [0.0] * len(xs)

    max_M = max((abs(m) for m in Ms), default=1e-9)
    max_V = max((abs(v) for v in Vs), default=1e-9)

    elapsed_ms = round((time.perf_counter() - t0) * 1000, 2)

    return {
        "xs":       xs,
        "Ms":       Ms,
        "Vs":       Vs,
        "Ns":       Ns,
        "maxM":     max_M,
        "maxV":     max_V,
        "maxN":     0.0,
        "reactions": reactions,
        "L":        L,
        "n_elem":   n_elem,
        "elapsed_ms": elapsed_ms,
    }


# ─────────────────────────────────────────────
# 2D KAFES (TRUSS) ÇÖZÜCÜ — Direct Stiffness
# ─────────────────────────────────────────────

def compute_truss(
    nodes:    list[TrussNode],
    members:  list[TrussMember],
    supports: list[TrussSupport],
    loads:    list[TrussLoad],
) -> dict:
    """
    2-D düzlem kafes sistemi — Direct Stiffness Method.

    Döndürür:
        members      : [{"id","n1","n2","force","status","L","EA"}]
        reactions    : [{"node_id","x","y","Fx","Fy"}]
        displacements: [{"id","x","y","dx","dy"}]
        maxForce, minForce
    """
    t0 = time.perf_counter()

    n = len(nodes)
    n_dof = 2 * n
    node_idx = {nd.id: i for i, nd in enumerate(nodes)}
    PEN = 1e12

    K = np.zeros((n_dof, n_dof))

    for m in members:
        i  = node_idx[m.n1]
        j  = node_idx[m.n2]
        xi, yi = nodes[i].x, nodes[i].y
        xj, yj = nodes[j].x, nodes[j].y
        Lm = math.sqrt((xj - xi) ** 2 + (yj - yi) ** 2)
        if Lm < 1e-10:
            raise ValueError(f"Sıfır uzunluklu eleman: {m.id}")
        cx, cy = (xj - xi) / Lm, (yj - yi) / Lm
        k = m.EA / Lm
        kmat = k * np.array([
            [ cx*cx,  cx*cy, -cx*cx, -cx*cy],
            [ cx*cy,  cy*cy, -cx*cy, -cy*cy],
            [-cx*cx, -cx*cy,  cx*cx,  cx*cy],
            [-cx*cy, -cy*cy,  cx*cy,  cy*cy],
        ])
        dofs = [2*i, 2*i+1, 2*j, 2*j+1]
        for a, da in enumerate(dofs):
            for b, db in enumerate(dofs):
                K[da, db] += kmat[a, b]

    # Yük vektörü
    F = np.zeros(n_dof)
    for ld in loads:
        ni = node_idx[ld.node_id]
        F[2*ni]   += ld.Fx
        F[2*ni+1] += ld.Fy

    K0 = K.copy()
    F0 = F.copy()

    # Sınır koşulları (ceza yöntemi)
    for s in supports:
        ni = node_idx[s.node_id]
        if s.type in ("pin",):
            K[2*ni,   2*ni]   += PEN
            K[2*ni+1, 2*ni+1] += PEN
        elif s.type == "roller_h":   # y sabit
            K[2*ni+1, 2*ni+1] += PEN
        elif s.type == "roller_v":   # x sabit
            K[2*ni,   2*ni]   += PEN

    # Çöz
    try:
        d = np.linalg.solve(K, F)
    except np.linalg.LinAlgError:
        raise ValueError("Kafes rijitlik matrisi tekil — mesnet/eleman konfigürasyonunu kontrol edin.")

    # Eleman kuvvetleri
    member_results = []
    forces = []
    for m in members:
        i  = node_idx[m.n1]
        j  = node_idx[m.n2]
        xi, yi = nodes[i].x, nodes[i].y
        xj, yj = nodes[j].x, nodes[j].y
        Lm = math.sqrt((xj - xi) ** 2 + (yj - yi) ** 2)
        if Lm < 1e-10:
            continue
        cx, cy = (xj - xi) / Lm, (yj - yi) / Lm
        delta = cx * (d[2*j] - d[2*i]) + cy * (d[2*j+1] - d[2*i+1])
        force = float(m.EA / Lm * delta)
        forces.append(force)
        status = "tension" if force > 1e-6 else ("compression" if force < -1e-6 else "zero")
        member_results.append({
            "id": m.id, "n1": m.n1, "n2": m.n2,
            "force": round(force, 6), "status": status,
            "L": round(Lm, 6), "EA": m.EA,
        })

    # Reaksiyonlar
    reactions = []
    seen = set()
    for s in supports:
        ni  = node_idx[s.node_id]
        key = s.node_id
        if key in seen:
            continue
        seen.add(key)
        Rx_val = float(K0[2*ni, :]   @ d - F0[2*ni])
        Ry_val = float(K0[2*ni+1, :] @ d - F0[2*ni+1])
        if s.type == "roller_h":
            Rx_val = 0.0   # x serbest
        elif s.type == "roller_v":
            Ry_val = 0.0   # y serbest
        reactions.append({
            "node_id": s.node_id,
            "x": nodes[ni].x, "y": nodes[ni].y,
            "Fx": round(Rx_val, 6), "Fy": round(Ry_val, 6),
        })

    # Düğüm yer değiştirmeleri
    displacements = [
        {"id": nd.id, "x": nd.x, "y": nd.y,
         "dx": round(float(d[2*i]),   8),
         "dy": round(float(d[2*i+1]), 8)}
        for i, nd in enumerate(nodes)
    ]

    max_force = max((abs(f) for f in forces), default=0.0)
    min_force = min(forces, default=0.0)

    elapsed_ms = round((time.perf_counter() - t0) * 1000, 2)

    return {
        "members":       member_results,
        "reactions":     reactions,
        "displacements": displacements,
        "maxForce":      round(max_force, 6),
        "minForce":      round(min_force, 6),
        "elapsed_ms":    elapsed_ms,
    }


# ─────────────────────────────────────────────
# YARDIMCI FONKSİYONLAR
# ─────────────────────────────────────────────

def _project_path(pid: str) -> Path:
    return PROJECTS_DIR / f"{pid}.json"


def _load_project(pid: str) -> dict:
    p = _project_path(pid)
    if not p.exists():
        raise HTTPException(status_code=404, detail=f"Proje bulunamadı: {pid}")
    return json.loads(p.read_text(encoding="utf-8"))


# ─────────────────────────────────────────────
# ENDPOINT'LER
# ─────────────────────────────────────────────

@app.get("/health", tags=["Sistem"])
def health():
    return {
        "status": "ok",
        "service": "Kiriş Hesaplayıcı API",
        "version": "1.0.0",
    }


@app.post("/api/calculate", tags=["Hesaplama"])
def calculate(req: BeamRequest):
    """
    FEM kiriş analizi yap.

    - **L**: Kiriş uzunluğu (m)
    - **supports**: Mesnet listesi (pin | roller | fixed)
    - **loads**: Yük listesi (point | moment | udl | triangular)
    - **n_elem**: FEM eleman sayısı (varsayılan: 100)
    """
    try:
        result = compute_beam(req.L, req.supports, req.loads, req.n_elem)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    return result


@app.post("/api/truss/calculate", tags=["Kafes"])
def truss_calculate(req: TrussRequest):
    """
    2-D düzlem kafes sistemi analizi (Direct Stiffness Method).

    - **nodes**: Düğüm noktaları [{id, x, y}]
    - **members**: Çubuklar [{id, n1, n2, EA}]
    - **supports**: Mesnetter [{node_id, type: pin|roller_h|roller_v}]
    - **loads**: Düğüm yükleri [{node_id, Fx, Fy}]
    """
    try:
        result = compute_truss(req.nodes, req.members, req.supports, req.loads)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    return result


@app.post("/api/projects", tags=["Projeler"], status_code=201)
def save_project(req: ProjectSaveRequest):
    """Kiriş konfigürasyonunu ve (varsa) sonuçlarını kaydet."""
    pid  = str(uuid.uuid4())
    data = {
        "id":         pid,
        "name":       req.name,
        "created_at": time.time(),
        "beam":       req.beam.model_dump(),
        "results":    req.results,
    }
    _project_path(pid).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"id": pid, "name": req.name, "created_at": data["created_at"]}


@app.get("/api/projects", tags=["Projeler"])
def list_projects() -> list[ProjectMeta]:
    """Kayıtlı tüm projelerin özetini döndür."""
    projects = []
    for p in sorted(PROJECTS_DIR.glob("*.json"), key=lambda f: f.stat().st_mtime, reverse=True):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            projects.append(ProjectMeta(
                id=data["id"],
                name=data["name"],
                created_at=data["created_at"],
                L=data["beam"]["L"],
                n_supports=len(data["beam"]["supports"]),
                n_loads=len(data["beam"]["loads"]),
            ))
        except Exception:
            continue
    return projects


@app.get("/api/projects/{pid}", tags=["Projeler"])
def get_project(pid: str):
    """Belirli bir projeyi tam detayıyla döndür."""
    return _load_project(pid)


@app.delete("/api/projects/{pid}", tags=["Projeler"])
def delete_project(pid: str):
    """Bir projeyi kalıcı olarak sil."""
    _load_project(pid)   # 404 kontrolü
    _project_path(pid).unlink()
    return {"deleted": pid}


# ─────────────────────────────────────────────
# FRONTEND
# ─────────────────────────────────────────────

@app.get("/", include_in_schema=False)
def serve_frontend():
    p = Path("static/index.html")
    if p.exists():
        return FileResponse(str(p), media_type="text/html")
    return HTMLResponse("<h2>static/index.html bulunamadi.</h2>", status_code=404)


# ─────────────────────────────────────────────
# GELİŞTİRME SUNUCUSU
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
