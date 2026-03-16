# LINE-BY-LINE DIFF ANALYSIS: index.html vs index_new.html

## DIFF HUNK 1: Removed Comments (~lines 388-421)

### Context: Lines 385-425 (approx)

**REMOVED from index.html:**
```
Line ~391: {/* Cetvel */}

Line ~404: {/* Hover çizgisi */}

Lines ~410-421: Multiple comment markers removed
  - {/* Kiriş gölgesi */}
  - {/* Kiriş */}
  - {/* Yükler */}
  - {/* Mesnetter */}
```

**STATUS:** These are React/JSX comment cleanup items - removed for code cleanliness

---

## DIFF HUNK 2: Major Refactor - Component Structure (~lines 650-700)

### OLD: index.html (Lines 650-701)
```javascript
/* ═══════════════════════════════════════════════
   ANA BİLEŞEN
═══════════════════════════════════════════════ */
let _id = 100;
const uid = () => String(++_id);

const S = {
  inp: { ... },
  card: { ... },
  lbl: { ... }
};

function Btn({ onClick, color="#38bdf8", children, active=false, small=false }) {
  return ( ... );
}

const modeColors = { ... };
const modeLabels = { ... };

const ModeBtn = ({ id }) => ( ... );

return (
  <div style={{ ... }}>
    {/* BAŞLIK */}
    <div style={{ ... }}>
      <h1>KİRİŞ HESAPLAYICI</h1>
      ...
    </div>
    
    {/* PROJE PANELİ */}
    {projPanel && ( ... )}
    
    {/* ... rest of App */}
```

### NEW: index_new.html (Lines 650-1440)
```javascript
// SAME through line ~673: uid, S styles, Btn component

/* ─── KİRİŞ SEKME ─── */
function BeamTab() {
  const [L, setL] = useState(10);
  const [supports, setSupports] = useState([...]);
  const [loads, setLoads] = useState([]);
  const [results, setResults] = useState(null);
  const [activeMode, setActiveMode] = useState("pin");
  const [magnitude, setMagnitude] = useState(10);
  const [isCalc, setIsCalc] = useState(false);
  const [error, setError] = useState(null);
  const [calcMs, setCalcMs] = useState(null);

  // Load form state
  const [loadType, setLoadType] = useState("point");
  const [loadX, setLoadX] = useState(5);
  const [loadP, setLoadP] = useState(10);
  const [loadM, setLoadM] = useState(10);
  const [loadX1, setLoadX1] = useState(0);
  const [loadX2, setLoadX2] = useState(5);
  const [loadW, setLoadW] = useState(5);
  const [loadW2, setLoadW2] = useState(0);

  const API_BASE = "http://localhost:8000";

  useEffect(() => {
    setSupports(prev => prev.map(s => ({ ...s, x: Math.min(s.x, L) })));
  }, [L]);

  const handleSupportAdd = useCallback((x, type) => { ... }, [L]);
  const handleLoadAdd = useCallback(load => { ... }, []);
  const handleRemoveAt = useCallback(x => { ... }, [L]);
  const handleAddLoadFromForm = () => { ... };
  const handleCalculate = async () => { ... };
  const handlePrint = () => { ... };
  const canvasOnClick = (e) => { ... };

  return (
    <div style={{ ... }}>
      {/* BAŞLIK (changed) */}
      <div style={{ textAlign:"center", marginBottom:18 }}>
        <h1>YAPI STATİĞİ HESAPLAYICI</h1>
      </div>
      
      {/* PROJECT PANEL REMOVED */}
      
      {/* ... BeamTab content */}
    </div>
  );
}

/* ─── KAFES SEKME ─── */
function TrussTab() {
  // NEW: Complete truss analysis component (~300+ lines)
  const [nodes, setNodes] = useState([...]);
  const [members, setMembers] = useState([...]);
  const [supports, setSupports] = useState([...]);
  const [loads, setLoads] = useState([...]);
  const [mode, setMode] = useState("addNode");
  const [supportType, setSupportType] = useState("pin");
  const [loadFx, setLoadFx] = useState(0);
  const [loadFy, setLoadFy] = useState(0);
  const [firstNode, setFirstNode] = useState(null);
  const [memberEA, setMemberEA] = useState(10000);
  const [canvasW, setCanvasW] = useState(40);
  const [canvasH, setCanvasH] = useState(30);
  const [trussResults, setTrussResults] = useState(null);
  const [trusError, setTrussError] = useState(null);
  const [trusCalcMs, setTrussCalcMs] = useState(null);

  const API_BASE = "http://localhost:8000";

  const onNodeAdd = useCallback((...) => { ... }, [canvasW, canvasH]);
  const onMemberAdd = useCallback((...) => { ... }, []);
  const onSupportAdd = useCallback((...) => { ... }, []);
  const onLoadAdd = useCallback((...) => { ... }, []);
  const onDelete = useCallback((...) => { ... }, []);
  
  const handleTrussCalculate = async () => { ... };

  return (
    <div>
      {/* BAŞLIK */}
      {/* AYARLAR */}
      {/* ARAÇ ÇUBUĞU */}
      {/* CANVAS */}
      <TrussCanvas {...props} />
      {/* ELEMAN LİSTELERİ */}
      {/* HESAPLAMA DÜĞMESI */}
      {/* SONUÇLAR */}
    </div>
  );
}

/* ─── UYGULAMA KÖKU ─── */
function App() {
  const [tab, setTab] = useState("beam");

  return (
    <div style={{ ... }}>
      {/* BAŞLIK (Updated) */}
      <div style={{ textAlign:"center", marginBottom:18 }}>
        <div>YAPI MÜHENDİSLİĞİ · YAPAY STATİK</div>
        <h1>YAPI STATİĞİ HESAPLAYICI</h1>
        <div>KİRİŞ (Euler–Bernoulli FEM) · KAFES (Direct Stiffness Method)</div>
      </div>

      {/* SEKMELER (NEW) */}
      <div style={{ display:"flex", gap:0, marginBottom:16, borderBottom:"1px solid #0f2540" }}>
        {[["beam","🔧 KİRİŞ"],["truss","🔩 KAFES SİSTEMİ"]].map(([id, label]) => (
          <button key={id} onClick={() => setTab(id)} style={{
            border:"none", borderBottom: tab===id ? "2px solid #38bdf8" : "2px solid transparent",
            padding:"10px 24px", background:"transparent",
            color: tab===id ? "#38bdf8" : "#2a4a6a",
            fontFamily:"'Courier New',monospace", fontSize:12, fontWeight: tab===id?700:400,
            cursor:"pointer", letterSpacing:1, marginBottom:"-1px"
          }}>{label}</button>
        ))}
      </div>

      {tab === "beam"  && <BeamTab/>}
      {tab === "truss" && <TrussTab/>}

      <div style={{ textAlign:"center", color:"#0a1a2e", fontSize:8, paddingBottom:16 }}>
        EULER–BERNOULLI FEM · DIRECT STIFFNESS METHOD · GAUSS ELİMİNASYON
      </div>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App/>);
```

---

## HUNK SUMMARY TABLE

| Hunk # | Old Range | New Range | Lines Added | Lines Removed | Change Description |
|--------|-----------|-----------|-------------|---------------|-------------------|
| 1 | ~388-391 | — | 0 | 1 | Remove `{/* Cetvel */}` comment |
| 2 | ~401-404 | — | 0 | 1 | Remove `{/* Hover çizgisi */}` comment |
| 3 | ~410-421 | — | 0 | 4 | Remove 4 JSX comments (Kiriş, Yükler, etc.) |
| 4 | 650-977 | 675-1440 | 765 | 327 | **MAJOR REFACTOR**: Split monolithic App() into BeamTab(), TrussTab(), App() wrapper |

---

## DETAILED CHANGE ANALYSIS

### HUNK 4 BREAKDOWN (The Major Refactor)

**What was removed from index.html (lines 650-977):**
1. Direct App component definition
2. Project panel state and UI (setProjPanel, projPanel, projects, etc.)
3. Project management handlers (handleSaveProject, handleLoadProject, etc.)
4. All beam-specific state as direct App state
5. BeamEditor, Trus Canvas, DiagramPlot components inline
6. Single unified results section

**What was added to index_new.html (lines 675-1440):**
1. `BeamTab()` function - Extracts all beam logic from App (lines 676-1390)
2. `TrussTab()` function - **NEW** complete truss analysis (lines 1091-1390 overlap range)
3. `App()` wrapper function - Simple tab switcher (lines 1402-1440)
4. Two separate result sections (one per tab)
5. Tabbed UI with active border styling
6. Updated title to reflect dual-capability tool

**Old state variables (now in BeamTab):**
```javascript
const [L, setL]
const [supports, setSupports]
const [loads, setLoads]
const [results, setResults]
const [activeMode, setActiveMode]
const [magnitude, setMagnitude]
const [isCalc, setIsCalc]
const [error, setError]
const [calcMs, setCalcMs]
const [projPanel, setProjPanel]           // REMOVED
const [projName, setProjName]             // REMOVED
const [projects, setProjects]             // REMOVED
```

**New state in TrussTab:**
```javascript
const [nodes, setNodes]
const [members, setMembers]
const [supports, setSupports]
const [loads, setLoads]
const [mode, setMode]
const [supportType, setSupportType]
const [loadFx, setLoadFx]
const [loadFy, setLoadFy]
const [firstNode, setFirstNode]
const [memberEA, setMemberEA]
const [canvasW, setCanvasW]
const [canvasH, setCanvasH]
const [trussResults, setTrussResults]
const [trusError, setTrussError]
const [trusCalcMs, setTrussCalcMs]
```

**New state in App:**
```javascript
const [tab, setTab]  // Simple tab selector
```

---

## CODE METRICS

| Metric | index.html | index_new.html | Change |
|--------|-----------|----------------|--------|
| **Total Lines** | 979 | 1446 | +467 (47.7%) |
| **Components** | 7 | 9 | +2 |
| **useState hooks** | ~10 | ~24 | +14 |
| **useCallback hooks** | ~3 | ~8 | +5 |
| **useEffect blocks** | ~2 | ~3 | +1 |
| **API endpoints** | 1 | 2 | +1 |
| **Comments removed** | — | — | 5 comment lines |

---

## FUNCTIONAL CHANGES

### NEW Features in index_new.html:
1. **Truss Analysis** - Direct Stiffness Method solver for trusses/frames
2. **Tabbed Interface** - User can switch between beam and truss analysis
3. **Dual Canvas Support** - Separate visualization for beam vs truss
4. **Enhanced Load Types** - Separate Fx/Fy for truss vs point/UDL for beam
5. **Support Types Expansion** - Roller support variations (horizontal/vertical)
6. **Grid Snap** - Node placement with intelligent grid snapping

### REMOVED Features in index_new.html:
1. **Project Management** - No local storage of designs
2. **Comments** - Cleaned up JSX comments
3. **Monolithic Design** - Code is now modular

### UNCHANGED:
1. Beam calculation logic (Euler-Bernoulli FEM)
2. Gauss elimination solver
3. Diagram visualization
4. Button and card styling
5. CSS framework

