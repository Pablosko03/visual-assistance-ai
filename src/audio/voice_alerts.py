"""
Voice Alert System - Phase 2 MVP
Sistema de alertas de voz para notificar obstáculos detectados.
"""

import pyttsx3
import time
import threading
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class AlertPriority(Enum):
    """Niveles de prioridad para las alertas."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Alert:
    """Estructura de datos para una alerta."""
    message: str
    priority: AlertPriority
    timestamp: float
    object_type: str
    distance: Optional[str] = None


class VoiceAlertSystem:
    """
    Sistema de alertas de voz con control de frecuencia y prioridades.
    """
    
    def __init__(self, language='es', rate=150, volume=0.9):
        """
        Inicializa el sistema de alertas de voz.
        
        Args:
            language (str): Idioma para TTS ('es' para español, 'en' para inglés)
            rate (int): Velocidad de habla (palabras por minuto)
            volume (float): Volumen (0.0 a 1.0)
        """
        self.engine = pyttsx3.init()
        self.language = language
        self.is_speaking = False
        self.alert_queue = []
        self.last_alerts = {}  # Para control de cooldown
        self.cooldown_times = {
            AlertPriority.LOW: 10.0,      # 10 segundos
            AlertPriority.MEDIUM: 5.0,    # 5 segundos
            AlertPriority.HIGH: 3.0,      # 3 segundos
            AlertPriority.CRITICAL: 1.0   # 1 segundo
        }
        
        # Configurar motor TTS
        self._setup_tts_engine(rate, volume)
        
        # Mensajes predefinidos en español
        self.messages_es = {
            "person": "Persona detectada",
            "car": "Vehículo detectado",
            "bicycle": "Bicicleta detectada",
            "motorcycle": "Motocicleta detectada",
            "bus": "Autobús detectado",
            "truck": "Camión detectado",
            "dog": "Perro detectado",
            "cat": "Gato detectado",
            "chair": "Silla detectada",
            "table": "Mesa detectada",
            "bottle": "Botella detectada",
            "backpack": "Mochila detectada",
            "suitcase": "Maleta detectada",
            "multiple_obstacles": "Múltiples obstáculos detectados",
            "obstacle_ahead": "Obstáculo adelante",
            "clear_path": "Camino despejado",
            "danger_zone": "Zona de peligro",
            "safe_zone": "Zona segura"
        }
        
        # Mensajes predefinidos en inglés
        self.messages_en = {
            "person": "Person detected",
            "car": "Vehicle detected",
            "bicycle": "Bicycle detected",
            "motorcycle": "Motorcycle detected",
            "bus": "Bus detected",
            "truck": "Truck detected",
            "dog": "Dog detected",
            "cat": "Cat detected",
            "chair": "Chair detected",
            "table": "Table detected",
            "bottle": "Bottle detected",
            "backpack": "Backpack detected",
            "suitcase": "Suitcase detected",
            "multiple_obstacles": "Multiple obstacles detected",
            "obstacle_ahead": "Obstacle ahead",
            "clear_path": "Path clear",
            "danger_zone": "Danger zone",
            "safe_zone": "Safe zone"
        }
        
        self.messages = self.messages_es if language == 'es' else self.messages_en
    
    def _setup_tts_engine(self, rate, volume):
        """Configura el motor de texto a voz."""
        try:
            # Configurar velocidad y volumen
            self.engine.setProperty('rate', rate)
            self.engine.setProperty('volume', volume)
            
            # Intentar configurar voz en español si está disponible
            voices = self.engine.getProperty('voices')
            if voices:
                for voice in voices:
                    if self.language == 'es' and ('spanish' in voice.name.lower() or 'es' in voice.id.lower()):
                        self.engine.setProperty('voice', voice.id)
                        break
                    elif self.language == 'en' and ('english' in voice.name.lower() or 'en' in voice.id.lower()):
                        self.engine.setProperty('voice', voice.id)
                        break
        except Exception as e:
            print(f"Warning: Error configurando TTS engine: {e}")
    
    def add_detection_alert(self, object_type: str, confidence: float = 0.5, distance: str = None):
        """
        Añade una alerta basada en una detección.
        
        Args:
            object_type (str): Tipo de objeto detectado
            confidence (float): Confianza de la detección
            distance (str): Distancia estimada (opcional)
        """
        # Determinar prioridad
        if object_type in ['car', 'truck', 'bus', 'motorcycle']:
            priority = AlertPriority.HIGH if confidence > 0.7 else AlertPriority.MEDIUM
        elif object_type in ['person', 'bicycle', 'dog']:
            priority = AlertPriority.MEDIUM if confidence > 0.6 else AlertPriority.LOW
        else:
            priority = AlertPriority.LOW
        
        # Control de cooldown
        current_time = time.time()
        key = f"{object_type}_{priority.name}"
        
        if key in self.last_alerts:
            time_since_last = current_time - self.last_alerts[key]
            if time_since_last < self.cooldown_times[priority]:
                return  # Skip this alert
        
        self.last_alerts[key] = current_time
        
        # Crear mensaje
        base_message = self.messages.get(object_type, f"{object_type} detectado")
        if distance:
            message = f"{base_message} a {distance}"
        else:
            message = base_message
        
        alert = Alert(
            message=message,
            priority=priority,
            timestamp=time.time(),
            object_type=object_type,
            distance=distance
        )
        
        self.add_alert(alert)
    
    def add_alert(self, alert: Alert):
        """Añade una alerta a la cola."""
        # Insertar en la posición correcta según prioridad
        inserted = False
        for i, existing_alert in enumerate(self.alert_queue):
            if alert.priority.value > existing_alert.priority.value:
                self.alert_queue.insert(i, alert)
                inserted = True
                break
        
        if not inserted:
            self.alert_queue.append(alert)
        
        # Procesar alertas si no estamos hablando
        if not self.is_speaking:
            self._process_next_alert()
    
    def _process_next_alert(self):
        """Procesa la siguiente alerta en la cola."""
        if not self.alert_queue or self.is_speaking:
            return
        
        alert = self.alert_queue.pop(0)
        self._speak_alert(alert)
    
    def _speak_alert(self, alert: Alert):
        """Reproduce una alerta de voz."""
        def speak_thread():
            try:
                self.is_speaking = True
                print(f"🔊 Alerta: {alert.message} (Prioridad: {alert.priority.name})")
                self.engine.say(alert.message)
                self.engine.runAndWait()
            except Exception as e:
                print(f"Error reproduciendo alerta: {e}")
            finally:
                self.is_speaking = False
                # Procesar siguiente alerta si hay alguna
                if self.alert_queue:
                    self._process_next_alert()
        
        # Ejecutar en hilo separado para no bloquear
        thread = threading.Thread(target=speak_thread)
        thread.daemon = True
        thread.start()
    
    def stop(self):
        """Detiene el sistema de alertas."""
        try:
            self.engine.stop()
        except:
            pass
        self.alert_queue.clear()


# Ejemplo de uso
if __name__ == "__main__":
    # Crear sistema de alertas
    alert_system = VoiceAlertSystem(language='es')
    
    # Simular algunas detecciones
    print("Probando sistema de alertas de voz...")
    
    alert_system.add_detection_alert("person", confidence=0.8)
    time.sleep(3)
    
    alert_system.add_detection_alert("car", confidence=0.9, distance="3 metros")
    time.sleep(3)
    
    print("Prueba completada.")
    alert_system.stop()
