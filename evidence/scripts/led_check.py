import time
import numpy as np
from picamera2 import Picamera2

CROP_FRACTION = 0.6
SAT_MIN = 25.0
VAL_MIN = 20.0

HUE_RED_MAX = 20.0
HUE_RED_MIN = 340.0
HUE_GREEN_MIN = 80.0
HUE_GREEN_MAX = 170.0
HUE_BLUE_MIN = 200.0
HUE_BLUE_MAX = 280.0

RESULT_TIMEOUT = 6.0
FRAME_SIZE = (640, 480)


def open_camera():
    cam = Picamera2()
    config = cam.create_still_configuration(
        main={"size": FRAME_SIZE, "format": "RGB888"}
    )
    cam.configure(config)
    cam.start()
    time.sleep(0.5)
    return cam


def classify_rgb(rgb):
    r, g, b = np.asarray(rgb, dtype=float) / 255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    d = mx - mn

    sat = d / mx * 100.0 if mx > 0 else 0.0
    val = mx * 100.0

    if sat < SAT_MIN or val < VAL_MIN:
        return "none"

    if d == 0.0:
        return "none"

    if mx == r:
        h = ((g - b) / d) % 6.0
    elif mx == g:
        h = (b - r) / d + 2.0
    else:
        h = (r - g) / d + 4.0

    h *= 60.0

    if h <= HUE_RED_MAX or h >= HUE_RED_MIN:
        return "red"

    if HUE_GREEN_MIN <= h < HUE_GREEN_MAX:
        return "green"

    if HUE_BLUE_MIN <= h < HUE_BLUE_MAX:
        return "blue"

    return "none"


def read_led_color(cam):
    frame = cam.capture_array()[..., ::-1]
    h, w = frame.shape[:2]

    cy, cx = h // 2, w // 2
    half_y = int(h * CROP_FRACTION / 2)
    half_x = int(w * CROP_FRACTION / 2)

    region = frame[
        cy - half_y:cy + half_y,
        cx - half_x:cx + half_x
    ]

    mean = region.reshape(-1, 3).mean(axis=0)
    return classify_rgb(mean)


def wait_led_color(cam, targets, timeout=RESULT_TIMEOUT):
    deadline = time.monotonic() + timeout
    last = "none"

    while time.monotonic() < deadline:
        last = read_led_color(cam)

        if last in targets:
            return last

        time.sleep(0.05)

    return last
