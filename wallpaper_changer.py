import os
import ctypes
from PIL import Image
from io import BytesIO
import random

# Define RECT structure
class RECT(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long)
    ]

def get_display_info():
    """Get the resolution and position of all connected monitors using ctypes."""
    user32 = ctypes.windll.user32
    monitors = []

    def monitor_enum_proc(hMonitor, hdcMonitor, lprcMonitor, dwData):
        # Structure to hold monitor info
        class MONITORINFOEX(ctypes.Structure):
            _fields_ = [
                ("cbSize", ctypes.c_ulong),
                ("rcMonitor", RECT),
                ("rcWork", RECT),
                ("dwFlags", ctypes.c_ulong),
                ("szDevice", ctypes.c_wchar * 32),
            ]

        monitor_info = MONITORINFOEX()
        monitor_info.cbSize = ctypes.sizeof(MONITORINFOEX)
        user32.GetMonitorInfoW(hMonitor, ctypes.byref(monitor_info))
        monitor_rect = monitor_info.rcMonitor

        # Extract monitor dimensions and positions
        width = monitor_rect.right - monitor_rect.left
        height = monitor_rect.bottom - monitor_rect.top
        position = (monitor_rect.left, monitor_rect.top, monitor_rect.right, monitor_rect.bottom)
        monitors.append({"resolution": (width, height), "position": position})
        return True

    MonitorEnumProc = ctypes.WINFUNCTYPE(
        ctypes.c_bool,
        ctypes.c_ulong,
        ctypes.c_ulong,
        ctypes.POINTER(RECT),
        ctypes.c_double,
    )

    user32.EnumDisplayMonitors(0, 0, MonitorEnumProc(monitor_enum_proc), 0)
    return monitors

def create_composite_wallpaper(image_paths, monitor_info):
    """Combine individual images into a single composite wallpaper."""
    # Calculate the virtual screen dimensions
    min_left = min(monitor["position"][0] for monitor in monitor_info)
    min_top = min(monitor["position"][1] for monitor in monitor_info)
    max_right = max(monitor["position"][2] for monitor in monitor_info)
    max_bottom = max(monitor["position"][3] for monitor in monitor_info)

    virtual_width = max_right - min_left
    virtual_height = max_bottom - min_top

    # Create a blank composite image
    composite = Image.new("RGB", (virtual_width, virtual_height))

    # Place each monitor's image at the correct position
    for img_path, monitor in zip(image_paths, monitor_info):
        img = Image.open(img_path)
        width, height = monitor["resolution"]
        left, top, _, _ = monitor["position"]

        # Resize the image to fit the monitor
        img = img.resize((width, height), Image.LANCZOS)

        # Paste the image at its correct position
        composite.paste(img, (left - min_left, top - min_top))

    # Save the composite wallpaper
    composite_path = os.path.join(os.getenv('TEMP'), 'composite_wallpaper.jpg')
    composite.save(composite_path, "JPEG")
    return composite_path

def set_wallpaper(image_path):
    """Set the wallpaper on Windows."""
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)

def main():
    print("Getting display information...")
    monitors = get_display_info()
    print(f"Monitor info: {monitors}")

    resolutions = [monitor["resolution"] for monitor in monitors]
    print(f"Resolutions: {resolutions}")

    print("Dividing wallpapers into landscape & portrait...")
    landscape = []
    portrait = []
    wallpapers_loc = os.path.join(os.getcwd(), 'imgs')
    wallpapers = os.listdir(wallpapers_loc)
    for i in wallpapers:
        img_path = os.path.join(wallpapers_loc, i)
        with Image.open(img_path) as img:
            width, height = img.size
            if width >= height:
                landscape.append(img_path)
            else:
                portrait.append(img_path)

    print("Matching wallpapers to corresponding monitors...")
    image_paths = []
    for i, res in enumerate(resolutions):
        width, height = res
        if width >= height:
            img = random.choice(landscape)
            landscape.remove(img)
        else:
            img = random.choice(portrait)
            portrait.remove(img)
        image_paths.append(img)


    print("Creating composite wallpaper...")
    composite_path = create_composite_wallpaper(image_paths, monitors)
    print(f"Composite wallpaper saved to: {composite_path}")

    print("Setting composite wallpaper...")
    set_wallpaper(composite_path)
    print("Wallpaper updated successfully!")

if __name__ == "__main__":
    main()
