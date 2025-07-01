# Contributing to Vandalizer Documentation

Thank you for your interest in contributing to the Vandalizer documentation! This guide will help you get started with making meaningful contributions to our project.

## Getting Started

### Request Repository Access

To contribute to this documentation, you'll need write access to the repository:

**Email**: nlayman@uidaho.edu  
**Subject**: "Vandalizer Documentation Access Request"

Please include:
- Your GitHub username
- Your affiliation with the Vandalizer project or research administration
- Brief description of your intended contributions (e.g., "updating interface documentation", "adding workflow examples")
- Your institutional email address

Response Time: Access requests are typically processed within 2-3 business days.

## Making Contributions

### Editing Pages

1. Navigate to the [live documentation](https://nate-layman.github.io/vandalizer-manual/)
2. Click the "Edit this page" button on any page you want to modify
3. Make your changes directly in the GitHub web editor
4. Write a clear, descriptive commit message
5. Commit your changes directly to the main branch

Changes will be automatically deployed to the live site within 2-5 minutes.

## Content Guidelines

### Writing Style
- Clear and Concise: Write for research administrators who may be new to AI tools
- Action-Oriented: Use active voice and specific instructions
- Consistent Terminology: Use the same terms throughout (refer to existing pages)
- Professional Tone: Maintain a helpful, professional voice

### Content Structure
- Descriptive Headers: Use clear, hierarchical headings (H1, H2, H3)
- Logical Flow: Organize content from general to specific
- Examples: Include practical examples and use cases when possible
- Cross-References: Link to related sections and external resources

### Markdown Guidelines
- Use Quarto-flavored Markdown syntax
- Include alt text for images: `![Description](path/to/image.png)`
- Use callout boxes for important information:
  ```markdown
  ::: {.callout-tip}
  ## Tip
  Your helpful tip here
  :::
  ```
- Code blocks should specify language: ````markdown ```python````

### Images and Assets
- Place images in the `images/` directory
- Use descriptive filenames: `workflow-diagram-grant-submission.png`
- Optimize images for web (< 500KB when possible)
- Include University of Idaho and collaborator logos appropriately

## Understanding Automated Workflows

### Daily Roadmap Updates
The repository includes automated issue tracking:
- Schedule: Runs daily at 6 AM UTC
- Function: Fetches issues from `ui-insight/vandalizer` repository
- Output: Updates `data/issues.json` and regenerates roadmap page
- Note: Don't edit `data/issues.json` manually - it's automatically overwritten

### Deployment Pipeline
- Trigger: Any push to `main` branch
- Process: Quarto renders all `.qmd` files to HTML
- Output: Deployed to GitHub Pages automatically
- Timeline: Changes are live within 2-5 minutes

## File Organization

### Page Structure
```
page-name.qmd                 # Main content file
├── YAML frontmatter         # Page configuration
├── Content sections         # Markdown content
└── References              # Links and citations
```

### Navigation Updates
To add new pages to the sidebar navigation, edit `_quarto.yml`:
```yaml
sidebar:
  contents:
    - text: "Your New Page"
      href: your-new-page.qmd
```

## Reporting Issues

### Documentation Issues
For problems with the documentation itself:
1. Use the GitHub Issues tab in this repository
2. Provide clear description of the problem
3. Include steps to reproduce if applicable
4. Suggest improvements when possible

### Vandalizer Product Issues
For issues with the Vandalizer tool itself:
- Report in the main Vandalizer repository
- Reference documentation issues if relevant

## Contribution Ideas

### High-Priority Areas
- Workflow Examples: Real-world use cases and step-by-step guides
- Interface Documentation: Screenshots and detailed UI explanations
- Troubleshooting: Common issues and solutions
- Integration Guides: Connecting Vandalizer with other RA tools

### Content Types Needed
- Video tutorials (embedded or linked)
- Downloadable templates and checklists
- Frequently asked questions
- Best practices and tips
- Case studies from early adopters

## Quality Standards

### Before Committing
- [ ] Content is accurate and up-to-date
- [ ] All links work correctly
- [ ] Images display properly and have alt text
- [ ] Spelling and grammar are correct
- [ ] Format is consistent with existing pages
- [ ] Commit message clearly describes the changes

### Best Practices
- Test links after making changes
- Preview your changes using GitHub's preview feature before committing
- Use clear, descriptive commit messages
- Make incremental changes rather than large overhauls when possible

## Community Guidelines

### Collaboration
- Be respectful and constructive in all interactions
- Coordinate with other contributors to avoid conflicts
- Ask questions when you need clarification
- Share knowledge and expertise openly

### Communication
- Use clear, professional language in commit messages
- Contact maintainers if you're unsure about changes
- Use GitHub issues for discussing larger changes
- Communicate with other contributors when working on related content

## Getting Help

### Technical Support
- Quarto Questions: [Quarto Documentation](https://quarto.org/docs/)
- Markdown Syntax: [Quarto Markdown Guide](https://quarto.org/docs/authoring/markdown-basics.html)
- Git/GitHub: [GitHub Docs](https://docs.github.com/)

### Project Support
- General Questions: Email nlayman@uidaho.edu
- Urgent Issues: Create a GitHub issue with "urgent" label
- Content Questions: Reach out to project maintainers

## Recognition

Contributors to this documentation will be acknowledged in:
- Git commit history (permanent record)
- Project acknowledgments (as appropriate)
- Community recognition for significant contributions

Thank you for helping make Vandalizer documentation better for the research administration community!

---

Questions? Don't hesitate to reach out to nlayman@uidaho.edu for any clarification or assistance.
