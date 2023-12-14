# Installation Instructions for SQL

## 1. Install pgAdmin 4

### For Windows:
- Download the installer from the [official pgAdmin download page](https://www.pgadmin.org/download/pgadmin-4-installer/).
- Follow the installation instructions provided by the installer.

### For macOS:
- Install pgAdmin 4 using Homebrew:
  ```bash
  brew install --cask pgadmin4
    ```
**For Linux:**

- Install pgAdmin 4 using the package manager for your distribution.

**For Ubuntu/Debian:**
```bash
sudo apt-get install pgadmin4
```
**For Fedora:**
```bash
sudo dnf install pgadmin4
```
Alternatively, download the installer from the [official pgAdmin download page](https://www.pgadmin.org/download/pgadmin-4-installer/).

Follow the installation instructions provided by the installer.

## 2. Install SQLTools in VS Code

1. Open Visual Studio Code (VS Code).
2. Go to the Extensions view by clicking on the Extensions icon in the Activity Bar on the side of the window or using the keyboard shortcut `Ctrl+Shift+X`.
3. Search for "SQLTools" in the Extensions view search box.
4. Click on the "Install" button next to the "SQLTools" extension provided by Matheus Teixeira.
5. Once installed, you might need to reload VS Code for the changes to take effect.

## 3. Install SQLTools PostgreSQL/Cockroach Driver in VS Code

1. After installing SQLTools, you need to install the PostgreSQL/Cockroach driver:
2. Open the SQLTools settings:
   - Go to the gear icon in the lower-left corner and click on "Settings."
   - Search for "SQLTools" in the settings search box.
   - Click on "SQLTools" in the settings list.
3. Scroll down to the "Drivers" section.
4. Click on "Install" next to "PostgreSQL/Cockroach."
5. Once installed, you might need to reload VS Code for the changes to take effect.

Now you should have pgAdmin 4 installed for managing your PostgreSQL databases, and SQLTools with the PostgreSQL/Cockroach driver in VS Code for executing SQL queries. Make sure to configure the connection details for your PostgreSQL database in SQLTools.
