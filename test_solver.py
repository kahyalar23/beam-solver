"""
Basit birim testler — backend kurulmadan önce FEM çözücüyü doğrular.
Çalıştır: python test_solver.py
"""
import sys
sys.path.insert(0, ".")

from main import compute_beam, compute_truss, Support, Load, TrussNode, TrussMember, TrussSupport, TrussLoad

def assert_close(a, b, tol=0.01, label=""):
    err = abs(a - b)
    if err > tol:
        print(f"  ✗ {label}: beklenen={b:.4f}  hesaplanan={a:.4f}  hata={err:.4f}")
        return False
    print(f"  ✓ {label}: {a:.4f}  ≈  {b:.4f}")
    return True


def test_simply_supported_midpoint():
    """
    Basit mesnetli kiriş, orta noktada P=100 kN
    Beklenen: Ra = Rb = 50 kN, M_max = 250 kNm
    """
    print("\n[Test 1] Basit mesnetli kiriş — orta nokta yük (P=100kN, L=10m)")
    r = compute_beam(
        L=10,
        supports=[Support(x=0, type="pin"), Support(x=10, type="roller")],
        loads=[Load(type="point", x=5, P=100)],
    )
    ok = True
    for rxn in r["reactions"]:
        ok &= assert_close(rxn["Fy"], 50.0, tol=0.5, label=f"Ra/Rb @x={rxn['x']:.1f}")
    ok &= assert_close(r["maxM"], 250.0, tol=2.0, label="maxM")
    return ok


def test_simply_supported_udl():
    """
    Basit mesnetli kiriş, tekdüze yayılı yük w=10 kN/m, L=6m
    Ra = Rb = 30 kN, M_max = 45 kNm @ x=3m
    """
    print("\n[Test 2] Basit mesnetli kiriş — UDL (w=10kN/m, L=6m)")
    r = compute_beam(
        L=6,
        supports=[Support(x=0, type="pin"), Support(x=6, type="roller")],
        loads=[Load(type="udl", x1=0, x2=6, w=10)],
    )
    ok = True
    for rxn in r["reactions"]:
        ok &= assert_close(rxn["Fy"], 30.0, tol=0.5, label=f"Ra/Rb @x={rxn['x']:.1f}")
    ok &= assert_close(r["maxM"], 45.0, tol=1.0, label="maxM")
    return ok


def test_cantilever_tip_load():
    """
    Ankastre kiriş, uç yükü P=50kN, L=5m
    Ra = 50 kN, Ma = -250 kNm
    """
    print("\n[Test 3] Ankastre kiriş — uç yükü (P=50kN, L=5m)")
    r = compute_beam(
        L=5,
        supports=[Support(x=0, type="fixed")],
        loads=[Load(type="point", x=5, P=50)],
    )
    ok = True
    rxn0 = next((rx for rx in r["reactions"] if abs(rx["x"]) < 0.01), None)
    if rxn0:
        ok &= assert_close(rxn0["Fy"], 50.0, tol=1.0, label="Fy @x=0")
        ok &= assert_close(abs(rxn0["Mz"]), 250.0, tol=3.0, label="|Mz| @x=0")
    ok &= assert_close(r["maxM"], 250.0, tol=3.0, label="maxM")
    return ok


def test_equilibrium():
    """
    Statik denge: ΣFy_reaksiyonlar == ΣFy_yükler
    """
    print("\n[Test 4] Statik denge kontrolü")
    r = compute_beam(
        L=8,
        supports=[Support(x=0, type="pin"), Support(x=8, type="roller")],
        loads=[
            Load(type="point", x=3,   P=80),
            Load(type="udl",   x1=4, x2=8, w=15),
        ],
    )
    total_load = 80 + 15 * 4
    total_rxn  = sum(rx["Fy"] for rx in r["reactions"])
    ok = assert_close(total_rxn, total_load, tol=1.0, label="ΣFy denge")
    return ok


def test_truss_simple_triangle():
    """
    Basit üçgen kafes: A(0,0)-B(4,0)-C(2,3)
    Pin @ A, roller_h @ B, Fy=-20 kN @ C
    Beklenen: ΣFy_reaksiyon = 20 kN
    """
    print("\n[Test 5] Kafes — basit üçgen (P=20kN)")
    r = compute_truss(
        nodes=[
            TrussNode(id="A", x=0, y=0),
            TrussNode(id="B", x=4, y=0),
            TrussNode(id="C", x=2, y=3),
        ],
        members=[
            TrussMember(id="AB", n1="A", n2="B", EA=10000),
            TrussMember(id="AC", n1="A", n2="C", EA=10000),
            TrussMember(id="BC", n1="B", n2="C", EA=10000),
        ],
        supports=[
            TrussSupport(node_id="A", type="pin"),
            TrussSupport(node_id="B", type="roller_h"),
        ],
        loads=[TrussLoad(node_id="C", Fx=0, Fy=-20)],
    )
    ok = True
    total_fy = sum(rx["Fy"] for rx in r["reactions"])
    ok &= assert_close(total_fy, 20.0, tol=0.1, label="ΣFy reaksiyon")
    ok &= len(r["members"]) == 3
    ok &= len(r["displacements"]) == 3
    print(f"  {'✓' if ok else '✗'} Çubuk sayısı: {len(r['members'])}, Yer değiştirme: {len(r['displacements'])}")
    return ok


def test_truss_equilibrium():
    """
    Kafes denge kontrolü: ΣFx_reaksiyon + ΣFx_yük = 0, ΣFy_reaksiyon + ΣFy_yük = 0
    """
    print("\n[Test 6] Kafes — denge kontrolü")
    r = compute_truss(
        nodes=[
            TrussNode(id="A", x=0, y=0),
            TrussNode(id="B", x=6, y=0),
            TrussNode(id="C", x=3, y=4),
        ],
        members=[
            TrussMember(id="AB", n1="A", n2="B", EA=5000),
            TrussMember(id="AC", n1="A", n2="C", EA=5000),
            TrussMember(id="BC", n1="B", n2="C", EA=5000),
        ],
        supports=[
            TrussSupport(node_id="A", type="pin"),
            TrussSupport(node_id="B", type="roller_h"),
        ],
        loads=[TrussLoad(node_id="C", Fx=10, Fy=-30)],
    )
    ok = True
    total_fx_rxn = sum(rx["Fx"] for rx in r["reactions"])
    total_fy_rxn = sum(rx["Fy"] for rx in r["reactions"])
    ok &= assert_close(total_fx_rxn + 10, 0.0, tol=0.1, label="ΣFx denge")
    ok &= assert_close(total_fy_rxn + (-30), 0.0, tol=0.1, label="ΣFy denge")
    return ok


if __name__ == "__main__":
    results = [
        test_simply_supported_midpoint(),
        test_simply_supported_udl(),
        test_cantilever_tip_load(),
        test_equilibrium(),
        test_truss_simple_triangle(),
        test_truss_equilibrium(),
    ]
    passed = sum(results)
    total  = len(results)
    print(f"\n{'='*40}")
    print(f"Sonuç: {passed}/{total} test geçti")
    if passed < total:
        sys.exit(1)
