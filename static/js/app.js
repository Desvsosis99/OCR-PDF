// OCR PDF Application - JavaScript optimizado y limpio
class PDFOCRApp {
    constructor() {
        this.fileInput = document.getElementById('file-input');
        this.uploadArea = document.getElementById('upload-area');
        this.selectBtn = document.getElementById('select-file-btn');
        this.progressSection = document.getElementById('progress-section');
        this.resultsSection = document.getElementById('results-section');
        this.progressBar = document.getElementById('progress-bar');
        this.progressText = document.getElementById('progress-text');
        this.errorModal = new bootstrap.Modal(document.getElementById('errorModal'));
        this.processing = false;
        
        this.initialize();
    }

    initialize() {
        this.setupEvents();
        this.checkSystemStatus();
    }

    setupEvents() {
        // Eventos de archivo
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        this.selectBtn.addEventListener('click', () => this.fileInput.click());
        
        // Drag & Drop
        this.uploadArea.addEventListener('dragover', (e) => this.handleDragOver(e));
        this.uploadArea.addEventListener('dragleave', (e) => this.handleDragLeave(e));
        this.uploadArea.addEventListener('drop', (e) => this.handleDrop(e));
        
        // Click en área de upload
        this.uploadArea.addEventListener('click', (e) => {
            if (!this.selectBtn.contains(e.target)) {
                this.fileInput.click();
            }
        });
    }

    handleDragOver(e) {
        e.preventDefault();
        this.uploadArea.classList.add('dragover');
    }

    handleDragLeave(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('dragover');
    }

    handleDrop(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.processFile(files[0]);
        }
    }

    handleFileSelect(e) {
        const file = e.target.files[0];
        if (file) {
            this.processFile(file);
        }
    }

    async processFile(file) {
        if (this.processing) return;

        // Validaciones
        if (!file.type.includes('pdf')) {
            this.showError('Solo se permiten archivos PDF');
            return;
        }

        if (file.size > 50 * 1024 * 1024) {
            this.showError('Archivo muy grande. Máximo 50MB');
            return;
        }

        this.processing = true;

        try {
            // Subir archivo
            const uploadResult = await this.uploadFile(file);
            
            if (uploadResult.success) {
                this.showProgress();
                
                // Procesar OCR
                const processResult = await this.processOCR(uploadResult.filename);
                
                if (processResult.success) {
                    this.showResults(processResult);
                } else {
                    this.showError(processResult.error || 'Error procesando archivo');
                }
            } else {
                this.showError(uploadResult.error || 'Error subiendo archivo');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showError('Error de conexión. Intenta de nuevo.');
        } finally {
            this.processing = false;
            this.fileInput.value = '';
        }
    }

    async uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Error de red');
        }

        return await response.json();
    }

    async processOCR(filename) {
        this.updateProgress(20, 'Convirtiendo PDF a imágenes...');
        
        const response = await fetch(`/process/${filename}`);
        const result = await response.json();
        
        if (!response.ok) {
            if (result.installation_help) {
                this.showError(`${result.error}\n\n${result.installation_help}`);
            }
            throw new Error(result.error || 'Error procesando');
        }
        
        // Simular progreso para mejor UX
        this.updateProgress(60, 'Extrayendo texto con OCR...');
        await this.delay(1000);
        
        this.updateProgress(90, 'Creando PDF final...');
        await this.delay(500);
        
        this.updateProgress(100, 'Completado');
        
        return result;
    }

    showProgress() {
        this.hideAllSections();
        this.progressSection.classList.remove('d-none');
        this.progressSection.classList.add('fade-in');
        this.updateProgress(10, 'Iniciando...');
    }

    updateProgress(percent, message) {
        this.progressBar.style.width = `${percent}%`;
        this.progressBar.setAttribute('aria-valuenow', percent);
        this.progressText.textContent = message;
    }

    showResults(result) {
        this.hideAllSections();
        this.resultsSection.classList.remove('d-none');
        this.resultsSection.classList.add('fade-in');
        
        document.getElementById('pages-count').textContent = result.pages_processed;
        document.getElementById('download-link').href = result.download_url;
        
        this.resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    showError(message) {
        document.getElementById('error-message').textContent = message;
        this.errorModal.show();
        this.hideAllSections();
    }

    hideAllSections() {
        this.progressSection.classList.add('d-none');
        this.resultsSection.classList.add('d-none');
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async checkSystemStatus() {
        try {
            const response = await fetch('/status');
            const status = await response.json();
            
            const statusDiv = document.getElementById('system-status');
            let html = '';
            
            if (status.tesseract_available) {
                html += '<span class="badge bg-success me-2">✓ Tesseract OCR</span>';
            } else {
                html += '<span class="badge bg-danger me-2">✗ Tesseract OCR</span>';
            }
            
            if (status.poppler_available) {
                html += '<span class="badge bg-success me-2">✓ Poppler</span>';
            } else {
                html += '<span class="badge bg-danger me-2">✗ Poppler</span>';
            }
            
            if (status.status === 'ready') {
                html += '<span class="badge bg-success">Sistema listo</span>';
            } else {
                html += '<span class="badge bg-warning">Dependencias faltantes</span>';
            }
            
            statusDiv.innerHTML = html;
        } catch (error) {
            console.error('Error verificando estado:', error);
            document.getElementById('system-status').innerHTML = 
                '<span class="badge bg-secondary">Estado desconocido</span>';
        }
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new PDFOCRApp();
});

// Prevenir drag & drop en toda la página
document.addEventListener('dragover', e => e.preventDefault());
document.addEventListener('drop', e => e.preventDefault());
