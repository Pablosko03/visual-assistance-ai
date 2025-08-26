"""
Ejemplo básico de detección de obstáculos.
Este script demuestra cómo usar el sistema de detección básico.
"""

import sys
import os

# Añadir el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from detection.detect_realtime import RealTimeObstacleDetector


def main():
    """Ejemplo básico de uso del detector en tiempo real."""
    
    print("🤖 Ejemplo Básico - Sistema de Asistencia Visual")
    print("=" * 50)
    
    # Crear detector con configuración básica
    detector = RealTimeObstacleDetector(
        model_path="yolov8n.pt",  # Modelo ligero para pruebas
        camera_id=0,              # Cámara por defecto
        language='es'             # Español
    )
    
    print("📋 Configuración:")
    print("   - Modelo: YOLOv8 Nano (ligero)")
    print("   - Cámara: ID 0 (por defecto)")
    print("   - Idioma: Español")
    print("   - Alertas de voz: Activadas")
    print()
    
    print("🎯 Instrucciones:")
    print("   - Presiona 'q' para salir")
    print("   - El rectángulo rojo es la zona de peligro")
    print("   - Los objetos en esta zona generarán alertas prioritarias")
    print()
    
    input("Presiona Enter para comenzar...")
    
    try:
        # Ejecutar detección
        detector.run(show_preview=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Detenido por el usuario")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        print("✅ Ejemplo completado")


if __name__ == "__main__":
    main()
