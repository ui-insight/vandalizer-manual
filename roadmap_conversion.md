# Roadmap Dashboard Migration: JavaScript → Python + Quarto

## Project Goal
Migrate existing JavaScript-based roadmap dashboard to Python + Quarto for better maintainability, version control, and data processing capabilities.

## Current State
- Interactive dashboard with timeline plots, pie charts, and weekly activity charts
- JavaScript code that processes JSON issue data client-side
- Plotly.js for visualizations with click events and modal interactions
- Custom functionality: priority extraction, cumulative calculations, date extensions to current date

## Target Architecture

**Language Choice:** Python (chosen over R)
- Pandas for data processing (similar to current JS logic)
- Plotly Python for interactive charts
- Quarto for document structure and rendering

**Project Structure:**
**Option A: Simple (Direct JSON)**
```
roadmap-analysis/
├── data/issues.json
├── src/plotting_functions.py  
├── roadmap_dashboard.qmd
└── _quarto.yml
```

**Option B: Intermediate (CSV Cache)**
```
roadmap-analysis/
├── data/
│   ├── raw/issues.json
│   └── processed/issues_processed.csv
├── src/data_processing.py
├── roadmap_dashboard.qmd
└── _quarto.yml
```

**Option C: Advanced (Parquet Pipeline)**
```
roadmap-analysis/
├── data/
│   ├── raw/issues.json
│   └── processed/issues_processed.parquet
├── src/
│   ├── data_processing.py
│   └── plotting_functions.py
├── roadmap_dashboard.qmd
└── _quarto.yml
```

## Migration Plan

**Phase 1:** Direct JSON Processing
- Load JSON directly with pandas (`pd.DataFrame(json.load())`)
- Convert JS date operations to pandas datetime
- Implement priority extraction and timeline extension
- Keep processing logic in Quarto document initially

**Phase 2:** Chart Recreation  
- Timeline chart (cumulative issues over time)
- Open issues trend with weekly impulse chart
- Priority and label pie charts
- Maintain click events and hover text

**Phase 3:** Quarto Integration
- Document structure and styling
- Interactive parameters/toggles
- HTML widgets for complex interactions

**Phase 4:** Enhanced Features
- Better data pipeline
- Automated updates
- Additional analytics

## Key Considerations
- **Interactivity:** Most current features translatable to Plotly Python
- **Custom modals:** May need different UX approach  
- **Performance:** Direct JSON processing (similar to current approach)
- **Deployment:** Static HTML output maintained
- **Simplicity:** No intermediate data files to manage

## Next Steps
1. Start with timeline chart migration as proof of concept
2. Set up basic Quarto document structure
3. Convert data processing functions
4. Recreate chart functionality piece by piece

## Progress

### ✅ Completed
**Phase 1 - Core Migration (In Progress)**
- [x] Set up Python + Quarto document structure
- [x] Converted JSON loading from JavaScript to pandas
- [x] Implemented timeline chart with current date extension
- [x] Created open issues trend chart
- [x] Built basic pie chart for labels
- [x] Preserved original layout and styling (logos, headers)
- [x] Added summary statistics display
- [x] Fixed timezone and date comparison issues

### 🔄 In Testing
- roadmap2.qmd created with basic functionality
- **Bug Fixes Applied**: Handle missing `closed_at` field, timezone issues, date comparisons
- Core charts rendering with Python/Plotly instead of JavaScript

### 📁 Next: Function Organization
**Recommended Structure:**
```
roadmap-analysis/
├── data/issues.json
├── src/
│   ├── __init__.py
│   ├── data_processing.py       # Data loading, processing functions
│   ├── plotting_functions.py    # Chart creation functions  
│   └── utils.py                 # Helper functions (HTML generation, etc.)
├── roadmap2.qmd
└── _quarto.yml
```

**Benefits:**
- Clean separation of concerns
- Reusable functions across notebooks
- Easier testing and maintenance
- Better version control

### ⏳ Next Steps
**Phase 2 - Function Organization & Enhanced Charts**
- [ ] **Cumulative Issues Plot**: Single chart with two traces (cumulative opened + cumulative closed over time)
- [ ] Move functions to separate modules in `src/` directory
- [ ] Weekly impulse chart (bar chart showing weekly activity)
- [ ] Priority pie chart with toggle functionality
- [ ] Click events for chart drill-downs
- [ ] Interactive toggles (All Issues vs Open Issues)

**Phase 3 - Advanced Features**
- [ ] Modal-like interactions (or alternative UX)
- [ ] Filter controls
- [ ] Export functionality
- [ ] Performance optimization if needed

## Current Status
Testing Phase 1 implementation in roadmap2.qmd. Basic charts functional, ready to add remaining interactive features once core functionality is validated.
