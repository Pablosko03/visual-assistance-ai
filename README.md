# Herramienta de Asistencia Visual con IA

## Descripción del Proyecto
Aplicación móvil que utiliza IA para detectar obstáculos en tiempo real, proporcionando feedback auditivo y/o háptico para ayudar a personas con visibilidad reducida a navegar de forma segura.

## Roadmap del Proyecto

### Fase 0: Preparación y Configuración del Entorno ✅
- [✅] Instalar Python (v3.9+), Git y VS Code
- [✅] Crear y activar un entorno virtual de Python
- [✅] Crear repositorio en GitHub
- [✅] Instalar librerías base: opencv-python, ultralytics, supervision, roboflow

### Fase 1: Prueba de Concepto (PoC) - Detección en Video
- [ ] Buscar y seleccionar dataset inicial desde Roboflow Universe
- [ ] Entrenar primer modelo YOLOv8
- [ ] Crear script detect_video.py
- [ ] Implementar anotaciones con supervision

### Fase 2: Prototipo Funcional (MVP) - Detección en Tiempo Real
- [ ] Modificar script para cámara en tiempo real
- [ ] Implementar sistema de alertas de voz
- [ ] Integrar seguimiento de objetos
- [ ] Definir zonas de peligro

### Fase 3: Pruebas de Campo y Validación
- [ ] Preparar prototipo para usuarios no técnicos
- [ ] Contactar organizaciones y reclutar probadores
- [ ] Realizar sesiones de prueba
- [ ] Recopilar y analizar feedback

### Fase 4: Optimización y Desarrollo Nativo
- [ ] Optimizar modelo (cuantización)
- [ ] Desarrollar aplicación nativa (iOS/Android)
- [ ] Diseñar UI accesible

### Fase 5: Despliegue y Mantenimiento
- [ ] Publicar en tiendas de apps
- [ ] Crear página web del proyecto
- [ ] Implementar sistema de monitorización

## Instalación

1. Clonar el repositorio
2. Crear entorno virtual: `python -m venv venv`
3. Activar entorno: `venv\Scripts\activate` (Windows) o `source venv/bin/activate` (Linux/Mac)
4. Instalar dependencias: `pip install -r requirements.txt`

## Estructura del Proyecto

```
visual-assistance-ai/
├── src/
│   ├── models/
│   ├── detection/
│   ├── audio/
│   └── utils/
├── data/
│   ├── datasets/
│   └── models/
├── tests/
├── docs/
└── requirements.txt
```

## Contribución
Este proyecto está diseñado para ayudar a personas con discapacidad visual. Las contribuciones son bienvenidas.

## Licencia
MIT License
