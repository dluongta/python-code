import numpy as np
from scipy.io.wavfile import write
from pydub import AudioSegment
import os
import random

# Cấu hình âm thanh
sample_rate = 44100
duration_note = 0.25  # thời lượng mỗi nốt (giây)
total_duration = 180  # độ dài bài nhạc (giây)

# Bảng nốt nhạc
notes = {
    'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
    'G4': 392.00, 'A4': 440.00, 'B4': 493.88, 'C5': 523.25,
    'D5': 587.33, 'E5': 659.25, 'F5': 698.46, 'G5': 783.99,
    'A5': 880.00, 'B5': 987.77, 'C6': 1046.50
}

note_names = list(notes.keys())

# Tạo sóng sine cho 1 nốt
def generate_note(freq, duration):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = 0.5 * np.sin(2 * np.pi * freq * t)
    return wave

# Tạo beat đơn giản
def generate_beat(duration):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    pulse = 0.5 * np.exp(-5 * t) * np.sin(2 * np.pi * 100 * t)
    return pulse

# Tạo hợp âm (chồng nhiều nốt)
def generate_chord(base_note, intervals, duration):
    base_freq = notes.get(base_note, 440.0)
    chord_wave = generate_note(base_freq, duration)
    for interval in intervals:
        freq = base_freq * 2 ** (interval / 12)
        chord_wave += generate_note(freq, duration)
    return chord_wave / len(intervals)

# Tạo giai điệu ngẫu nhiên có logic
def generate_dynamic_melody(num_notes):
    melody = []
    current_index = note_names.index('C4')

    for _ in range(num_notes):
        step = random.choice([-2, -1, 0, 1, 2, 3])  # Nhảy các quãng ngắn
        current_index = max(0, min(len(note_names) - 1, current_index + step))
        note = note_names[current_index]
        melody.append(note)
    return melody

# Tổng số nốt cần tạo
num_notes = int(total_duration / duration_note)

# Giai điệu thay đổi phức tạp hơn
melody_pattern = generate_dynamic_melody(num_notes)

# Tạo bản nhạc
full_wave = np.array([])

for i, note in enumerate(melody_pattern):
    freq = notes.get(note, 440.0)

    # Thêm hợp âm thỉnh thoảng
    if i % 16 == 0:
        tone = generate_chord(note, [4, 7], duration_note)  # Hợp âm trưởng
    else:
        tone = generate_note(freq, duration_note)

    # Beat mỗi 2 nốt
    if i % 2 == 0:
        beat = generate_beat(duration_note)
        combined = tone + beat
    else:
        combined = tone

    full_wave = np.concatenate((full_wave, combined))

# Lưu ra file WAV tạm
wav_file = "electro_temp.wav"
full_wave_int16 = np.int16(full_wave / np.max(np.abs(full_wave)) * 32767)
write(wav_file, sample_rate, full_wave_int16)

# Chuyển sang MP3
mp3_file = "electro_track_complex.mp3"
sound = AudioSegment.from_wav(wav_file)
sound.export(mp3_file, format="mp3")

# Xóa WAV tạm
os.remove(wav_file)

print("✅ Đã tạo bản nhạc phức tạp hơn:", mp3_file)
