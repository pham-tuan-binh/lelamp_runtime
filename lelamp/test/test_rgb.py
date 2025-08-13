import time
from rpi_ws281x import PixelStrip, Color

# LED strip configuration:
LED_COUNT = 40        # Number of LEDs in your strip
LED_PIN = 18          # GPIO pin connected to the pixels (18 supports PWM)
LED_FREQ_HZ = 800000  # WS2812B LED signal frequency (800kHz)
LED_DMA = 10          # DMA channel to use
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (if needed)
LED_CHANNEL = 0       # 0 for GPIO 18, 1 for GPIO 13,19, etc.

# Create PixelStrip object
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

def color_wipe(color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

print("Testing WS2812B on GPIO 18...")

# Red, Green, Blue test
color_wipe(Color(255, 0, 0))  # Red
time.sleep(0.5)
color_wipe(Color(0, 255, 0))  # Green
time.sleep(0.5)
color_wipe(Color(0, 0, 255))  # Blue
time.sleep(0.5)

# Rainbow cycle
def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow_cycle(wait_ms=20, iterations=5):
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i * 256 // strip.numPixels() + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)

rainbow_cycle()
