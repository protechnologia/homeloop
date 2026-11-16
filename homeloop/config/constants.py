# Audio pipeline constants – fixed by the components (VAD, wake word, STT)

# --- Microphone: audio format used by the whole pipeline ---
CHANNELS           = 1                    # mono
RATE               = 16000                # samples per second
DTYPE              = "int16"              # 16-bit samples

# --- Wake word ---
WAKE_BLOCK_SAMPLES = RATE * 80 // 1000    # 80 ms required by openWakeWord (1280 at 16 kHz)
