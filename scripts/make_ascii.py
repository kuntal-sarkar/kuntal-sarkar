from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from pathlib import Path
import html

# --------------------------------
# Paths
# --------------------------------
ROOT = Path(__file__).resolve().parent.parent

INPUT = ROOT / "assets" / "profile-source.jpeg"
OUTPUT = ROOT / "assets" / "ascii.svg"

# --------------------------------
# Crop
# --------------------------------
# Face + shoulders focused crop
CROP = (70, 45, 390, 390)

# --------------------------------
# ASCII settings
# --------------------------------
WIDTH = 84

# IMPORTANT:
# There is NO space at the end.
# This keeps the right side filled.
CHARS = "@%#*+=-:."

# --------------------------------
# Load image
# --------------------------------
img = Image.open(INPUT).convert("L")

# Crop
img = img.crop(CROP)

# --------------------------------
# Image enhancement
# --------------------------------

# Stretch black/white range
img = ImageOps.autocontrast(img, cutoff=1)

# Stronger facial definition
img = ImageEnhance.Contrast(img).enhance(1.35)

# Sharpen eyes, lips, hair and beard edges
img = img.filter(
    ImageFilter.UnsharpMask(
        radius=2,
        percent=170,
        threshold=3
    )
)

# --------------------------------
# Gamma correction
# --------------------------------
# Slightly darkens darker facial details,
# making eyes/lips/hair more prominent.
gamma = 1.25

lut = [
    int(255 * ((i / 255) ** gamma))
    for i in range(256)
]

img = img.point(lut)

# --------------------------------
# Resize
# --------------------------------
aspect = img.height / img.width

height = int(WIDTH * aspect * 0.48)

img = img.resize(
    (WIDTH, height),
    Image.Resampling.LANCZOS
)

# --------------------------------
# Convert to ASCII
# --------------------------------
pixels = img.load()

lines = []

for y in range(height):

    line = ""

    for x in range(WIDTH):

        pixel = pixels[x, y]

        # Dark -> dense characters
        # Bright -> light characters
        index = int(
            (255 - pixel)
            / 256
            * len(CHARS)
        )

        if index >= len(CHARS):
            index = len(CHARS) - 1

        line += CHARS[index]

    # DO NOT rstrip()
    # We intentionally keep the full width.
    lines.append(line)

# --------------------------------
# SVG dimensions
# --------------------------------
FONT_SIZE = 10
LINE_HEIGHT = 11

PADDING_X = 18
PADDING_Y = 18

svg_width = WIDTH * 8 + PADDING_X * 2
svg_height = len(lines) * LINE_HEIGHT + PADDING_Y * 2

# --------------------------------
# SVG text
# --------------------------------
svg_lines = []

for i, line in enumerate(lines):

    safe_line = html.escape(line)

    # Each line gets its own staggered boot delay.
    # This creates a proper terminal build effect.
    delay = i * 0.075

    # Alternate direction slightly.
    # Even lines enter from left,
    # odd lines enter from right.
    direction = -14 if i % 2 == 0 else 14

    svg_lines.append(
        f'''
        <text
            x="{PADDING_X}"
            y="{PADDING_Y + (i + 1) * LINE_HEIGHT}"
            class="ascii-line"
            style="
                --delay:{delay:.3f}s;
                --direction:{direction}px;
            "
        >{safe_line}</text>
        '''
    )

svg_content = "\n".join(svg_lines)

# --------------------------------
# Animated SVG
# --------------------------------

# Animation timing
# --------------------------------
# 0% - 42%   : boot / build
# 42% - 68%  : stable portrait
# 68% - 72%  : final glitch
# 72% - 100% : clean hold
#
# The next cycle then starts again.
# --------------------------------

svg = f'''<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{svg_width}"
    height="{svg_height}"
    viewBox="0 0 {svg_width} {svg_height}"
>

    <!-- =================================
         TERMINAL BACKGROUND
         ================================= -->

    <rect
        width="100%"
        height="100%"
        rx="10"
        fill="#0D1117"
    />


    <style>

        /* =================================
           ASCII PORTRAIT
           ================================= */

        .ascii-line {{
            font-family: "Courier New", monospace;
            font-size: {FONT_SIZE}px;
            font-weight: bold;

            fill: #C9D1D9;

            opacity: 0;

            animation:
                boot 10.5s cubic-bezier(.22,.61,.36,1)
                var(--delay)
                infinite;

            transform-origin: center;
        }}


        /* =================================
           MAIN DIGITAL BOOT
           ================================= */

        @keyframes boot {{

            /* -----------------------------
               INITIAL DIGITAL NOISE
               ----------------------------- */

            0% {{
                opacity: 0;

                transform:
                    translateX(var(--direction))
                    skewX(5deg);
            }}


            /* -----------------------------
               QUICK SIGNAL HIT
               ----------------------------- */

            3% {{
                opacity: 0.18;

                transform:
                    translateX(10px)
                    skewX(-4deg);
            }}


            6% {{
                opacity: 0.48;

                transform:
                    translateX(-6px)
                    skewX(3deg);
            }}


            /* -----------------------------
               GLITCH SNAP
               ----------------------------- */

            9% {{
                opacity: 0.72;

                transform:
                    translateX(4px)
                    skewX(-2deg);
            }}


            12% {{
                opacity: 0.42;

                transform:
                    translateX(-3px)
                    skewX(1deg);
            }}


            15% {{
                opacity: 0.90;

                transform:
                    translateX(1px)
                    skewX(0deg);
            }}


            /* -----------------------------
               PORTRAIT LOCK
               ----------------------------- */

            19% {{
                opacity: 0.94;

                transform:
                    translateX(0)
                    skewX(0deg);
            }}


            /* -----------------------------
               DIGITAL FLICKER
               ----------------------------- */

            23% {{
                opacity: 0.72;
            }}

            24.5% {{
                opacity: 0.98;
            }}

            26% {{
                opacity: 0.80;
            }}

            27.5% {{
                opacity: 0.94;
            }}


            /* -----------------------------
               CLEAN PORTRAIT
               ----------------------------- */

            32% {{
                opacity: 0.92;
            }}

            62% {{
                opacity: 0.92;
            }}


            /* -----------------------------
               SECONDARY GLITCH
               ----------------------------- */

            64% {{
                opacity: 0.70;

                transform:
                    translateX(-3px)
                    skewX(1deg);
            }}

            65.5% {{
                opacity: 0.98;

                transform:
                    translateX(3px)
                    skewX(-1deg);
            }}

            67% {{
                opacity: 0.76;

                transform:
                    translateX(-1px)
                    skewX(0deg);
            }}

            69% {{
                opacity: 0.94;

                transform:
                    translateX(0)
                    skewX(0deg);
            }}


            /* -----------------------------
               FINAL CLEAN HOLD
               ----------------------------- */

            70% {{
                opacity: 0.92;

                transform:
                    translateX(0)
                    skewX(0deg);
            }}

            100% {{
                opacity: 0.92;

                transform:
                    translateX(0)
                    skewX(0deg);
            }}

        }}


        /* =================================
           MAIN SCAN
           ================================= */

        .scan-line {{

            fill: #C9D1D9;

            opacity: 0;

            animation:
                scan 10.5s linear infinite;
        }}


        @keyframes scan {{

            0% {{
                opacity: 0;

                transform:
                    translateY(-30px);
            }}

            10% {{
                opacity: 0;
            }}

            16% {{
                opacity: 0.04;
            }}

            24% {{
                opacity: 0.11;
            }}

            31% {{
                opacity: 0.04;
            }}

            38% {{
                opacity: 0;
            }}

            100% {{
                opacity: 0;

                transform:
                    translateY({svg_height + 40}px);
            }}

        }}


        /* =================================
           FAST SECOND SCAN
           ================================= */

        .scan-line-fast {{

            fill: #FFFFFF;

            opacity: 0;

            animation:
                fastScan 10.5s linear infinite;
        }}


        @keyframes fastScan {{

            0% {{
                opacity: 0;

                transform:
                    translateY({svg_height + 20}px);
            }}

            38% {{
                opacity: 0;
            }}

            43% {{
                opacity: 0.03;
            }}

            46% {{
                opacity: 0.12;
            }}

            49% {{
                opacity: 0.03;
            }}

            52% {{
                opacity: 0;
            }}

            100% {{
                opacity: 0;

                transform:
                    translateY(-30px);
            }}

        }}


        /* =================================
           PORTRAIT FLASH
           ================================= */

        .portrait-flash {{

            fill: #FFFFFF;

            opacity: 0;

            animation:
                flash 10.5s ease-in-out infinite;
        }}


        @keyframes flash {{

            0% {{
                opacity: 0;
            }}

            14% {{
                opacity: 0;
            }}

            16% {{
                opacity: 0.035;
            }}

            18% {{
                opacity: 0;
            }}

            65% {{
                opacity: 0;
            }}

            67% {{
                opacity: 0.045;
            }}

            69% {{
                opacity: 0;
            }}

            100% {{
                opacity: 0;
            }}

        }}


        /* =================================
           TERMINAL FRAME
           ================================= */

        .terminal-frame {{

            fill: none;

            stroke: #C9D1D9;

            stroke-width: 1;

            opacity: 0.12;

            animation:
                framePulse 10.5s ease-in-out infinite;
        }}


        @keyframes framePulse {{

            0% {{
                opacity: 0.08;
            }}

            8% {{
                opacity: 0.40;
            }}

            13% {{
                opacity: 0.15;
            }}

            20% {{
                opacity: 0.20;
            }}

            65% {{
                opacity: 0.14;
            }}

            68% {{
                opacity: 0.38;
            }}

            72% {{
                opacity: 0.13;
            }}

            100% {{
                opacity: 0.10;
            }}

        }}


        /* =================================
           STATUS LIGHT
           ================================= */

        .status-light {{

            fill: #C9D1D9;

            animation:
                statusPulse 10.5s ease-in-out infinite;
        }}


        @keyframes statusPulse {{

            0% {{
                opacity: 0.12;
            }}

            8% {{
                opacity: 0.85;
            }}

            12% {{
                opacity: 0.25;
            }}

            30% {{
                opacity: 0.25;
            }}

            65% {{
                opacity: 0.25;
            }}

            69% {{
                opacity: 0.90;
            }}

            73% {{
                opacity: 0.18;
            }}

            100% {{
                opacity: 0.12;
            }}

        }}

    </style>


    <!-- =================================
         ASCII PORTRAIT
         ================================= -->

    <g>
        {svg_content}
    </g>


    <!-- =================================
         SUBTLE PORTRAIT FLASH
         ================================= -->

    <rect
        class="portrait-flash"
        x="0"
        y="0"
        width="{svg_width}"
        height="{svg_height}"
    />


    <!-- =================================
         SCAN EFFECTS
         ================================= -->

    <rect
        class="scan-line"
        x="0"
        y="0"
        width="{svg_width}"
        height="2"
    />

    <rect
        class="scan-line-fast"
        x="0"
        y="0"
        width="{svg_width}"
        height="1"
    />


    <!-- =================================
         TERMINAL FRAME
         ================================= -->

    <rect
        class="terminal-frame"
        x="5"
        y="5"
        width="{svg_width - 10}"
        height="{svg_height - 10}"
        rx="8"
    />


    <!-- =================================
         STATUS LIGHT
         ================================= -->

    <circle
        class="status-light"
        cx="{svg_width - 16}"
        cy="14"
        r="2"
    />

</svg>
'''

# --------------------------------
# Save
# --------------------------------

OUTPUT.write_text(
    svg,
    encoding="utf-8"
)

print(f"[+] Source : {INPUT}")
print(f"[+] Output : {OUTPUT}")
print("[+] Dhasu animated ASCII portrait generated!")