# English PDF Analyzer

A web-based tool to analyze English vocabulary in PDF documents based on CEFR (Common European Framework of Reference for Languages) levels. Upload a PDF and get highlighted vocabulary with automatic glossary generation.

**Made by AAII**

## Features

- 📄 **PDF Analysis**: Upload PDFs and analyze vocabulary complexity
- 🎨 **Color-Coded Highlighting**: Words highlighted by CEFR level (A1-C2)
- 📚 **Automatic Glossary**: Generate glossaries with definitions
- 📊 **Statistics**: Visual breakdown of vocabulary levels
- 🔧 **Customizable**: Select specific CEFR levels to analyze
- 🌐 **Web Interface**: User-friendly dashboard

## Quick Start

### Option 1: Docker (Recommended)

```bash
# Pull and run the latest version
docker pull aaiiz/english-pdf-analyzer:latest
docker run -d -p 8080:8080 aaiiz/english-pdf-analyzer:latest

# Access at http://localhost:8080
```

### Option 2: Docker Compose (Production)

```bash
# Download configuration files from the repository
# Start services
docker-compose up -d

# Access at http://localhost (or your domain)
```

**For SSL/HTTPS setup:**

1. **Install Certbot:**
   ```bash
   # Ubuntu/Debian
   sudo apt update && sudo apt install certbot
   
   # CentOS/RHEL
   sudo yum install certbot
   ```

2. **Get SSL Certificate** (choose one method):

   **Option A: Standalone (recommended for VPS/dedicated servers)**
   ```bash
   sudo certbot certonly --standalone \
     -d yourdomain.com \
     --email your-email@example.com --agree-tos
   ```

   **Option B: DNS Challenge (for any server, works behind firewalls)**
   ```bash
   sudo certbot certonly --manual \
     --preferred-challenges=dns \
     -d yourdomain.com
   ```
   Follow the prompts to add a TXT record to your DNS.

3. **Update docker-compose.yml:**
   ```yaml
   nginx:
     volumes:
       - ./nginx/conf.d:/etc/nginx/conf.d:ro
       - /etc/letsencrypt:/etc/nginx/ssl:ro  # Add this line
   ```

4. **Enable HTTPS:**
   ```bash
   cp nginx/conf.d/app-ssl.conf.example nginx/conf.d/app.conf
   sed -i 's/yourdomain.com/YOUR_DOMAIN/g' nginx/conf.d/app.conf
   docker-compose restart nginx
   ```

5. **Access your site:** `https://yourdomain.com` 🔒

> **Note:** Certbot automatically sets up certificate renewal. Verify with `sudo systemctl status certbot.timer`

For detailed SSL setup, see [SSL_SETUP_GUIDE.md](SSL_SETUP_GUIDE.md)

### Option 3: Local Development

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Run the application
python app.py

# Access at http://localhost:8080
```

## Usage

1. **Upload a PDF**: Click "Choose PDF File" and select your document
2. **Select CEFR Levels**: Choose which levels to highlight (A1-C2)
3. **Configure Options**:
   - **Include Definitions**: Fetch word definitions (slower but more informative)
   - **Estimate Levels**: Use frequency-based estimation for unknown words
4. **Analyze**: Click "Analyze PDF" and wait for processing
5. **Download**: Download your analyzed PDF with highlights and glossary

## CEFR Levels

| Level | Description | Color |
|-------|-------------|-------|
| A1 | Beginner | Light Green |
| A2 | Elementary | Green |
| B1 | Intermediate | Light Yellow |
| B2 | Upper Intermediate | Orange |
| C1 | Advanced | Light Red |
| C2 | Proficiency | Red |

## CLI Usage

The tool also supports command-line usage:

```bash
python main.py input.pdf output.pdf --levels B2 C1 --include-definitions --estimate
```

**Options:**
- `--levels`: CEFR levels to analyze (default: all)
- `--include-definitions`: Include word definitions in glossary
- `--estimate`: Enable frequency-based level estimation

## Deployment

### Docker Hub

Pull the pre-built image:
```bash
docker pull aaiiz/english-pdf-analyzer:latest
docker run -d -p 8080:8080 aaiiz/english-pdf-analyzer:latest
```

### GitHub Actions CI/CD

The project includes automated Docker builds. To trigger a build:

```bash
# Create and push a version tag
git tag v1.0.0
git push origin v1.0.0
```

See [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) for details.

## Project Structure

```
english-pdf-analyser/
├── analyzer/              # Core analysis modules
│   ├── cefr.py           # CEFR level detection
│   ├── definitions.py    # Definition fetching
│   ├── extraction.py     # PDF text extraction
│   ├── nlp.py           # NLP processing
│   └── pdf_writer.py    # PDF generation
├── data/                 # CEFR word lists
├── nginx/               # Nginx configuration
├── templates/           # HTML templates
├── static/             # CSS and assets
├── app.py              # Flask web application
├── main.py             # CLI entry point
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose setup
└── requirements.txt    # Python dependencies
```

## Configuration

### Environment Variables

None required for basic usage. For production:
- Configure domain in `nginx/conf.d/app.conf`
- Set up SSL certificates (see SSL_SETUP_GUIDE.md)

### Customization

- **CEFR Dictionary**: Edit `data/cefr_dict.json` to add/modify word levels
- **Upload Limits**: Modify `client_max_body_size` in Nginx config
- **Timeouts**: Adjust proxy timeouts in Nginx config

## Documentation

- [SSL Setup Guide](SSL_SETUP_GUIDE.md) - HTTPS configuration with Certbot
- [Docker Compose Quick Start](DOCKER_COMPOSE_QUICKSTART.md) - Quick reference
- [GitHub Actions Setup](GITHUB_ACTIONS_SETUP.md) - CI/CD configuration
- [Docker Hub Setup](DOCKER_HUB_SETUP.md) - Publishing to Docker Hub

## Requirements

- Python 3.11+
- Docker (optional, for containerized deployment)
- Domain name (optional, for SSL/HTTPS)

## Dependencies

- Flask - Web framework
- PyMuPDF - PDF processing
- spaCy - NLP and lemmatization
- wordfreq - Word frequency analysis
- ReportLab - PDF generation
- Matplotlib - Statistics visualization

## License

See [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Author

**AAII**

## Support

For issues and questions:
- Check the documentation files
- Review existing GitHub issues
- Create a new issue with detailed information

---

**English PDF Analyzer** © 2026 | Made by AAII
