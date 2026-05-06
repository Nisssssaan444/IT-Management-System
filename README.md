# IT Onboarding & Offboarding Automation Toolkit

A lightweight, Python-based CLI tool designed for IT administrators to automate user lifecycle management, asset tracking, and audit logging. This toolkit streamlines the most repetitive parts of IT admin work—onboarding new employees and offboarding departing ones—simulating integrations with Active Directory and Microsoft 365.

## Why I Built This
I developed this project to demonstrate hands-on experience with core IT administration workflows. Managing employee onboarding, offboarding, and asset inventory manually is prone to errors, security oversights, and lost hardware. This tool automates these repetitive tasks, securely reclaims hardware during offboarding, generates checklists, and maintains a strict audit trail, showcasing a proactive approach to IT operations and process improvement.

## Core Features
- **Automated User Provisioning (Onboarding):** Creates simulated AD/M365 accounts, generates secure random passwords, assigns users to departments, and generates localized welcome emails.
- **Secure Offboarding Workflow:** One-command offboarding that disables accounts, revokes access, flags assigned physical assets for reclamation, and generates an offboarding checklist.
- **Asset Inventory Tracking:** A built-in SQLite-backed register to track hardware (laptops, peripherals, etc.). Quickly assign assets, view unassigned equipment, or generate CSV reports.
- **Compliance & Audit Logging:** Every IT action (creation, deletion, asset assignment) is automatically timestamped and logged for security and compliance audits.

## Tech Stack
- **Python 3.8+** - Core script logic and CLI parsing (`argparse`).
- **SQLite3** - Lightweight, zero-config local database for Users, Assets, and Logs.
- **PyYAML** - Configuration management (`config.yaml`).

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/it-management-toolkit.git
   cd it-management-toolkit
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your environment:**
   Edit `config.yaml` to match your organization's domain, name, and default password policies.

## Usage & Workflows

### 1. Onboarding a New Employee
Creates a user account structure, sets up temporary credentials, and logs the action.
```bash
python itkit.py onboard --name "John Doe" --dept Engineering --manager alice@acmecorp.com
```

### 2. Managing IT Assets
Add hardware to the inventory and assign it to the new hire.
```bash
python itkit.py asset --add --name "Latitude 7420" --assigned-to john.doe --type laptop --serial SN9876543
python itkit.py asset --list --unassigned
python itkit.py asset --report
```

### 3. Offboarding a Departing Employee
Disables the user profile, flags their assets as unassigned, and provides a clear separation checklist.
```bash
python itkit.py offboard --user john.doe@acmecorp.com
```

### 4. Security & Audit Trail
Check the audit log to verify recent administrative actions.
```bash
python itkit.py audit --last 10
python itkit.py audit --user john.doe --export audit_report.csv
```

## Project Structure
```text
.
├── config.yaml          # Company configuration (domain, depts)
├── itkit.py             # Main CLI entrypoint
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
└── src/
    ├── assets.py        # Asset tracking logic
    ├── audit.py         # Audit logging and reporting
    ├── db.py            # SQLite schema and initialization
    ├── offboarding.py   # Account termination workflow
    └── onboarding.py    # User creation workflow
```
