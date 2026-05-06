# IT Management Toolkit - Project Description

## 1. Project Overview & Core Concept
The **IT Onboarding & Offboarding Lifecycle Toolkit** is a lightweight, Python-based Command-Line Interface (CLI) application designed for IT administrators. It automates and provides a structured framework for managing the employee lifecycle from an IT perspective.

The core concept centers around replacing manual, error-prone IT provisioning and de-provisioning processes with a single, unified tool. It simulates the workflows an IT administrator would typically perform when someone joins or leaves a company, such as creating directory accounts (like Active Directory or Microsoft 365), assigning hardware assets, securely offboarding departing employees, and keeping a rigorous audit trail of all these administrative actions.

## 2. Design Philosophy
- **Simplicity & Speed:** Built as a CLI tool (`itkit.py`) so IT professionals can execute complex workflows with a single typed command rather than navigating through multiple web portals.
- **Traceability:** Every action taken via the toolkit is logged into an irreversible audit trail, helping organizations meet compliance and security standards.
- **State Management:** Uses a local database (SQLite) to maintain the state of the company's assets, user accounts, and historical logs without requiring entirely separate, heavy-weight server infrastructure.
- **Configurability:** Abstracted company-specific variables (like domain names, password policies, and departments) into a manageable `config.yaml` file so the tool can be easily adapted to any organization.

## 3. Technologies Used
- **Language:** Python 3.8+ (Chosen for scriptability, vast standard library, and ease of use).
- **CLI Parsing:** `argparse` (Built-in Python library used to handle commands, subcommands, and flags).
- **Database:** SQLite3 (A C-language library that implements a small, fast, self-contained, high-reliability SQL database engine). Used for storing users, hardware inventory, and the audit log.
- **Configuration:** PyYAML (`yaml` parser) to cleanly define company constants.

## 4. Code Structure & Components

The application follows a modular architecture, splitting responsibilities into specific domains inside the `src/` directory.

```text
.
├── config.yaml          # Defines company constants (e.g., domain, valid departments)
├── itkit.py             # The main entry point. Handles CLI parsing and routes commands
├── requirements.txt     # Python package dependencies (PyYAML)
├── README.md            # Quick-start documentation
└── src/                 # Core logic modules
    ├── assets.py        # Manages hardware lifecycle (add laptops, assign, report)
    ├── audit.py         # Manages the system's security and action logs
    ├── db.py            # SQLite database initialization and schema logic
    ├── offboarding.py   # Handles employee termination, revoking access, unassigning assets
    └── onboarding.py    # Handles employee creation, initial password generation
```

### Component Details
1. **`itkit.py` (CLI Router):** Uses `argparse` to define the vocabulary of the tool. It understands sub-commands like `onboard`, `offboard`, `asset`, and `audit` and passes execution to the respective modules in `src/`.
2. **`src/db.py` (Data Layer):** Initializes the SQLite database upon first run. It creates necessary tables for Users, Assets, and Audit logs. 
3. **`src/onboarding.py` (User Provisioning):** Takes a user's name, department, and manager. It automatically constructs their corporate email based on the `config.yaml` domain, generates a secure initial password, logs the creation, and hypothetically sends the welcome email.
4. **`src/offboarding.py` (De-provisioning):** Takes a user identifier and disables their simulated account. Crucially, it queries the database for any assigned hardware and flags them for return, outputting a separation checklist.
5. **`src/assets.py` (Inventory Management):** Allows adding items via serial number and assigning them to user profiles. It can generate status reports or filter by explicitly unassigned hardware.
6. **`src/audit.py` (Compliance Logger):** A standalone module that write/reads from the audit table. Every other module imports this to record actions like `"USER_CREATED"` or `"ASSET_ASSIGNED"`.

## 5. Main Workflows

- **Initialization:** On every run, `itkit.py` calls `init_db()` to ensure the SQLite file and schema exist.
- **The Onboarding Flow:** `itkit onboard --name ...` -> Parses args -> Loads YAML config -> Generates Email/Password -> Writes to DB -> Writes to Audit Log.
- **The Asset Flow:** `itkit asset --add ...` -> Parses args -> Validates presence of serial/type -> Writes to DB -> Optionally links to a user -> Writes to Audit Log.
- **The Offboarding Flow:** `itkit offboard --user ...` -> Parses args -> Looks up User in DB -> Disables User -> Looks up associated Assets in DB -> Removes Asset assignment -> Writes to Audit Log -> Prints checklist.

## 6. Important Questions & Answers

### Q: What have I used to store the details of employees, and how do I manage it?
**A:** I used **SQLite3**, a built-in, lightweight relational database in Python. The database is a single local file named `itkit.db`.

**How it's structured:**
Within this database, there is a specific `users` table created in `src/db.py` that stores employee states including: `id`, `name`, `username`, `email`, `department`, `manager`, and `status` (active vs disabled). 

**How it's managed:**
All employee management is handled via the CLI commands, abstracting away direct database interaction:
1. **Adding Data:** When you run the `onboard` command, the application verifies the input and fires a SQL `INSERT` command to add the employee's details into the `users` table.
2. **Updating Data:** When you run the `offboard` command, the app queries the database to find the user and executes an `UPDATE` command to change their status to disabled, while unassigning related hardware in the `assets` table.
3. **Database Access:** The logic to connect to and interact with the database is centralized in `src/db.py`. Users of the script don't need database knowledge; they just use the simple CLI commands.

