# Guía de Configuración - Sistema de Asistencia Visual con IA

## Requisitos del Sistema

### Hardware Mínimo
- **CPU**: Intel i5 o AMD Ryzen 5 (o equivalente)
- **RAM**: 8 GB mínimo, 16 GB recomendado
- **Almacenamiento**: 2 GB de espacio libre
- **Cámara**: Webcam USB o cámara integrada
- **Audio**: Altavoces o auriculares para alertas de voz

### Hardware Recomendado
- **GPU**: NVIDIA GTX 1060 o superior (para mejor rendimiento)
- **CPU**: Intel i7 o AMD Ryzen 7
- **RAM**: 16 GB o más
- **Cámara**: Cámara HD (1080p) con buen rendimiento en condiciones de poca luz

### Software
- **Sistema Operativo**: Windows 10/11, macOS 10.15+, o Ubuntu 18.04+
- **Python**: 3.9 o superior
- **Git**: Para clonar el repositorio

## Instalación Paso a Paso

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/visual-assistance-ai.git
cd visual-assistance-ai
```

### 2. Crear Entorno Virtual

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Verificar Instalación

```bash
python -c "import cv2, ultralytics, supervision; print('✅ Instalación exitosa')"
```

## Configuración Inicial

### 1. Probar la Cámara

```bash
python -c "import cv2; cap = cv2.VideoCapture(0); print('✅ Cámara OK' if cap.isOpened() else '❌ Error de cámara'); cap.release()"
```

### 2. Probar Audio (TTS)

```bash
cd src/audio
python voice_alerts.py
```

### 3. Descargar Modelo Base

El modelo YOLOv8n se descargará automáticamente en la primera ejecución. Para descargarlo manualmente:

```bash
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

## Primeras Pruebas

### 1. Ejemplo Básico

```bash
python examples/basic_detection.py
```

### 2. Detección en Video

```bash
python src/detection/detect_video.py ruta/a/tu/video.mp4
```

### 3. Detección en Tiempo Real

```bash
python src/detection/detect_realtime.py
```

## Configuración Avanzada

### 1. Configurar GPU (NVIDIA)

Si tienes una GPU NVIDIA compatible:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 2. Configurar Múltiples Cámaras

Para usar una cámara específica:

```bash
python src/detection/detect_realtime.py --camera 1
```

### 3. Cambiar Idioma

Para usar el sistema en inglés:

```bash
python src/detection/detect_realtime.py --language en
```

## Solución de Problemas Comunes

### Error: "No se pudo abrir la cámara"

1. Verificar que la cámara no esté siendo usada por otra aplicación
2. Probar con diferentes IDs de cámara (0, 1, 2...)
3. En Linux, verificar permisos: `sudo usermod -a -G video $USER`

### Error: "ModuleNotFoundError"

1. Verificar que el entorno virtual esté activado
2. Reinstalar dependencias: `pip install -r requirements.txt`

### Audio no funciona

1. Verificar que los altavoces estén conectados
2. En Linux: `sudo apt-get install espeak espeak-data`
3. Probar con diferentes motores TTS

### Rendimiento lento

1. Usar modelo más ligero: `--model yolov8n.pt`
2. Reducir resolución de cámara
3. Cerrar otras aplicaciones que usen la GPU

### Error de permisos en Windows

Ejecutar como administrador o verificar permisos de la cámara en Configuración > Privacidad.

## Próximos Pasos

1. **Fase 1**: Probar detección en videos pregrabados
2. **Fase 2**: Usar detección en tiempo real con alertas
3. **Fase 3**: Entrenar modelo personalizado con Roboflow
4. **Fase 4**: Optimizar para dispositivos móviles

## Soporte

- **Documentación**: Ver carpeta `docs/`
- **Ejemplos**: Ver carpeta `examples/`
- **Issues**: Reportar problemas en GitHub
- **Comunidad**: Unirse al Discord del proyecto

---

¿Necesitas ayuda? Consulta la [documentación completa](../README.md) o abre un issue en GitHub.
