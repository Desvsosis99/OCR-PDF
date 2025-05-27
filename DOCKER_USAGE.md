# Script para ejecutar la aplicación OCR PDF con Docker

## Requisitos
- Docker Desktop instalado y ejecutándose
- Docker Compose (incluido con Docker Desktop)

## Comandos disponibles

### Construir y ejecutar la aplicación
```powershell
# Construir la imagen Docker
docker-compose build

# Ejecutar la aplicación
docker-compose up

# Ejecutar en segundo plano
docker-compose up -d
```

### Gestión del contenedor
```powershell
# Ver logs de la aplicación
docker-compose logs -f

# Detener la aplicación
docker-compose down

# Reconstruir y ejecutar (después de cambios en el código)
docker-compose up --build
```

### Comandos de desarrollo
```powershell
# Acceder al contenedor para debugging
docker-compose exec ocr-pdf bash

# Ver estado de los contenedores
docker-compose ps

# Reiniciar el servicio
docker-compose restart ocr-pdf
```

## Ventajas de usar Docker

✅ **Sin instalación manual** - Tesseract y Poppler se instalan automáticamente
✅ **Entorno consistente** - Funciona igual en cualquier sistema con Docker
✅ **Fácil deployment** - Un solo comando para ejecutar todo
✅ **Aislamiento** - No afecta tu sistema host
✅ **Escalabilidad** - Fácil de replicar y distribuir

## Acceso a la aplicación

Una vez ejecutado `docker-compose up`, la aplicación estará disponible en:
- http://localhost:5000

Los archivos se guardan en las carpetas locales `uploads/` y `downloads/` que se sincronizan con el contenedor.
