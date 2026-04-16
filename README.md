<div align="center">
  <img src="logo.png" alt="Novon logo" width="120" />
  <h1>Novon Extensions</h1>
  <p>The official extension repository and developer SDK for the Novon ecosystem.</p>
  <p>
    <img alt="API Version" src="https://img.shields.io/badge/API-v1-6C63FF" />
    <img alt="Language" src="https://img.shields.io/badge/Language-JavaScript-F7DF1E" />
    <img alt="Status" src="https://img.shields.io/badge/Status-Alpha-orange" />
  </p>
</div>

## Table of Contents

- [Overview](#overview)
- [How to Create an Extension](#how-to-create-an-extension)
- [Project Structure](#project-structure)
- [Bundling & Automation](#bundling--automation)
- [Disclaimer](#disclaimer)
- [Authors & Maintainers](#authors--maintainers)
- [License](#license)

---

## Overview

> [!WARNING]
> **Educational & Testing Purpose Only**
>
> This repository is intended as a **technical demonstration and testing environment** for Novon extension development. The extensions provided here are examples and are **not recommended for use in the production Novon application**.
>
> For reliable and verified extensions, please refer to the official Novon extension channels.

This repository acts as a centralized registry for Novon extensions. It contains the source code for provider integrations and the automated infrastructure required to bundle them into `.novext` packages for the application.

## Getting Started with Development

> [!TIP]
> **Recommended Starting Point**
>
> We have provided a **Template Palette** (`com.novon.template`) that implements the full source interface. Use this as your foundation when building new extensions.

Before you begin, please review the [Source Script Technical Specification](https://novon.iprog.dev/docs/reference/source-script) for the exact Dart-JS contract requirements.

## How to Create an Extension

Creating a Novon extension involves defining a manifest, a source script, and an icon.

### 1. The Manifest (`manifest.json`)
The manifest defines the core metadata for your extension. It must match the following schema:

```json
{
  "id": "com.novon.mysource",
  "name": "My Source Name",
  "version": "1.0.0",
  "apiVersion": "1",
  "minAppVersion": "0.0.1",
  "lang": "en",
  "baseUrl": "https://source.com",
  "authorName": "MultiX0",
  "icon": "icon.png"
}
```

### 2. The Source Script (`source.js`)
The JS engine executes this script. It should define the logic for:
- Popular/Recent novel fetching
- Search results
- Novel details (description, status, chapters)
- Page fetching (content extraction)

### 3. The Icon (`icon.png`)
A square 128x128 or 256x256 PNG image representing the source.

## Project Structure

```text
extensions-example/
├── com.novon.kolnovel/      # Extension source directory
│   ├── manifest.json        # Extension metadata
│   ├── source.js            # Provider logic
│   └── icon.png             # Source icon
├── bundles/                 # Generated .novext packages
├── icons/                   # Synced icons for the index
├── index.json               # The global repo registry
└── bundle_extensions.py     # Automation & Bundling script
```

## Novon Management Shell

The repository includes a Command Line Interface (CLI) to manage the extension lifecycle and project configuration.

### 1. Getting Started

Launch the Novon Shell by running the wrapper script for your platform:

- **Windows**: `.\novon.ps1`
- **Linux/macOS**: `./novon.sh`

> [!NOTE]
> On Linux and macOS, you may need to grant execution permissions before running the script:
> `chmod +x novon.sh`

If run without arguments, the tool enters an interactive REPL mode.

### 2. Available Commands

| Command | Usage | Description |
| :--- | :--- | :--- |
| `bundle` | `bundle [--upgrade]` | Packages extensions and updates the registry. |
| `config` | `config` | Displays the current settings from novon_config.json. |
| `set` | `set <key> <val>` | Updates a configuration value in novon_config.json. |
| `list` | `list` | Lists all extensions found in the root directory. |
| `help` | `help` | Displays command usage and descriptions. |
| `exit` | `exit` | Terminates the shell session. |

## Bundling & Automation

The bundling engine automates the packaging, hashing, and registry synchronization process.

### 1. Automated Versioning
When running the `bundle` command, the script provides an option to automatically increment the patch version (e.g., 1.0.0 to 1.0.1) in the `manifest.json` for all discovered extensions.

### 2. Integrity and Validation
- **Source Integrity**: Calculates SHA-256 hashes for every `source.js` to ensure script integrity within the manifest.
- **Bundle Integrity**: Generates SHA-256 hashes for the final `.novext` packages for download verification.

### 3. Registry Synchronization
The script automatically updates `index.json` with the updated versions, hashes, and raw GitHub URLs based on the configuration settings.

### 4. Headless Execution (CI/CD)
The CLI supports one-shot execution for automated environments:
```bash
./novon.sh bundle --upgrade
```

## Project Structure

```text
extensions-example/
├── com.novon.kolnovel/      # Extension source directory
│   ├── manifest.json        # Extension metadata
│   ├── source.js            # Provider logic
│   └── icon.png             # Source icon
├── bundles/                 # Generated .novext packages
├── index.json               # The global repo registry
├── novon_config.json        # Centralized project configuration
├── novon.py                 # CLI entry point
├── bundle_extensions.py     # Bundling logic engine
├── novon.sh                 # Bash entry point
└── novon.ps1                # PowerShell entry point
```

> [!NOTE]
> Ensure you increment the `version` field in your `manifest.json` before running the bundling script, otherwise the registry will not detect the update as a new release.

## Disclaimer

> [!CAUTION]
> **Legal Disclaimer**
>
> This repository and its maintainers do not host, mirror, or distribute any novel content. The extensions provided here are simply tools (parsers) that allow users to access content from third-party websites through the Novon application.
>
> By using these extensions, you acknowledge that:
> 1. You are responsible for the content you access.
> 2. You must comply with the Terms of Service of the respective third-party providers.
> 3. The maintainers of this repository are not affiliated with, nor do they endorse, any content found on the provider websites.
>
> Use of these extensions is at your own risk.

## Contributing

We welcome contributions from the community. To maintain the quality of the project, we follow a simple workflow for all changes.

Please note that we do not accept direct pushes to the `main` branch. To contribute, please follow these steps:

1. **Fork the Repository**: Create your own copy of the project.
2. **Create a Branch**: Make your changes in a new branch on your fork.
3. **Open a Pull Request**: Submit your changes for review by opening a pull request against our `main` branch.

All pull requests must receive at least one approval from a maintainer before they can be merged. Thank you for helping improve the Novon ecosystem

## Authors & Maintainers

- **MultiX0** — Lead Developer & Maintainer

## License

Licensed under the Apache License 2.0. See [LICENSE](LICENSE) for full details.
