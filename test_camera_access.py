#!/usr/bin/env python3
"""
Test de acceso a cámara para el sistema de asistencia visual
"""

import cv2
import time

def test_camera_access():
    """Prueba el acceso a la cámara del sistema."""
    print("📹 Test de Acceso a Cámara")
    print("=" * 40)
    
    try:
        # Intentar abrir la cámara
        print("🔍 Intentando acceder a la cámara (ID: 0)...")
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ No se pudo acceder a la cámara principal (ID: 0)")
            print("🔍 Intentando con cámara ID: 1...")
            cap = cv2.VideoCapture(1)
            
            if not cap.isOpened():
                print("❌ No se pudo acceder a ninguna cámara")
                print("💡 Posibles causas:")
                print("   - No hay cámara conectada")
                print("   - Cámara en uso por otra aplicación")
                print("   - Permisos de acceso denegados")
                return False
        
        # Obtener información de la cámara
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        print(f"✅ Cámara accesible")
        print(f"📊 Resolución: {width}x{height}")
        print(f"🎬 FPS: {fps}")
        
        # Intentar capturar algunos frames
        print("📸 Probando captura de frames...")
        frames_captured = 0
        for i in range(5):
            ret, frame = cap.read()
            if ret:
                frames_captured += 1
                print(f"   Frame {i+1}: ✅ Capturado ({frame.shape})")
            else:
                print(f"   Frame {i+1}: ❌ Error en captura")
            time.sleep(0.1)
        
        cap.release()
        
        if frames_captured > 0:
            print(f"✅ Test completado: {frames_captured}/5 frames capturados")
            return True
        else:
            print("❌ No se pudieron capturar frames")
            return False
            
    except Exception as e:
        print(f"❌ Error durante el test: {e}")
        return False

def test_camera_settings():
    """Prueba diferentes configuraciones de cámara."""
    print("\n🔧 Test de Configuraciones de Cámara")
    print("=" * 45)
    
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Cámara no disponible para test de configuraciones")
            return False
        
        # Probar diferentes resoluciones
        resolutions = [(640, 480), (1280, 720), (1920, 1080)]
        
        for width, height in resolutions:
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            
            actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            if actual_width == width and actual_height == height:
                print(f"✅ Resolución {width}x{height}: Soportada")
            else:
                print(f"⚠️  Resolución {width}x{height}: No soportada (actual: {actual_width}x{actual_height})")
        
        cap.release()
        return True
        
    except Exception as e:
        print(f"❌ Error en test de configuraciones: {e}")
        return False

if __name__ == "__main__":
    print("🤖 Sistema de Asistencia Visual - Test de Cámara")
    print("=" * 55)
    
    # Test básico de acceso
    camera_ok = test_camera_access()
    
    # Test de configuraciones (solo si la cámara funciona)
    if camera_ok:
        settings_ok = test_camera_settings()
    else:
        settings_ok = False
    
    print("\n📋 Resumen de Tests:")
    print(f"   Acceso a cámara: {'✅ OK' if camera_ok else '❌ FALLO'}")
    print(f"   Configuraciones: {'✅ OK' if settings_ok else '❌ FALLO'}")
    
    if camera_ok:
        print("\n🎉 ¡Cámara lista para detección en tiempo real!")
    else:
        print("\n⚠️  La detección en tiempo real requerirá una cámara funcional")
    
    exit(0 if camera_ok else 1)
