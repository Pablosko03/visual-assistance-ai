"""
Configuration settings for the Visual Assistance AI project.
"""

import os
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class ModelConfig:
    """Configuración del modelo YOLO."""
    default_model: str = "yolov8n.pt"
    confidence_threshold: float = 0.5
    iou_threshold: float = 0.45
    max_detections: int = 100
    device: str = "auto"  # "auto", "cpu", "cuda"


@dataclass
class CameraConfig:
    """Configuración de la cámara."""
    default_camera_id: int = 0
    frame_width: int = 640
    frame_height: int = 480
    fps: int = 30


@dataclass
class AudioConfig:
    """Configuración del sistema de audio."""
    default_language: str = "es"
    speech_rate: int = 150  # palabras por minuto
    volume: float = 0.9
    cooldown_times: Dict[str, float] = None
    
    def __post_init__(self):
        if self.cooldown_times is None:
            self.cooldown_times = {
                "LOW": 10.0,
                "MEDIUM": 5.0,
                "HIGH": 3.0,
                "CRITICAL": 1.0
            }


@dataclass
class DetectionConfig:
    """Configuración de detección de obstáculos."""
    # Clases de obstáculos por prioridad
    high_priority_objects: List[str] = None
    medium_priority_objects: List[str] = None
    low_priority_objects: List[str] = None
    
    # Zona de peligro (porcentaje del frame)
    danger_zone_margin_x: float = 0.25  # 25% de margen horizontal
    danger_zone_margin_y: float = 0.25  # 25% de margen vertical
    
    # Seguimiento
    tracking_enabled: bool = True
    max_disappeared: int = 30
    max_distance: int = 50
    
    def __post_init__(self):
        if self.high_priority_objects is None:
            self.high_priority_objects = ['car', 'truck', 'bus', 'motorcycle']
        
        if self.medium_priority_objects is None:
            self.medium_priority_objects = ['person', 'bicycle', 'dog']
        
        if self.low_priority_objects is None:
            self.low_priority_objects = [
                'chair', 'table', 'bottle', 'backpack', 'cat', 'handbag', 
                'suitcase', 'cup', 'couch', 'potted plant', 'tv'
            ]


class AppConfig:
    """Configuración principal de la aplicación."""
    
    def __init__(self):
        self.model = ModelConfig()
        self.camera = CameraConfig()
        self.audio = AudioConfig()
        self.detection = DetectionConfig()
        
        # Rutas del proyecto
        self.project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.data_dir = os.path.join(self.project_root, "data")
        self.models_dir = os.path.join(self.data_dir, "models")
        self.datasets_dir = os.path.join(self.data_dir, "datasets")
        self.logs_dir = os.path.join(self.project_root, "logs")
        
        # Crear directorios si no existen
        self._create_directories()
    
    def _create_directories(self):
        """Crea los directorios necesarios si no existen."""
        directories = [
            self.data_dir,
            self.models_dir,
            self.datasets_dir,
            self.logs_dir
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)


# Instancia global de configuración
config = AppConfig()


# Mapeo de clases COCO a nombres en español e inglés
COCO_CLASSES_ES = {
    0: "persona", 1: "bicicleta", 2: "coche", 3: "motocicleta", 4: "avión",
    5: "autobús", 6: "tren", 7: "camión", 8: "barco", 9: "semáforo",
    10: "boca de incendios", 11: "señal de stop", 12: "parquímetro", 13: "banco",
    14: "pájaro", 15: "gato", 16: "perro", 17: "caballo", 18: "oveja", 19: "vaca",
    20: "elefante", 21: "oso", 22: "cebra", 23: "jirafa", 24: "mochila",
    25: "paraguas", 26: "bolso", 27: "corbata", 28: "maleta", 29: "frisbee",
    30: "esquís", 31: "snowboard", 32: "pelota deportiva", 33: "cometa", 34: "bate de béisbol",
    35: "guante de béisbol", 36: "monopatín", 37: "tabla de surf", 38: "raqueta de tenis",
    39: "botella", 40: "copa de vino", 41: "taza", 42: "tenedor", 43: "cuchillo",
    44: "cuchara", 45: "bol", 46: "plátano", 47: "manzana", 48: "sándwich",
    49: "naranja", 50: "brócoli", 51: "zanahoria", 52: "perrito caliente", 53: "pizza",
    54: "donut", 55: "tarta", 56: "silla", 57: "sofá", 58: "planta en maceta",
    59: "cama", 60: "mesa de comedor", 61: "inodoro", 62: "televisión", 63: "portátil",
    64: "ratón", 65: "mando a distancia", 66: "teclado", 67: "teléfono móvil", 68: "microondas",
    69: "horno", 70: "tostadora", 71: "fregadero", 72: "nevera", 73: "libro",
    74: "reloj", 75: "jarrón", 76: "tijeras", 77: "oso de peluche", 78: "secador de pelo",
    79: "cepillo de dientes"
}

COCO_CLASSES_EN = {
    0: "person", 1: "bicycle", 2: "car", 3: "motorcycle", 4: "airplane",
    5: "bus", 6: "train", 7: "truck", 8: "boat", 9: "traffic light",
    10: "fire hydrant", 11: "stop sign", 12: "parking meter", 13: "bench",
    14: "bird", 15: "cat", 16: "dog", 17: "horse", 18: "sheep", 19: "cow",
    20: "elephant", 21: "bear", 22: "zebra", 23: "giraffe", 24: "backpack",
    25: "umbrella", 26: "handbag", 27: "tie", 28: "suitcase", 29: "frisbee",
    30: "skis", 31: "snowboard", 32: "sports ball", 33: "kite", 34: "baseball bat",
    35: "baseball glove", 36: "skateboard", 37: "surfboard", 38: "tennis racket",
    39: "bottle", 40: "wine glass", 41: "cup", 42: "fork", 43: "knife",
    44: "spoon", 45: "bowl", 46: "banana", 47: "apple", 48: "sandwich",
    49: "orange", 50: "broccoli", 51: "carrot", 52: "hot dog", 53: "pizza",
    54: "donut", 55: "cake", 56: "chair", 57: "couch", 58: "potted plant",
    59: "bed", 60: "dining table", 61: "toilet", 62: "tv", 63: "laptop",
    64: "mouse", 65: "remote", 66: "keyboard", 67: "cell phone", 68: "microwave",
    69: "oven", 70: "toaster", 71: "sink", 72: "refrigerator", 73: "book",
    74: "clock", 75: "vase", 76: "scissors", 77: "teddy bear", 78: "hair drier",
    79: "toothbrush"
}


def get_class_names(language: str = "es") -> Dict[int, str]:
    """
    Obtiene los nombres de las clases en el idioma especificado.
    
    Args:
        language: Idioma ('es' o 'en')
        
    Returns:
        Dict[int, str]: Mapeo de ID de clase a nombre
    """
    return COCO_CLASSES_ES if language == "es" else COCO_CLASSES_EN
