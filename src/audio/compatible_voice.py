
import platform
import sys

class CompatibleVoiceSystem:
    """Sistema de voz compatible con Python 3.7+"""
    
    def __init__(self, language='es'):
        self.language = language
        self.engine = None
        self.fallback_method = None
        self._initialize_engine()
    
    def _initialize_engine(self):
        """Inicializa el motor de voz más compatible."""
        
        # Método 1: Intentar pyttsx3 con manejo de errores
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 0.8)
            print("✅ pyttsx3 inicializado correctamente")
            return
        except Exception as e:
            print(f"⚠️  pyttsx3 falló: {e}")
        
        # Método 2: Windows SAPI (solo Windows)
        if platform.system() == "Windows":
            try:
                import win32com.client
                self.engine = win32com.client.Dispatch("SAPI.SpVoice")
                self.fallback_method = "sapi"
                print("✅ Windows SAPI inicializado")
                return
            except ImportError:
                pass
        
        # Método 3: Fallback a print (sin voz)
        print("⚠️  No hay motor TTS disponible - usando modo texto")
        self.fallback_method = "text"
    
    def speak(self, text):
        """Reproduce texto como voz."""
        if self.engine and self.fallback_method != "text":
            try:
                if self.fallback_method == "sapi":
                    self.engine.Speak(text)
                else:
                    self.engine.say(text)
                    self.engine.runAndWait()
            except Exception as e:
                print(f"🔊 [VOICE ERROR] {text}")
        else:
            print(f"🔊 [VOICE] {text}")
    
    def stop(self):
        """Detiene el motor de voz."""
        if self.engine and hasattr(self.engine, 'stop'):
            try:
                self.engine.stop()
            except:
                pass
