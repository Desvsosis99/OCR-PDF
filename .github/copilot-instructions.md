<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# PDF OCR Application Instructions

Este es un proyecto Flask para aplicación web de OCR en archivos PDF.

## Tecnologías utilizadas:
- Flask para el backend web
- Tesseract OCR para reconocimiento óptico de caracteres
- pdf2image para convertir PDF a imágenes
- reportlab para generar PDFs con texto searchable
- Bootstrap para UI moderna y responsive

## Estructura del proyecto:
- `app.py`: Aplicación Flask principal
- `templates/`: Templates HTML
- `static/`: Archivos CSS, JS e imágenes
- `uploads/`: Directorio temporal para archivos subidos
- `downloads/`: Directorio para archivos procesados

## Funcionalidades:
- Subida de archivos PDF mediante drag & drop
- Procesamiento OCR de PDFs escaneados
- Generación de PDFs con texto seleccionable y buscable
- Descarga de archivos procesados
- Interfaz web moderna y responsive
