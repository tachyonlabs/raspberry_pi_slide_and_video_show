import kivy
kivy.require('1.0.6') # replace with your current kivy version !
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.video import Video
from kivy.clock import Clock
import requests
import json
import os
import random
from datetime import datetime
import ConfigParser

class SlideAndVideoShow(App):
    def __init__(self):
        super(SlideAndVideoShow, self).__init__()
        self.INSTAGRAM_ACCESS_TOKEN = "put your access token here"
        self.MOST_RECENT_PHOTOS_AND_VIDEOS_URL = "https://api.instagram.com/v1/users/self/media/recent/?access_token={}".format(self.INSTAGRAM_ACCESS_TOKEN)
        self.LOCAL_PHOTO_AND_VIDEO_DIRECTORY_PATH = "./instagram_photos_and_videos/"
        self.INI_FILE = "./instagram_slide_and_video_show.ini"
        self.title = "Instagram Slide and Video Show"
        self.HOUR_IN_SECONDS = 60 * 60
        # default configuration settings, used to create instagram_slide_and_video_show.ini if ir doesn't already exist
        self.SECONDS_BEFORE_CHANGING_PHOTO = 15
        self.PHOTO_AND_VIDEO_DISPLAY_ORDER_DIRECTORY = "directory"
        self.PHOTO_AND_VIDEO_DISPLAY_ORDER_RANDOM = "random"
        self.PHOTO_AND_VIDEO_DISPLAY_ORDER_SORTED = "sorted"
        self.PHOTO_AND_VIDEO_DISPLAY_ORDER = self.PHOTO_AND_VIDEO_DISPLAY_ORDER_RANDOM
        # get stored configuration settings
        self.get_preferences_from_ini_file()
        # download any new photos or videos
        self.download_any_new_instagram_photos_or_videos()
        # get the filenames of all newly and/or previously-downloaded photos and videos
        self.photos_and_videos = self.get_photo_and_video_filenames()
        self.current_image_index = -1

    def get_preferences_from_ini_file(self):
        if os.path.isfile(self.INI_FILE):
            # if the .ini file exists, read in the configuration settings
            config = ConfigParser.RawConfigParser()
            config.read(self.INI_FILE)
            self.PHOTO_AND_VIDEO_DISPLAY_ORDER = config.get("DisplaySettings", "photo_and_video_display_order")
            self.SECONDS_BEFORE_CHANGING_PHOTO = int(config.get("DisplaySettings", "seconds_before_changing_photo"))
        else:
            # or if it doesn't exist, create it with the default settings
            self.create_ini_file()

    def create_ini_file(self):
        # create the ini file with the default settings the first time you run the program,
        config = ConfigParser.RawConfigParser(allow_no_value=True)
        ini_file = open(self.INI_FILE, 'w')
        config.add_section("DisplaySettings")
        config.set('DisplaySettings', '; Valid display order settings are directory, random, or sorted')
        config.set("DisplaySettings", "photo_and_video_display_order", self.PHOTO_AND_VIDEO_DISPLAY_ORDER)
        config.set("DisplaySettings", "seconds_before_changing_photo", self.SECONDS_BEFORE_CHANGING_PHOTO)
        config.write(ini_file)
        ini_file.close()

    def download_any_new_instagram_photos_or_videos(self, value=None):
        # create the instagram_photos_and_videos subdirectory if it doesn't already exist
        if not os.path.isdir(self.LOCAL_PHOTO_AND_VIDEO_DIRECTORY_PATH):
            os.mkdir(self.LOCAL_PHOTO_AND_VIDEO_DIRECTORY_PATH)

        print ("Checking for any new Instagram photos or videos at {} ...".format(datetime.now()))
        internet_connection = True

        # get URLs, captions, etc. on the 20 most recent Instagram photos and videos
        try:
            json_data = json.loads(requests.get(self.MOST_RECENT_PHOTOS_AND_VIDEOS_URL).text)
        except:
            internet_connection = False
            print ("Unable to reach Instagram ... check your Internet connection. Showing stored photos and videos.")

        if internet_connection:
            new_photos_and_videos_downloaded = False

            # and check to see whether or not they have already been downloaded
            try:
                for photo_or_video in json_data["data"]:
                    if "videos" in photo_or_video:
                        photo_or_video_url = photo_or_video["videos"]["standard_resolution"]["url"]
                    else:
                        photo_or_video_url = photo_or_video["images"]["standard_resolution"]["url"]

                    photo_or_video_filename = photo_or_video_url[photo_or_video_url.rindex("/") + 1:]
                    if not os.path.isfile(self.LOCAL_PHOTO_AND_VIDEO_DIRECTORY_PATH + photo_or_video_filename):
                        new_photos_and_videos_downloaded = True
                        print ('Downloading and saving "{}"'.format(photo_or_video["caption"]["text"].encode("utf8")))
                        photo_or_video_file = requests.get(photo_or_video_url).content
                        with open(self.LOCAL_PHOTO_AND_VIDEO_DIRECTORY_PATH + photo_or_video_filename, 'wb') as handler:
                            handler.write(photo_or_video_file)
            except:
                print ("Instagram error:", json_data)

            if new_photos_and_videos_downloaded:
                # update the list of filenames in the instagram_photos_and_videos subdirectory
                self.get_photo_and_video_filenames()
            else:
                print ("No new photos or videos found.")

        # check for new photos and videos once an hour
        Clock.schedule_once(self.download_any_new_instagram_photos_or_videos, self.HOUR_IN_SECONDS)

    def on_position_change(self, instance, value):
        # I'm doing it this way because eos wasn't always firing at the end of a video,
        # plus position isn't updated often enough to get all the way to the duration value.
        # If the program hangs at the end of a video you may need to increase the .3 value
        # (which means .3 of a second) a little more.
        if value > self.video_duration - .3:
            self.video.unload()
            self.next_photo_or_video()

    def on_duration_change(self, instance, value):
        self.video_duration = value

    def on_video_loaded_or_unloaded(self, instance, value):
        # I'm doing it this way because I couldn't get loaded or on_load to actually fire,
        # but texture has reliably only been there only after a video finishes loading.
        if self.video.texture:
            self.video.opacity = 1
            self.photo.opacity = 0

    def build(self):
        # This line is for running under Windows but crashes things on the Raspberry Pi
        # Window.fullscreen = "auto"
        Window.show_cursor = False
        self.photo = Image()
        self.photo.allow_stretch = True
        # Without this line the Raspberry Pi starts blacking out photos after a few images.
        self.photo.nocache = True
        self.video = Video(allow_stretch=True, options={'eos': 'stop'})
        self.video.bind(position=self.on_position_change, duration=self.on_duration_change, texture=self.on_video_loaded_or_unloaded)
        self.video.opacity = 0
        self.screen = FloatLayout()
        self.screen.add_widget(self.photo)
        self.screen.add_widget(self.video)
        Clock.schedule_once(self.next_photo_or_video, 1)
        return self.screen

    def next_photo_or_video(self, value=None):
        if self.PHOTO_AND_VIDEO_DISPLAY_ORDER in [self.PHOTO_AND_VIDEO_DISPLAY_ORDER_DIRECTORY, self.PHOTO_AND_VIDEO_DISPLAY_ORDER_SORTED]:
            self.current_image_index = (self.current_image_index + 1) % len(self.photos_and_videos)
        elif self.PHOTO_AND_VIDEO_DISPLAY_ORDER == self.PHOTO_AND_VIDEO_DISPLAY_ORDER_RANDOM:
            self.current_image_index = random.randint(0, len(self.photos_and_videos) - 1)

        next = self.LOCAL_PHOTO_AND_VIDEO_DIRECTORY_PATH + self.photos_and_videos[self.current_image_index]
        if next.endswith(".jpg"):
            self.photo.source = next
            self.video.opacity = 0
            self.photo.opacity = 1
            Clock.schedule_once(self.next_photo_or_video, self.SECONDS_BEFORE_CHANGING_PHOTO)
        else:
            self.video.source = next
            self.video.state = "play"

    def get_photo_and_video_filenames(self):
        # get all the jpg and mp4 filenames in the instagram_photos_and_videos subdirectory
        photo_and_video_filenames = [file for file in os.listdir(self.LOCAL_PHOTO_AND_VIDEO_DIRECTORY_PATH) if file.endswith(".jpg") or file.endswith(".mp4")]
        if self.PHOTO_AND_VIDEO_DISPLAY_ORDER == self.PHOTO_AND_VIDEO_DISPLAY_ORDER_SORTED:
            photo_and_video_filenames.sort()

        if not photo_and_video_filenames:
            # If there are no stored photos and/or videos, and the program was not able to download any,
            # you need to fix your Internet connection and/or Instagram Access Token.
            print ("No stored photos or videos found. Make sure that you're")
            print ("(1) connected to the Internet, and")
            print ("(2) that you've obtained an Instagram Access Token for the Instagram account you want to use, and entered it correctly as the self.INSTAGRAM_ACCESS_TOKEN value at the beginning of the code,")
            print ("and then try again.")
            exit()

        return photo_and_video_filenames

if __name__ == '__main__':
    SlideAndVideoShow().run()
