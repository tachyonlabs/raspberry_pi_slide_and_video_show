# Raspberry Pi Instagram Slide and Video Show

## About

I'm a volunteer at the [Idea Fab Labs](https://santacruz.ideafablabs.com/) maker/hacker/artspace here in Santa Cruz, and I was asked to set up a Raspberry Pi with a large monitor by the front entrance so that all you had to do was plug it in and it would start running a slideshow of [Idea Fab Labs' Instagram feed](https://www.instagram.com/ideafablabs/) of photos of projects, facilities, and events.

I had written my original [Raspberry Pi Instagram Slideshow](https://github.com/tachyonlabs/raspberry_pi_instagram_slideshow) version in Python using the Tkinter GUI, but when I was asked to update it to include Instagram videos as well as photos, I rewrote it (still in Python) using the Kivy Framework. I'm running it with Python 2 on a Raspberry Pi 2 Model B running Raspbian Jessie now, and will soon be testing it on a Raspberry Pi 2 Model B running Raspbian Wheezy, in addition to Python 3.

Anyway, if you'd like to do a similar installation with your own Instagram feed, the instructions below will walk you through getting the slide and video show set up on your Raspberry Pi.

Because (at least as of September 2017) the Instagram API in [Sandbox Mode](https://www.instagram.com/developer/sandbox/) only gets the 20 most recent photos and videos from an Instagram account, and in the interest of both reducing bandwidth and being able to run the slide and video show even when your internet connection is down, once an hour the program checks Instagram to see if any new photos and videos have been posted to the account, and if so, downloads them to its `instagram_photos_and_videos` directory. (If you like you can also copy other jpg and mp4 files to the directory and they will also be included in the slide and video show -- for that matter I used the [InstaG Downloader Chrome Extension](https://chrome.google.com/webstore/detail/instag-downloader/jnkdcmgmnegofdddphijckfagibepdlb?hl=en) to download all the photos and videos from the Idea Fab Labs Instagram feed that were older than the 20 most recent, so they would be in the `instagram_photos_and_videos` directory too.)

You can configure whether the program displays photos and videos in random order, in the order they are in the `instagram_photos_and_videos` directory, or in sorted lexicographic order (the default is random), and/or configure how long the program displays a photo before moving on to the next photo or video (the default is 15 seconds). Right now you can do this by editing the `instagram_slide_and_video_show.ini` file that the program creates in the `instagram_slide_and_video` directory the first time it runs, or by modifying the code, but later I'll probably add a settings dialog box as I had done in the Tkinter version.

More features later perhaps ...

## Known issues

* **Hanging**: I'm still working on tracking down an issue where the slide and video show will sometimes hang seemingly randomly. As the program is otherwise working, I decided to go ahead and put the initial version up on GitHub now, but I hope to find and fix the bug soon.

* **"Error loading texture" error messages**: Every time the program loads a video, an "Error loading texture" message gets printed to the console or terminal window. On one hand I haven't found a way to get rid of them yet, but on the other hand, the videos are playing just fine regardless.

## Getting the slide and video show set up on your Raspberry Pi
Follow these instructions to get the slide and video show set up and running on your Raspberry Pi:

1. **Command-line vs. GUI?**

    The slide and video show doesn't require the Raspberry Pi GUI desktop to run, and because of the limited resources of the Raspberry Pi vs. playing videos, I would recommend that when running it you have your Raspberry Pi boot to the command line rather than to the GUI desktop, but you can run it either way.

2. **Configure your Raspberry Pi to connect to your Wifi if you haven't done so already**

    To download Instagram photos and videos (or for that matter to continue following these instructions) your Raspberry Pi needs to be connected to the Internet. If you haven't already done so, do the following to select your Wifi network and enter the password:

    * Here's the [official Raspberry Pi documentation on setting Wifi up via the command line](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md).

    * Or for Raspbian Wheezy and the LXDE GUI desktop, in the Raspberry Pi GUI Menu select `Preferences` and then `WIFI Configuration`.

    * Or for Raspbian Jessie and the Pixel GUI desktop, click the Wifi icon at the top right of the taskbar.

3. **Configure the Raspberry Pi to allocate more memory to its GPU (graphics processing unit)**

    At one point when I was wrestling with Kivy and video I followed a suggestion to use the instructions on [this RPiconfig page](http://elinux.org/RPiconfig) to add the line
    ```
    gpu_mem=128
    ```
    to the `/boot/config` file. For this particular application this may or may not actually make a difference, but you might want to experiment with that or different gpu_mem values.

4. **Install the Kivy framework on your Raspberry Pi**

    Follow the instructions at [https://kivy.org/docs/installation/installation-rpi.html](https://kivy.org/docs/installation/installation-rpi.html) to download/install/compile Kivy on your Raspberry Pi, noting that the instructions vary a little depending on whether your version of Raspbian is Jessie or Wheezy. Warning: This can seriously sometimes take hours to complete, so start it sometime when you can just let things run.

5. **Install the Python requests library**

    The slide and video show uses the Python requests library to talk to the Instagram API -- install it by entering the following at the command line or into a terminal window:
    ```
    sudo pip install requests
    ```

6. **Create a directory for the slideshow, and copy the files from this repo into it**

    Create a directory `instagram_slide_and_video_show` in the `/home/pi/` directory, and copy the files `instagram_slide_and_video_show.py`, `instagram_slide_and_video_show.bat`, and `instagram_slide_and_video_show_gui.bat` from this repo into it. (Or if you prefer you can use a different slideshow directory name and/or location, adjusting its name/location in subsequent steps accordingly.)

7. **Make `instagram_slide_and_video_show.bat` and `instagram_slide_and_video_show_gui.bat` executable.**

    Make the files `instagram_slide_and_video_show.bat` and `instagram_slide_and_video_show_gui.bat` executable by entering the following at the command line or into a terminal window:
    ```
    chmod 755 /home/pi/instagram_slide_and_video_show/instagram_slide_and_video_show.bat
    chmod 755 /home/pi/instagram_slide_and_video_show/instagram_slide_and_video_show_gui.bat
    ```

8. **Get the Instagram access token for the account you want to use with the slide and video show, and enter it into the program code**

    There are other ways to download Instagram photos than their API, but I used their API. When I was using the Instagram API for another project last year, all you needed to do to download photos from an account was to register as a developer and get a client id, but now you have to go through a lot more steps to generate an access token for the account you want to access. To get the access token I followed the instructions on this [How to get Instagram API access token and fix your broken feed](https://github.com/adrianengine/jquery-spectragram/wiki/How-to-get-Instagram-API-access-token-and-fix-your-broken-feed) page, and as I do some Django development I used the Django development server (as `python manage.py runserver 0.0.0.0:8000` on my Windows system) in their "your favorite MAMP, LAMP, Node whatever you use to create a local server" step.

    When you get the access token you need, use a text editor or IDE to substitute it for "put your access token here" in the line
    ```
    self.INSTAGRAM_ACCESS_TOKEN = "put your access token here"
    ```
    in `instagram_slide_and_video_show.py`.

9. **Set the Raspberry Pi to run the slideshow automatically when it boots**

    * If your Raspberry Pi is set to boot to the command line:

        Follow the instructions on the official [Raspberry Pi rc.local page](https://www.raspberrypi.org/documentation/linux/usage/rc-local.md) to add the line
        ```
        /home/pi/instagram_slide_and_video_show/instagram_slide_and_video_show.bat &
        ```
        to your `etc.rclocal` file.

    * If your Raspberry Pi is set to boot to the GUI desktop:

        The issue here is that you want the program to run not only after the Raspberry Pi boots, but after the GUI loads.

        What worked for me was following the instructions in one of the posts in the [How to launch programs on LXDE startup](https://www.raspberrypi.org/forums/viewtopic.php?f=27&t=11256) topic in the raspberypi.org forums, doing

        * For Raspbian Wheezy with the LXDE GUI desktop: `sudo nano /etc/xdg/lxsession/LXDE-pi/autostart`

        * For Raspbian Jessie with the Pixel GUI desktop: `sudo nano /home/pi/.config/lxsession/LXDE-pi/autostart`

    to edit the autostart file, adding the line
    ```
    @/home/pi/instagram_slide_and_video_show/instagram_slide_and_video_show_gui.bat
    ```
    to the end of the file, and saving it.

10. **Disable the Raspberry Pi screensaver**

    It's great to be have the Raspberry Pi set up so that all you have to do is plug it in and the slide and video show will start, without needing to have a keyboard and/or mouse connected, but pretty sad if it only lasts for ten or fifteen minutes until the screensaver blanks the screen. :-(

    * What worked for me with Raspbian Jessie set to boot to the command line was following the `consoleblank=0` instructions on the official [Raspberry Pi "Setting the Screen Saver/Screen Blanking"](https://www.raspberrypi.org/documentation/configuration/screensaver.md) page.

    * What worked for me with Raspbian Wheezy and the LXDE GUI desktop was following the "2 – Disabling the blank screen forever" instuctions in this [How to Disable the Blank Screen on Raspberry Pi (Raspbian)](http://www.geeks3d.com/hacklab/20160108/how-to-disable-the-blank-screen-on-raspberry-pi-raspbian/) HackLab post.

    * What worked for me with Raspbian Jessie and the Pixel GUI desktop was adding the line `xserver-command=X -s 0 dpms` to `/etc/lightdm/lightdm.conf` as described in this [Raspberry Pi Stack Exchange comment](https://raspberrypi.stackexchange.com/questions/752/how-do-i-prevent-the-screen-from-going-blank/51687#51687).

## Running the slide and video show on your Raspberry Pi

Once you've followed all the above steps, reboot your Raspberry Pi, and once it finishes booting the slideshow should start running automatically.

Or if you didn't want to set it to run automatically, you can just run it from the command-line (if you're running the GUI desktop then this would be in a terminal window) by navigating to the `/home/pi/instagram_slide_and_video_show/` directory and entering
```
python instagram_slide_and_video_show.py
```
at the prompt.

The first time you run the program, it will create an `instagram_photos_and_videos` subdirectory, and you'll see messages about photos and videos being downloaded before it starts displaying them.

If your Raspberry Pi isn't connected to the Internet, or if you haven't obtained an Instagram Access Token for the Instagram account you want to use, and entered it correctly as the `self.INSTAGRAM_ACCESS_TOKEN` value at the beginning of the code, you'll see error messages about that instead of photos and videos.

If at any point you want to close the slideshow, just press `Esc`.
