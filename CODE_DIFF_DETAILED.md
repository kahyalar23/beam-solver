# DETAILED CODE DIFF: Key Changes

## Change 1: Title/Header Update

### OLD (index.html, lines 706-712)
```jsx
<div style={{ fontSize:8, letterSpacing:7, color:"#1a3050", marginBottom:4 }}>YAPI MÜHENDİSLİĞİ</div>
<h1 style={{ fontSize:30, fontWeight:800, margin:0, letterSpacing:3, color:"#38bdf8" }}>
  KİRİŞ HESAPLAYICI
</h1>
<div style={{ color:"#1e3a5f", fontSize:9, marginTop:5, letterSpacing:4 }}>
  EULER–BERNOULLI · FEM ÇÖZÜCÜ · M / V / N DİYAGRAMLARI
</div>
```

### NEW (index_new.html, lines 1410-1416)
```jsx
<div style={{ fontSize:8, letterSpacing:7, color:"#1a3050", marginBottom:4 }}>YAPI MÜHENDİSLİĞİ · YAPAY STATİK</div>
<h1 style={{ fontSize:28, fontWeight:800, margin:0, letterSpacing:3, color:"#38bdf8" }}>
  YAPI STATİĞİ HESAPLAYICI
</h1>
<div style={{ color:"#1e3a5f", fontSize:9, marginTop:4, letterSpacing:4 }}>
  KİRİŞ (Euler–Bernoulli FEM) · KAFES (Direct Stiffness Method)
</div>
```

**Key differences:**
- Title changed from "KİRİŞ HESAPLAYICI" → "YAPI STATİĞİ HESAPLAYICI"
- Subtitle now mentions both beam and truss methods
- Font size reduced: 30 → 28 px
- Margin adjusted: marginTop 5 → 4

---

## Change 2: Addition of Tabbed Interface

### OLD (index.html)
```jsx
// No tabs - direct beam UI rendering
return (
  <div style={{ ... }}>
    {/* BAŞLIK */}
    <div>...</div>
    
    {/* PROJE PANELİ */}
    {projPanel && ( ... )}
    
    // Direct beam content here
  </div>
);
```

### NEW (index_new.html, lines 1419-1433)
```jsx
// NEW TAB NAVIGATION COMPONENT
<div style={{ display:"flex", gap:0, marginBottom:16, borderBottom:"1px solid #0f2540" }}>
  {[["beam","🔧 KİRİŞ"],["truss","🔩 KAFES SİSTEMİ"]].map(([id, label]) => (
    <button key={id} onClick={() => setTab(id)} style={{
      border:"none", 
      borderBottom: tab===id ? "2px solid #38bdf8" : "2px solid transparent",
      padding:"10px 24px", 
      background:"transparent",
      color: tab===id ? "#38bdf8" : "#2a4a6a",
      fontFamily:"'Courier New',monospace", 
      fontSize:12, 
      fontWeight: tab===id?700:400,
      cursor:"pointer", 
      letterSpacing:1, 
      marginBottom:"-1px"
    }}>{label}</button>
  ))}
</div>

{tab === "beam"  && <BeamTab/>}
{tab === "truss" && <TrussTab/>}
```

**Key features:**
- Flexbox layout with gap:0 (no gap between tabs)
- Bottom border indicates active tab (2px solid #38bdf8)
- Active: blue text + bold font
- Inactive: muted color + regular font weight
- Negative marginBottom (-1px) to align with container border
- Two tabs: "🔧 KİRİŞ" (Beam) and "🔩 KAFES SİSTEMİ" (Truss)

---

## Change 3: Component Structure - From Monolith to Modular

### OLD (index.html, line 701 onward)
```jsx
// All state in one place
const [L, setL] = useState(10);
const [supports, setSupports] = useState([...]);
const [loads, setLoads] = useState([]);
const [results, setResults] = useState(null);
const [activeMode, setActiveMode] = useState("pin");
const [magnitude, setMagnitude] = useState(10);
const [isCalc, setIsCalc] = useState(false);
const [error, setError] = useState(null);
const [calcMs, setCalcMs] = useState(null);
const [projPanel, setProjPanel] = useState(false);
const [projName, setProjName] = useState("");
const [projects, setProjects] = useState(JSON.parse(localStorage.getItem("beam_projects") || "[]"));

return (
  <div style={{ minHeight:"100vh", background:"#020810", padding:"20px 24px", maxWidth:920, margin:"0 auto" }}>
    {/* BAŞLIK with project panel button */}
    <div style={{ textAlign:"center", marginBottom:22 }}>
      <h1>KİRİŞ HESAPLAYICI</h1>
      <button onClick={() => setProjPanel(p=>!p)}>💾 Projeler</button>
    </div>
    
    {/* PROJE PANELİ */}
    {projPanel && (
      <div style={{ ...S.card, border:"1px solid #1e3a5f", marginBottom:12 }}>
        <div>💾 PROJE KAYDET / YÜKLE</div>
        {/* Project UI here */}
      </div>
    )}
    
    {/* ARAÇ ÇUBUĞU - MODE SELECTION */}
    <div style={S.card}>
      <div>ARAÇLAR</div>
      <div>{["pin", "roller", "fixed", "point", "moment", "delete"].map(id => (
        <ModeBtn key={id} id={id}/>
      ))}</div>
    </div>
    
    {/* BEAM EDITOR CANVAS */}
    <BeamEditor L={L} supports={supports} loads={loads} ... />
    
    {/* All beam results inline */}
    {results && (
      <div>
        {/* Reactions table */}
        {/* Diagrams */}
        {/* PDF button */}
      </div>
    )}
  </div>
);
```

### NEW (index_new.html)

#### BeamTab() - Lines 676-1390
```jsx
/* ─── KİRİŞ SEKME ─── */
function BeamTab() {
  // Beam-specific state
  const [L, setL] = useState(10);
  const [supports, setSupports] = useState([...]);
  const [loads, setLoads] = useState([]);
  const [results, setResults] = useState(null);
  const [activeMode, setActiveMode] = useState("pin");
  const [magnitude, setMagnitude] = useState(10);
  const [isCalc, setIsCalc] = useState(false);
  const [error, setError] = useState(null);
  const [calcMs, setCalcMs] = useState(null);
  
  // Load form state (NEW)
  const [loadType, setLoadType] = useState("point");
  const [loadX, setLoadX] = useState(5);
  const [loadP, setLoadP] = useState(10);
  const [loadM, setLoadM] = useState(10);
  const [loadX1, setLoadX1] = useState(0);
  const [loadX2, setLoadX2] = useState(5);
  const [loadW, setLoadW] = useState(5);
  const [loadW2, setLoadW2] = useState(0);
  
  const API_BASE = "http://localhost:8000";
  
  // Handlers
  const handleSupportAdd = useCallback((x, type) => { ... }, [L]);
  const handleLoadAdd = useCallback(load => { ... }, []);
  const handleRemoveAt = useCallback(x => { ... }, [L]);
  const handleAddLoadFromForm = () => { ... };
  const handleCalculate = async () => {
    const res = await fetch(`${API_BASE}/api/calculate`, {
      method: "POST",
      body: JSON.stringify({ L, supports, loads })
    });
    // ...
  };
  
  return (
    <div style={{ minHeight:"100vh", background:"#020810", padding:"20px 24px", maxWidth:940, margin:"0 auto" }}>
      {/* Beam-only UI */}
    </div>
  );
}
```

#### TrussTab() - Lines 1091-1390 (NEW COMPONENT)
```jsx
/* ─── KAFES SEKME ─── */
function TrussTab() {
  // Truss-specific state
  const [nodes, setNodes] = useState([
    { id:"A", x:0, y:0 }, { id:"B", x:10, y:0 }, { id:"C", x:5, y:5 }
  ]);
  const [members, setMembers] = useState([
    { id:"m1", n1:"A", n2:"B", EA:10000 },
    { id:"m2", n1:"B", n2:"C", EA:10000 },
    { id:"m3", n1:"A", n2:"C", EA:10000 }
  ]);
  const [supports, setSupports] = useState([
    { node_id:"A", type:"pin" }, { node_id:"B", type:"roller_h" }
  ]);
  const [loads, setLoads] = useState([]);
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
  const [trusCalcMs, setTrusCalcMs] = useState(null);
  
  const API_BASE = "http://localhost:8000";
  
  // Truss-specific handlers
  const onNodeAdd = useCallback((...) => { ... }, [canvasW, canvasH]);
  const onMemberAdd = useCallback((...) => { ... }, []);
  const onSupportAdd = useCallback((...) => { ... }, []);
  const onLoadAdd = useCallback((...) => { ... }, []);
  const onDelete = useCallback((...) => { ... }, []);
  
  const handleTrussCalculate = async () => {
    const res = await fetch(`${API_BASE}/api/calculate/truss`, {
      method: "POST",
      body: JSON.stringify({ nodes, members, supports, loads })
    });
    // ...
  };
  
  return (
    <div>
      {/* Truss-only UI */}
      <TrussCanvas nodes={nodes} members={members} ... />
      {trussResults && (/* Results */)}
    </div>
  );
}
```

#### App() - Lines 1402-1440 (NEW WRAPPER)
```jsx
function App() {
  const [tab, setTab] = useState("beam");
  
  return (
    <div style={{ minHeight:"100vh", background:"#020810", padding:"20px 24px", maxWidth:940, margin:"0 auto" }}>
      {/* Shared header */}
      <div style={{ textAlign:"center", marginBottom:18 }}>
        <h1>YAPI STATİĞİ HESAPLAYICI</h1>
      </div>
      
      {/* Tab switcher */}
      <div style={{ display:"flex", gap:0, marginBottom:16, borderBottom:"1px solid #0f2540" }}>
        {/* Tab buttons */}
      </div>
      
      {/* Conditional rendering */}
      {tab === "beam"  && <BeamTab/>}
      {tab === "truss" && <TrussTab/>}
      
      {/* Shared footer */}
      <div style={{ textAlign:"center", color:"#0a1a2e", fontSize:8 }}>
        EULER–BERNOULLI FEM · DIRECT STIFFNESS METHOD · GAUSS ELİMİNASYON
      </div>
    </div>
  );
}
```

---

## Change 4: Removed Project Management

### OLD (index.html, lines 720-750+)
```jsx
{/* PROJE PANELİ */}
{projPanel && (
  <div style={{ ...S.card, border:"1px solid #1e3a5f", marginBottom:12 }}>
    <div style={{ color:"#38bdf8", fontSize:9, letterSpacing:2, marginBottom:10 }}>💾 PROJE KAYDET / YÜKLE</div>
    <div style={{ display:"flex", gap:8, marginBottom:12, alignItems:"center" }}>
      <input value={projName} onChange={e=>setProjName(e.target.value)}
        placeholder="Proje adı..."
        style={{ ...S.inp, flex:1, width:"auto" }}/>
      <button onClick={handleSaveProject}>Kaydet</button>
    </div>
    {projects.length === 0
      ? <div>Henüz kayıtlı proje yok</div>
      : projects.map(p => (
        <div key={p.id}>
          <span>{p.name}</span>
          <button onClick={() => handleLoadProject(p.id)}>Yükle</button>
          <button onClick={() => handleDeleteProject(p.id)}>✕</button>
        </div>
      ))}
  </div>
)}
```

### NEW (index_new.html)
```jsx
// PROJECT PANEL COMPLETELY REMOVED
// No projPanel state
// No projects state
// No handleSaveProject/handleLoadProject/handleDeleteProject methods
// No "💾 Projeler" button
```

**Reason:** Project management moved to backend/separate feature

---

## Change 5: API Endpoint Changes

### OLD (index.html)
```javascript
// No explicit API_BASE defined
// Assumed local/inline computation
// Results calculated with computeBeam() function

const results = computeBeam(L, supports, loads);
setResults(results);
```

### NEW (index_new.html)

#### Beam API
```javascript
const API_BASE = "http://localhost:8000";

const handleCalculate = async () => {
  if (supports.length === 0) { setError("En az bir mesnet ekleyin"); return; }
  if (loads.length === 0)    { setError("En az bir yük ekleyin");   return; }
  setError(null); 
  setIsCalc(true);
  try {
    const t0 = performance.now();
    const res = await fetch(`${API_BASE}/api/calculate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ L, supports, loads })
    });
    const data = await res.json();
    setResults(data);
    setCalcMs(Math.round(performance.now() - t0));
  } catch (err) {
    setError(String(err));
  } finally {
    setIsCalc(false);
  }
};
```

#### Truss API (NEW)
```javascript
const handleTrussCalculate = async () => {
  if (nodes.length < 2) { setTrussError("En az 2 düğüm gerekli"); return; }
  if (members.length === 0) { setTrussError("En az 1 çubuk gerekli"); return; }
  if (supports.length === 0) { setTrussError("En az 1 mesnet gerekli"); return; }
  
  setTrussError(null);
  setIsCalc(true);
  try {
    const t0 = performance.now();
    const res = await fetch(`${API_BASE}/api/calculate/truss`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nodes, members, supports, loads })
    });
    const data = await res.json();
    setTrussResults(data);
    setTrusCalcMs(Math.round(performance.now() - t0));
  } catch (err) {
    setTrussError(String(err));
  } finally {
    setIsCalc(false);
  }
};
```

---

## Change 6: Footer Text Update

### OLD (index.html, line 969)
```javascript
<div style={{ textAlign:"center", color:"#0a1a2e", fontSize:8, letterSpacing:3, paddingBottom:16 }}>
  EULER–BERNOULLI · FEM 100 ELEMAN · GAUSS ELİMİNASYON · DENGE YÖNTEMİ (M,V)
</div>
```

### NEW (index_new.html, line 1435-1436)
```javascript
<div style={{ textAlign:"center", color:"#0a1a2e", fontSize:8, letterSpacing:3, paddingBottom:16, marginTop:8 }}>
  EULER–BERNOULLI FEM · DIRECT STIFFNESS METHOD · GAUSS ELİMİNASYON
</div>
```

**Changes:**
- Removed: "100 ELEMAN"
- Removed: "DENGE YÖNTEMİ (M,V)"
- Added: "DIRECT STIFFNESS METHOD"
- Added: marginTop:8
- Same letterSpacing, color, fontSize

---

## Summary of Changes

| Aspect | Old | New | Impact |
|--------|-----|-----|--------|
| **Main Component** | Single `App()` | `App()` + `BeamTab()` + `TrussTab()` | Better code organization |
| **State Management** | All in App | Split per tab | Cleaner, isolated state |
| **Features** | Beam only | Beam + Truss | Expanded functionality |
| **Project Management** | Yes (localStorage) | No | Simplified backend workflow |
| **API Integration** | Assumed local | Explicit remote | Scalable architecture |
| **Styling** | 920px width | 940px width | Slightly wider layout |
| **Comments** | 5 JSX comments | Cleaned | Better code clarity |

