# AWS Deployment Guide: Text Summarization API

This guide walks you through deploying the fully decoupled FastAPI and React (Vite) application to an AWS EC2 instance running Ubuntu, using Nginx as a reverse proxy.

### Phase 1: EC2 Provisioning (Deep Learning Adjusted)

Because this application runs a state-of-the-art **BART Deep Learning Model** locally, you can no longer use the AWS Free Tier `t2.micro` instances (they only have 1GB RAM and will instantly trigger an Out-of-Memory crash).

**Your Hardware Budget ($120 for 15 Days):**
You require around ~3GB of RAM safely. A **`t3.large`** instance provides 2 vCPUs and 8GB RAM, giving the deep learning model plenty of headroom.
- Cost of `t3.large`: ~$0.083 per hour.
- Cost for 15 days (360 hours): **~$30.00**.
This fits incredibly securely inside your $120 budget.

1.  **Launch an EC2 Instance:**
    *   **AMI:** Select **Ubuntu Server 24.04 LTS** (64-bit x86).
    *   **Instance Type:** Select **`t3.large`**.
    *   **Key Pair:** Create a new key pair (RSA, .pem) and download it securely.
    *   **Network Settings:** Allow SSH traffic (Port 22), HTTPS (443), and HTTP (80) from anywhere (0.0.0.0/0).
    *   **Storage:** Increase the Root volume to at least **20 GB** (`gp3`) to accommodate the 1.6GB Hugging Face model permutations.

## 2. Server Configuration
SSH into your instance using your key pair:
```bash
ssh -i "txt-summ-key.pem" ubuntu@<your-ec2-public-ip>
```

### Install Dependencies
Run the following commands to update the system and install Python, Node.js, and Nginx:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx git curl -y

# Install Node.js (via NodeSource for latest LTS)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

## 3. Clone and Setup the Project
Clone your repository (replace the URL with your actual git URL):
```bash
git clone https://github.com/your-username/Text-summarizer-DL.git
cd Text-summarizer-DL
```

### Backend Setup (FastAPI)
Create a Python virtual environment and install the required dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn uvicorn
```

#### Run Backend as a Systemd Service
Create a systemd service file so the backend runs in the background and restarts automatically.
```bash
sudo nano /etc/systemd/system/txtsumm.service
```

Paste the following configuration:
```ini
[Unit]
Description=Gunicorn daemon for Text Summarization API
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/Text-summarizer-DL
Environment="PATH=/home/ubuntu/Text-summarizer-DL/venv/bin"
ExecStart=/home/ubuntu/Text-summarizer-DL/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app -b 127.0.0.1:8000

[Install]
WantedBy=multi-user.target
```

Start and enable the service:
```bash
sudo systemctl start txtsumm
sudo systemctl enable txtsumm
```

### Frontend Setup (Vite / React)
Navigate into the `frontend` folder, install packages, and build the production static files.
```bash
cd /home/ubuntu/Text-summarizer-DL/frontend
npm install
npm run build
```
This generates a `dist/` directory containing the minified frontend files.

## 4. Configure Nginx
Nginx will serve our static frontend site on port 80 and forward `/summarize` traffic to the local FastAPI app running on port 8000.

Create a new Nginx configuration block:
```bash
sudo nano /etc/nginx/sites-available/txtsumm
```

Paste the following Nginx configuration (replace `server_name` if you have a custom domain):
```nginx
server {
    listen 80;
    server_name _; # Or use your public IP or Domain Name

    # Serve the Vite Frontend from the dist folder
    location / {
        root /home/ubuntu/Text-summarizer-DL/frontend/dist;
        index index.html index.htm;
        try_files $uri $uri/ /index.html;
    }

    # Reverse proxy backend API calls to FastAPI
    location /summarize {
        proxy_pass http://127.0.0.1:8000/summarize;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the configuration and restart Nginx:
```bash
# Remove the default nginx site
sudo rm /etc/nginx/sites-enabled/default

# Create a symlink to enable your new config
sudo ln -s /etc/nginx/sites-available/txtsumm /etc/nginx/sites-enabled/

# Test the configuration for syntax errors
sudo nginx -t

# Restart Nginx to apply changes
sudo systemctl restart nginx
```

## 5. You're Live!
Navigate to your EC2 instance's Public IP address in your browser:
`http://<your-ec2-public-ip>`

Your complete, decoupled architecture should now be fully live, highly performant, and production ready!
