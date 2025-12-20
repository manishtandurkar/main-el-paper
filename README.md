# ADRDS IEEE Demo Track Paper - Team Collaboration Guide

## 📋 Project Overview
This is the LaTeX source for the ADRDS (Adaptive Dynamic Ransomware Detection System) demo track paper. The project is structured for **5-person team collaboration** with clear ownership and minimal conflicts.

## 🎯 Ground Rules (Non-Negotiable)

1. **One main file:** `main.tex` (Person 1 owns this - DO NOT EDIT unless you're Person 1)
2. **One section per person:** Each team member owns their `.tex` files
3. **One references file:** `references.bib` (shared, but Person 1 ensures no duplicates)
4. **Figures go in:** `/figures` folder
5. **Tables go in:** `/tables` folder
6. **Compile locally before pushing:** Ensure your section compiles without errors

## 📁 Project Structure

```
IEEE_Conference_Template/
├── main.tex                    # 👤 PERSON 1 ONLY
├── references.bib              # Shared (all team members add citations)
├── IEEEtran.cls               # IEEE style file (DO NOT MODIFY)
├── sections/
│   ├── abstract.tex           # 👤 Person 1
│   ├── introduction.tex       # 👤 Person 2
│   ├── related_work.tex       # 👤 Person 2
│   ├── threat_model.tex       # 👤 Person 2
│   ├── system_overview.tex    # 👤 Person 3
│   ├── taxonomy.tex           # 👤 Person 3
│   ├── implementation.tex     # 👤 Person 4
│   ├── demo.tex               # 👤 Person 4
│   ├── experiments.tex        # 👤 Person 5
│   ├── results.tex            # 👤 Person 5
│   ├── discussion.tex         # 👤 Person 5
│   └── conclusion.tex         # 👤 Person 1
├── figures/
│   ├── architecture.pdf       # 👤 Person 3
│   ├── gui_screenshot.png     # 👤 Person 4
│   ├── attack_timeline.pdf    # 👤 Person 3
│   └── roc_curves.pdf         # 👤 Person 5
└── tables/
    └── (created as needed by Person 5)
```

## 👥 Team Responsibilities

### 👤 Person 1: Lead / Integrator
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

### 👤 Person 2: Background & Threat Modeling
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

### 👤 Person 3: System & Taxonomy Architect
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

### 👤 Person 4: Implementation & Demo Experience
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

### 👤 Person 5: ML & Evaluation Lead
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

## 🧠 Timeline (5-Day Sprint)

### Day 1-2: Content Creation
- **Everyone:** Write rough drafts of your sections
- **Focus:** Content first, polish later
- **Goal:** All sections have substantive content (even if rough)

### Day 3: Integration
- **Person 1:** Integrates all sections into `main.tex`
- **Everyone:** Fix cross-references and flow issues
- **Goal:** Full paper compiles successfully

### Day 4: Figures & Results
- **Person 3, 4, 5:** Finalize all figures and tables
- **Person 5:** Verify all experimental numbers
- **Goal:** All visuals publication-ready

### Day 5: Polish & Submission
- **Person 1:** Final proofreading, formatting, page limit compliance (4-6 pages)
- **Everyone:** Quick review of full paper
- **Goal:** Submit camera-ready PDF

---

## 🚀 How to Compile

### Local Compilation
```bash
# Navigate to project directory
cd IEEE_Conference_Template

# Compile (run twice for references)
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

### VS Code Users
Install **LaTeX Workshop** extension, then click "Build LaTeX project" button.

### Overleaf Users
Upload the entire folder and compile `main.tex`.

---

## ⚠️ Common Mistakes to AVOID

1. ❌ **DO NOT** let everyone edit Introduction
2. ❌ **DO NOT** let multiple people tweak Abstract
3. ❌ **DO NOT** dump code listings into the paper (this is a demo paper, not a code manual)
4. ❌ **DO NOT** edit `main.tex` unless you're Person 1
5. ❌ **DO NOT** use symbols, special characters, or math in Abstract or Title

---

## 📊 Page Budget (4-6 pages total)

| Section | Owner | Target Pages |
|---------|-------|--------------|
| Abstract | Person 1 | 0.2 |
| Introduction | Person 2 | 0.8-1.0 |
| Related Work | Person 2 | 0.7-1.0 |
| Threat Model | Person 2 | 0.3-0.5 |
| System Overview | Person 3 | 0.7-1.0 |
| Taxonomy | Person 3 | 0.8-1.0 |
| Implementation | Person 4 | 0.7-1.0 |
| Demo | Person 4 | 0.5-0.7 |
| Experiments | Person 5 | 0.6-0.8 |
| Results | Person 5 | 0.8-1.0 |
| Discussion | Person 5 | 0.4-0.6 |
| Conclusion | Person 1 | 0.3-0.5 |

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

## 🔗 Cross-References Between Sections

- **Person 2:** Reference system architecture when discussing contributions (Person 3's work)
- **Person 3:** Reference demo scenarios when describing visualizer (Person 4's work)
- **Person 4:** Reference experimental results when discussing demo value (Person 5's work)
- **Person 5:** Reference taxonomy when describing features (Person 3's work)

**Coordination:** Use Slack/Teams to confirm figure numbers and section references.

---

## ✅ Pre-Submission Checklist

### Person 1 Final Tasks:
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

## 🆘 Need Help?

- **LaTeX issues:** Check IEEE template documentation
- **Merge conflicts:** Person 1 resolves
- **Content questions:** Discuss in team meeting
- **Citation format:** Use `\cite{ref1}` in text, maintain `references.bib`

---

## 🎯 Success Criteria

This paper succeeds if:
1. ✅ The demo sounds **exciting** and **valuable**
2. ✅ The system architecture is **clear**
3. ✅ The experimental results are **credible**
4. ✅ The paper tells a **coherent story**
5. ✅ It compiles **without errors**
6. ✅ It meets **page limits** (4-6 pages)

---

**Let's build an awesome demo paper! 🚀**

*Questions? Contact Person 1 (Lead Integrator)*

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
