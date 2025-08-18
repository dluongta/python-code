import numpy as np
from scipy.io.wavfile import write
from pydub import AudioSegment
import os

# Cấu hình âm thanh
sample_rate = 44100
duration_note = 0.25  # thời lượng mỗi nốt (giây)
total_duration = 180  # độ dài bài nhạc (giây) ~ 3 phút

# Bảng nốt nhạc (tần số cơ bản)
notes = {
    'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
    'G4': 392.00, 'A4': 440.00, 'B4': 493.88, 'C5': 523.25,
    'D5': 587.33, 'E5': 659.25, 'F5': 698.46, 'G5': 783.99,
    'A5': 880.00
}

# Giai điệu chính (sống động, điện tử)
melody_pattern = [
    'C5', 'E5', 'G5', 'C5',
    'D5', 'F5', 'A5', 'D5',
    'E5', 'G5', 'B5', 'E5',
    'F5', 'A5', 'C5', 'F5'
]

# Tạo sóng sine cho một nốt
def generate_note(freq, duration):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = 0.5 * np.sin(2 * np.pi * freq * t)
    return wave

# Tạo beat đơn giản (pulse drum)
def generate_beat(duration):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    pulse = 0.5 * np.exp(-5 * t) * np.sin(2 * np.pi * 100 * t)
    return pulse

# Tạo bản nhạc
full_wave = np.array([])
melody_length = len(melody_pattern)
num_notes = int(total_duration / duration_note)

for i in range(num_notes):
    note = melody_pattern[i % melody_length]
    freq = notes.get(note, 440.0)
    tone = generate_note(freq, duration_note)
    
    if i % 2 == 0:
        beat = generate_beat(duration_note)
        combined = tone + beat
    else:
        combined = tone

    full_wave = np.concatenate((full_wave, combined))

# Lưu ra file WAV tạm thời
wav_file = "electro_temp.wav"
full_wave_int16 = np.int16(full_wave / np.max(np.abs(full_wave)) * 32767)
write(wav_file, sample_rate, full_wave_int16)

# Chuyển sang MP3
mp3_file = "electro_track.mp3"
sound = AudioSegment.from_wav(wav_file)
sound.export(mp3_file, format="mp3")

# Xóa file WAV tạm
os.remove(wav_file)

print("✅ Đã tạo bản nhạc:", mp3_file)
