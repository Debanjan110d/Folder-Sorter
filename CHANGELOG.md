# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive test suite for config, categories, sorting, date sorting, undo, doctor, and CLI subcommands.
- GitHub Actions CI/CD workflow running tests across OS platforms and building executables.
- Autocomplete configuration options and documentation.
- Non-blocking update check utility verifying latest releases against GitHub API.
- `update` subcommand to explicitly query and upgrade the installed version.
- `config edit` command to launch global config file inside default system text editor.
- Automated installation scripts `install.ps1` (Windows) and `install.sh` (macOS/Linux) managing global installation, PATH configuration, and virtualenv wrapping.

## [0.1.0] - 2026-06-28

### Added
- Core CLI commands (`sort`, `undo`, `doctor`, `config`) powered by Typer and Rich.
- Interactive mode menu system for beginner-friendly execution.
- Smart sorting grouping files into type categories (Images, Videos, Documents, Archives, Code).
- Resolution and format-based sub-sorting for images using Pillow.
- Chronological sorting grouping files under year/month directories.
- Sequential undo operations using a local database history log.
- Diagnostics doctor environment check.
- Custom categories mapping configured dynamically via JSON.
