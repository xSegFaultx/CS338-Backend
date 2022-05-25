from modules import image_search
import text_to_speech
import custom_animations
import os

import os


def main():
    input = [
        {"name": {"first": "Ken", "last": "Griffin", "pronoun_1": "he", "pronoun_2": "his", "pronoun_3": "him"}},
        {"birth": {"date": "", "location": "Florida, USA"}},
        {"childhood": {"location": "Florida, USA", "start_year": "1968", "end_year": "1986"}},
        {"school": {"name": "Harvard College", "start_year": "1986", "end_year": "1989",
                    "location": "Massachusetts, USA"}},
        {"previous_work": {"start_year": "1989", "end_year": "1990", "name": "Glenwood Capital Investments",
                           "position": "trader"}},
        {"current_status": {"age": "53", "location": "Illinois, USA", "occupation": "CEO",
                            "company": "Citadel LLC"}},
        {"wedding": {"wedding_date": "July 19, 2003", "spouse_name": "Anne Dias-Griffin",
                     "location": "Illinois, USA"}}
    ]

    image_paths = image_search.image_search(input)
    # print(image_paths)
    # audio_paths = text_to_speech.text_to_speech(input)
    # FOR TESTING
    audio_paths = [
        {"birth": os.path.join(os.getcwd(), "modules/test_media/testsound.mp3")},
        {"childhood": os.path.join(os.getcwd(), "modules/test_media/testsound.mp3")},
        {"school": os.path.join(os.getcwd(), "modules/test_media/testsound.mp3")},
        {"previous_work": os.path.join(os.getcwd(), "modules/test_media/testsound.mp3")},
        {"current_status": os.path.join(os.getcwd(), "modules/test_media/testsound.mp3")},
        {"wedding": os.path.join(os.getcwd(), "modules/test_media/testsound.mp3")},
        {"birth": os.path.join(os.getcwd(), "modules/test_media/testsound.mp3")},
        {"school": os.path.join(os.getcwd(), "modules/test_media/testsound.mp3")}
    ]
    video_name = "new_video.mp4"
    video_path = custom_animations.make_movie(image_paths, audio_paths, video_name=video_name)


if __name__ == "__main__":
    main()
