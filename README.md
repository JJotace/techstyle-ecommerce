# TechStyle Online Shop

A fashion e-commerce app for developers. Built with Python Flask + SQLite.

## 📋 Project Overview

TechStyle is a 25-year-old fashion retailer modernizing its online shop. This
repository contains the Flask e-commerce application, now under structured
version control as part of the DevOps transformation project.

## 🚀 Quick Start

```bash
./run_dev.sh
```

This creates a virtual environment, installs dependencies, seeds the database, and starts the dev server.

Open http://localhost:5000

### Manual setup (without the script)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python seed_data.py
python app.py
```

## Deploy to Production

```bash
./deploy.sh
```

Make sure `~/.ssh/techstyle_prod.pem` exists and the server IP in `deploy.sh` is correct.

## ✨ Features

- Product catalogue (20 items, multiple categories)
- Session-based shopping cart
- Checkout (no real payment)
- Admin panel at /admin

## 📁 Project Structure
