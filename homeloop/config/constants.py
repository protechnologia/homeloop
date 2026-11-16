# Audio pipeline constants – fixed by the components (VAD, wake word, STT)

# --- Microphone: audio format used by the whole pipeline ---
CHANNELS           = 1                    # mono
SAMPLES_PER_SECOND = 16000                # sample rate: 16 kHz
DTYPE              = "int16"              # 16-bit samples

# --- Wake word ---
WAKE_BLOCK_SAMPLES = SAMPLES_PER_SECOND * 80 // 1000    # 80 ms required by openWakeWord (1280 at 16 kHz)
