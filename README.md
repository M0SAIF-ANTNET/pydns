# 🌐 pydns

pydns is a lightweight local domain manager for Linux built with Python, Flask, and Nginx. It automates local development workflows by mapping custom domain names to local applications running on specific ports.

Instead of remembering ports like `localhost:5000`, you can access your applications using clean, custom domains like `http://myapp.local`.

---

## Dashboard Preview

<img width="1003" height="592" alt="image" src="https://github.com/user-attachments/assets/b1321112-9b4b-4b6e-8e0c-0e07cb0e99b2" />

---

## Features

- **Dynamic Domain Creation:** Add local domains on the fly.
- **Nginx Reverse Proxy Automation:** Automatically generates server blocks.
- **Hosts File Management:** Automatically injects and cleans up `127.0.0.1` entries.
- **Minimalist Web UI:** Simple dashboard to manage your local domains.
- **Clean Removal:** Deletes configuration files, symlinks, and host entries safely.
- **System Integration:** Automatically tests and reloads Nginx service.

---

## Project Structure

```text
pydns/
│
├── app.py               # Main Flask application with system automation logic
├── requirements.txt     # Python dependencies
├── templates/
│   └── index.html       # Web Dashboard UI
├── static/
│   └── style.css        # Dashboard styling
└── README.md            # Project 
```

## Prerequisites & Requirements

Since this tool modifies system files (`/etc/hosts`, `/etc/nginx/`), it requires the following setup:

- **OS:** Linux (Ubuntu/Debian recommended)
- **Python:** Version 3.x or higher
- **Web Server:** Nginx installed and running
- **Privileges:** Root/Sudo permissions (required to write to system paths and reload services)
---

## Setup & Installation

Follow these steps to get **pydns** up and running on your local machine using a Virtual Environment (`venv`):

### 1. Clone the Repository
```bash
git clone https://github.com/M0SAIF-ANTNET/pydns.git
cd pydns
```

### 2. Create and Activate Virtual Environment
```bash
# Create the virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. How to Run
```bash
sudo ./venv/bin/python app.py
```

⚠️ Note: Running just sudo python3 app.py will use the global system Python instead of your virtual environment, which will cause ModuleNotFoundError for Flask. Using the explicit path sudo ./venv/bin/python solves this perfectly.

Once started, open your browser and navigate to:

http://localhost:8080 (or http://0.0.0.0:8080)

License
This project is open-source and available under the MIT License.
