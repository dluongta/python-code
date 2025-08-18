from moviepy.editor import ImageClip, CompositeVideoClip
from moviepy.video.fx import all as vfx

# Configuration for effects and video durations
EFFECT_DURATION = 0.3  # Duration of the transition effect
CLIP_DURATION = 3.3    # Duration of each image clip

# Load image clips and resize them to match the screen resolution (1280x720)
input_image1 = ImageClip("input-image1.png").set_duration(CLIP_DURATION).resize((1280, 720))
input_image2 = ImageClip("input-image2.png").set_duration(CLIP_DURATION).resize((1280, 720))
input_image3 = ImageClip("input-image3.png").set_duration(CLIP_DURATION).resize((1280, 720))

# List of clips
clips = [input_image1, input_image2, input_image3]

# Function for custom slide-out effect (to simulate sliding out to the left)
def slide_out(clip, direction="left", duration=EFFECT_DURATION):
    if direction == "left":
        return clip.set_position(lambda t: (min(0, t * (clip.size[0] / duration) - clip.size[0]), "center"))
    elif direction == "right":
        return clip.set_position(lambda t: (max(0, -t * (clip.size[0] / duration) + clip.size[0]), "center"))

# Function for custom slide-in effect (to simulate sliding in from the right)
def slide_in(clip, direction="right", duration=EFFECT_DURATION):
    if direction == "right":
        return clip.set_position(lambda t: (max(0, -clip.size[0] + t * (clip.size[0] / duration)), "center"))
    elif direction == "left":
        return clip.set_position(lambda t: (min(0, clip.size[0] - t * (clip.size[0] / duration)), "center"))

# First clip stays visible for the duration
first_clip = CompositeVideoClip(
    [clips[0]]  # First image clip stays visible
).set_start(0).set_duration(CLIP_DURATION)  # Set duration for the first clip

# Second clip slides in from the right, while the first clip slides out
second_clip = CompositeVideoClip(
    [slide_out(clips[1], direction="left", duration=EFFECT_DURATION),  # Slide out the first image
     slide_in(clips[0], direction="right", duration=EFFECT_DURATION)]  # Slide in the second image
).set_start(CLIP_DURATION - EFFECT_DURATION).set_duration(CLIP_DURATION)  # Second clip starts after first

# Third clip slides in from the right, while the second clip slides out
third_clip = CompositeVideoClip(
    [slide_out(clips[2], direction="left", duration=EFFECT_DURATION),  # Slide out the second image
     slide_in(clips[1], direction="right", duration=EFFECT_DURATION)]  # Slide in the third image
).set_start(CLIP_DURATION * 2 - EFFECT_DURATION).set_duration(CLIP_DURATION)  # Third clip starts after second

# Combine all clips into one final video
all_clips = [first_clip, second_clip, third_clip]

# Final video composite
final_video = CompositeVideoClip(all_clips)

# Write the final video to file
final_video.write_videofile(
    "final_video_with_slider.mp4",
    codec="libx264",
    audio_codec="aac",
    preset="ultrafast",
    fps=24,
    threads=24,
    ffmpeg_params=["-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2", "-pix_fmt", "yuv420p"],
)
