#!/usr/bin/env python3
"""
Test básico del sistema de detección sin alertas de voz
"""

import cv2
import supervision as sv
from ultralytics import YOLO
import numpy as np

def test_basic_detection():
    """Prueba básica del sistema de detección."""
    print("🤖 Prueba Básica - Sistema de Detección")
    print("=" * 50)
    
    try:
        # Cargar modelo YOLO
        print("📱 Cargando modelo YOLOv8...")
        model = YOLO("yolov8n.pt")
        print("✅ Modelo cargado correctamente")
        
        # Configurar supervision
        print("🔧 Configurando supervision...")
        box_annotator = sv.BoxAnnotator(thickness=2)
        print("✅ Supervision configurado")
        
        # Crear imagen de prueba
        print("🖼️ Creando imagen de prueba...")
        test_image = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(test_image, "TEST IMAGE", (200, 240), 
                   cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        
        # Realizar detección
        print("🔍 Realizando detección...")
        results = model(test_image)[0]
        detections = sv.Detections.from_ultralytics(results)
        print(f"✅ Detección completada: {len(detections)} objetos encontrados")
        
        # Anotar imagen
        annotated_image = box_annotator.annotate(
            scene=test_image.copy(), detections=detections
        )
        
        # Guardar resultado
        cv2.imwrite("test_detection_result.jpg", annotated_image)
        print("✅ Resultado guardado en: test_detection_result.jpg")
        
        print("\n🎉 ¡Prueba básica completada exitosamente!")
        print("📊 Resumen:")
        print(f"   - Modelo YOLO: Funcionando")
        print(f"   - Supervision: Funcionando")
        print(f"   - Detecciones: {len(detections)} objetos")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        return False

if __name__ == "__main__":
    success = test_basic_detection()
    exit(0 if success else 1)
