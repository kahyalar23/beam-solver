# Unified Diff: index.html vs index_new.html

## File Statistics
- **index.html** (original):     979 lines, ~45 KB
- **index_new.html** (new):    1446 lines, ~69 KB
- **Net change**: +467 lines (+47.7%)

## MAJOR STRUCTURAL CHANGES

### 1. ARCHITECTURE REFACTOR
The original monolithic App() component has been split into TWO main components with a tabbed interface:

**OLD STRUCTURE (index.html):**
- Single `App()` component handling beam calculations only
- Direct state management within App()
- Project save/load functionality integrated

**NEW STRUCTURE (index_new.html):**
- `BeamTab()` - Beam analysis component (formerly the main App)
- `TrussTab()` - NEW: Truss/frame analysis component  
- `App()` - NEW: Wrapper component with tabbed interface
- Each tab is independently managed

### 2. REMOVED COMMENTS (Early in file ~lines 388-421)
Several JSX/React comment markers removed from index.html:
- `{/* Cetvel */}` (line ~391)
- `{/* Hover çizgisi */}` (line ~404)  
- `{/* Kiriş gölgesi */}`
- `{/* Kiriş */}`
- `{/* Yükler */}`
- `{/* Mesnetter */}`

### 3. COMPONENT EXTRACTION (LINES 675-1439 NEW FILE)

#### BeamTab() Function (index_new.html lines 675-1390)
Extracted from the original App() function:
- Handles all beam analysis logic
- State hooks: L, supports, loads, results, activeMode, magnitude, etc.
- Load form state: loadType, loadX, loadP, loadM, loadX1, loadX2, loadW, loadW2
- API_BASE set to "http://localhost:8000"
- Methods:
  - `handleSupportAdd()` - Add/modify supports
  - `handleLoadAdd()` - Add loads
  - `handleRemoveAt()` - Remove supports/loads
  - `handleAddLoadFromForm()` - Validate and add loads from form
  - `handleCalculate()` - Fetch calculation from API
  - `handlePrint()` - Print/PDF export
  - `canvasOnClick()` - Canvas interaction for beam editor

#### TrussTab() Function (index_new.html lines 1091-1390) 
**COMPLETELY NEW**: Adds truss/frame structure analysis capability
- State for: nodes, members, supports, loads, mode, supportType, etc.
- Canvas interaction for drawing trusses
- Member EA (stiffness) management
- Support types: pin, roller_h, roller_v
- Load management (Fx, Fy components)
- Methods for adding nodes, members, supports, loads
- TrussCanvas component for visualization
- Results display for internal forces

### 4. UI CHANGES

#### Header Title Changes
**OLD (lines 707-711):**
```
YAPI MÜHENDİSLİĞİ
KİRİŞ HESAPLAYICI
EULER–BERNOULLI · FEM ÇÖZÜCÜ · M / V / N DİYAGRAMLARI
```

**NEW (lines 1410-1416):**
```
YAPI MÜHENDİSLİĞİ · YAPAY STATİK
YAPI STATİĞİ HESAPLAYICI
KİRİŞ (Euler–Bernoulli FEM) · KAFES (Direct Stiffness Method)
```

#### Tab Navigation (NEW - lines 1419-1430)
Added tabbed interface with two buttons:
- "🔧 KİRİŞ" (Beam) - Active when tab === "beam"
- "🔩 KAFES SİSTEMİ" (Truss System) - Active when tab === "truss"
- Styled with bottom border indicating active tab

#### Removed Project Management
- Project panel functionality (`{/* PROJE PANELİ */}` section around line 720) appears to be **removed** in new version
- No project save/load UI in new BeamTab

### 5. NEW CANVAS INTERACTIONS

#### BeamEditor Enhancements
- BeamEditor component now handles clicking on the canvas  
- Support for hovering ruler
- Beam shadow visualization
- Improved visual feedback

#### NEW TrussCanvas Component
- Drawing interface for truss structures
- Node creation with grid snap (0.5m, 1m, or 2m)
- Member connection UI
- Support placement and configuration
- Load application (separate Fx/Fy)
- Interactive force/displacement visualization

### 6. API INTEGRATION

Both tabs now use API calls to `http://localhost:8000/api/calculate`:

**Beam:**
```javascript
POST /api/calculate
Body: { L, supports, loads }
Returns: { reactions, Ms, Vs, Ns, maxM, maxV }
```

**Truss:**
```javascript
POST /api/calculate/truss
Body: { nodes, members, supports, loads }
Returns: { displacements, internal_forces, support_reactions }
```

### 7. SHARED COMPONENTS (NO CHANGE)
- `Btn()` component - Button styling
- `DiagramPlot()` component - Chart rendering
- `BeamEditor()` component - Beam visualization
- `TrussCanvas()` component - **NEW for truss**
- Gauss elimination solver (`gaussSolve()`)
- Beam computation (`computeBeam()`)
- Modal calculation function (`getW()`)

### 8. STYLING CHANGES
- Container maxWidth: 920px → 940px
- Margins and spacing adjusted for tabbed interface
- New tab styling with border-bottom active state
- Overall layout more flexible for dual-tab support

### 9. FOOTER TEXT

**OLD (line 969):**
```
EULER–BERNOULLI · FEM 100 ELEMAN · GAUSS ELİMİNASYON · DENGE YÖNTEMİ (M,V)
```

**NEW (line 1436):**
```
EULER–BERNOULLI FEM · DIRECT STIFFNESS METHOD · GAUSS ELİMİNASYON
```

## SUMMARY OF CHANGES

| Category | Change |
|----------|--------|
| **Architecture** | Monolithic → Tabbed/Modular |
| **Components** | 7 → 9 (added BeamTab, TrussTab, App wrapper) |
| **Features** | Beam only → Beam + Truss analysis |
| **Lines** | 979 → 1446 (+467 lines) |
| **New Functionality** | Truss structure analysis (Direct Stiffness Method) |
| **Removed Features** | Project save/load panel |
| **API Calls** | 1 endpoint → 2 endpoints |
| **State Management** | Centralized → Split across tabs |

## KEY ADDITIONS IN NEW VERSION

1. ✅ Tabbed interface for multiple analysis types
2. ✅ Truss/Frame structure analysis (NEW)
3. ✅ Separate UX for different problem types
4. ✅ More modular component structure
5. ✅ Support for 2D frame analysis
6. ✅ Dual-endpoint API communication

## REMOVED IN NEW VERSION

1. ❌ Project save/load functionality
2. ❌ Several comment markers from JSX
3. ❌ Monolithic single-purpose architecture

