import numpy as np
from scipy.io.wavfile import write
from pydub import AudioSegment
import os
import random

# Cấu hình âm thanh
sample_rate = 44100
duration_note = 0.2  # nhanh hơn để có tiết tấu EDM
total_duration = 120  # 2 phút

# Bảng nốt (tăng cường cảm giác EDM)
notes = {
    'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
    'G4': 392.00, 'A4': 440.00, 'B4': 493.88, 'C5': 523.25,
    'D5': 587.33, 'E5': 659.25, 'F5': 698.46, 'G5': 783.99,
    'A5': 880.00, 'B5': 987.77, 'C6': 1046.50
}

# Scale C major (cho cảm giác vui nhộn)
scale_major = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'F5', 'G5']

# Tạo sóng sine
def generate_note(freq, duration):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    return 0.5 * np.sin(2 * np.pi * freq * t)

# Kick drum EDM
def generate_kick(duration):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    envelope = np.exp(-40 * t)
    freq = 100 * (1 - t)  # sweep xuống
    return 0.8 * envelope * np.sin(2 * np.pi * freq * t)

# Hợp âm EDM
def generate_chord(base_note, intervals, duration):
    base_freq = notes.get(base_note, 440.0)
    chord = generate_note(base_freq, duration)
    for interval in intervals:
        freq = base_freq * 2 ** (interval / 12)
        chord += generate_note(freq, duration)
    return chord / (len(intervals) + 1)

# Giai điệu ngẫu nhiên với scale major
def generate_melody(num_notes):
    melody = []
    current_index = scale_major.index('C4')
    for _ in range(num_notes):
        step = random.choice([-2, -1, 0, 1, 2])
        current_index = max(0, min(len(scale_major) - 1, current_index + step))
        melody.append(scale_major[current_index])
    return melody

# Tổng số nốt
num_notes = int(total_duration / duration_note)
melody_pattern = generate_melody(num_notes)

# Tạo bản nhạc
full_wave = np.array([])

for i, note in enumerate(melody_pattern):
    freq = notes[note]

    # Thêm hợp âm mỗi 16 nốt (drop EDM)
    if i % 16 == 0:
        tone = generate_chord(note, [4, 7, 11], duration_note)
    else:
        tone = generate_note(freq, duration_note)

    # Thêm kick mỗi 4 nốt (giống EDM beat)
    if i % 4 == 0:
        kick = generate_kick(duration_note)
        combined = tone + kick
    else:
        combined = tone

    full_wave = np.concatenate((full_wave, combined))

# Normal hóa và lưu WAV
wav_file = "edm_fun_temp.wav"
full_wave_int16 = np.int16(full_wave / np.max(np.abs(full_wave)) * 32767)
write(wav_file, sample_rate, full_wave_int16)

# Chuyển sang MP3
mp3_file = "edm_electro_fun.mp3"
sound = AudioSegment.from_wav(wav_file)
sound.export(mp3_file, format="mp3")

# Xóa WAV
os.remove(wav_file)

print("✅ Đã tạo bản nhạc EDM vui nhộn:", mp3_file)
