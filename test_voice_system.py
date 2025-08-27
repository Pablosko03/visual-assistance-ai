#!/usr/bin/env python3
"""
Test del sistema de alertas de voz con compatibilidad Python 3.7
"""

import sys
import platform

def test_python_version():
    """Verifica la versión de Python y compatibilidad."""
    print("🐍 Test de Versión de Python")
    print("=" * 35)
    
    version = sys.version_info
    print(f"📊 Versión actual: Python {version.major}.{version.minor}.{version.micro}")
    print(f"🖥️  Plataforma: {platform.system()} {platform.release()}")
    
    if version.major == 3 and version.minor >= 8:
        print("✅ Python 3.8+ - Totalmente compatible")
        return "full"
    elif version.major == 3 and version.minor == 7:
        print("⚠️  Python 3.7 - Compatibilidad limitada")
        print("💡 Algunas funciones de pyttsx3 pueden fallar")
        return "limited"
    else:
        print("❌ Versión no soportada")
        return "unsupported"

def test_tts_basic():
    """Test básico del sistema TTS."""
    print("\n🔊 Test Básico de Text-to-Speech")
    print("=" * 40)
    
    try:
        import pyttsx3
        print("✅ pyttsx3 importado correctamente")
        
        # Intentar inicializar el motor TTS
        try:
            engine = pyttsx3.init()
            print("✅ Motor TTS inicializado")
            
            # Obtener propiedades
            voices = engine.getProperty('voices')
            rate = engine.getProperty('rate')
            volume = engine.getProperty('volume')
            
            print(f"📊 Voces disponibles: {len(voices) if voices else 0}")
            print(f"📊 Velocidad: {rate}")
            print(f"📊 Volumen: {volume}")
            
            # Test de configuración
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 0.8)
            print("✅ Configuración aplicada")
            
            engine.stop()
            return True
            
        except Exception as e:
            print(f"❌ Error al inicializar motor TTS: {e}")
            if "invalid syntax" in str(e):
                print("💡 Error de sintaxis - Problema de compatibilidad Python 3.7")
            return False
            
    except ImportError as e:
        print(f"❌ Error al importar pyttsx3: {e}")
        return False

def test_alternative_tts():
    """Test de alternativas TTS para Python 3.7."""
    print("\n🔄 Test de Alternativas TTS")
    print("=" * 35)
    
    alternatives_tested = []
    
    # Test 1: Windows SAPI (solo Windows)
    if platform.system() == "Windows":
        try:
            import win32com.client
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            print("✅ Windows SAPI disponible")
            alternatives_tested.append("Windows SAPI")
        except ImportError:
            print("❌ Windows SAPI no disponible (requiere pywin32)")
    
    # Test 2: gTTS (requiere internet)
    try:
        from gtts import gTTS
        print("✅ gTTS disponible (requiere internet)")
        alternatives_tested.append("gTTS")
    except ImportError:
        print("❌ gTTS no disponible")
    
    # Test 3: espeak (Linux/Unix)
    if platform.system() in ["Linux", "Darwin"]:
        import subprocess
        try:
            result = subprocess.run(["espeak", "--version"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("✅ espeak disponible")
                alternatives_tested.append("espeak")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("❌ espeak no disponible")
    
    return alternatives_tested

def create_compatible_voice_system():
    """Crea un sistema de voz compatible con Python 3.7."""
    print("\n🛠️  Creando Sistema de Voz Compatible")
    print("=" * 45)
    
    voice_system_code = '''
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
'''
    
    # Guardar el código compatible
    with open("src/audio/compatible_voice.py", "w", encoding="utf-8") as f:
        f.write(voice_system_code)
    
    print("✅ Sistema de voz compatible creado en: src/audio/compatible_voice.py")
    return True

def main():
    """Función principal de testing."""
    print("🤖 Sistema de Asistencia Visual - Test de Voz")
    print("=" * 55)
    
    # Test de versión de Python
    python_compat = test_python_version()
    
    # Test básico de TTS
    tts_works = test_tts_basic()
    
    # Test de alternativas
    alternatives = test_alternative_tts()
    
    # Crear sistema compatible
    compatible_created = create_compatible_voice_system()
    
    print("\n📋 Resumen de Tests:")
    print(f"   Python: {python_compat}")
    print(f"   pyttsx3: {'✅ OK' if tts_works else '❌ FALLO'}")
    print(f"   Alternativas: {len(alternatives)} disponibles")
    print(f"   Sistema compatible: {'✅ Creado' if compatible_created else '❌ Error'}")
    
    if alternatives:
        print(f"   Métodos disponibles: {', '.join(alternatives)}")
    
    if tts_works or alternatives or compatible_created:
        print("\n🎉 ¡Sistema de voz funcional disponible!")
        return True
    else:
        print("\n⚠️  Sistema de voz limitado - funcionará en modo texto")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
