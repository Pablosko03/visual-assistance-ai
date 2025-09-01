#!/usr/bin/env python3
"""
Test de integración completo del Sistema de Asistencia Visual
"""

import cv2
import supervision as sv
from ultralytics import YOLO
import numpy as np
import time
import sys
import os

# Añadir el directorio src al path
sys.path.append('src')

def test_full_pipeline():
    """Test completo del pipeline de detección."""
    print("🔄 Test de Pipeline Completo")
    print("=" * 35)
    
    try:
        # 1. Cargar modelo
        print("📱 Cargando modelo YOLOv8...")
        model = YOLO("yolov8n.pt")
        print("✅ Modelo cargado")
        
        # 2. Configurar supervision
        print("🔧 Configurando supervision...")
        box_annotator = sv.BoxAnnotator(thickness=2)
        print("✅ Supervision configurado")
        
        # 3. Configurar sistema de voz compatible
        print("🔊 Configurando sistema de voz...")
        from audio.compatible_voice import CompatibleVoiceSystem
        voice_system = CompatibleVoiceSystem(language='es')
        print("✅ Sistema de voz configurado")
        
        # 4. Crear imagen de prueba con objetos simulados
        print("🖼️ Creando imagen de prueba con objetos...")
        test_image = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Simular algunos objetos (rectángulos de colores)
        cv2.rectangle(test_image, (100, 100), (200, 200), (255, 0, 0), -1)  # Azul
        cv2.rectangle(test_image, (300, 150), (400, 250), (0, 255, 0), -1)  # Verde
        cv2.rectangle(test_image, (450, 200), (550, 300), (0, 0, 255), -1)  # Rojo
        
        cv2.putText(test_image, "INTEGRATION TEST", (150, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # 5. Realizar detección
        print("🔍 Realizando detección...")
        results = model(test_image)[0]
        
        # Crear detecciones manualmente para compatibilidad
        if hasattr(results, 'boxes') and results.boxes is not None:
            boxes = results.boxes.xyxy.cpu().numpy()
            confidences = results.boxes.conf.cpu().numpy()
            class_ids = results.boxes.cls.cpu().numpy().astype(int)
            
            detections = sv.Detections(
                xyxy=boxes,
                confidence=confidences,
                class_id=class_ids
            )
        else:
            detections = sv.Detections.empty()
        
        print(f"✅ Detección completada: {len(detections)} objetos")
        
        # 6. Procesar detecciones y generar alertas
        if len(detections) > 0:
            print("🚨 Generando alertas...")
            for i, (bbox, class_id, confidence) in enumerate(
                zip(detections.xyxy, detections.class_id, detections.confidence)
            ):
                # Calcular área para estimar distancia
                x1, y1, x2, y2 = bbox
                area = (x2 - x1) * (y2 - y1)
                
                if area > 10000:
                    distance = "cerca"
                elif area > 5000:
                    distance = "distancia media"
                else:
                    distance = "lejos"
                
                alert_text = f"Objeto detectado a {distance}"
                print(f"   🔊 Alerta {i+1}: {alert_text}")
                voice_system.speak(alert_text)
        else:
            print("ℹ️  No se detectaron objetos")
            voice_system.speak("No se detectaron obstáculos")
        
        # 7. Anotar imagen
        print("🎨 Anotando imagen...")
        annotated_image = box_annotator.annotate(
            scene=test_image.copy(), detections=detections
        )
        
        # Añadir información de estado
        cv2.putText(annotated_image, f"Detecciones: {len(detections)}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(annotated_image, "Sistema Activo", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # 8. Guardar resultado
        cv2.imwrite("integration_test_result.jpg", annotated_image)
        print("✅ Resultado guardado en: integration_test_result.jpg")
        
        # 9. Limpiar recursos
        voice_system.stop()
        
        return True
        
    except Exception as e:
        print(f"❌ Error en pipeline: {e}")
        return False

def test_zone_detection():
    """Test del sistema de zonas de peligro."""
    print("\n🚧 Test de Zonas de Peligro")
    print("=" * 35)
    
    try:
        # Crear zona de peligro
        width, height = 640, 480
        margin_x = width // 4
        margin_y = height // 4
        
        danger_zone_points = np.array([
            [margin_x, margin_y],
            [width - margin_x, margin_y],
            [width - margin_x, height - margin_y],
            [margin_x, height - margin_y]
        ])
        
        danger_zone = sv.PolygonZone(
            polygon=danger_zone_points,
            frame_resolution_wh=(width, height)
        )
        print("✅ Zona de peligro creada")
        
        # Simular detecciones en diferentes posiciones
        test_detections = [
            [100, 100, 150, 150],  # Fuera de zona
            [200, 200, 250, 250],  # Dentro de zona
            [500, 300, 550, 350],  # Fuera de zona
        ]
        
        detections = sv.Detections(
            xyxy=np.array(test_detections),
            confidence=np.array([0.8, 0.9, 0.7]),
            class_id=np.array([0, 0, 0])
        )
        
        # Verificar objetos en zona de peligro
        objects_in_danger = danger_zone.trigger(detections)
        danger_count = sum(objects_in_danger)
        
        print(f"✅ Test completado: {danger_count}/3 objetos en zona de peligro")
        return True
        
    except Exception as e:
        print(f"❌ Error en test de zonas: {e}")
        return False

def test_performance():
    """Test de rendimiento del sistema."""
    print("\n⚡ Test de Rendimiento")
    print("=" * 25)
    
    try:
        model = YOLO("yolov8n.pt")
        test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        
        # Medir tiempo de inferencia
        times = []
        for i in range(5):
            start_time = time.time()
            results = model(test_image)[0]
            end_time = time.time()
            times.append(end_time - start_time)
        
        avg_time = sum(times) / len(times)
        fps = 1.0 / avg_time
        
        print(f"✅ Tiempo promedio: {avg_time:.3f}s")
        print(f"✅ FPS estimado: {fps:.1f}")
        
        if fps >= 10:
            print("🎉 Rendimiento excelente para tiempo real")
        elif fps >= 5:
            print("👍 Rendimiento aceptable")
        else:
            print("⚠️  Rendimiento bajo - considerar optimización")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test de rendimiento: {e}")
        return False

def main():
    """Función principal de testing de integración."""
    print("🤖 Sistema de Asistencia Visual - Test de Integración")
    print("=" * 65)
    
    # Ejecutar todos los tests
    tests_results = {
        "Pipeline Completo": test_full_pipeline(),
        "Zonas de Peligro": test_zone_detection(),
        "Rendimiento": test_performance()
    }
    
    # Resumen final
    print("\n📋 Resumen Final de Tests:")
    print("=" * 35)
    
    passed = 0
    total = len(tests_results)
    
    for test_name, result in tests_results.items():
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n📊 Resultado: {passed}/{total} tests pasaron")
    
    if passed == total:
        print("🎉 ¡Todos los tests de integración pasaron!")
        print("🚀 Sistema listo para Fase 1 (Proof of Concept)")
    elif passed >= total * 0.7:
        print("👍 La mayoría de tests pasaron - sistema funcional")
        print("🔧 Revisar tests fallidos para optimización")
    else:
        print("⚠️  Varios tests fallaron - revisar configuración")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
