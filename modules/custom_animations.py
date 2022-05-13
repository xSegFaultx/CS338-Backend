from collections import OrderedDict
from email.mime import image
import os
import random

import numpy as np

from moviepy.editor import *
import moviepy.video.fx.all as mvpfx
from skimage import transform as tf

### Globals
RESOLUTION = (1920, 1080)

### Utility functions
def scale_image_percent(im_clip, resolution, scale):
    # Compare aspect ratio of canvas and clip
    canvas_aspect_rat = resolution[0] / resolution[1]
    im_clip_aspect_rat = im_clip.aspect_ratio

    # If clip is wider, scale along x
    if im_clip_aspect_rat >= canvas_aspect_rat:
        im_clip = mvpfx.resize(im_clip, width = resolution[0] * scale)
    # If clip is taller, scale along y
    else:
        im_clip = mvpfx.resize(im_clip, height = resolution[1] * scale)
    return im_clip

def dynamic_resize_func(fade_in_dur = 0, start_size = 0, fade_out_dur = 0, end_size = 0, clip_dur = 10):
    # Returns a funciton for use in moviepy resizing according to specified parameters
    if start_size == 0:
        start_size = 0.01
    if end_size == 0:
        end_size = 0.01

    def resize_func(t):
        if t > clip_dur:
            # Went past the expected time. Just hold at our end size
            return end_size
        elif t < fade_in_dur:
            # Fading in
            return start_size + ((t / fade_in_dur) * (1 - start_size))
        elif t >= clip_dur - fade_out_dur:
            # Fading out
            return (1 - (t - (clip_dur - fade_out_dur)) / fade_out_dur) * (1 - end_size) + end_size
        else:
            return 1

    return resize_func


### Bases for animations

def single_fadeinout(image_paths, audio_path, resolution, scale = 0.75, position = "center", fade_duration = 1.5, min_clip_duration=0):
    """
    image_path: list of path to image for clip
    audio_path: path for audio for clip
    resolution: desired resolution of clip
    position: position for image to be located (default: "center")
    scale: relative scaling of image to canvas (default: 0.75)
    fade_duration: duration of fade effect (default: 1.5)
    min_clip_duration: minimum length of clip (default: 0)
    """
    if len(image_paths) < 1:
        raise("Clip Generation: No images received")
    image_path = image_paths[0]

    aud_clip = AudioFileClip(audio_path, fps = 44100)
    aud_clip = aud_clip.set_start(fade_duration/2)
    
    clip_duration = max(aud_clip.duration + fade_duration, min_clip_duration)
    im_clip = ImageClip(image_path, duration=clip_duration).crossfadein(fade_duration)
    im_clip = im_clip.crossfadeout(fade_duration)
    im_clip = im_clip.set_position(position)
    im_clip = scale_image_percent(im_clip, resolution, scale)

    out_audio = CompositeAudioClip(
        [aud_clip],
    )
    out_video = CompositeVideoClip(
        [im_clip],
        size = resolution,
    )

    out_video.audio = out_audio

    out_video = out_video.set_duration(clip_duration)

    return out_video

def single_growinout(image_paths, audio_path, resolution, scale = 0.75, position = "center", anim_duration = 1, min_clip_duration=0):
    """
    image_path: list of path to image for clip
    audio_path: path for audio for clip
    resolution: desired resolution of clip
    position: position for image to be located (default: "center")
    scale: relative scaling of image to canvas (default: 0.75)
    fade_duration: duration of fade effect (default: 1.5)
    min_clip_duration: minimum length of clip (default: 0)
    """
    if len(image_paths) < 1:
        raise("Clip Generation: No images received")
    image_path = image_paths[0]

    aud_clip = AudioFileClip(audio_path, fps = 44100)
    aud_clip = aud_clip.set_start(anim_duration / 2)
    
    clip_duration = max(aud_clip.duration + anim_duration*1.5, min_clip_duration)
    resize_fun = dynamic_resize_func(
        fade_in_dur = anim_duration,
        start_size = 0,
        fade_out_dur = anim_duration/2,
        end_size = 0,
        clip_dur = clip_duration
    )
    
    im_clip = ImageClip(image_path, duration=clip_duration)
    im_clip = scale_image_percent(im_clip, resolution, scale)
    im_clip = im_clip.resize(resize_fun)
    im_clip = im_clip.set_position(position)


    out_audio = CompositeAudioClip(
        [aud_clip],
    )
    out_video = CompositeVideoClip(
        [im_clip],
        size = resolution,
    )

    out_video.audio = out_audio

    out_video = out_video.set_duration(clip_duration)

    return out_video

def single_fadeinout_pan(image_paths, audio_path, resolution, scale = 0.9, start_pos = (0, 0), end_pos = None, fade_duration = 2.5, min_clip_duration = 0):
    if len(image_paths) < 1:
        raise("Clip Generation: No images received")
    image_path = image_paths[0]

    if end_pos is None:
        # Default to resolution
        end_pos = resolution

    aud_clip = AudioFileClip(audio_path, fps=44100)
    aud_clip = aud_clip.set_start(fade_duration/2)

    clip_duration = max(aud_clip.duration + fade_duration, min_clip_duration)

    im_clip = ImageClip(image_path, duration=clip_duration).crossfadein(fade_duration)
    im_clip = im_clip.crossfadeout(fade_duration)
    im_clip = scale_image_percent(im_clip, resolution, scale)
    end_pos = (end_pos[0] - im_clip.w, end_pos[1] - im_clip.h)
    im_clip = im_clip.set_position(lambda t: ((end_pos[0] - start_pos[0])*(t/clip_duration), (end_pos[1] - start_pos[1])*(t/clip_duration)))

    out_audio = CompositeAudioClip(
        [aud_clip],
    )
    out_video = CompositeVideoClip(
        [im_clip],
        size = resolution,
    )

    out_video.audio = out_audio

    out_video = out_video.set_duration(clip_duration)

    return out_video

def single_fadein_pan(image_paths, audio_path, resolution, scale = 0.9, start_pos = (0, 0), end_pos = None, fade_duration = 2.5, min_clip_duration = 0):
    if len(image_paths) < 1:
        raise("Clip Generation: No images received")
    image_path = image_paths[0]

    if end_pos is None:
        # Default to resolution
        end_pos = resolution

    aud_clip = AudioFileClip(audio_path, fps=44100)
    aud_clip = aud_clip.set_start(fade_duration/2)

    clip_duration = max(aud_clip.duration + fade_duration, min_clip_duration)

    im_clip = ImageClip(image_path, duration=clip_duration).crossfadein(fade_duration)
    im_clip = scale_image_percent(im_clip, resolution, scale)
    im_clip = im_clip.set_position(lambda t: ((end_pos[0] - start_pos[0])*(t/clip_duration), (end_pos[1] - start_pos[1])*(t/clip_duration)))

    out_audio = CompositeAudioClip(
        [aud_clip],
    )
    out_video = CompositeVideoClip(
        [im_clip],
        size = resolution,
    )

    out_video.audio = out_audio

    out_video = out_video.set_duration(clip_duration)

    return out_video

def double_corner_fadein(image_paths, audio_path, resolution, scale = 0.65, positions = (("left", "top"), ("right", "bottom")), fade_duration = (1.5, 1.5), min_clip_duration = 0):
    aud_clip = AudioFileClip(audio_path, fps = 44100)
    aud_clip = aud_clip.set_start(fade_duration[0]/2)

    clip_duration = max(aud_clip.duration + fade_duration[0], min_clip_duration)
    im_clip_1 = ImageClip(image_paths[0], duration = clip_duration).crossfadein(fade_duration[0])
    im_clip_1 = im_clip_1.crossfadeout(fade_duration[0]).set_position(positions[0])
    im_clip_1 = scale_image_percent(im_clip_1, resolution, scale)

    im_clip_2 = ImageClip(image_paths[1], duration = clip_duration * 2/3).crossfadein(fade_duration[1])
    im_clip_2 = im_clip_2.crossfadeout(fade_duration[0]).set_position(positions[1]).set_start(clip_duration * 1/3)
    im_clip_2 = scale_image_percent(im_clip_2, resolution, scale)

    out_audio = CompositeAudioClip(
        [aud_clip],
    )

    out_video = CompositeVideoClip(
        [im_clip_1, im_clip_2],
        size = resolution
    )

    out_video.audio = out_audio

    out_video = out_video.set_duration(clip_duration)

    return out_video

def double_fade_conseq(image_paths, audio_path, resolution, scale = 0.75, positions = ("center", "center"), fade_duration = (1.5, 1.5), min_clip_duration = 5):
    aud_clip = AudioFileClip(audio_path, fps = 44100)
    aud_clip = aud_clip.set_start(fade_duration[0]/2)

    clip_duration = max(aud_clip.duration + fade_duration[0], min_clip_duration)
    im_clip_1 = ImageClip(image_paths[0], duration = clip_duration/2).crossfadein(fade_duration[0])
    im_clip_1 = im_clip_1.crossfadeout(fade_duration[0]).set_position(positions[0])
    im_clip_1 = scale_image_percent(im_clip_1, resolution, scale)

    im_clip_2 = ImageClip(image_paths[1], duration = clip_duration/2).crossfadein(fade_duration[1])
    im_clip_2 = im_clip_2.crossfadeout(fade_duration[0]).set_position(positions[1]).set_start(clip_duration/2)
    im_clip_2 = scale_image_percent(im_clip_2, resolution, scale)

    out_audio = CompositeAudioClip(
        [aud_clip],
    )

    out_video = CompositeVideoClip(
        [im_clip_1, im_clip_2],
        size = resolution
    )

    out_video.audio = out_audio

    out_video = out_video.set_duration(clip_duration)

    return out_video

def triple_2corner_fadein(image_paths, audio_path, resolution, scale = (0.60, 0.45, 0.45), positions = ("center", ("left", "top"), ("right", "bottom")), fade_duration = (1.5, 1.0, 1.0), min_clip_duration = 5):
    audio_delay = 1.4

    aud_clip = AudioFileClip(audio_path, fps = 44100)
    aud_clip = aud_clip.set_start(audio_delay)

    clip_duration = max(aud_clip.duration + audio_delay, min_clip_duration)
    im_clip_1 = ImageClip(image_paths[0], duration = clip_duration - 2).crossfadein(fade_duration[0])
    im_clip_1 = im_clip_1.crossfadeout(fade_duration[0]).set_position(positions[0]).set_start(2)
    im_clip_1 = scale_image_percent(im_clip_1, resolution, scale[0])

    im_clip_2 = ImageClip(image_paths[1], duration = clip_duration).crossfadein(fade_duration[1])
    im_clip_2 = im_clip_2.crossfadeout(fade_duration[1]).set_position(positions[1])
    im_clip_2 = scale_image_percent(im_clip_2, resolution, scale[1])

    im_clip_3 = ImageClip(image_paths[2], duration = clip_duration - 0.8).crossfadein(fade_duration[2])
    im_clip_3 = im_clip_3.crossfadeout(fade_duration[2]).set_position(positions[2]).set_start(0.8)
    im_clip_3 = scale_image_percent(im_clip_3, resolution, scale[2])

    out_audio = CompositeAudioClip(
        [aud_clip],
    )

    out_video = CompositeVideoClip(
        [im_clip_2, im_clip_3, im_clip_1],
        size = resolution
    )

    out_video.audio = out_audio

    out_video = out_video.set_duration(clip_duration)

    return out_video

def triple_fade_conseq(image_paths, audio_path, resolution, scale = 0.75, positions = ("center", "center", "center"), fade_duration = (1.0, 1.5, 1.5), min_clip_duration = 8):
    aud_clip = AudioFileClip(audio_path, fps = 44100)
    aud_clip = aud_clip.set_start(fade_duration[0]/2)

    clip_duration = max(aud_clip.duration + fade_duration[0], min_clip_duration)
    im_clip_1 = ImageClip(image_paths[0], duration = clip_duration/3).crossfadein(fade_duration[0])
    im_clip_1 = im_clip_1.crossfadeout(fade_duration[0]).set_position(positions[0])
    im_clip_1 = scale_image_percent(im_clip_1, resolution, scale)

    im_clip_2 = ImageClip(image_paths[1], duration = clip_duration/3).crossfadein(fade_duration[1])
    im_clip_2 = im_clip_2.crossfadeout(fade_duration[1]).set_position(positions[1]).set_start(clip_duration/3)
    im_clip_2 = scale_image_percent(im_clip_2, resolution, scale)

    im_clip_3 = ImageClip(image_paths[2], duration = clip_duration/3).crossfadein(fade_duration[2])
    im_clip_3 = im_clip_3.crossfadeout(fade_duration[2]).set_position(positions[2]).set_start(2*clip_duration/3)
    im_clip_3 = scale_image_percent(im_clip_3, resolution, scale)

    out_audio = CompositeAudioClip(
        [aud_clip],
    )

    out_video = CompositeVideoClip(
        [im_clip_1, im_clip_2, im_clip_3],
        size = resolution
    )

    out_video.audio = out_audio

    out_video = out_video.set_duration(clip_duration)

    return out_video

### Second-order animation functions, set up w/ consistent args images_paths, audio_paths, resolution

def single_fadeinout_center_75(image_paths, audio_path, resolution):
    return single_fadeinout(image_paths, audio_path, resolution, scale = 0.75, position = "center", fade_duration = 1.5, min_clip_duration=0)

def single_fadeinout_center_90(image_paths, audio_path, resolution):
    return single_fadeinout(image_paths, audio_path, resolution, scale = 0.9, position = "center", fade_duration = 3, min_clip_duration=0)

def single_fadeinout_upleft(image_paths, audio_path, resolution):
    return single_fadeinout(image_paths, audio_path, resolution, scale = 0.9, position=("left", "top"), fade_duration = 2, min_clip_duration=0)

def single_fadeinout_downright(image_paths, audio_path, resolution):
    return single_fadeinout(image_paths, audio_path, resolution, scale = 0.9, position=("right", "bottom"), fade_duration=2, min_clip_duration=0)

def single_fadeinout_pan_90(image_paths, audio_path, resolution):
    return single_fadeinout_pan(image_paths, audio_path, resolution)

def single_fadein_panout_l2r(image_paths, audio_path, resolution):
    return single_fadein_pan(image_paths, audio_path, resolution, scale = 0.9, start_pos = (0, 54), end_pos = (resolution[0], 54), fade_duration = 3, min_clip_duration = 5)

def single_growinout_center(image_paths, audio_path, resolution):
    return single_growinout(image_paths, audio_path, resolution, scale = 0.75, position="center")

def single_growinout_upright(image_paths, audio_path, resolution):
    return single_growinout(image_paths, audio_path, resolution, scale = 0.75, position=("right", "top"))

def single_growinout_downleft(image_paths, audio_path, resolution):
    return single_growinout(image_paths, audio_path, resolution, scale = 0.75, position=("left", "bottom"))

def double_corner_fi_uldr(image_paths, audio_path, resolution):
    return double_corner_fadein(image_paths, audio_path, resolution)

def double_corner_fi_drul(image_paths, audio_path, resolution):
    return double_corner_fadein(image_paths, audio_path, resolution, positions = (("right", "bottom"), ("left", "top")))

def double_corner_fi_urdl(image_paths, audio_path, resolution):
    return double_corner_fadein(image_paths, audio_path, resolution, positions = (("right", "top"), ("left", "bottom")))

def double_corner_fi_dlur(image_paths, audio_path, resolution):
    return double_corner_fadein(image_paths, audio_path, resolution, positions = (("left", "bottom"), ("right", "top")))

ANIMATIONS = {
    1: [
        single_fadeinout_center_75,
        single_fadeinout_center_90,
        single_fadeinout_upleft,
        single_fadeinout_downright,
        single_fadeinout_pan_90,
        single_fadein_panout_l2r,
        single_growinout_center,
        single_growinout_downleft,
        single_growinout_upright,
        ],
    2: [
        double_corner_fi_uldr,
        double_corner_fi_drul,
        double_corner_fi_urdl,
        double_corner_fi_dlur,
        double_fade_conseq,
        ],
    3: [
        triple_2corner_fadein,
        triple_fade_conseq,
    ],
}

def compose_clip(clip):
    clip_im_size = len(clip["images"])
    clip_fun = random.choice(ANIMATIONS[clip_im_size])

    return clip_fun(clip['images'], clip['audio'], RESOLUTION)



def make_movie(images, audios, video_name = "tmp.mp4"):
    file_path = os.path.join(os.getcwd(), "video/")
    is_exist = os.path.exists(file_path)

    if not is_exist:
        os.makedirs(file_path)

    file_path = os.path.join(file_path, video_name)
    clips = OrderedDict()

    for dic in images:
        for key, im in dic.items():
            clips[key] = {"images": im}
    print(clips)
    print("IMAGES")
    print(images)
    for dic in audios:
        for key, aud in dic.items():
            clips[key]["audio"] = aud

    composed_clips = [compose_clip(clip) for _, clip in clips.items()]

    video = concatenate_videoclips(composed_clips)
    video.write_videofile(file_path, fps=30, codec="libx264", audio_codec='aac')

    return file_path


if __name__ == '__main__':
    images = [
        {"birth": [os.path.join(os.getcwd(), "backend/modules/test_media/birthday.jpg")]},
        {"death": [os.path.join(os.getcwd(), "backend/modules/test_media/headstone.jpeg"),
            os.path.join(os.getcwd(), "backend/modules/test_media/birthday.jpg")]},
        {"fake": [os.path.join(os.getcwd(), "backend/modules/test_media/headstone.jpeg"), 
            os.path.join(os.getcwd(), "backend/modules/test_media/northwestern.png"),
            os.path.join(os.getcwd(), "backend/modules/test_media/birthday.jpg")]}
    ]
    audios = [
        {"birth": os.path.join(os.getcwd(), "backend/modules/test_media/testsound.mp3")},
        {"death": os.path.join(os.getcwd(), "backend/modules/test_media/testsound.mp3")},
        {"fake": os.path.join(os.getcwd(), "backend/modules/test_media/testsound.mp3")}
    ]

    make_movie(images, audios)
    #tclip1 = single_image_fadeinout("birthday.jpg", "testsound.mp3", (1920, 1080))
    #tclip2 = single_image_fadeinout("bday_cake.jpg", "testsound.mp3", (1920, 1080))
    #testvid = concatenate_videoclips([tclip1, tclip2])
    #testvid.write_videofile("spamtest.mp4", fps=24, codec='libx264')