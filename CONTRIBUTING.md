# Contributing to Vandalizer Documentation

Thank you for your interest in contributing! This guide will help you get started quickly.

## Quick Start

### 1. Get Access

**Email**: nlayman@uidaho.edu  
**Subject**: "Vandalizer Documentation Access Request"

Include:
- Your GitHub username
- Your affiliation with Vandalizer or research administration
- What you'd like to contribute (e.g., "workflow examples", "interface screenshots")

*Response time: 2-3 business days*

### 2. Make Your First Edit

1. Go to the [live documentation](https://nate-layman.github.io/vandalizer-manual/)
2. Click "Edit this page" on any page
3. Make your changes in the GitHub editor
4. Write a clear commit message describing what you changed
5. Commit to main branch

Your changes go live automatically in 2-5 minutes!

### 3. Alternative: Email Your Ideas

Don't want to edit directly? **Email your ideas to nlayman@uidaho.edu** and I'll incorporate them into the manual.

## What We Need Most

**High Priority:**
- Real-world workflow examples with step-by-step instructions
- Screenshots of the Vandalizer interface with explanations
- Common troubleshooting issues and solutions
- Integration guides for connecting with other RA tools

**Content Types:**
- Video tutorials or links
- Downloadable templates and checklists
- FAQ entries
- Best practices and tips

## Writing Guidelines

**Keep it simple:**
- Write for research administrators who may be new to AI tools
- Use clear, action-oriented language
- Include practical examples when possible
- Break up long sections with headers

**Format basics:**
- Use descriptive headings (## Main Section, ### Subsection)
- Add alt text to images: `![Description](image.png)`
- Use tip boxes for important info:
  ```markdown
  ::: {.callout-tip}
  ## Tip
  Your helpful tip here
  :::
  ```

## Before You Commit

Quick checklist:
- [ ] Content is accurate and helpful
- [ ] Links work
- [ ] Images display properly
- [ ] Commit message clearly describes changes

## Need Help?

- **General questions**: Email nlayman@uidaho.edu
- **Technical issues**: Create a GitHub issue
- **Quarto/Markdown help**: [Quarto Documentation](https://quarto.org/docs/)

## Technical Details

<details>
<summary>For Advanced Contributors (click to expand)</summary>

### File Organization
- Main content: `.qmd` files in root directory
- Images: Store in `images/` folder
- Navigation: Edit `_quarto.yml` to add new pages

### Automated Features
- **Daily roadmap updates**: Issues from main repository auto-sync at 6 AM UTC
- **Auto-deployment**: All changes to main branch deploy automatically
- **Don't edit**: `data/issues.json` (auto-generated)

### Adding New Pages

**Step 1:** Create your new page using this required header template:
```yaml
---
title: "Your Page Title"
format:
  html:
    page-layout: full
    include-after-body: scripts.html
---

:::: {.header-logos}
::: {.grid}
::: {.g-col-2 .d-flex .justify-content-center .align-items-center}
![](images/uidaho_logo.png){width=100px}
:::
::: {.g-col-7 .d-flex .justify-content-center .align-items-center}
![](images/vandalizer_logo.png){width=500px}
:::
::: {.g-col-3 .d-flex .justify-content-center .align-items-center}
![](images/suu_logo.png){width=200px}
:::
:::
::::

---

[Your content starts here]
```

**Step 2:** Add to navigation by editing `_quarto.yml`:
```yaml
sidebar:
  contents:
    - text: "Your New Page"
      href: your-new-page.qmd
```

### Quality Standards
- Test all links after changes
- Use GitHub preview before committing
- Make incremental changes when possible
- Coordinate with other contributors on large changes

</details>

---

**Questions?** Email nlayman@uidaho.edu - we're here to help make contributing as easy as possible!
