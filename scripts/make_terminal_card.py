from pathlib import Path

OUTPUT = Path("assets/terminal-card.svg")

WIDTH = 900
HEIGHT = 430

BG = "#0D1117"
BORDER = "#30363D"
TEXT = "#E6EDF3"
MUTED = "#8B949E"
GREEN = "#7EE787"


lines = [
    ("OS", "GitHub Profile"),
    ("USER", "Kuntal-sarkar"),
    ("ROLE", "CSE Student"),
    ("INTERESTED IN", "Software Development"),
    ("LEARNING", "Python • Java • Backend"),
    ("EXPLORING", "Cybersecurity • AI"),
]


svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
    width="{WIDTH}"
    height="{HEIGHT}"
    viewBox="0 0 {WIDTH} {HEIGHT}">

<defs>

    <!-- Soft green glow -->
    <filter id="greenGlow" x="-50%" y="-50%" width="200%" height="200%">
        <feGaussianBlur stdDeviation="3" result="blur"/>
        <feMerge>
            <feMergeNode in="blur"/>
            <feMergeNode in="SourceGraphic"/>
        </feMerge>
    </filter>

    <!-- Very subtle window glow -->
    <filter id="windowGlow" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="2" result="blur"/>
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

    .main-text {{
        font-weight: 700;
    }}

    /* Boot animation */
    .boot {{
        opacity: 0;
        transform: translateY(8px);
        animation: boot 0.65s ease-out forwards;
    }}

    .line1 {{ animation-delay: 0.20s; }}
    .line2 {{ animation-delay: 0.38s; }}
    .line3 {{ animation-delay: 0.56s; }}
    .line4 {{ animation-delay: 0.74s; }}
    .line5 {{ animation-delay: 0.92s; }}
    .line6 {{ animation-delay: 1.10s; }}

    @keyframes boot {{
        0% {{
            opacity: 0;
            transform: translateY(8px);
        }}

        70% {{
            opacity: 1;
            transform: translateY(-1px);
        }}

        100% {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    /* Cursor */
    .cursor {{
        animation: cursorBlink 0.85s steps(1) infinite;
    }}

    @keyframes cursorBlink {{
        0%, 45% {{
            opacity: 1;
        }}

        46%, 100% {{
            opacity: 0;
        }}
    }}

    /* Online indicator */
    .status {{
        animation: statusPulse 1.8s ease-in-out infinite;
    }}

    @keyframes statusPulse {{
        0%, 100% {{
            opacity: 0.55;
        }}

        50% {{
            opacity: 1;
        }}
    }}

    /* Window border */
    .terminal-box {{
        animation: terminalPulse 4s ease-in-out infinite;
    }}

    @keyframes terminalPulse {{
        0%, 100% {{
            stroke-opacity: 0.70;
        }}

        50% {{
            stroke-opacity: 1;
        }}
    }}

    /* Small scan effect */
    .scan {{
        animation: scan 5s ease-in-out infinite;
    }}

    @keyframes scan {{
        0%, 65%, 100% {{
            opacity: 0;
        }}

        68% {{
            opacity: 0.12;
        }}

        72% {{
            opacity: 0;
        }}
    }}

</style>


<!-- ====================================================== -->
<!-- TERMINAL WINDOW -->
<!-- ====================================================== -->

<rect
    x="10"
    y="10"
    width="{WIDTH - 20}"
    height="{HEIGHT - 20}"
    rx="15"
    fill="{BG}"
    stroke="{BORDER}"
    stroke-width="2"
    class="terminal-box"
    filter="url(#windowGlow)"
/>


<!-- ====================================================== -->
<!-- macOS TRAFFIC LIGHTS -->
<!-- ====================================================== -->

<circle
    cx="34"
    cy="38"
    r="7"
    fill="#FF5F57"
/>

<circle
    cx="58"
    cy="38"
    r="7"
    fill="#FEBC2E"
/>

<circle
    cx="82"
    cy="38"
    r="7"
    fill="#28C840"
/>


<!-- ====================================================== -->
<!-- TERMINAL TITLE -->
<!-- ====================================================== -->

<text
    x="112"
    y="44"
    fill="{MUTED}"
    font-size="17"
    class="terminal">
    kuntal@github
</text>


<!-- ====================================================== -->
<!-- HEADER DIVIDER -->
<!-- ====================================================== -->

<line
    x1="30"
    y1="70"
    x2="870"
    y2="70"
    stroke="{BORDER}"
    stroke-width="1"
/>


<!-- ====================================================== -->
<!-- BOOT COMMAND -->
<!-- ====================================================== -->

<text
    x="35"
    y="105"
    fill="{GREEN}"
    font-size="17"
    class="terminal main-text"
    filter="url(#greenGlow)">
    kuntal@github:~$ who am i
</text>


<!-- ====================================================== -->
<!-- USER -->
<!-- ====================================================== -->

<text
    x="35"
    y="135"
    fill="{TEXT}"
    font-size="17"
    class="terminal main-text">
    Kuntal-sarkar
</text>


<!-- ====================================================== -->
<!-- INFORMATION -->
<!-- ====================================================== -->
'''

y = 180

for i, (label, value) in enumerate(lines, start=1):

    svg += f'''
<g class="boot line{i}">

    <text
        x="35"
        y="{y}"
        fill="{MUTED}"
        font-size="16"
        class="terminal">
        {label}
    </text>

    <text
        x="218"
        y="{y}"
        fill="{TEXT}"
        font-size="16"
        class="terminal main-text">
        {value}
    </text>

</g>
'''

    y += 32


svg += f'''

<!-- ====================================================== -->
<!-- STATUS -->
<!-- ====================================================== -->

<g class="boot line6">

    <text
        x="35"
        y="385"
        fill="{MUTED}"
        font-size="16"
        class="terminal">
        STATUS
    </text>

    <circle
        cx="218"
        cy="380"
        r="6"
        fill="{GREEN}"
        class="status"
        filter="url(#greenGlow)"
    />

    <text
        x="233"
        y="385"
        fill="{GREEN}"
        font-size="16"
        class="terminal main-text">
        ONLINE
    </text>

</g>


<!-- ====================================================== -->
<!-- BOTTOM COMMAND -->
<!-- ====================================================== -->

<text
    x="35"
    y="414"
    fill="{GREEN}"
    font-size="16"
    class="terminal main-text">
    kuntal@github:~$
</text>


<!--
    "$" ends around x=251.
    One character-space after "$" starts around x=200.
    Cursor placed there intentionally.
-->

<rect
    x="200"
    y="397"
    width="9"
    height="19"
    rx="1"
    fill="{GREEN}"
    class="cursor"
    filter="url(#greenGlow)"
/>


<!-- ====================================================== -->
<!-- SUBTLE SCAN LINE -->
<!-- ====================================================== -->

<rect
    x="25"
    y="80"
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