"""
Video Detection Script - Phase 1 PoC
Detecta obstáculos en videos pregrabados usando YOLOv8 y supervision.
"""

import cv2
import supervision as sv
from ultralytics import YOLO
import argparse
import os
from pathlib import Path


class VideoObstacleDetector:
    """
    Detector de obstáculos en video usando YOLOv8.
    """
    
    def __init__(self, model_path="yolov8n.pt"):
        """
        Inicializa el detector con el modelo especificado.
        
        Args:
            model_path (str): Ruta al modelo YOLO (.pt file)
        """
        self.model = YOLO(model_path)
        self.box_annotator = sv.BoxAnnotator(thickness=2, text_thickness=1, text_scale=0.5)
        
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
    
    def detect_obstacles(self, frame):
        """
        Detecta obstáculos en un frame individual.
        
        Args:
            frame: Frame de video (numpy array)
            
        Returns:
            tuple: (detections, annotated_frame)
        """
        # Realizar detección
        results = self.model(frame)[0]
        detections = sv.Detections.from_yolov8(results)
        
        # Filtrar solo obstáculos relevantes
        obstacle_mask = [
            class_id in self.obstacle_classes 
            for class_id in detections.class_id
        ]
        detections = detections[obstacle_mask]
        
        # Crear etiquetas
        labels = [
            f"{self.obstacle_classes.get(class_id, 'unknown')} {confidence:.2f}"
            for class_id, confidence in zip(detections.class_id, detections.confidence)
        ]
        
        # Anotar frame con cajas y etiquetas
        annotated_frame = self.box_annotator.annotate(
            scene=frame.copy(), detections=detections
        )
        
        # Añadir etiquetas manualmente usando cv2
        for detection, label in zip(detections.xyxy, labels):
            x1, y1, x2, y2 = detection.astype(int)
            # Dibujar etiqueta con fondo
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
            cv2.rectangle(annotated_frame, (x1, y1 - label_size[1] - 10), 
                         (x1 + label_size[0], y1), (0, 0, 0), -1)
            cv2.putText(annotated_frame, label, (x1, y1 - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return detections, annotated_frame
    
    def process_video(self, input_path, output_path=None, show_preview=True):
        """
        Procesa un video completo detectando obstáculos.
        
        Args:
            input_path (str): Ruta del video de entrada
            output_path (str): Ruta del video de salida (opcional)
            show_preview (bool): Mostrar preview en tiempo real
        """
        # Abrir video
        cap = cv2.VideoCapture(input_path)
        
        if not cap.isOpened():
            raise ValueError(f"No se pudo abrir el video: {input_path}")
        
        # Obtener propiedades del video
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"Procesando video: {input_path}")
        print(f"Resolución: {width}x{height}, FPS: {fps}, Frames: {total_frames}")
        
        # Configurar writer si se especifica output
        writer = None
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_count = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Detectar obstáculos
                detections, annotated_frame = self.detect_obstacles(frame)
                
                # Mostrar información de detecciones
                if len(detections) > 0:
                    print(f"Frame {frame_count}: {len(detections)} obstáculos detectados")
                    for i, (class_id, confidence) in enumerate(zip(detections.class_id, detections.confidence)):
                        obstacle_name = self.obstacle_classes.get(class_id, 'unknown')
                        print(f"  - {obstacle_name}: {confidence:.2f}")
                
                # Guardar frame si se especifica
                if writer:
                    writer.write(annotated_frame)
                
                # Mostrar preview
                if show_preview:
                    cv2.imshow('Obstacle Detection', annotated_frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                
                frame_count += 1
                
                # Mostrar progreso
                if frame_count % 30 == 0:
                    progress = (frame_count / total_frames) * 100
                    print(f"Progreso: {progress:.1f}%")
        
        finally:
            # Limpiar recursos
            cap.release()
            if writer:
                writer.release()
            if show_preview:
                cv2.destroyAllWindows()
        
        print(f"Procesamiento completado. Frames procesados: {frame_count}")
        if output_path:
            print(f"Video guardado en: {output_path}")


def main():
    """
    Función principal para ejecutar el detector desde línea de comandos.
    """
    parser = argparse.ArgumentParser(description="Detector de obstáculos en video")
    parser.add_argument("input", help="Ruta del video de entrada")
    parser.add_argument("-o", "--output", help="Ruta del video de salida")
    parser.add_argument("-m", "--model", default="yolov8n.pt", 
                       help="Ruta del modelo YOLO (default: yolov8n.pt)")
    parser.add_argument("--no-preview", action="store_true", 
                       help="No mostrar preview en tiempo real")
    
    args = parser.parse_args()
    
    # Verificar que el archivo de entrada existe
    if not os.path.exists(args.input):
        print(f"Error: El archivo {args.input} no existe")
        return
    
    # Crear detector
    detector = VideoObstacleDetector(args.model)
    
    # Procesar video
    try:
        detector.process_video(
            input_path=args.input,
            output_path=args.output,
            show_preview=not args.no_preview
        )
    except Exception as e:
        print(f"Error durante el procesamiento: {e}")


if __name__ == "__main__":
    main()
