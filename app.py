from flask import Flask, render_template, request, redirect
import os
import subprocess

app = Flask(__name__)

NGINX_AVAILABLE = "/etc/nginx/sites-available"
NGINX_ENABLED = "/etc/nginx/sites-enabled"
HOSTS_FILE = "/etc/hosts"


def add_domain(domain, port):
    hosts_entry = f"127.0.0.1 {domain}\n"

    with open(HOSTS_FILE, "r") as f:
        hosts_content = f.read()

    if domain not in hosts_content:
        with open(HOSTS_FILE, "a") as f:
            f.write(hosts_entry)

    nginx_config = f"""
server {{
    listen 80;
    listen 443 ssl;
    server_name {domain};

    ssl_certificate /etc/ssl/certs/ssl-cert-snakeoil.pem;
    ssl_certificate_key /etc/ssl/private/ssl-cert-snakeoil.key;

    location / {{
        proxy_pass http://127.0.0.1:{port};
        proxy_http_version 1.1;

        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_cache_bypass $http_upgrade;
    }}
}}
"""

    config_path = f"{NGINX_AVAILABLE}/{domain}"

    with open(config_path, "w") as f:
        f.write(nginx_config)

    enabled_path = f"{NGINX_ENABLED}/{domain}"

    if not os.path.exists(enabled_path):
        os.symlink(config_path, enabled_path)

    subprocess.run(["nginx", "-t"])
    subprocess.run(["systemctl", "reload", "nginx"])


def remove_domain(domain):
    with open(HOSTS_FILE, "r") as f:
        lines = f.readlines()

    with open(HOSTS_FILE, "w") as f:
        for line in lines:
            if domain not in line:
                f.write(line)

    config_path = f"{NGINX_AVAILABLE}/{domain}"
    enabled_path = f"{NGINX_ENABLED}/{domain}"

    if os.path.exists(enabled_path):
        os.remove(enabled_path)

    if os.path.exists(config_path):
        os.remove(config_path)

    subprocess.run(["nginx", "-t"])
    subprocess.run(["systemctl", "reload", "nginx"])


@app.route("/", methods=["GET", "POST"])
def index():
    message = None

    if request.method == "POST":
        action = request.form.get("action")
        domain = request.form.get("domain")
        port = request.form.get("port")

        if action == "add":
            add_domain(domain, port)
            message = f"Domain created: http://{domain} and https://{domain}"

        elif action == "remove":
            remove_domain(domain)
            message = f"Domain removed: {domain}"

    return render_template("index.html", message=message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)