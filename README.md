# Vandalizer User Manual and Wiki

Welcome to the official documentation repository for Vandalizer - an AI management tool designed to assist research administrators in managing and streamlining their work.

## About This Repository

This repository contains the source code for the [Vandalizer User Manual and Wiki](https://nate-layman.github.io/vandalizer-manual/) Which includes the following pages:

- Introduction - Overview of Vandalizer and its capabilities
- Interface - User interface guide and navigation
- Tasks - Detailed task documentation
- Workflows - Process guides and workflow documentation
- Examples - Practical examples and use cases
- Roadmap - Project roadmap with automated issue tracking

## Architecture

- Public Repository: Anyone can view this repository and the manual
- Framework: [Quarto](https://quarto.org/) for documentation generation
- Deployment: Automated deployment to GitHub Pages
- Roadmap Integration: Automatic issue data collection from the main Vandalizer repository

## Contributing

We welcome contributions to improve the Vandalizer documentation! Please see our [Contributing Guide](CONTRIBUTING.md) for detailed instructions.

**Have ideas but prefer not to edit directly?** Contributors can also email me their ideas, suggestions, or content contributions at **nlayman@uidaho.edu** and I would be happy to incorporate them into the manual.

## Contribution Ideas

### High-Priority Areas

- Workflow Examples: Real-world use cases and step-by-step guides
- Interface Documentation: Screenshots and detailed UI explanations
- Troubleshooting: Common issues and solutions
- Integration Guides: Connecting Vandalizer with other RA tools

### Quick Start for Contributors

#### Editing a Page

1. Request access
2. Click the "Edit this page" button on any page
3. Make changes using the GitHub web editor
4. Commit directly to the main branch with a descriptive message
5. Changes are automatically deployed within 2-5 minutes

#### Requesting Access

If you'd like to contribute to the documentation but don't have access:

**Email**: nlayman@uidaho.edu  
**Subject**: "Vandalizer Documentation Access Request"  
**Include**:
- Your GitHub username
- Your affiliation with the Vandalizer project
- Brief description of your intended contributions

Each page on the live documentation includes an "Edit this page" button that allows authorized contributors to edit content directly and commit to the main branch.

## Automated Features

### Daily Roadmap Updates

The repository includes an automated workflow that:
- Runs daily at 6 AM UTC
- Fetches issues from the main Vandalizer repository (`ui-insight/vandalizer`)
- Updates the roadmap dashboard with current project status
- Automatically commits and deploys changes

### Continuous Deployment

- All changes to the `main` branch automatically trigger a rebuild and redeploy
- Documentation is always up-to-date with the latest commits

## Repository Structure

```
├── .github/workflows/          # GitHub Actions workflows
│   ├── build-deploy.yml        # Build and deploy to GitHub Pages
│   └── update-dashboard.yml    # Sync roadmap issues
├── docs/                       # Generated output (auto-generated)
├── images/                     # Logo and image assets
├── scripts.html                # Custom JavaScript for roadmap
├── styles.css                  # Custom styling
├── _quarto.yml                 # Quarto configuration
├── index.qmd                   # Homepage content
├── roadmap.qmd                 # Roadmap page with interactive dashboard
├── [other-pages].qmd           # Additional documentation pages
├── CONTRIBUTING.md             # Contribution guidelines
└── README.md                   # This file
```

## Support

For technical issues with the documentation or access requests:
- Create an issue in this repository, or
- Email [nlayman@uidaho.edu](nlayman@uidaho.edu) for help

## License

This documentation is part of the Vandalizer project. Please refer to the main project repository for licensing information.
