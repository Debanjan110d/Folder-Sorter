# Contributing to Folder Sorter

Thank you for your interest in contributing to Folder Sorter. We want to keep the contribution process simple, friendly, and straightforward.

## Getting Started

Here is how you can set up the project on your machine to start making improvements.

### 1. Fork the Repository
Click the Fork button at the top right of the GitHub page to create a copy of this repository under your own GitHub account.

### 2. Clone Your Fork
Clone your fork to your computer using your terminal:

```bash
git clone https://github.com/YOUR_USERNAME/Folder-Sorter.git
cd Folder-Sorter
```

### 3. Install Dependencies
Make sure you have Python 3.8 or newer installed. Install the package in editable mode along with development tools:

```bash
pip install -e .
pip install -r requirements-dev.txt
```

### 4. Create a Branch
Create a new branch for your changes:

```bash
git checkout -b my-new-feature
```

### 5. Make Changes and Test
Make your code or documentation changes. Before committing, run the tests to make sure everything works:

```bash
pytest
```

### 6. Commit Your Changes
Write a clear commit message explaining what you did:

```bash
git commit -am "fix: resolve path checking on Windows"
```

### 7. Push and Open a Pull Request
Push your branch to your GitHub fork:

```bash
git push origin my-new-feature
```

Then, go to the original Folder Sorter repository on GitHub. You will see a prompt to open a Pull Request. Fill out the pull request template with details of what you changed.

---

## Issues, Labels, and Project Board

### Opening Issues
If you find a bug or have a suggestion, open an issue using the Bug Report or Feature Request templates. Try to provide as much detail as possible so we can help you quickly.

### Issue Labels
We use standard labels to categorize and track issues:
- bug: Something is broken or behaving incorrectly.
- enhancement: A new feature request or improvement.
- documentation: Improvements to markdown guides or web docs.
- good first issue: Simple issues suitable for new contributors.
- help wanted: Extra help is needed to resolve the issue.
- question: Inquiries about how to use the tool or configure mappings.

### Project Board
We manage all active tasks on the community Project Board, which is divided into four main sections:
- Todo: Approved ideas or confirmed bugs waiting for someone to work on them.
- In Progress: Tasks that contributors are actively working on.
- Testing: Completed changes that are currently being reviewed or tested.
- Done: Merged changes that are officially part of the project.
