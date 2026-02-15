# Quick Start: Docker Compose

## Running Without SSL (Development/Testing)

### 1. Download Configuration Files
Download `docker-compose.yml` and the `nginx/` directory from the repository.

### 2. Start the Application
```bash
docker-compose up -d
```

The latest image (`aaiiz/english-pdf-analyzer:latest`) will be pulled automatically.

### 3. Access the Application
Open your browser and go to:
- `http://localhost` (if running locally)
- `http://your-server-ip` (if running on a server)

### 4. Stop the Application
```bash
docker-compose down
```

## Running With SSL (Production)

### Prerequisites
- A domain name pointing to your server
- Ports 80 and 443 open
- Certbot installed on your host

### 1. Install Certbot
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install certbot

# CentOS/RHEL
sudo yum install certbot
```

### 2. Configure Your Domain
Edit `nginx/conf.d/app.conf` and replace `yourdomain.com`:
```bash
sed -i 's/yourdomain.com/YOUR_DOMAIN/g' nginx/conf.d/app.conf
```

### 3. Start Services
```bash
docker-compose up -d
```

### 4. Obtain SSL Certificate
```bash
sudo certbot certonly --standalone \
  -d yourdomain.com -d www.yourdomain.com \
  --email your-email@example.com --agree-tos
```

### 5. Update Docker Compose for SSL
Edit `docker-compose.yml` and add the certificate mount:
```yaml
nginx:
  volumes:
    - ./nginx/conf.d:/etc/nginx/conf.d:ro
    - /etc/letsencrypt:/etc/nginx/ssl:ro  # Add this line
    - certbot-webroot:/var/www/certbot:ro
```

### 6. Enable HTTPS
```bash
# Copy SSL configuration
cp nginx/conf.d/app-ssl.conf.example nginx/conf.d/app.conf

# Update domain
sed -i 's/yourdomain.com/YOUR_DOMAIN/g' nginx/conf.d/app.conf

# Restart Nginx
docker-compose restart nginx
```

### 7. Setup Auto-Renewal
Certbot automatically sets up a systemd timer for renewal:
```bash
# Test renewal
sudo certbot renew --dry-run

# Check renewal timer
sudo systemctl status certbot.timer
```

### 8. Access via HTTPS
Open `https://yourdomain.com`

## Common Commands

```bash
# View logs
docker-compose logs -f

# Restart a service
docker-compose restart nginx

# Pull latest image
docker-compose pull pdf-analyzer
docker-compose up -d pdf-analyzer

# Check Nginx configuration
docker-compose exec nginx nginx -t
```

## Troubleshooting

**Port already in use:**
```bash
sudo netstat -tlnp | grep ':80\|:443'
sudo systemctl stop apache2  # or other service
```

**View application logs:**
```bash
docker-compose logs pdf-analyzer
```

**Nginx won't start:**
```bash
docker-compose logs nginx
docker-compose exec nginx nginx -t
```

For detailed SSL setup instructions, see [SSL_SETUP_GUIDE.md](SSL_SETUP_GUIDE.md)
