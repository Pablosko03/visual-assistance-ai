#!/usr/bin/env python3
"""
Script para crear videos de prueba con obstáculos simulados.
Útil para testing del sistema de detección cuando no hay videos reales disponibles.
"""

import cv2
import numpy as np
import os
from pathlib import Path


def create_test_video_with_moving_objects():
    """
    Crea un video de prueba con objetos en movimiento que simula obstáculos.
    """
    # Configuración del video
    width, height = 640, 480
    fps = 30
    duration_seconds = 10
    total_frames = fps * duration_seconds
    
    # Crear directorio de salida
    output_dir = Path("data/test_videos")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "test_moving_obstacles.mp4"
    
    # Configurar writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
    
    print(f"🎬 Creando video de prueba: {output_path}")
    print(f"📐 Resolución: {width}x{height}, FPS: {fps}, Duración: {duration_seconds}s")
    
    for frame_num in range(total_frames):
        # Crear frame base (fondo gris)
        frame = np.ones((height, width, 3), dtype=np.uint8) * 50
        
        # Añadir texto de información
        cv2.putText(frame, f"Frame: {frame_num}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, "Test Video - Moving Obstacles", (10, height - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        # Simular persona caminando (rectángulo azul)
        person_x = int(50 + (frame_num * 2) % (width - 100))
        person_y = height - 200
        cv2.rectangle(frame, (person_x, person_y), (person_x + 60, person_y + 150), 
                     (255, 100, 100), -1)  # Azul
        cv2.putText(frame, "PERSON", (person_x, person_y - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Simular coche moviéndose (rectángulo rojo)
        car_x = int(width - 100 - (frame_num * 3) % (width - 100))
        car_y = height - 100
        cv2.rectangle(frame, (car_x, car_y), (car_x + 80, car_y + 40), 
                     (0, 0, 255), -1)  # Rojo
        cv2.putText(frame, "CAR", (car_x, car_y - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Simular silla estática (rectángulo verde)
        chair_x, chair_y = 300, 200
        cv2.rectangle(frame, (chair_x, chair_y), (chair_x + 50, chair_y + 80), 
                     (0, 255, 0), -1)  # Verde
        cv2.putText(frame, "CHAIR", (chair_x, chair_y - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Simular botella (círculo amarillo)
        bottle_x = int(200 + 50 * np.sin(frame_num * 0.1))
        bottle_y = 300
        cv2.circle(frame, (bottle_x, bottle_y), 15, (0, 255, 255), -1)  # Amarillo
        cv2.putText(frame, "BOTTLE", (bottle_x - 20, bottle_y - 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        # Escribir frame
        writer.write(frame)
        
        # Mostrar progreso
        if frame_num % 60 == 0:
            progress = (frame_num / total_frames) * 100
            print(f"Progreso: {progress:.1f}%")
    
    writer.release()
    print(f"✅ Video creado exitosamente: {output_path}")
    return str(output_path)


def create_static_obstacles_video():
    """
    Crea un video con obstáculos estáticos para testing básico.
    """
    # Configuración del video
    width, height = 640, 480
    fps = 15
    duration_seconds = 5
    total_frames = fps * duration_seconds
    
    # Crear directorio de salida
    output_dir = Path("data/test_videos")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "test_static_obstacles.mp4"
    
    # Configurar writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
    
    print(f"🎬 Creando video estático: {output_path}")
    
    for frame_num in range(total_frames):
        # Crear frame base (fondo blanco)
        frame = np.ones((height, width, 3), dtype=np.uint8) * 200
        
        # Título
        cv2.putText(frame, "Static Obstacles Test", (width//2 - 120, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        
        # Simular varios obstáculos estáticos
        obstacles = [
            {"name": "PERSON", "pos": (100, 150), "size": (60, 150), "color": (255, 100, 100)},
            {"name": "CAR", "pos": (300, 300), "size": (120, 60), "color": (0, 0, 255)},
            {"name": "CHAIR", "pos": (500, 200), "size": (50, 80), "color": (0, 255, 0)},
            {"name": "TABLE", "pos": (200, 350), "size": (100, 40), "color": (150, 75, 0)},
        ]
        
        for obs in obstacles:
            x, y = obs["pos"]
            w, h = obs["size"]
            color = obs["color"]
            name = obs["name"]
            
            # Dibujar obstáculo
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, -1)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 2)
            
            # Etiqueta
            cv2.putText(frame, name, (x, y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        
        # Información del frame
        cv2.putText(frame, f"Frame: {frame_num + 1}/{total_frames}", (10, height - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        
        writer.write(frame)
    
    writer.release()
    print(f"✅ Video estático creado: {output_path}")
    return str(output_path)


def main():
    """
    Función principal para crear videos de prueba.
    """
    print("🎬 Generador de Videos de Prueba")
    print("=" * 40)
    
    try:
        # Crear ambos tipos de videos
        moving_video = create_test_video_with_moving_objects()
        static_video = create_static_obstacles_video()
        
        print("\n✅ Videos de prueba creados exitosamente:")
        print(f"   📹 Video con movimiento: {moving_video}")
        print(f"   📹 Video estático: {static_video}")
        print("\n🎯 Estos videos pueden usarse para probar detect_video.py")
        print("💡 Ejemplo de uso:")
        print(f"   python src/detection/detect_video.py {moving_video} -o output_moving.mp4")
        print(f"   python src/detection/detect_video.py {static_video} -o output_static.mp4")
        
    except Exception as e:
        print(f"❌ Error creando videos: {e}")
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
