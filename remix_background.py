import subprocess
import numpy as np
from scipy.io import wavfile

# --- 1. THÔNG SỐ CHUNG ---
SAMPLE_RATE = 44100
BPM = 128
BEAT = 60 / BPM
TONG_THOI_GIAN = 18.0  # Chính xác 18 giây

# --- 2. CÔNG CỤ TẠO ÂM THANH (SYNTHESIZERS) ---

def tao_kick():
    t = np.linspace(0, 0.4, int(SAMPLE_RATE * 0.4), False)
    freqs = 150 * np.exp(-20 * t) + 40
    phase = np.cumsum(freqs) * 2 * np.pi / SAMPLE_RATE
    wave = np.sin(phase)
    env = np.exp(-6 * t)
    return wave * env * 1.2

def tao_clap():
    t = np.linspace(0, 0.3, int(SAMPLE_RATE * 0.3), False)
    noise = np.random.uniform(-1, 1, len(t))
    env = np.exp(-15 * t)
    body = np.sin(2 * np.pi * 250 * t) * np.exp(-30 * t)
    return (noise * env + body) * 0.6

def tao_hihat(open_hat=False):
    dur = 0.2 if open_hat else 0.05
    t = np.linspace(0, dur, int(SAMPLE_RATE * dur), False)
    noise = np.random.uniform(-1, 1, len(t))
    env = np.exp(- (20 if not open_hat else 10) * t)
    return noise * env * 0.4

def tao_bass_saw(freq, duration=0.25):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    wave = 2 * (t * freq - np.floor(t * freq + 0.5))
    env = np.exp(-5 * t)
    return wave * env * 0.6

def tao_supersaw_synth(freq, duration=0.2):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    w1 = 2 * (t * freq * 1.00 - np.floor(t * freq * 1.00 + 0.5))
    w2 = 2 * (t * freq * 1.01 - np.floor(t * freq * 1.01 + 0.5))
    w3 = 2 * (t * freq * 0.99 - np.floor(t * freq * 0.99 + 0.5))
    wave = (w1 + w2 + w3) / 3.0
    env = np.exp(-4 * t)
    return wave * env * 0.3

# --- 3. BÀN MIXER TỔNG ---

def them_vao_track(track, am_thanh, start_time):
    idx_start = int(start_time * SAMPLE_RATE)
    idx_end = idx_start + len(am_thanh)
    if idx_start >= len(track):
        return
    if idx_end > len(track):
        am_thanh = am_thanh[:len(track) - idx_start]
    track[idx_start:idx_start + len(am_thanh)] += am_thanh

def apply_delay(track, delay_time, feedback=0.4):
    delay_samples = int(delay_time * SAMPLE_RATE)
    out = np.copy(track)
    for i in range(delay_samples, len(out)):
        out[i] += out[i - delay_samples] * feedback
    return out

# Tạo rãnh âm thanh (18 giây)
so_luong_mau = int(TONG_THOI_GIAN * SAMPLE_RATE)
track_drum = np.zeros(so_luong_mau)
track_bass = np.zeros(so_luong_mau)
track_synth = np.zeros(so_luong_mau)

kick = tao_kick()
clap = tao_clap()
hat_c = tao_hihat(open_hat=False)
hat_o = tao_hihat(open_hat=True)

bass_notes = [55.0, 43.65, 65.41, 49.00] 
melody_notes = [
    [440.0, 523.25, 659.25, 880.0],
    [349.23, 440.0, 523.25, 698.46],
    [523.25, 659.25, 783.99, 1046.5],
    [392.00, 493.88, 587.33, 783.99]
]

print("Đang tính toán tín hiệu nhạc...")

# --- 4. SẮP XẾP BÀI HÁT ---
so_nhip = int(np.ceil(TONG_THOI_GIAN / BEAT))
for nhip in range(so_nhip):
    t = nhip * BEAT
    if t >= TONG_THOI_GIAN:
        break
    
    them_vao_track(track_drum, kick, t)
    
    if nhip % 2 == 1:
        them_vao_track(track_drum, clap, t)
        
    them_vao_track(track_drum, hat_o, t + BEAT * 0.5)
    them_vao_track(track_drum, hat_c, t + BEAT * 0.75)
    
    bar_hien_tai = nhip // 4
    hop_am_idx = bar_hien_tai % 4
    
    note_bass = tao_bass_saw(bass_notes[hop_am_idx], BEAT * 0.25)
    them_vao_track(track_bass, note_bass, t + BEAT * 0.25)
    them_vao_track(track_bass, note_bass, t + BEAT * 0.5)
    them_vao_track(track_bass, note_bass, t + BEAT * 0.75)
    
    tap_hop_not = melody_notes[hop_am_idx]
    if nhip % 4 < 3:
        n1 = tao_supersaw_synth(tap_hop_not[0])
        n2 = tao_supersaw_synth(tap_hop_not[1])
        n3 = tao_supersaw_synth(tap_hop_not[2])
        them_vao_track(track_synth, n1, t)
        them_vao_track(track_synth, n2, t + BEAT * 0.33)
        them_vao_track(track_synth, n3, t + BEAT * 0.66)
    else:
        n_cao = tao_supersaw_synth(tap_hop_not[3])
        them_vao_track(track_synth, n_cao, t)
        them_vao_track(track_synth, tao_supersaw_synth(tap_hop_not[2]), t + BEAT * 0.5)

# --- 5. AUDIO EFFECTS ---
track_synth = apply_delay(track_synth, delay_time=BEAT * 0.75, feedback=0.3)
thoi_gian_tuyen_tinh = np.linspace(0, TONG_THOI_GIAN, len(track_bass), False)
sidechain_env = 1 - 0.8 * np.exp(-15 * (thoi_gian_tuyen_tinh % BEAT))

track_bass = track_bass * sidechain_env
track_synth = track_synth * sidechain_env

master_track = track_drum + track_bass * 1.2 + track_synth * 0.8

# Fade out 1 giây cuối
fade_out_samples = int(SAMPLE_RATE * 1.0)
fade_out = np.linspace(1.0, 0.0, fade_out_samples)
master_track[-fade_out_samples:] *= fade_out

max_amp = np.max(np.abs(master_track))
master_track = master_track / max_amp * 0.9

master_16bit = np.int16(master_track * 32767)

# --- 6. XUẤT TRỰC TIẾP RA MP3 BẰNG SUBPROCESS & FFMPEG ---
print("Đang ép xung và chuyển đổi trực tiếp sang MP3 (320kbps)...")

# Bước tạm lưu ra wav ẩn hoặc truyền thẳng luồng dữ liệu qua stdin của ffmpeg
temp_wav = "temp_output.wav"
wavfile.write(temp_wav, SAMPLE_RATE, master_16bit)

output_mp3 = "remix_background.mp3"
# Gọi lệnh ffmpeg để nén sang mp3 chất lượng cao nhất (320k)
subprocess.run([
    "ffmpeg", "-y", "-i", temp_wav, 
    "-b:a", "320k", output_mp3
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Xóa file wav tạm
import os
if os.path.exists(temp_wav):
    os.remove(temp_wav)

print(f"Thành công! Đã tạo file: {output_mp3} chuẩn chất lượng 320kbps.")