# PDF OCR Web Application

A modern web application for converting scanned PDFs into searchable and selectable text documents using OCR (Optical Character Recognition) technology.

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Features

- 🔍 **OCR Processing**: Convert scanned PDFs to searchable text using Tesseract OCR
- 📱 **Modern Web Interface**: Responsive Bootstrap 5 design with drag-and-drop functionality
- 🔒 **Privacy First**: All processing happens locally - your documents never leave your computer
- 🐳 **Docker Support**: Easy deployment with Docker and Docker Compose
- 📄 **PDF Generation**: Creates new PDFs with selectable and searchable text
- 🖼️ **Image Enhancement**: Automatic image optimization for better OCR accuracy
- 🧹 **Auto Cleanup**: Automatic removal of temporary files
- 🌐 **Multi-language**: Supports Spanish and English OCR (configurable for more languages)

## Quick Start

### Option 1: Docker (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/pdf-ocr-app.git
   cd pdf-ocr-app
   ```

2. **Run with Docker:**
   ```bash
   docker-compose up --build
   ```

3. **Open your browser** and go to `http://localhost:5000`

### Option 2: Local Installation

1. **Prerequisites:**
   - Python 3.7+
   - Tesseract OCR
   - Poppler Utils

2. **Install dependencies:**
   ```bash
   git clone https://github.com/your-username/pdf-ocr-app.git
   cd pdf-ocr-app
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

## Installation

### System Requirements

- **Python**: 3.7 or higher
- **Tesseract OCR**: Required for text recognition
- **Poppler Utils**: Required for PDF processing

### Installing System Dependencies

#### Windows
```bash
# Using Chocolatey (recommended)
choco install tesseract poppler

# Or download manually:
# Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
# Poppler: https://blog.alivate.com.au/poppler-windows/
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install tesseract-ocr poppler-utils
```

#### macOS
```bash
# Using Homebrew
brew install tesseract poppler
```

## Usage

1. **Upload a PDF**: Drag and drop your scanned PDF file into the upload area
2. **Process**: Click "Convert to Searchable PDF" and wait for processing
3. **Download**: Your searchable PDF will be ready for download

### Supported Features

- **Languages**: Spanish and English (configurable for more)
- **File Types**: PDF input, PDF output with searchable text
- **File Size**: No artificial limits (limited only by system resources)
- **Privacy**: All processing happens locally

## Configuration

### OCR Language Settings

Edit `app.py` to change OCR languages:

```python
# Default: Spanish + English
ocr_result = pytesseract.image_to_string(image, lang='spa+eng')

# For other languages, install language packs:
# Example: French + English
ocr_result = pytesseract.image_to_string(image, lang='fra+eng')
```

### Environment Variables

Create a `.env` file for custom configuration:

```env
FLASK_ENV=production
UPLOAD_FOLDER=uploads
DOWNLOAD_FOLDER=downloads
MAX_FILE_SIZE=50MB
OCR_LANGUAGE=spa+eng
```

## Project Structure

```
pdf-ocr-app/
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Web interface
├── static/
│   ├── css/              # Stylesheets
│   ├── js/               # JavaScript (app.js)
│   └── images/           # Static assets
├── uploads/              # Temporary upload directory
├── downloads/            # Processed files directory
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose setup
└── README.md           # This file
```

## API Reference

### Endpoints

- `GET /` - Main application interface
- `POST /upload` - Upload PDF file
- `GET /process/<file_id>` - Process uploaded PDF
- `GET /download/<filename>` - Download processed file
- `GET /status` - Check processing status

## Development

### Setting Up Development Environment

```bash
git clone https://github.com/your-username/pdf-ocr-app.git
cd pdf-ocr-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run in development mode
export FLASK_ENV=development  # On Windows: set FLASK_ENV=development
python app.py
```

### Running Tests

```bash
# Install test dependencies
pip install pytest flask-testing

# Run tests
pytest tests/
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## Troubleshooting

### Common Issues

**Tesseract not found:**
- Ensure Tesseract is installed and in your system PATH
- On Windows, you may need to add the installation directory to PATH manually

**PDF processing fails:**
- Check that Poppler utils are installed correctly
- Verify PDF file is not corrupted or password-protected

**Memory issues with large files:**
- Process files one at a time
- Ensure sufficient RAM is available
- Consider using Docker with memory limits

### Performance Tips

- **Better OCR Results**: Use high-resolution scanned documents
- **Faster Processing**: Smaller file sizes process quicker
- **Memory Usage**: Close other applications when processing large files

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) - OCR engine
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [pdf2image](https://github.com/Belval/pdf2image) - PDF to image conversion
- [Bootstrap](https://getbootstrap.com/) - UI framework

## Support

If you find this project helpful, please give it a ⭐ on GitHub!

For issues and questions, please use the [GitHub Issues](https://github.com/your-username/pdf-ocr-app/issues) page.