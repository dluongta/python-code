from moviepy.editor import VideoFileClip
import subprocess

def hms_to_seconds(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)
def cut_video_keep_quality(input_path, output_path, start_time, end_time):
    if isinstance(start_time, str):
        start_time_sec = hms_to_seconds(start_time)
    else:
        start_time_sec = float(start_time)

    if isinstance(end_time, str):
        end_time_sec = hms_to_seconds(end_time)
    else:
        end_time_sec = float(end_time)

    duration = end_time_sec - start_time_sec
    if duration <= 0:
            print("Thời lượng cắt phải lớn hơn 0.")
            return
    cmd = [
        "ffmpeg",
        "-ss", str(start_time),       
        "-i", input_path,            
        "-t", str(duration),          
        "-c", "copy",                 
        output_path
    ]

    try:
        subprocess.run(cmd, check=True)
        print("Cắt video thành công:", output_path)
    except subprocess.CalledProcessError as e:
        print("Lỗi khi cắt video:", e)

"""
def cut_video_with_moviepy(input_path, output_path, start_time, end_time):

    with VideoFileClip(input_path) as video:
        new_clip = video.subclip(start_time, end_time)
        
        new_clip.write_videofile(
            output_path,
            codec="libx264",      
            audio_codec="aac",    
            preset="medium",      
            threads=4,
            bitrate="5000k"      
        )

cut_video_with_moviepy("input.mp4", "output_cut.mp4", 10, 60)
"""
"""
cut_video_keep_quality(
    input_path="video_with_audio.mp4",
    output_path="output.mp4",
    start_time=0,
    end_time=600
)
"""
cut_video_keep_quality(
    input_path="video_with_audio.mp4",
    output_path="output_cut.mp4",
    start_time="00:00:00",
    end_time="00:10:00"
)

