#!/bin/bash

set -e  # Exit if any command fails

echo "check before running: chmod +x install_prometheus.sh and ./install_prometheus.sh and change target IP"

PROM_VERSION="2.52.0"
TARGET_PRIVATE_IP="<TARGET_EC2_PRIVATE_IP>"  # Replace this before running

echo "🚀 Updating system and installing dependencies..."
sudo apt update && sudo apt install -y wget tar

echo "👤 Creating Prometheus user..."
sudo useradd --no-create-home --shell /bin/false prometheus

echo "⬇️ Downloading Prometheus v$PROM_VERSION..."
wget https://github.com/prometheus/prometheus/releases/download/v$PROM_VERSION/prometheus-$PROM_VERSION.linux-amd64.tar.gz

echo "📦 Extracting Prometheus archive..."
tar -xvf prometheus-$PROM_VERSION.linux-amd64.tar.gz
cd prometheus-$PROM_VERSION.linux-amd64

echo "🚚 Moving Prometheus binaries to /usr/local/bin..."
sudo mv prometheus /usr/local/bin/
sudo mv promtool /usr/local/bin/

echo "📁 Creating required directories..."
sudo mkdir -p /etc/prometheus /var/lib/prometheus
sudo cp -r consoles/ console_libraries/ /etc/prometheus/
sudo cp prometheus.yml /etc/prometheus/

echo "📝 Overwriting prometheus.yml with target configuration..."
cat <<EOF | sudo tee /etc/prometheus/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['$TARGET_PRIVATE_IP:9100']

  - job_name: 'custom-app'
    static_configs:
      - targets: ['$TARGET_PRIVATE_IP:8000']
EOF

echo "⚙️ Creating Prometheus systemd service file..."
cat <<EOF | sudo tee /etc/systemd/system/prometheus.service
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service] 
User=prometheus 
ExecStart=/usr/local/bin/prometheus \ =
  --config.file=/etc/prometheus/prometheus.yml \ 
  --storage.tsdb.path=/var/lib/prometheus/ \ 
  --web.route-prefix=/prometheus 

[Install]
WantedBy=default.target
EOF

echo "🔐 Setting permissions..."
sudo chown -R prometheus:prometheus /etc/prometheus /var/lib/prometheus

echo "🔄 Reloading systemd and starting Prometheus..."
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable --now prometheus
sudo systemctl restart prometheus

echo "✅ Prometheus installation complete. Service status:"
sudo systemctl status prometheus --no-pager
