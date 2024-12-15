Wallpaper Changer

A Python-based application to dynamically fetch and set wallpapers for multi-monitor setups. The script fetches random images for each monitor, creates a composite wallpaper that spans all screens (including portrait and landscape orientations), and updates your desktop background automatically.
Features

    Dynamic Multi-Monitor Support:
        Detects monitor resolutions and orientations (landscape or portrait).
        Creates a composite wallpaper that aligns perfectly across all displays.

    Random Wallpapers:
        Fetches high-quality random images from Lorem Picsum.

    Automated Execution:
        Can be scheduled to run at startup and every 30 minutes using Task Scheduler.

Requirements

    Operating System: Windows 10 or later.
    Python: Version 3.6 or higher.
    Python Libraries:
        requests
        Pillow

Install required libraries:

```pip install requests pillow```

or if windows

```py -m pip install requests pillow```

How It Works

    Detects all connected monitors and their resolutions.
    Fetches random images sized to fit each monitor.
    Combines these images into a composite wallpaper spanning all monitors.
    Updates the desktop background automatically.

Installation

Clone the repository:

```
git clone https://github.com/<your-username>/wallpaper-changer.git
cd wallpaper-changer
```

Usage

Run Manually

Execute the script directly:

```
python wallpaper_changer.py
```

or if windows 

```
py wallpaper_changer.py
```


Automate with Task Scheduler


To run the script every 30 minutes and at startup:

Create a .bat file to execute the script:

@echo off
python "C:\path\to\wallpaper_changer.py"
or
py "C:\path\to\wallpaper_changer.py"

Add the .bat file to Windows Task Scheduler:
    Set triggers for on login and repeat 30-minutes indefinitely.
    Use the "Run only when user is logged on" option.

Customization

Change Image Source:
    Modify the fetch_image_from_web function to use a different image source (e.g., Wikimedia Commons, Unsplash, or a local folder).
Adjust Execution Interval:
    Change the interval in Task Scheduler to your preferred frequency.

Troubleshooting

Wallpaper Not Aligning:
    Ensure your display settings are set to "Span" under Background options.
    Verify monitor resolutions in the get_display_info() output.

Task Scheduler Issues:
    Use the "Run only when user is logged on" setting if you don’t have a password.

License

This project is licensed under the MIT License. See the LICENSE file for details.
Contributing

Feel free to submit issues or pull requests to improve the script. Contributions are welcome!
