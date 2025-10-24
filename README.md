# Vandalizer User Manual and Wiki

Welcome to the official documentation repository for Vandalizer - an AI management tool designed to assist research administrators in managing and streamlining their work.

## About This Repository

This repository contains the source code for the [Vandalizer User Manual and Wiki](https://nate-layman.github.io/vandalizer-manual/). The manual includes the following pages:

- **Introduction** - Overview of Vandalizer core concepts (tasks, steps, workflows, workspaces)
- **Interface** - User interface guide and navigation
- **Tasks** - Detailed task documentation
- **Workflows** - Process guides and workflow documentation
- **Examples** - Practical examples and use cases
- **Roadmap** - Interactive project roadmap with issue tracking and analytics
- **Disclaimer** - Legal and usage disclaimers

## Technology Stack

### Core Framework

- **Quarto**: Documentation generation framework that renders QMD files to HTML
- **Python**: Powers roadmap analytics and data processing (`src/` modules)
- **Plotly**: Interactive charting library for roadmap visualizations
- **GitHub Pages**: Hosting and deployment platform

### Build Tools

- **Pixi**: Environment and dependency management (configured in `.pixi`)
- **GitHub Actions**: Automated build, deployment, and data synchronization

## Architecture Overview

### Build Pipeline

```
Source (*.qmd files) → Quarto Render → HTML Output (docs/) → GitHub Pages Deployment
                              ↓
                      Python processes (if applicable)
                              ↓
                      Post-render: Copy data/issues.json → docs/
```

### Roadmap Feature Architecture

The roadmap page (`roadmap.qmd`) uses a hybrid Python + JavaScript approach:

1. **Python Processing** (`src/` modules):
   - `data_processing.py`: Loads and processes GitHub issues JSON
   - `plotting_functions.py`: Creates Plotly charts with pre-computed data
   - `interactive_functions.py`: Generates embedded JavaScript for interactivity
   - `utils.py`: Helper functions for HTML generation

2. **JavaScript Interactivity** (`scripts.html`):
   - Click handlers for modal popups showing issue details
   - Image enlargement toggle for documentation screenshots
   - Plotly chart interactions and custom hover templates

3. **Data Flow**:
   - GitHub Actions workflow (`update-roadmap.yml`) fetches issues daily at 6 AM UTC
   - Issues stored in `data/issues.json`
   - Post-render step copies data to `docs/issues.json` for web access
   - JavaScript dynamically loads and visualizes the data

### CSS & Styling

- `styles.css`: Global styling for navigation, charts, and responsive layouts
- Uses Quarto's sandstone theme as base
- Customizations for:
  - Sidebar navigation (larger fonts, better spacing)
  - Image popups with enlargement feature
  - Issue cards and charts
  - Mobile responsiveness

## Repository Structure

```
vandalizer-manual/
├── .github/
│   └── workflows/
│       ├── build-deploy.yaml          # Quarto build → GitHub Pages deploy
│       └── update-roadmap.yml         # Daily issue data sync (6 AM UTC)
├── src/                               # Python modules for roadmap
│   ├── __init__.py
│   ├── data_processing.py            # Load/process GitHub issues
│   ├── plotting_functions.py          # Generate Plotly charts
│   ├── interactive_functions.py       # Generate interactive JavaScript
│   └── utils.py                       # Helper functions
├── data/                              # Data storage
│   └── issues.json                   # GitHub issues (auto-updated daily)
├── images/                            # Logo and screenshot assets
├── docs/                              # Generated HTML output (auto-generated)
├── _extensions/                       # Quarto extensions
├── .pixi/                             # Pixi environment cache
├── _quarto.yml                        # Quarto project configuration
├── scripts.html                       # Embedded JavaScript for roadmap interactivity
├── styles.css                         # Custom CSS styling
├── *.qmd                              # Quarto markdown source files
├── CONTRIBUTING.md                    # Contribution guidelines
└── README.md                          # This file
```

## Key Features

### Interactive Roadmap Dashboard

The roadmap page includes several interactive visualizations:

- **Cumulative Issues Chart**: Timeline of total opened vs closed issues
- **Open Issues Trend**: Running count of currently open issues (click to view details)
- **Weekly Activity**: Bar chart of issues opened/closed per week
- **Issues by Priority**: Pie chart with toggle for open/all issues
- **Issues by Label**: Pie chart with toggle for open/all issues

**Interactivity**:
- Click chart elements to view detailed issue lists
- Toggle between "Open Issues Only" and "All Issues"
- Issues grouped by priority level (High → Medium → Low → No Priority)
- Modal popups show full issue details

### Image Enlargement Feature

All documentation screenshots include a click-to-enlarge feature:
- Click any image to view it fullscreen
- Click again to restore to original size
- Implemented via JavaScript in `scripts.html`

## Development & Deployment

### Automated Workflows

#### 1. Build and Deploy (`build-deploy.yaml`)

Triggers on:
- Push to `main` branch
- Manual workflow dispatch
- Completion of "Update Roadmap" workflow

Process:
1. Checkout repository
2. Setup Pixi environment
3. Run `pixi run quarto render`
4. Upload built HTML to artifact
5. Deploy to GitHub Pages

**Deployment URL**: https://nate-layman.github.io/vandalizer-manual/

#### 2. Update Roadmap (`update-roadmap.yml`)

Runs daily at **6 AM UTC** (manually triggerable)

Process:
1. Fetch issues from `ui-insight/vandalizer` repository
2. Filter out pull requests (issues only)
3. Extract issue metadata: ID, title, URL, state, created_at, updated_at, labels, assignees
4. Save to `data/issues.json`
5. Commit and push changes (if any)
6. Triggers build-deploy workflow

**Requirements**:
- GitHub token with access to `ui-insight/vandalizer` repository
- Token stored as repository secret: `VANDALIZER_ISSUES_TOKEN`
- Token must have `public_repo` scope

### Dependencies

View in `pixi.toml` (Pixi project configuration):
- Python 3.13
- Quarto
- Plotly
- Pandas
- NumPy

## Contributing

We welcome contributions to improve the Vandalizer documentation! Please see our [Contributing Guide](CONTRIBUTING.md) for detailed instructions.

**Have ideas but prefer not to edit directly?** Contributors can also email suggestions to **nlayman@uidaho.edu** and we'll incorporate them.

### High-Priority Areas

- Workflow Examples: Real-world use cases and step-by-step guides
- Interface Documentation: Screenshots and detailed UI explanations
- Troubleshooting: Common issues and solutions
- Integration Guides: Connecting Vandalizer with other RA tools

### Quick Start for Contributors

#### Editing a Page

1. Request access (if needed)
2. Click the "Edit this page" button on any page (visible on live site)
3. Make changes using the GitHub web editor
4. Commit directly to the main branch with a descriptive message
5. Changes automatically deploy within 2-5 minutes

#### Requesting Access

**Email**: nlayman@uidaho.edu
**Subject**: "Vandalizer Documentation Access Request"
**Include**:
- Your GitHub username
- Your affiliation with the Vandalizer project
- Brief description of your intended contributions

## Local Development

### Prerequisites

- [Pixi](https://prefix.dev/) (or install dependencies manually)
- Python 3.13+
- Quarto

### Building Locally

```bash
# Using Pixi
pixi run quarto render

# Or manually
quarto render
```

Generated HTML output is created in the `docs/` directory.

### Viewing Locally

```bash
# Start a local server (navigate to the docs directory)
cd docs
python -m http.server 8000

# Visit http://localhost:8000 in your browser
```

### Working with Roadmap Data

The roadmap page requires `data/issues.json` to be present. For local testing:

1. Manually fetch issues from GitHub:
   ```bash
   gh api repos/ui-insight/vandalizer/issues?state=all --paginate > data/issues.json
   ```

2. Or create sample data for testing

3. Re-render: `quarto render roadmap.qmd`

## Troubleshooting

### Roadmap Not Showing Data

**Issue**: Roadmap dashboard appears empty or errors in browser console

**Solutions**:
1. Check if `data/issues.json` exists and is valid JSON
2. Verify Plotly library loaded: Check browser Network tab for `plotly-3.0.1.min.js`
3. Check browser console for JavaScript errors
4. Ensure `scripts.html` is included in `index.qmd` format settings

### Build Fails

**Issue**: GitHub Actions build workflow fails

**Solutions**:
1. Check workflow logs in GitHub Actions
2. Verify Pixi environment is working: `pixi info`
3. Ensure all `*.qmd` files have valid YAML frontmatter
4. Check for Python import errors in `src/` modules

### Data Not Updating

**Issue**: Roadmap issues not updating after 6 AM UTC run

**Solutions**:
1. Check if `update-roadmap.yml` workflow ran successfully
2. Verify `VANDALIZER_ISSUES_TOKEN` secret exists and is valid
3. Verify token has access to `ui-insight/vandalizer` repository
4. Check GitHub Actions logs for authentication errors
5. Manually trigger workflow: GitHub Actions → "Update Roadmap" → "Run workflow"

## Support

For technical issues with the documentation:
- Create an issue in this repository
- Email [nlayman@uidaho.edu](nlayman@uidaho.edu) for help

## License

This documentation is part of the Vandalizer project. Please refer to the main project repository for licensing information.
