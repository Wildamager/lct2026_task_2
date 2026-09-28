import sys
import time
import RPi.GPIO as GPIO

from led_check import open_camera, read_led_color, wait_led_color

PIN_A = 17
PIN_B = 18
PIN_C = 27

DIGITS_COUNT = 4
DIGIT_VALUES = 10

STEP_DELAY = 0.025
BUTTON_PRESS_TIME = 0.10
BUTTON_RELEASE_TIME = 0.15
SETTLE_DELAY = 0.15
ATTEMPT_DELAY = 1.20

IDLE_HIGH = False
CCW_INCREMENTS = True
RESET_AFTER_ATTEMPT = True
BUTTON_ACTIVE_LOW = True

DETENT = (1, 1) if IDLE_HIGH else (0, 0)

if IDLE_HIGH:
    CW = [(0, 1), (0, 0), (1, 0), (1, 1)]
    CCW = [(1, 0), (0, 0), (0, 1), (1, 1)]
else:
    CW = [(1, 0), (1, 1), (0, 1), (0, 0)]
    CCW = [(0, 1), (1, 1), (1, 0), (0, 0)]

current_digit = 0


def set_state(state):
    GPIO.output(PIN_A, state[0])
    GPIO.output(PIN_B, state[1])
    time.sleep(STEP_DELAY)


def rotate(sequence, steps=1):
    for _ in range(steps):
        for state in sequence:
            set_state(state)


def rotate_cw(steps=1):
    rotate(CW, steps)


def rotate_ccw(steps=1):
    rotate(CCW, steps)


def step_to(target):
    global current_digit

    if target == current_digit:
        return

    diff = (target - current_digit) % DIGIT_VALUES

    if CCW_INCREMENTS:
        rotate(CCW, diff)
    else:
        rotate(CW, diff)

    current_digit = target


def press_b():
    global current_digit

    time.sleep(SETTLE_DELAY)
    GPIO.setup(PIN_C, GPIO.OUT)
    GPIO.output(PIN_C, GPIO.LOW if BUTTON_ACTIVE_LOW else GPIO.HIGH)
    time.sleep(BUTTON_PRESS_TIME)
    GPIO.setup(PIN_C, GPIO.IN)
    time.sleep(BUTTON_RELEASE_TIME)

    current_digit = 0


def main():
    global current_digit

    GPIO.setmode(GPIO.BCM)

    for pin in (PIN_A, PIN_B):
        GPIO.setup(pin, GPIO.OUT)

    GPIO.output(PIN_A, DETENT[0])
    GPIO.output(PIN_B, DETENT[1])

    cam = open_camera()
    current_digit = 0

    try:
        start_code = int(sys.argv[1]) if len(sys.argv) > 1 else 0
        end_code = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

        code = 0

        while code <= end_code:
            i = code // 1000
            j = (code // 100) % 10
            z = (code // 10) % 10
            u = code % 10

            step_to(i)
            press_b()
            step_to(j)
            press_b()
            step_to(z)
            press_b()
            step_to(u)
            press_b()

            color = wait_led_color(cam, ("red", "green"))

            if color == "green":
                print(f"OTVET NAIDEN: {code:04d}")
                return

            print(f"{code:04d}: {color}")

            if RESET_AFTER_ATTEMPT:
                step_to(0)

            time.sleep(ATTEMPT_DELAY)
            code += 1

    finally:
        cam.stop()
        GPIO.cleanup()


if __name__ == "__main__":
    main()
