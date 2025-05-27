#!/usr/bin/env python3
"""
Aplicación OCR PDF optimizada - Similar a iLovePDF OCR
Convierte PDFs escaneados a PDFs con texto seleccionable y buscable
"""

import os
import uuid
import tempfile
import shutil
import atexit
import time
from flask import Flask, render_template, request, send_file, jsonify, url_for
from werkzeug.utils import secure_filename
import pytesseract
from pdf2image import convert_from_path
from pdf2image.exceptions import PDFInfoNotInstalledError
from PIL import Image, ImageEnhance, ImageFilter
from PyPDF2 import PdfWriter, PdfReader
import subprocess

# Configuración de Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ocr-pdf-secret-key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DOWNLOAD_FOLDER'] = 'downloads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB máximo

# Crear directorios necesarios
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

# Lista global para archivos temporales
temp_files = []

def cleanup_temp_files():
    """Limpiar archivos temporales al cerrar la aplicación"""
    for file_path in temp_files:
        try:
            if os.path.exists(file_path):
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                else:
                    os.remove(file_path)
        except Exception:
            pass

# Registrar limpieza al cerrar
atexit.register(cleanup_temp_files)

def check_tesseract():
    """Verificar si Tesseract OCR está disponible"""
    try:
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def check_poppler():
    """Verificar si Poppler está disponible"""
    try:
        result = subprocess.run(['pdftoppm', '-v'], 
                              capture_output=True, text=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

# Verificar dependencias
TESSERACT_OK = check_tesseract()
POPPLER_OK = check_poppler()

# Configuración de archivos permitidos
ALLOWED_EXTENSIONS = {'pdf'}

def is_allowed_file(filename):
    """Verificar si el archivo tiene extensión permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clean_old_files():
    """Limpiar archivos antiguos (más de 1 hora)"""
    current_time = time.time()
    for folder in [app.config['UPLOAD_FOLDER'], app.config['DOWNLOAD_FOLDER']]:
        try:
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path):
                    if current_time - os.path.getmtime(file_path) > 3600:  # 1 hora
                        os.remove(file_path)
        except Exception as e:
            print(f"Error limpiando archivos: {e}")

@app.route('/')
def index():
    """Página principal"""
    clean_old_files()
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Subir archivo PDF para procesar"""
    if 'file' not in request.files:
        return jsonify({'error': 'No se seleccionó archivo'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No se seleccionó archivo'}), 400
    
    if not is_allowed_file(file.filename):
        return jsonify({'error': 'Solo se permiten archivos PDF'}), 400
    
    try:
        # Generar nombre único
        unique_filename = f"{uuid.uuid4()}_{secure_filename(file.filename)}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        return jsonify({
            'success': True,
            'filename': unique_filename,
            'process_url': url_for('process_pdf', filename=unique_filename)
        })
    except Exception as e:
        print(f"Error subiendo archivo: {e}")
        return jsonify({'error': 'Error guardando archivo'}), 500

@app.route('/process/<filename>')
def process_pdf(filename):
    """Procesar PDF con OCR"""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'Archivo no encontrado'}), 404
    
    if not TESSERACT_OK:
        return jsonify({
            'error': 'Tesseract OCR no disponible',
            'installation_help': 'Instala Tesseract OCR en el container'
        }), 500
    
    if not POPPLER_OK:
        return jsonify({
            'error': 'Poppler no disponible',
            'installation_help': 'Instala Poppler en el container'
        }), 500
    
    try:
        print(f"🔄 Procesando PDF: {filename}")
        
        # Convertir PDF a imágenes
        images = convert_from_path(filepath, dpi=300, fmt='png')
        print(f"📄 PDF convertido: {len(images)} páginas")
        
        # Crear PDF con OCR
        output_filename = f"ocr_{filename}"
        output_path = os.path.join(app.config['DOWNLOAD_FOLDER'], output_filename)
        
        success = create_ocr_pdf(images, output_path)
        
        if success:
            # Limpiar archivo original
            try:
                os.remove(filepath)
            except:
                pass
            
            return jsonify({
                'success': True,
                'download_url': url_for('download_file', filename=output_filename),
                'pages_processed': len(images),
                'message': f'PDF procesado exitosamente: {len(images)} páginas'
            })
        else:
            return jsonify({'error': 'Error creando PDF con OCR'}), 500
        
    except PDFInfoNotInstalledError:
        return jsonify({
            'error': 'Poppler no instalado correctamente',
            'installation_help': 'Reinstala el container Docker'
        }), 500
    except Exception as e:
        print(f"❌ Error procesando: {e}")
        return jsonify({'error': f'Error procesando archivo: {str(e)}'}), 500

def enhance_image_for_ocr(image):
    """Mejorar imagen para mejor OCR (similar a iLovePDF)"""
    try:
        # Convertir a RGB si es necesario
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Mejorar contraste ligeramente
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.1)
        
        # Mejorar nitidez
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.05)
        
        # Reducir ruido con filtro suave
        image = image.filter(ImageFilter.MedianFilter(size=3))
        
        return image
    except Exception as e:
        print(f"⚠️ Error mejorando imagen: {e}")
        return image

def create_ocr_pdf(images, output_path):
    """Crear PDF con OCR optimizado (estilo iLovePDF)"""
    temp_dir = None
    try:
        print("🔍 Creando PDF con OCR...")
        
        # Crear directorio temporal
        temp_dir = tempfile.mkdtemp()
        temp_files.append(temp_dir)
        
        page_pdfs = []
        
        for i, image in enumerate(images):
            print(f"📝 Procesando página {i + 1}/{len(images)}")
            
            # Mejorar imagen para OCR
            image = enhance_image_for_ocr(image)
            
            # Rutas temporales
            temp_img_path = os.path.join(temp_dir, f'page_{i}.png')
            temp_pdf_path = os.path.join(temp_dir, f'page_{i}.pdf')
            
            # Guardar imagen optimizada
            image.save(temp_img_path, 'PNG', dpi=(300, 300), optimize=True)
            
            try:
                # Configuración optimizada de Tesseract para PDFs
                config = r'--oem 3 --psm 1 -c tessedit_create_pdf=1'
                
                # Crear PDF con OCR usando Tesseract
                pdf_bytes = pytesseract.image_to_pdf_or_hocr(
                    temp_img_path,
                    lang='spa+eng',  # Español e Inglés
                    extension='pdf',
                    config=config
                )
                
                if pdf_bytes and len(pdf_bytes) > 1000:
                    with open(temp_pdf_path, 'wb') as f:
                        f.write(pdf_bytes)
                    page_pdfs.append(temp_pdf_path)
                    print(f"✅ Página {i + 1} procesada")
                else:
                    print(f"⚠️ Página {i + 1} generó PDF pequeño")
                    
            except Exception as e:
                print(f"❌ Error en página {i + 1}: {e}")
                continue
        
        if not page_pdfs:
            print("❌ No se pudieron procesar páginas")
            return False
        
        # Combinar PDFs
        print(f"📋 Combinando {len(page_pdfs)} páginas...")
        return merge_pdf_pages(page_pdfs, output_path)
        
    except Exception as e:
        print(f"❌ Error en create_ocr_pdf: {e}")
        return False
    finally:
        # Limpiar directorio temporal
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except:
                pass

def merge_pdf_pages(pdf_files, output_path):
    """Combinar páginas PDF de manera eficiente"""
    try:
        writer = PdfWriter()
        
        for pdf_file in pdf_files:
            if os.path.exists(pdf_file):
                try:
                    with open(pdf_file, 'rb') as f:
                        reader = PdfReader(f)
                        for page in reader.pages:
                            writer.add_page(page)
                except Exception as e:
                    print(f"⚠️ Error leyendo {pdf_file}: {e}")
                    continue
        
        # Escribir PDF final
        with open(output_path, 'wb') as f:
            writer.write(f)
        
        print(f"✅ PDF combinado: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error combinando PDFs: {e}")
        return False

@app.route('/download/<filename>')
def download_file(filename):
    """Descargar archivo procesado"""
    try:
        file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=filename)
        else:
            return jsonify({'error': 'Archivo no encontrado'}), 404
    except Exception as e:
        print(f"❌ Error descargando: {e}")
        return jsonify({'error': 'Error descargando archivo'}), 500

@app.route('/status')
def status():
    """Estado del sistema"""
    return jsonify({
        'tesseract_available': TESSERACT_OK,
        'poppler_available': POPPLER_OK,
        'status': 'ready' if TESSERACT_OK and POPPLER_OK else 'dependencies_missing',
        'system': 'Docker Container' if os.path.exists('/.dockerenv') else 'Local',
        'version': '2.0'
    })

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 PDF OCR Application - Estilo iLovePDF")
    print("=" * 50)
    print(f"✅ Tesseract OCR: {'Disponible' if TESSERACT_OK else '❌ No disponible'}")
    print(f"✅ Poppler: {'Disponible' if POPPLER_OK else '❌ No disponible'}")
    
    if not TESSERACT_OK:
        print("⚠️  ADVERTENCIA: Tesseract OCR no está disponible")
    if not POPPLER_OK:
        print("⚠️  ADVERTENCIA: Poppler no está disponible")
    
    if TESSERACT_OK and POPPLER_OK:
        print("🎉 Sistema listo para procesar PDFs")
    
    # Limpiar archivos antiguos al iniciar
    clean_old_files()
    
    print("🌐 Iniciando servidor en http://localhost:5000")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=False)
