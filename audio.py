import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from pydub import AudioSegment
import os

sample_rate = 44100  

notes = {
    'C4': 261.63,
    'D4': 293.66,
    'E4': 329.63,
    'F4': 349.23,
    'G4': 392.00,
    'A4': 440.00,
    'B4': 493.88,
    'C5': 523.25
}

melody = ['C4', 'D4', 'E4', 'C4', 'C4', 'D4', 'E4', 'C4']
duration = 0.4  

full_wave = np.array([])

for note in melody:
    freq = notes[note]
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = 0.5 * np.sin(2 * np.pi * freq * t)
    full_wave = np.concatenate((full_wave, wave))

sd.play(full_wave, samplerate=sample_rate)
sd.wait()

wav_file = "audio_temp.wav"
full_wave_int16 = np.int16(full_wave * 32767)
write(wav_file, sample_rate, full_wave_int16)

mp3_file = "audio.mp3"
sound = AudioSegment.from_wav(wav_file)
sound.export(mp3_file, format="mp3")

os.remove(wav_file)

print("Đã lưu file:", mp3_file)
