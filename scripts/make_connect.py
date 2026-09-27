from pathlib import Path
from html import escape


ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"


links = [
    (
        "LINKEDIN",
        "kuntal-sarkar-dev",
        "https://www.linkedin.com/in/kuntal-sarkar-dev",
        "linkedin",
    ),
    (
        "LEETCODE",
        "kuntal_exe",
        "https://leetcode.com/kuntal_exe",
        "leetcode",
    ),
    (
        "X",
        "kuntal_074",
        "https://twitter.com/kuntal_074",
        "x",
    ),
    (
        "INSTAGRAM",
        "kuntal.exe.x",
        "https://instagram.com/kuntal.exe.x",
        "instagram",
    ),
]


STYLE = '''
<style>

.mono {
    font-family: "DejaVu Sans Mono", "Liberation Mono", monospace;
}

.title {
    fill: #E6EDF3;
    font-size: 13px;
}

.prompt {
    fill: #7EE787;
    font-size: 14px;
}

.command {
    fill: #E6EDF3;
    font-size: 14px;
}

.label {
    fill: #8B949E;
    font-size: 10px;
    letter-spacing: 1.5px;
}

.username {
    fill: #E6EDF3;
    font-size: 14px;
}

.card {
    fill: #0D1117;
    stroke: #30363D;
    stroke-width: 1;
}

.dot {
    fill: #7EE787;
}

.footer {
    fill: #484F58;
    font-size: 10px;
}

</style>
'''


def make_card(label, username, output_name):

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
width="195" height="62" viewBox="0 0 195 62">

<defs>
{STYLE}
</defs>

<rect
    x="1"
    y="1"
    width="193"
    height="60"
    rx="9"
    class="card"
/>

<circle
    cx="19"
    cy="21"
    r="4"
    class="dot"
/>

<text
    x="32"
    y="25"
    class="mono label"
>
    {escape(label)}
</text>

<text
    x="19"
    y="48"
    class="mono username"
>
    {escape(username)}
</text>

</svg>
'''

    output = ASSETS / output_name
    output.write_text(svg, encoding="utf-8")

    print(f"Generated: {output}")


def make_full_connect():

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
width="900" height="230" viewBox="0 0 900 230">

<defs>
{STYLE}
</defs>


<!-- TERMINAL WINDOW -->

<rect
    x="10"
    y="10"
    width="880"
    height="210"
    rx="14"
    fill="#0D1117"
    stroke="#30363D"
    stroke-width="1"
/>


<!-- TRAFFIC LIGHTS -->

<circle cx="34" cy="34" r="5" fill="#FF7B72"/>
<circle cx="52" cy="34" r="5" fill="#D29922"/>
<circle cx="70" cy="34" r="5" fill="#7EE787"/>


<!-- TERMINAL TITLE -->

<text
    x="92"
    y="39"
    class="mono title"
>
    kuntal@github — connect
</text>


<line
    x1="25"
    y1="56"
    x2="875"
    y2="56"
    stroke="#21262D"
/>


<!-- COMMAND -->

<text
    x="35"
    y="84"
    class="mono prompt"
>
    kuntal@github:~$
</text>

<text
    x="178"
    y="84"
    class="mono command"
>
    ./connect.sh
</text>


<line
    x1="35"
    y1="101"
    x2="865"
    y2="101"
    stroke="#30363D"
/>


<!-- CARDS -->

'''

    card_positions = [30, 245, 460, 675]

    for (label, username, url, key), x in zip(links, card_positions):

        svg += f'''
<rect
    x="{x}"
    y="118"
    width="195"
    height="62"
    rx="9"
    class="card"
/>

<circle
    cx="{x + 18}"
    cy="139"
    r="4"
    class="dot"
/>

<text
    x="{x + 31}"
    y="143"
    class="mono label"
>
    {escape(label)}
</text>

<text
    x="{x + 18}"
    y="166"
    class="mono username"
>
    {escape(username)}
</text>

'''

    svg += '''
<!-- FOOTER -->

<text
    x="35"
    y="204"
    class="mono footer"
>
    [ 4 endpoints available ]
</text>


<text
    x="865"
    y="204"
    text-anchor="end"
    class="mono"
    fill="#7EE787"
    font-size="10"
>
    ONLINE
</text>


</svg>
'''

    output = ASSETS / "connect.svg"
    output.write_text(svg, encoding="utf-8")

    print(f"Generated: {output}")


ASSETS.mkdir(parents=True, exist_ok=True)


# Generate individual clickable cards
make_card(
    "LINKEDIN",
    "kuntal-sarkar-dev",
    "connect-linkedin.svg",
)

make_card(
    "LEETCODE",
    "kuntal_exe",
    "connect-leetcode.svg",
)

make_card(
    "X",
    "kuntal_074",
    "connect-x.svg",
)

make_card(
    "INSTAGRAM",
    "kuntal.exe.x",
    "connect-instagram.svg",
)


# Generate the original complete visual
make_full_connect()