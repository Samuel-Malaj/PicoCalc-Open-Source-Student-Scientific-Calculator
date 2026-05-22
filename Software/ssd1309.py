"""
ssd1309.py — SSD1309 128×64 OLED driver for MicroPython (Raspberry Pi Pico)

Driver generated with the assistance of Claude AI (Anthropic)
Adapted and tested for the Seengreat 2.42" OLED module

Wiring (default):
    OLED DIN  →  GP16  (SDA)
    OLED CLK  →  GP17  (SCL)
    OLED VCC  →  3.3V
    OLED GND  →  GND
    OLED RST  →  optional, tie to 3.3V if unused
    OLED CS   →  GND or 3.3V (not used in I2C mode)
    OLED D/C  →  GND = address 0x3C  |  3.3V = address 0x3D

Usage:
    from ssd1309 import SSD1309
    oled = SSD1309()          # uses GP16/GP17, address 0x3C
    oled.clear()
    oled.text("Hello!", 0, 0)
    oled.show()
"""

from machine import I2C, Pin
import framebuf
import time

# ── Commands ──────────────────────────────────────────────────────────────

CMD_DISPLAY_OFF    = 0xAE
CMD_DISPLAY_ON     = 0xAF
CMD_SET_CONTRAST   = 0x81
CMD_RESUME_RAM     = 0xA4
CMD_NORMAL         = 0xA6
CMD_INVERT         = 0xA7
CMD_SET_MEM_ADDR   = 0x20
CMD_SET_COL_ADDR   = 0x21
CMD_SET_PAGE_ADDR  = 0x22
CMD_SET_MUX        = 0xA8
CMD_SET_OFFSET     = 0xD3
CMD_SET_START_LINE = 0x40
CMD_SEG_REMAP_127  = 0xA1
CMD_COM_SCAN_DEC   = 0xC8
CMD_SET_COM_PINS   = 0xDA
CMD_SET_CLK        = 0xD5
CMD_SET_PRECHARGE  = 0xD9
CMD_SET_VCOMH      = 0xDB

WIDTH  = 128
HEIGHT = 64
PAGES  = HEIGHT // 8


class SSD1309:
    """
    SSD1309 OLED driver using MicroPython's built-in framebuf for drawing.

    Parameters
    ----------
    sda  : int  — GPIO pin number for SDA  (default 16)
    scl  : int  — GPIO pin number for SCL  (default 17)
    freq : int  — I2C clock frequency in Hz (default 400_000)
    addr : int  — I2C address: 0x3C or 0x3D  (default 0x3C)
    """

    def __init__(self, sda: int = 16, scl: int = 17,
                 freq: int = 400_000, addr: int = 0x3C):
        self.addr = addr
        self.i2c  = I2C(0, sda=Pin(sda), scl=Pin(scl), freq=freq)

        # Frame buffer — MONO_VLSB matches the SSD1309 page layout exactly
        self._buf = bytearray(WIDTH * PAGES)
        self.fb   = framebuf.FrameBuffer(self._buf, WIDTH, HEIGHT, framebuf.MONO_VLSB)

        self._init_display()

    # ── Low-level I2C ─────────────────────────────────────────────────────

    def _cmd(self, *commands):
        """Send one or more command bytes."""
        for c in commands:
            self.i2c.writeto(self.addr, bytes([0x00, c]))

    def _data(self):
        """Send the entire frame buffer as pixel data."""
        # 0x40 = control byte: Co=0, D/C=1 (data stream)
        payload = bytearray(1 + len(self._buf))
        payload[0] = 0x40
        payload[1:] = self._buf
        self.i2c.writeto(self.addr, payload)

    # ── Initialisation sequence ───────────────────────────────────────────

    def _init_display(self):
        self._cmd(CMD_DISPLAY_OFF)
        self._cmd(CMD_SET_CLK,       0x80)
        self._cmd(CMD_SET_MUX,       0x3F)   # 1/64 duty
        self._cmd(CMD_SET_OFFSET,    0x00)
        self._cmd(CMD_SET_START_LINE | 0)
        self._cmd(CMD_SEG_REMAP_127)          # flip horizontal
        self._cmd(CMD_COM_SCAN_DEC)           # flip vertical
        self._cmd(CMD_SET_COM_PINS,  0x12)
        self._cmd(CMD_SET_CONTRAST,  0xCF)
        self._cmd(CMD_SET_PRECHARGE, 0xF1)
        self._cmd(CMD_SET_VCOMH,     0x40)
        self._cmd(CMD_RESUME_RAM)
        self._cmd(CMD_NORMAL)
        self._cmd(CMD_SET_MEM_ADDR,  0x00)   # horizontal addressing mode
        self._cmd(CMD_DISPLAY_ON)
        time.sleep_ms(100)

    # ── Push buffer to display ────────────────────────────────────────────

    def show(self):
        """Flush the frame buffer to the OLED."""
        self._cmd(CMD_SET_COL_ADDR,  0, WIDTH - 1)
        self._cmd(CMD_SET_PAGE_ADDR, 0, PAGES - 1)
        self._data()

    # ── Drawing — wrappers around MicroPython framebuf ────────────────────

    def clear(self, show: bool = False):
        """Clear the screen to black."""
        self.fb.fill(0)
        if show:
            self.show()

    def fill(self, show: bool = False):
        """Fill the screen white."""
        self.fb.fill(1)
        if show:
            self.show()

    def pixel(self, x: int, y: int, on: int = 1):
        self.fb.pixel(x, y, on)

    def text(self, string: str, x: int, y: int, on: int = 1):
        """
        Draw text using MicroPython's built-in 8×8 bitmap font.
        Each character is 8 pixels wide, so max ~16 chars across.
        Call show() to push to the display.
        """
        self.fb.text(string, x, y, on)

    def line(self, x0: int, y0: int, x1: int, y1: int, on: int = 1):
        self.fb.line(x0, y0, x1, y1, on)

    def rect(self, x: int, y: int, w: int, h: int,
             on: int = 1, fill: bool = False):
        """Draw a rectangle. w/h are width and height (not x1/y1)."""
        if fill:
            self.fb.fill_rect(x, y, w, h, on)
        else:
            self.fb.rect(x, y, w, h, on)

    def hline(self, x: int, y: int, w: int, on: int = 1):
        self.fb.hline(x, y, w, on)

    def vline(self, x: int, y: int, h: int, on: int = 1):
        self.fb.vline(x, y, h, on)

    def scroll(self, dx: int, dy: int):
        """Scroll the framebuffer by dx/dy pixels (call show() after)."""
        self.fb.scroll(dx, dy)

    def blit(self, src_fb, x: int, y: int):
        """Blit another FrameBuffer onto this one at (x, y)."""
        self.fb.blit(src_fb, x, y)

    # ── Display control ───────────────────────────────────────────────────

    def contrast(self, level: int):
        """Set brightness: 0 = dimmest, 255 = brightest."""
        self._cmd(CMD_SET_CONTRAST, level & 0xFF)

    def invert(self, invert: bool):
        """Invert all pixels on the display."""
        self._cmd(CMD_INVERT if invert else CMD_NORMAL)

    def power(self, on: bool):
        """Turn the display on or off (does not lose frame buffer)."""
        self._cmd(CMD_DISPLAY_ON if on else CMD_DISPLAY_OFF)