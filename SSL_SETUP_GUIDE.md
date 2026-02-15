# SSL Setup Guide for English PDF Analyzer with Nginx

This guide explains how to set up SSL/HTTPS for your English PDF Analyzer application using Nginx and Certbot with Docker Compose.

## Prerequisites

- A domain name pointing to your server's IP address
- Docker and Docker Compose installed
- Ports 80 and 443 open on your firewall

## Architecture

The setup includes:
- **Nginx**: Reverse proxy handling SSL termination and routing
- **PDF Analyzer**: Your application running on port 8080 (internal)
- **Certbot**: Automated SSL certificate management with Let's Encrypt

## Step-by-Step Setup

### Step 1: Configure Your Domain

Edit `nginx/conf.d/app.conf` and replace `yourdomain.com` with your actual domain:

```nginx
server_name yourdomain.com www.yourdomain.com;
```

### Step 2: Start Services (HTTP Only First)

```bash
# Create the Docker network
docker network create app-network 2>/dev/null || true

# Start the services
docker-compose up -d nginx pdf-analyzer
```

Verify the application is accessible at `http://yourdomain.com`

### Step 3: Obtain SSL Certificate with Certbot

Run Certbot to obtain your SSL certificate:

```bash
docker-compose run --rm certbot certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  --email your-email@example.com \
  --agree-tos \
  --no-eff-email \
  -d yourdomain.com \
  -d www.yourdomain.com
```

**Important**: Replace `your-email@example.com` with your actual email address.

### Step 4: Enable SSL Configuration

Once you have the certificate:

```bash
# Copy the SSL configuration
cp nginx/conf.d/app-ssl.conf.example nginx/conf.d/app.conf

# Update the domain in the SSL config
sed -i 's/yourdomain.com/YOUR_ACTUAL_DOMAIN/g' nginx/conf.d/app.conf

# Reload Nginx
docker-compose exec nginx nginx -s reload
```

### Step 5: Enable Auto-Renewal

The Certbot container is configured to automatically renew certificates. Start it:

```bash
docker-compose up -d certbot
```

This will check for renewal twice daily and renew certificates when they're close to expiration.

## Alternative: Manual Certbot Installation

If you prefer to use Certbot installed directly on your host system:

### Install Certbot

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install certbot

# CentOS/RHEL
sudo yum install certbot
```

### Obtain Certificate

```bash
sudo certbot certonly --standalone \
  --preferred-challenges http \
  -d yourdomain.com \
  -d www.yourdomain.com
```

### Update Docker Compose

Modify `docker-compose.yml` to mount the host's Let's Encrypt directory:

```yaml
nginx:
  volumes:
    - ./nginx/conf.d:/etc/nginx/conf.d:ro
    - /etc/letsencrypt:/etc/nginx/ssl:ro  # Mount host certificates
```

### Setup Auto-Renewal

```bash
# Test renewal
sudo certbot renew --dry-run

# Certbot automatically sets up a cron job for renewal
# Verify with:
sudo systemctl status certbot.timer
```

## Configuration Files Explained

### docker-compose.yml
- Defines three services: nginx, pdf-analyzer, and certbot
- Creates a shared network for inter-container communication
- Mounts volumes for SSL certificates and webroot verification

### nginx/conf.d/app.conf
- Initial HTTP-only configuration
- Includes `.well-known/acme-challenge/` location for Certbot verification
- Proxies requests to the PDF analyzer container

### nginx/conf.d/app-ssl.conf.example
- Full HTTPS configuration with SSL termination
- Redirects HTTP to HTTPS
- Includes security headers
- Configured for large PDF uploads (50MB max)

## Testing Your Setup

### Test HTTP (Before SSL)
```bash
curl http://yourdomain.com
```

### Test HTTPS (After SSL)
```bash
curl https://yourdomain.com
```

### Check SSL Certificate
```bash
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com
```

### Test SSL Grade
Visit: https://www.ssllabs.com/ssltest/analyze.html?d=yourdomain.com

## Troubleshooting

### Certificate Not Found
```bash
# Check if certificates exist
docker-compose exec nginx ls -la /etc/nginx/ssl/live/yourdomain.com/

# If missing, re-run certbot
docker-compose run --rm certbot certonly --webroot ...
```

### Nginx Won't Start
```bash
# Check Nginx configuration
docker-compose exec nginx nginx -t

# View Nginx logs
docker-compose logs nginx
```

### Port Already in Use
```bash
# Check what's using port 80/443
sudo netstat -tlnp | grep ':80\|:443'

# Stop conflicting services
sudo systemctl stop apache2  # or other web server
```

### Certificate Renewal Fails
```bash
# Manually renew
docker-compose run --rm certbot renew

# Check certbot logs
docker-compose logs certbot
```

## Security Best Practices

1. **Keep Certificates Secure**: The `nginx/ssl` directory contains private keys
   ```bash
   chmod 700 nginx/ssl
   ```

2. **Regular Updates**: Keep Docker images updated
   ```bash
   docker-compose pull
   docker-compose up -d
   ```

3. **Firewall Configuration**: Only expose necessary ports
   ```bash
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```

4. **Monitor Certificate Expiration**: Let's Encrypt certificates expire after 90 days
   - Certbot auto-renewal handles this
   - Set up monitoring to alert if renewal fails

## Production Deployment Checklist

- [ ] Domain DNS configured correctly
- [ ] Firewall ports 80 and 443 open
- [ ] SSL certificates obtained and installed
- [ ] HTTPS redirect working
- [ ] Auto-renewal configured
- [ ] Security headers enabled
- [ ] SSL test passes (A+ grade)
- [ ] Application accessible via HTTPS
- [ ] Certbot renewal tested

## Quick Commands Reference

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Restart Nginx
docker-compose restart nginx

# Obtain/Renew certificate
docker-compose run --rm certbot certonly --webroot -w /var/www/certbot -d yourdomain.com

# Test Nginx config
docker-compose exec nginx nginx -t

# Reload Nginx
docker-compose exec nginx nginx -s reload
```

## Support

For issues with:
- **Certbot**: https://certbot.eff.org/docs/
- **Nginx**: https://nginx.org/en/docs/
- **Let's Encrypt**: https://letsencrypt.org/docs/
