# ADRDS IEEE Demo Track Paper - Team Collaboration Guide

## 📋 Project Overview
This is the LaTeX source for the ADRDS (Adaptive Dynamic Ransomware Detection System) demo track paper. The project is structured for **5-person team collaboration** with clear ownership and minimal conflicts.

## ✅ Setup Complete!

**All dependencies are now installed:**
- ✅ MiKTeX 24.1 (LaTeX distribution)
- ✅ VS Code LaTeX Workshop extension
- ✅ Project structure (figures/ and tables/ directories)
- ✅ Successfully compiled PDF (main.pdf)

## 🚀 Quick Start

### Compile the Document
**Option 1: Using LaTeX Workshop in VS Code**
- Open `main.tex`
- Press `Ctrl+Alt+B` to build
- PDF preview will open automatically

**Option 2: Command Line**
```powershell
cd "path\to\main-el-paper"
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

### View the PDF
- The compiled PDF is at: `main.pdf`
- Use the built-in PDF viewer in VS Code or any PDF reader

## 🎯 Ground Rules (Non-Negotiable)

1. **One main file:** `main.tex` (Manish T)
2. **One section per person:** Each team member owns their `.tex` files
3. **One references file:** `references.bib` (shared, but Manish T ensures no duplicates)
4. **Figures go in:** `/figures` folder
5. **Tables go in:** `/tables` folder
6. **Compile locally before pushing:** Ensure your section compiles without errors

## 📁 Project Structure

```
IEEE_Conference_Template/
├── main.tex                    # 👤 Manish T
├── references.bib              # Shared (all team members add citations)
├── IEEEtran.cls               # IEEE style file (DO NOT MODIFY)
├── sections/
│   ├── abstract.tex           # 👤 Manish T
│   ├── introduction.tex       # 👤 Manish H
│   ├── related_work.tex       # 👤 Manish H
│   ├── threat_model.tex       # 👤 Manish H
│   ├── system_overview.tex    # 👤 Nikhil
│   ├── taxonomy.tex           # 👤 Nikhil
│   ├── implementation.tex     # 👤 Aditya
│   ├── demo.tex               # 👤 Aditya
│   ├── experiments.tex        # 👤 Vinay
│   ├── results.tex            # 👤 Vinay
│   ├── discussion.tex         # 👤 Vinay
│   └── conclusion.tex         # 👤 Manish T
├── figures/
│   ├── architecture.pdf       # 👤 Nikhil
│   ├── gui_screenshot.png     # 👤 Aditya
│   ├── attack_timeline.pdf    # 👤 Nikhil
│   └── roc_curves.pdf         # 👤 Vinay
└── tables/
    └── (created as needed by Vinay)
```

## 👥 Team Responsibilities

### 👤 Manish T: Lead / Integrator
**Role:** Keeps narrative coherent + submission ready

**Sections:**
- Title / Authors / Affiliations (in `main.tex`)
- `sections/abstract.tex`
- `sections/conclusion.tex`
- Acknowledgments (in `main.tex`)

**Responsibilities:**
- ✅ Final proofreading & formatting
- ✅ Ensure demo-track focus throughout
- ✅ Final compile + submission PDF
- ✅ Manage `references.bib` (no duplicates)
- ✅ Keep story tight and consistent

---

### 👤 Manish H: Background & Threat Modeling
**Role:** Owns "why this matters" and safety

**Sections:**
- `sections/introduction.tex`
- `sections/related_work.tex`
- `sections/threat_model.tex`

**Key Tasks:**
- ✅ Motivation with statistics/real incidents
- ✅ Identify gap in current solutions
- ✅ Position ADRDS clearly
- ✅ Include the **killer demo paragraph** (in introduction or demo section)
- ✅ Survey 10-15 key papers

**Killer Demo Paragraph (MUST INCLUDE):**
> "During the live demo, attendees interactively control ransomware stages, observe real-time behavioral visualization, and see on-the-fly ML classification outcomes with adjustable thresholds."

---

### 👤 Nikhil: System & Taxonomy Architect
**Role:** Owns how ADRDS works conceptually

**Sections:**
- `sections/system_overview.tex`
- `sections/taxonomy.tex`

**Figures:**
- Figure 1: Architecture diagram (`figures/architecture.pdf`)
- Figure 3: Attack timeline/stage progression (`figures/attack_timeline.pdf`)

**Key Tasks:**
- ✅ Explain components: simulator, detector, visualizer
- ✅ Define L1/L2 behavioral taxonomy
- ✅ Reference `simulator_full.py`, `integrate_l1_l2.py`
- ✅ Create clear, publication-quality diagrams

---

### 👤 Aditya: Implementation & Demo Experience
**Role:** Owns what users actually see

**Sections:**
- `sections/implementation.tex`
- `sections/demo.tex`

**Figures:**
- Figure 2: GUI screenshots (`figures/gui_screenshot.png`)

**Key Tasks:**
- ✅ Describe tech stack (Python, libraries, GUI)
- ✅ Explain core modules (NO CODE DUMPS)
- ✅ Detail 2-3 interactive demo scenarios
- ✅ Reference `demo_complete.py`
- ✅ Make demo vivid and compelling

---

### 👤 Vinay: ML & Evaluation Lead
**Role:** Owns credibility via numbers

**Sections:**
- `sections/experiments.tex`
- `sections/results.tex`
- `sections/discussion.tex`

**Figures & Tables:**
- Figure 4: ROC curves (`figures/roc_curves.pdf`)
- Table 1: Dataset characteristics
- Table 2: Classification results
- Table 3: Latency/performance

**Key Tasks:**
- ✅ Dataset description with statistics
- ✅ Feature engineering details
- ✅ ML model evaluation (RF, SVM, NN)
- ✅ Present results with tables/figures
- ✅ Honest discussion of limitations
- ✅ Defend metrics and methodology


---

## 🚀 How to Compile

Install **LaTeX Workshop** extension, then click "Build LaTeX project" button.

---

## 📊 Page Budget (4-6 pages total)

| Section | Owner | Target Pages |
|---------|-------|--------------|
| Abstract | Manish T | 0.2 |
| Introduction | Manish H | 0.8-1.0 |
| Related Work | Manish H | 0.7-1.0 |
| Threat Model | Manish H | 0.3-0.5 |
| System Overview | Nikhil | 0.7-1.0 |
| Taxonomy | Nikhil | 0.8-1.0 |
| Implementation | Aditya | 0.7-1.0 |
| Demo | Aditya | 0.5-0.7 |
| Experiments | Vinay | 0.6-0.8 |
| Results | Vinay | 0.8-1.0 |
| Discussion | Vinay | 0.4-0.6 |
| Conclusion | Manish T | 0.3-0.5 |

**Total:** ~4-6 pages (figures and tables included)

---

## 📝 Writing Tips

### For Everyone:
- Write in **active voice** when possible
- Use **present tense** for describing the system
- Keep paragraphs focused (one idea per paragraph)
- Reference figures/tables properly: `Figure~\ref{fig:label}`, `Table~\ref{tab:label}`

### For Demo Track:
- Emphasize **interactivity** and **hands-on** experience
- Show **practical value** for security practitioners
- Make the demo **sound exciting and educational**
- Include **screenshots** and **visual evidence**

---

## ✅ Pre-Submission Checklist

### Manish T Final Tasks:
- [ ] All author names and affiliations correct
- [ ] Abstract has no symbols, math, or footnotes
- [ ] All sections compile without errors
- [ ] All figures and tables referenced in text
- [ ] References formatted consistently (IEEE style)
- [ ] Page limit respected (4-6 pages)
- [ ] Final PDF generated and reviewed

### Everyone:
- [ ] Your section compiles locally
- [ ] All placeholders (XXX, [TODO]) removed
- [ ] Figures/tables have proper captions
- [ ] Cross-references work correctly
- [ ] Spelling and grammar checked

---


## Continuous Integration (GitHub Actions)

A GitHub Actions workflow has been added to compile `main.tex` on pushes and pull requests to `main`. The workflow builds `main.pdf` using `latexmk` and uploads the produced PDF as a workflow artifact.

How it works (on GitHub):

```bash
# Triggered on push / pull_request to main
# Installs TeX Live packages and latexmk
latexmk -pdf -interaction=nonstopmode -file-line-error main.tex
```

Artifact: `main.pdf` is uploaded and available for download from the workflow run UI.

Note: The workflow file is at `.github/workflows/latex.yml`. If you need additional TeX packages, edit that file to install them before running `latexmk`.
