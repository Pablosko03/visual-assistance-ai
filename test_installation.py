"""
Script de verificación de instalación
Verifica que todas las dependencias estén correctamente instaladas.
"""

import sys
import importlib
from pathlib import Path

def test_import(module_name, description):
    """Prueba la importación de un módulo."""
    try:
        importlib.import_module(module_name)
        print(f"✅ {description}: OK")
        return True
    except ImportError as e:
        print(f"❌ {description}: ERROR - {e}")
        return False

def test_camera():
    """Prueba el acceso a la cámara."""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✅ Cámara: OK")
            cap.release()
            return True
        else:
            print("❌ Cámara: No se pudo abrir")
            return False
    except Exception as e:
        print(f"❌ Cámara: ERROR - {e}")
        return False

def test_tts():
    """Prueba el sistema de texto a voz."""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        print("✅ Sistema TTS: OK")
        engine.stop()
        return True
    except Exception as e:
        print(f"❌ Sistema TTS: ERROR - {e}")
        return False

def main():
    """Función principal de verificación."""
    print("🔍 Verificando instalación del Sistema de Asistencia Visual con IA")
    print("=" * 70)
    
    # Lista de módulos a verificar
    modules_to_test = [
        ("cv2", "OpenCV"),
        ("ultralytics", "YOLOv8 (Ultralytics)"),
        ("supervision", "Supervision"),
        ("roboflow", "Roboflow"),
        ("pyttsx3", "Text-to-Speech"),
        ("numpy", "NumPy"),
        ("PIL", "Pillow"),
    ]
    
    # Verificar importaciones
    print("\n📦 Verificando dependencias:")
    success_count = 0
    for module, description in modules_to_test:
        if test_import(module, description):
            success_count += 1
    
    print(f"\n📊 Dependencias: {success_count}/{len(modules_to_test)} OK")
    
    # Verificar hardware
    print("\n🔧 Verificando hardware:")
    camera_ok = test_camera()
    tts_ok = test_tts()
    
    # Verificar estructura del proyecto
    print("\n📁 Verificando estructura del proyecto:")
    required_paths = [
        "src/detection/detect_video.py",
        "src/detection/detect_realtime.py",
        "src/audio/voice_alerts.py",
        "src/utils/config.py",
        "examples/basic_detection.py",
        "docs/SETUP.md",
        "requirements.txt"
    ]
    
    structure_ok = 0
    for path in required_paths:
        if Path(path).exists():
            print(f"✅ {path}: OK")
            structure_ok += 1
        else:
            print(f"❌ {path}: NO ENCONTRADO")
    
    print(f"\n📊 Estructura: {structure_ok}/{len(required_paths)} OK")
    
    # Resumen final
    print("\n" + "=" * 70)
    print("📋 RESUMEN DE VERIFICACIÓN:")
    
    if success_count == len(modules_to_test) and camera_ok and tts_ok and structure_ok == len(required_paths):
        print("🎉 ¡INSTALACIÓN COMPLETA Y EXITOSA!")
        print("\n🚀 Próximos pasos:")
        print("   1. Ejecutar: python examples/basic_detection.py")
        print("   2. Probar detección en tiempo real")
        print("   3. Continuar con Fase 1 del roadmap")
    else:
        print("⚠️  INSTALACIÓN INCOMPLETA")
        print("\n🔧 Acciones recomendadas:")
        if success_count < len(modules_to_test):
            print("   - Reinstalar dependencias: pip install -r requirements.txt")
        if not camera_ok:
            print("   - Verificar conexión de cámara")
        if not tts_ok:
            print("   - Verificar sistema de audio")
        print("   - Consultar docs/SETUP.md para más ayuda")
    
    print("\n📚 Documentación disponible:")
    print("   - README.md: Información general del proyecto")
    print("   - docs/SETUP.md: Guía detallada de instalación")
    print("   - TODO.md: Estado actual y próximos pasos")

if __name__ == "__main__":
    main()
