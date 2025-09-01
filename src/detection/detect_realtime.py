"""
Real-time Detection Script - Phase 2 MVP
Detecta obstáculos en tiempo real usando la cámara y proporciona alertas de voz.
"""

import cv2
import supervision as sv
from ultralytics import YOLO
import argparse
import time
import numpy as np
from typing import Dict, List, Tuple, Optional
import sys
import os

# Añadir el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from audio.voice_alerts import VoiceAlertSystem, AlertPriority
try:
    from audio.compatible_voice import CompatibleVoiceSystem
    VOICE_SYSTEM_AVAILABLE = True
except ImportError:
    VOICE_SYSTEM_AVAILABLE = False
    print("⚠️ Sistema de voz no disponible")


class RealTimeObstacleDetector:
    """
    Detector de obstáculos en tiempo real con alertas de voz y seguimiento.
    """
    
    def __init__(self, model_path="yolov8n.pt", camera_id=0, language='es'):
        """
        Inicializa el detector en tiempo real.
        
        Args:
            model_path (str): Ruta al modelo YOLO
            camera_id (int): ID de la cámara (0 para cámara por defecto)
            language (str): Idioma para alertas ('es' o 'en')
        """
        # Inicializar modelo YOLO
        self.model = YOLO(model_path)
        
        # Configurar cámara
        self.camera_id = camera_id
        self.cap = None
        
        # Configurar anotadores (compatible con supervision v0.11.1)
        self.box_annotator = sv.BoxAnnotator(thickness=2)
        
        # Tracking no disponible en supervision v0.11.1
        # self.tracker = sv.ByteTrack()
        
        # Sistema de alertas de voz
        if VOICE_SYSTEM_AVAILABLE:
            self.alert_system = CompatibleVoiceSystem(language=language)
        else:
            self.alert_system = None
        
        # Zona de peligro (centro de la pantalla)
        self.danger_zone = None
        self.zone_annotator = None
        
        # Clases de obstáculos relevantes (COCO dataset)
        self.obstacle_classes = {
            0: "person",      # persona
            1: "bicycle",     # bicicleta
            2: "car",         # coche
            3: "motorcycle",  # motocicleta
            5: "bus",         # autobús
            7: "truck",       # camión
            15: "cat",        # gato
            16: "dog",        # perro
            24: "backpack",   # mochila
            26: "handbag",    # bolso
            28: "suitcase",   # maleta
            39: "bottle",     # botella
            41: "cup",        # taza
            56: "chair",      # silla
            57: "couch",      # sofá
            58: "potted plant", # planta
            60: "dining table", # mesa
            72: "tv",         # televisión
        }
        
        # Estadísticas
        self.frame_count = 0
        self.fps_counter = 0
        self.fps_start_time = time.time()
        self.current_fps = 0
        
        # Control de alertas
        self.last_detection_time = {}
        self.detection_cooldown = 2.0  # segundos
    
    def setup_camera(self):
        """Configura y abre la cámara."""
        self.cap = cv2.VideoCapture(self.camera_id)
        
        if not self.cap.isOpened():
            raise ValueError(f"No se pudo abrir la cámara {self.camera_id}")
        
        # Configurar resolución (opcional)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Obtener dimensiones reales
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        print(f"Cámara configurada: {width}x{height}")
        
        # Configurar zona de peligro (centro de la pantalla)
        margin_x = width // 4
        margin_y = height // 4
        danger_zone_points = np.array([
            [margin_x, margin_y],
            [width - margin_x, margin_y],
            [width - margin_x, height - margin_y],
            [margin_x, height - margin_y]
        ])
        
        self.danger_zone = sv.PolygonZone(polygon=danger_zone_points)
        # Usar color RGB en lugar de sv.Color.RED para compatibilidad
        try:
            self.zone_annotator = sv.PolygonZoneAnnotator(
                zone=self.danger_zone, color=(255, 0, 0), thickness=2, 
                text_thickness=1, text_scale=0.5
            )
        except:
            # Fallback si hay problemas con el anotador
            self.zone_annotator = None
        
        return width, height
    
    def calculate_distance_estimate(self, bbox_area: float, object_type: str) -> str:
        """
        Estima la distancia basada en el área del bounding box.
        
        Args:
            bbox_area (float): Área del bounding box
            object_type (str): Tipo de objeto
            
        Returns:
            str: Estimación de distancia
        """
        # Valores aproximados basados en el área del bbox
        if bbox_area > 50000:  # Muy cerca
            return "muy cerca"
        elif bbox_area > 20000:  # Cerca
            return "cerca"
        elif bbox_area > 5000:   # Distancia media
            return "distancia media"
        else:  # Lejos
            return "lejos"
    
    def process_detections(self, detections: sv.Detections, frame_shape: Tuple[int, int]) -> sv.Detections:
        """
        Procesa las detecciones y genera alertas.
        
        Args:
            detections: Detecciones de YOLO
            frame_shape: Forma del frame (height, width)
            
        Returns:
            sv.Detections: Detecciones filtradas y procesadas
        """
        if len(detections) == 0:
            return detections
        
        # Filtrar solo obstáculos relevantes
        obstacle_mask = [
            class_id in self.obstacle_classes 
            for class_id in detections.class_id
        ]
        detections = detections[obstacle_mask]
        
        if len(detections) == 0:
            return detections
        
        # Verificar objetos en zona de peligro
        objects_in_danger_zone = self.danger_zone.trigger(detections)
        
        # Procesar cada detección (sin tracking por compatibilidad)
        current_time = time.time()
        objects_detected = []
        
        for i, (bbox, class_id, confidence) in enumerate(
            zip(detections.xyxy, detections.class_id, detections.confidence)
        ):
            object_type = self.obstacle_classes.get(class_id, 'unknown')
            objects_detected.append(object_type)
            
            # Calcular área del bbox para estimar distancia
            x1, y1, x2, y2 = bbox
            bbox_area = (x2 - x1) * (y2 - y1)
            distance_estimate = self.calculate_distance_estimate(bbox_area, object_type)
            
            # Verificar si el objeto está en zona de peligro
            in_danger_zone = objects_in_danger_zone[i] if i < len(objects_in_danger_zone) else False
            
            # Control de cooldown para alertas (simplificado sin tracking)
            alert_key = f"{object_type}_{i}"
            should_alert = (
                alert_key not in self.last_detection_time or 
                current_time - self.last_detection_time[alert_key] > self.detection_cooldown
            )
            
            if should_alert:
                self.last_detection_time[alert_key] = current_time
                
                # Generar alerta de voz
                if self.alert_system:
                    alert_text = f"Obstáculo detectado: {object_type} a {distance_estimate}"
                    self.alert_system.speak(alert_text)
        
        return detections
    
    def update_fps(self):
        """Actualiza el contador de FPS."""
        self.fps_counter += 1
        current_time = time.time()
        
        if current_time - self.fps_start_time >= 1.0:
            self.current_fps = self.fps_counter
            self.fps_counter = 0
            self.fps_start_time = current_time
    
    def annotate_frame(self, frame: np.ndarray, detections: sv.Detections) -> np.ndarray:
        """
        Anota el frame con las detecciones y información adicional.
        
        Args:
            frame: Frame original
            detections: Detecciones procesadas
            
        Returns:
            np.ndarray: Frame anotado
        """
        # Anotar zona de peligro
        if self.zone_annotator:
            annotated_frame = self.zone_annotator.annotate(scene=frame.copy())
        else:
            annotated_frame = frame.copy()
            # Dibujar zona de peligro manualmente
            if self.danger_zone:
                cv2.polylines(annotated_frame, [self.danger_zone.polygon.astype(int)], 
                             True, (0, 0, 255), 2)
        
        if len(detections) > 0:
            # Crear etiquetas (sin tracking)
            labels = []
            for i, (class_id, confidence) in enumerate(
                zip(detections.class_id, detections.confidence)
            ):
                object_name = self.obstacle_classes.get(class_id, 'unknown')
                label = f"{object_name} #{i} {confidence:.2f}"
                labels.append(label)
            
            # Anotar cajas (compatible con supervision v0.11.1)
            annotated_frame = self.box_annotator.annotate(
                scene=annotated_frame, detections=detections
            )
            
            # Añadir etiquetas manualmente usando OpenCV
            for i, (bbox, label) in enumerate(zip(detections.xyxy, labels)):
                x1, y1, x2, y2 = bbox.astype(int)
                cv2.putText(annotated_frame, label, (x1, y1 - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Añadir información de estado
        cv2.putText(annotated_frame, f"FPS: {self.current_fps}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(annotated_frame, f"Obstaculos: {len(detections)}", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(annotated_frame, "Presiona 'q' para salir", (10, annotated_frame.shape[0] - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return annotated_frame
    
    def run(self, show_preview=True, save_output=None):
        """
        Ejecuta el detector en tiempo real.
        
        Args:
            show_preview (bool): Mostrar ventana de preview
            save_output (str): Ruta para guardar video (opcional)
        """
        try:
            # Configurar cámara
            width, height = self.setup_camera()
            
            # Configurar grabación si se especifica
            writer = None
            if save_output:
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                writer = cv2.VideoWriter(save_output, fourcc, 20.0, (width, height))
            
            print("🚀 Iniciando detección en tiempo real...")
            print("📹 Presiona 'q' para salir")
            print("🔊 Sistema de alertas de voz activado")
            
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("Error: No se pudo leer frame de la cámara")
                    break
                
                # Realizar detección
                results = self.model(frame)[0]
                detections = sv.Detections.from_ultralytics(results)
                
                # Procesar detecciones
                detections = self.process_detections(detections, frame.shape[:2])
                
                # Anotar frame
                annotated_frame = self.annotate_frame(frame, detections)
                
                # Guardar frame si se especifica
                if writer:
                    writer.write(annotated_frame)
                
                # Mostrar preview
                if show_preview:
                    cv2.imshow('Detección de Obstáculos - Asistencia Visual', annotated_frame)
                    
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        break
                
                # Actualizar estadísticas
                self.frame_count += 1
                self.update_fps()
        
        except KeyboardInterrupt:
            print("\n🛑 Deteniendo detección...")
        
        except Exception as e:
            print(f"❌ Error durante la detección: {e}")
        
        finally:
            # Limpiar recursos
            if self.cap:
                self.cap.release()
            if writer:
                writer.release()
            if show_preview:
                cv2.destroyAllWindows()
            
            if self.alert_system:
                self.alert_system.stop()
            print("✅ Recursos liberados correctamente")


def main():
    """Función principal para ejecutar el detector desde línea de comandos."""
    parser = argparse.ArgumentParser(description="Detector de obstáculos en tiempo real")
    parser.add_argument("-m", "--model", default="yolov8n.pt", 
                       help="Ruta del modelo YOLO (default: yolov8n.pt)")
    parser.add_argument("-c", "--camera", type=int, default=0, 
                       help="ID de la cámara (default: 0)")
    parser.add_argument("-l", "--language", choices=['es', 'en'], default='es',
                       help="Idioma para alertas (default: es)")
    parser.add_argument("--no-preview", action="store_true", 
                       help="No mostrar ventana de preview")
    parser.add_argument("-o", "--output", help="Guardar video de salida")
    
    args = parser.parse_args()
    
    print("🤖 Iniciando Sistema de Asistencia Visual con IA")
    print(f"📱 Modelo: {args.model}")
    print(f"📹 Cámara: {args.camera}")
    print(f"🗣️ Idioma: {args.language}")
    
    # Crear detector
    detector = RealTimeObstacleDetector(
        model_path=args.model,
        camera_id=args.camera,
        language=args.language
    )
    
    # Ejecutar detección
    detector.run(
        show_preview=not args.no_preview,
        save_output=args.output
    )


if __name__ == "__main__":
    main()
