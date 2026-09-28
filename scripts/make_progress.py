from pathlib import Path

OUTPUT = Path("assets/progress.svg")

WIDTH = 900
HEIGHT = 470

BG = "#0D1117"
BORDER = "#30363D"
TEXT = "#E6EDF3"
MUTED = "#8B949E"
GREEN = "#7EE787"
GREEN_DIM = "#238636"

# Self-assessed learning progress
skills = [
    ("FRONTEND DEVELOPMENT", 75, "75%"),
    ("BACKEND DEVELOPMENT", 70, "70%"),
    ("PYTHON", 60, "60%"),
    ("JAVA", 40, "40%"),
    ("CYBERSECURITY", 40, "EXPLORING"),
    ("DSA", 70, "PRACTICING"),
]


BAR_X = 390
BAR_WIDTH = 300
BAR_HEIGHT = 10

START_Y = 155
ROW_GAP = 43


# ==========================================================
# Percentage counter generator
# ==========================================================

def make_counter_frames(
    x,
    y,
    target,
    start_delay,
    duration=5.5,
):
    frames = []

    if target <= 0:
        return ""

    step_time = duration / target

    for number in range(target + 1):

        start = start_delay + (number * step_time)

        frames.append(
            f'''
<text
    x="{x}"
    y="{y}"
    fill="{GREEN}"
    font-size="15"
    class="terminal bold counter-frame counter-{target}-{number}"
    opacity="0">

    {number}%

    <animate
        attributeName="opacity"
        values="0;1"
        dur="0.08s"
        begin="{start:.4f}s"
        fill="freeze"
    />
</text>
'''
        )

    return "".join(frames)


svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
    width="{WIDTH}"
    height="{HEIGHT}"
    viewBox="0 0 {WIDTH} {HEIGHT}">

<defs>

    <filter id="glow">
        <feGaussianBlur stdDeviation="2.5" result="blur"/>
        <feMerge>
            <feMergeNode in="blur"/>
            <feMergeNode in="SourceGraphic"/>
        </feMerge>
    </filter>

</defs>

<style>

    .terminal {{
        font-family: "Courier New", monospace;
    }}

    .bold {{
        font-weight: 700;
    }}

    /* Terminal entrance */
    .boot {{
        opacity: 0;
        animation: boot 0.6s ease-out forwards;
    }}

    .row1 {{ animation-delay: 0.25s; }}
    .row2 {{ animation-delay: 0.45s; }}
    .row3 {{ animation-delay: 0.65s; }}
    .row4 {{ animation-delay: 0.85s; }}
    .row5 {{ animation-delay: 1.05s; }}
    .row6 {{ animation-delay: 1.25s; }}

    @keyframes boot {{
        from {{
            opacity: 0;
            transform: translateX(-10px);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}

   /* Progress bar animation */
.progress {{
    transform-box: fill-box;
    transform-origin: left center;
    transform: scaleX(0);
    animation: load 5.5s cubic-bezier(.25,.1,.25,1) forwards;
}}

    .p1 {{ animation-delay: 0.45s; }}
    .p2 {{ animation-delay: 0.65s; }}
    .p3 {{ animation-delay: 0.85s; }}
    .p4 {{ animation-delay: 1.05s; }}
    .p5 {{ animation-delay: 1.25s; }}
    .p6 {{ animation-delay: 1.45s; }}

    @keyframes load {{
        from {{
            transform: scaleX(0);
        }}
        to {{
            transform: scaleX(1);
        }}
    }}

    /* Status text pulse */
    .status {{
        animation: statusPulse 2.8s ease-in-out infinite;
    }}

    @keyframes statusPulse {{
        0%, 100% {{
            opacity: 0.65;
        }}
        50% {{
            opacity: 1;
        }}
    }}

    /* Counter frame base */
    .counter-frame {{
        pointer-events: none;
    }}

    /* Cursor */
    .cursor {{
        animation: cursorBlink 0.8s steps(1) infinite;
    }}

    @keyframes cursorBlink {{
        0%, 45% {{
            opacity: 1;
        }}
        46%, 100% {{
            opacity: 0;
        }}
    }}

    /* Scan effect */
    .scan {{
        animation: scan 5s ease-in-out infinite;
    }}

    @keyframes scan {{
        0%, 65%, 100% {{
            opacity: 0;
        }}
        68% {{
            opacity: 0.15;
        }}
        72% {{
            opacity: 0;
        }}
    }}

    /* Border pulse */
    .window {{
        animation: borderPulse 4s ease-in-out infinite;
    }}

    @keyframes borderPulse {{
        0%, 100% {{
            stroke-opacity: 0.7;
        }}
        50% {{
            stroke-opacity: 1;
        }}
    }}

</style>


<!-- ===================================================== -->
<!-- TERMINAL WINDOW -->
<!-- ===================================================== -->

<rect
    x="10"
    y="10"
    width="{WIDTH - 20}"
    height="{HEIGHT - 20}"
    rx="15"
    fill="{BG}"
    stroke="{BORDER}"
    stroke-width="2"
    class="window"
/>


<!-- ===================================================== -->
<!-- MACOS TRAFFIC LIGHTS -->
<!-- ===================================================== -->

<circle cx="34" cy="38" r="7" fill="#FF5F57"/>
<circle cx="58" cy="38" r="7" fill="#FEBC2E"/>
<circle cx="82" cy="38" r="7" fill="#28C840"/>


<!-- Terminal title -->

<text
    x="112"
    y="44"
    fill="{MUTED}"
    font-size="17"
    class="terminal">
    kuntal@github
</text>


<!-- Divider -->

<line
    x1="30"
    y1="70"
    x2="870"
    y2="70"
    stroke="{BORDER}"
    stroke-width="1"
/>


<!-- ===================================================== -->
<!-- COMMAND -->
<!-- ===================================================== -->

<text
    x="35"
    y="105"
    fill="{GREEN}"
    font-size="17"
    class="terminal bold"
    filter="url(#glow)">
    kuntal@github:~$ ./progress.sh
</text>


<!-- Section heading -->

<text
    x="35"
    y="132"
    fill="{TEXT}"
    font-size="17"
    class="terminal bold">
    03 — CURRENTLY LOADING...
</text>

'''


# ==========================================================
# SKILL ROWS
# ==========================================================

for i, (skill, value, label) in enumerate(skills, start=1):

    y = START_Y + (i - 1) * ROW_GAP

    progress_width = BAR_WIDTH * (value / 100)

    bar_delay = 0.45 + ((i - 1) * 0.20)

    svg += f'''
<g class="boot row{i}">

    <!-- Skill name -->

    <text
        x="35"
        y="{y}"
        fill="{MUTED}"
        font-size="15"
        class="terminal bold">
        {skill}
    </text>


    <!-- Empty bar -->

    <rect
        x="{BAR_X}"
        y="{y - 10}"
        width="{BAR_WIDTH}"
        height="{BAR_HEIGHT}"
        rx="5"
        fill="#21262D"
    />


    <!-- Filled bar -->

    <rect
        x="{BAR_X}"
        y="{y - 10}"
        width="{progress_width}"
        height="{BAR_HEIGHT}"
        rx="5"
        fill="{GREEN}"
        class="progress p{i}"
        filter="url(#glow)"
    />
'''

    # Numeric percentage rows
    if "%" in label:

        # Animated percentage counter.
        # Final percentage remains visible permanently.

        svg += f'''
    <!-- Animated percentage counter -->

    <g>
'''

        step_time = 5.5 / value

        for number in range(value + 1):

            frame_start = bar_delay + (number * step_time)

            if number == value:

                # Final value stays permanently visible.

                svg += f'''
        <text
            x="720"
            y="{y}"
            fill="{GREEN}"
            font-size="15"
            class="terminal bold counter-frame"
            opacity="0">

            {number}%

            <animate
                attributeName="opacity"
                values="0;1"
                dur="0.12s"
                begin="{frame_start:.4f}s"
                fill="freeze"
            />

        </text>
'''

            else:

                # Each number appears briefly and then disappears
                # when the next number takes its place.

                svg += f'''
        <text
            x="720"
            y="{y}"
            fill="{GREEN}"
            font-size="15"
            class="terminal bold counter-frame"
            opacity="0">

            {number}%

            <animate
                attributeName="opacity"
                values="0;1"
                dur="0.07s"
                begin="{frame_start:.4f}s"
                fill="freeze"
            />

            <animate
                attributeName="opacity"
                values="1;0"
                dur="0.07s"
                begin="{frame_start + 0.07:.4f}s"
                fill="freeze"
            />

        </text>
'''

        svg += '''
    </g>
'''

    else:

        # Exploring / Practicing remain exactly as before.

        svg += f'''
    <!-- Percentage / status -->

    <text
        x="720"
        y="{y}"
        fill="{GREEN}"
        font-size="15"
        class="terminal bold status">
        {label}
    </text>
'''

    svg += '''
</g>
'''


svg += f'''

<!-- ===================================================== -->
<!-- FOOTER -->
<!-- ===================================================== -->

<line
    x1="35"
    y1="415"
    x2="865"
    y2="415"
    stroke="{BORDER}"
    stroke-width="1"
/>


<text
    x="35"
    y="445"
    fill="{GREEN}"
    font-size="16"
    class="terminal bold">
    &gt; Progress &gt; Perfection
</text>


<!-- Blinking cursor -->

<rect
    x="265"
    y="429"
    width="9"
    height="18"
    rx="1"
    fill="{GREEN}"
    class="cursor"
    filter="url(#glow)"
/>


<!-- Subtle scan -->

<rect
    x="25"
    y="82"
    width="850"
    height="1"
    fill="{GREEN}"
    class="scan"
/>


</svg>
'''


OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(svg, encoding="utf-8")

print(f"Generated: {OUTPUT}")