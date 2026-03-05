# Contributing to Cartoony Downloader Pro

First off, thank you for considering contributing to this project! It's people like you that make it a great tool for everyone.

## Development Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/kalidahmdev/cartoony-downloader.git
   cd cartoony-downloader
   ```

2. **Environment Setup**:
   - Run `scripts/setup.bat` (Windows) or follow the manual installation steps in the README.
   - Ensure you have a `.env` file based on `config/.env.example`.

3. **Project Structure**:
   - `src/`: Contains all Python backend logic.
   - `static/`: Contains HTML, CSS, and JS frontend assets.
   - `config/`: Configuration templates and requirements.
   - `scripts/`: Platform-specific setup and launch scripts.

## Pull Request Guidelines

- **Keep it focused**: One feature or bug fix per PR.
- **Maintain Style**: Follow the existing coding style for both Python (PEP 8) and JavaScript.
- **Test your changes**: Ensure the automation still works as expected and fails gracefully.
- **Document**: Update the README if you add new configuration options or features.

## Reporting Issues

Use the provided GitHub Issue Templates:

- [Bug Report](https://github.com/kalidahmdev/cartoony-downloader/issues/new?template=bug_report.md)
- [Feature Request](https://github.com/kalidahmdev/cartoony-downloader/issues/new?template=feature_request.md)

Happy Coding! 🚀
