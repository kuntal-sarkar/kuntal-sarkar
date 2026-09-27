from pathlib import Path
import urllib.request
import json
import os
import html

USERNAME = "Kuntal-sarkar"
OUTPUT = Path("assets/github-stats.svg")

TOKEN = os.environ.get("GITHUB_TOKEN")

if not TOKEN:
    raise RuntimeError(
        "GITHUB_TOKEN not found. Set your GitHub token as an environment variable."
    )


# ==========================================================
# GitHub GraphQL
# ==========================================================

QUERY = """
query($login: String!) {
  user(login: $login) {

    repositories(
      first: 100
      ownerAffiliations: OWNER
      privacy: PUBLIC
    ) {
      nodes {
        name

        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges {
            size
            node {
              name
            }
          }
        }
      }
    }

    contributionsCollection {
      contributionCalendar {
        totalContributions
      }

      totalCommitContributions
      totalIssueContributions
      totalPullRequestContributions
      totalPullRequestReviewContributions
    }
  }
}
"""


payload = json.dumps({
    "query": QUERY,
    "variables": {
        "login": USERNAME
    }
}).encode("utf-8")


request = urllib.request.Request(
    "https://api.github.com/graphql",
    data=payload,
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "User-Agent": "Kuntal-GitHub-Profile"
    },
    method="POST"
)


with urllib.request.urlopen(request) as response:
    result = json.loads(response.read().decode())


if "errors" in result:
    raise RuntimeError(
        "GitHub API Error:\n" +
        json.dumps(result["errors"], indent=2)
    )


user = result["data"]["user"]


# ==========================================================
# Contributions
# ==========================================================

contributions = user["contributionsCollection"]

total_contributions = (
    contributions["contributionCalendar"]["totalContributions"]
)

commits = contributions["totalCommitContributions"]
issues = contributions["totalIssueContributions"]
pull_requests = contributions["totalPullRequestContributions"]
reviews = contributions["totalPullRequestReviewContributions"]


# ==========================================================
# Repository count
# ==========================================================

repositories = user["repositories"]["nodes"]


# ==========================================================
# Calculate language usage
# ==========================================================

language_totals = {}

for repo in repositories:

    languages = repo.get("languages")

    if not languages:
        continue

    for edge in languages["edges"]:

        language = edge["node"]["name"]
        size = edge["size"]

        language_totals[language] = (
            language_totals.get(language, 0) + size
        )


sorted_languages = sorted(
    language_totals.items(),
    key=lambda item: item[1],
    reverse=True
)


top_languages = sorted_languages[:5]

total_language_bytes = sum(
    language_totals.values()
)


# ==========================================================
# Calculate percentages
# ==========================================================

language_data = []

for language, size in top_languages:

    percentage = (
        (size / total_language_bytes) * 100
        if total_language_bytes
        else 0
    )

    language_data.append(
        (
            language,
            percentage
        )
    )


top_language = (
    language_data[0][0]
    if language_data
    else "N/A"
)


# ==========================================================
# SVG SETTINGS
# ==========================================================

WIDTH = 900
HEIGHT = 500

BG = "#0D1117"
BORDER = "#30363D"
TEXT = "#E6EDF3"
MUTED = "#8B949E"
GREEN = "#7EE787"
GREEN_DIM = "#238636"


# ==========================================================
# SVG
# ==========================================================

svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
    width="{WIDTH}"
    height="{HEIGHT}"
    viewBox="0 0 {WIDTH} {HEIGHT}">

<style>

    .terminal {{
        font-family: "Courier New", monospace;
    }}

    .bold {{
        font-weight: 700;
    }}

    .value {{
        fill: {GREEN};
        font-size: 24px;
        font-weight: 700;
    }}

    .label {{
        fill: {MUTED};
        font-size: 14px;
    }}

    .language {{
        fill: {MUTED};
        font-size: 14px;
    }}

    .bar-bg {{
        fill: #21262D;
    }}

    .language-bar {{
        fill: {GREEN};
    }}

    .counter-frame {{
        pointer-events: none;
    }}

    .cursor {{
        animation: blink 0.8s steps(1) infinite;
    }}

    @keyframes blink {{
        0%, 45% {{
            opacity: 1;
        }}

        46%, 100% {{
            opacity: 0;
        }}
    }}

    .window {{
        animation: pulse 4s ease-in-out infinite;
    }}

    @keyframes pulse {{
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
    width="880"
    height="480"
    rx="15"
    fill="{BG}"
    stroke="{BORDER}"
    stroke-width="2"
    class="window"
/>


<!-- ===================================================== -->
<!-- TRAFFIC LIGHTS -->
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
/>


<!-- ===================================================== -->
<!-- COMMAND -->
<!-- ===================================================== -->

<text
    x="35"
    y="105"
    fill="{GREEN}"
    font-size="18"
    class="terminal bold">
    kuntal@github:~$ github_stats
</text>


<!-- Heading -->

<text
    x="35"
    y="140"
    fill="{TEXT}"
    font-size="18"
    class="terminal bold">
    05 — GITHUB ANALYTICS
</text>


<!-- ===================================================== -->
<!-- CONTRIBUTION STATS -->
<!-- ===================================================== -->

<text
    x="65"
    y="185"
    fill="{MUTED}"
    font-size="14"
    class="terminal">
    TOTAL CONTRIBUTIONS
</text>

<text
    x="65"
    y="220"
    class="terminal value">
    {total_contributions}
</text>


<text
    x="300"
    y="185"
    fill="{MUTED}"
    font-size="14"
    class="terminal">
    COMMITS
</text>

<text
    x="300"
    y="220"
    class="terminal value">
    {commits}
</text>


<text
    x="500"
    y="185"
    fill="{MUTED}"
    font-size="14"
    class="terminal">
    PULL REQUESTS
</text>

<text
    x="500"
    y="220"
    class="terminal value">
    {pull_requests}
</text>


<text
    x="720"
    y="185"
    fill="{MUTED}"
    font-size="14"
    class="terminal">
    ISSUES
</text>

<text
    x="720"
    y="220"
    class="terminal value">
    {issues}
</text>


<!-- ===================================================== -->
<!-- TOP LANGUAGE -->
<!-- ===================================================== -->

<text
    x="65"
    y="265"
    fill="{MUTED}"
    font-size="14"
    class="terminal">
    TOP LANGUAGE
</text>

<text
    x="65"
    y="295"
    fill="{GREEN}"
    font-size="17"
    class="terminal bold">
    {html.escape(top_language)}
</text>


<!-- ===================================================== -->
<!-- LANGUAGE BREAKDOWN -->
<!-- ===================================================== -->

<text
    x="300"
    y="265"
    fill="{TEXT}"
    font-size="16"
    class="terminal bold">
    LANGUAGE BREAKDOWN
</text>
'''


# ==========================================================
# Language bars + animated counters
# ==========================================================

LANG_X = 300
BAR_X = 470
BAR_WIDTH = 300
BAR_HEIGHT = 9
LANG_START_Y = 292
LANG_GAP = 30

BAR_DURATION = 5.5


for index, (language, percentage) in enumerate(language_data):

    y = LANG_START_Y + (index * LANG_GAP)

    filled_width = BAR_WIDTH * (percentage / 100)

    target = max(0, min(100, round(percentage)))

    bar_delay = 0.45 + (index * 0.20)

    step_time = (
        BAR_DURATION / max(target, 1)
    )

    svg += f'''
<text
    x="{LANG_X}"
    y="{y}"
    fill="{MUTED}"
    font-size="14"
    class="terminal">
    {html.escape(language)}
</text>

<rect
    x="{BAR_X}"
    y="{y - 8}"
    width="{BAR_WIDTH}"
    height="{BAR_HEIGHT}"
    rx="4"
    class="bar-bg"
/>

<rect
    x="{BAR_X}"
    y="{y - 8}"
    width="0"
    height="{BAR_HEIGHT}"
    rx="4"
    class="language-bar">

    <animate
        attributeName="width"
        from="0"
        to="{filled_width:.2f}"
        dur="{BAR_DURATION}s"
        begin="{bar_delay:.2f}s"
        fill="freeze"
    />

</rect>
'''


    # ======================================================
    # Animated percentage counter
    # ======================================================

    for number in range(target + 1):

        frame_start = (
            bar_delay +
            (number * step_time)
        )

        if number == target:

            # Final actual percentage stays visible.

            svg += f'''
<text
    x="785"
    y="{y}"
    fill="{GREEN}"
    font-size="14"
    class="terminal bold counter-frame"
    opacity="0">

    {percentage:.1f}%

    <animate
        attributeName="opacity"
        values="0;1;1"
        dur="{step_time:.4f}s"
        begin="{frame_start:.4f}s"
        fill="freeze"
    />

</text>
'''

        else:

            # Each number appears once for its step
            # and then disappears permanently.

           svg += f'''
<text
    x="785"
    y="{y}"
    fill="{GREEN}"
    font-size="14"
    class="terminal bold counter-frame"
    opacity="0">

    {number}%

    <animate
        attributeName="opacity"
        values="0;1;1;0"
        keyTimes="0;0.01;0.99;1"
        dur="{step_time:.4f}s"
        begin="{frame_start:.4f}s"
        fill="freeze"
    />

</text>
'''


svg += f'''

<!-- ===================================================== -->
<!-- FOOTER -->
<!-- ===================================================== -->

<line
    x1="35"
    y1="450"
    x2="865"
    y2="450"
    stroke="{BORDER}"
/>


<text
    x="35"
    y="475"
    fill="{GREEN}"
    font-size="15"
    class="terminal bold">
    &gt; Live data • GitHub GraphQL API
</text>


<rect
    x="330"
    y="461"
    width="8"
    height="17"
    fill="{GREEN}"
    class="cursor"
/>


</svg>
'''


# ==========================================================
# Save
# ==========================================================

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

OUTPUT.write_text(
    svg,
    encoding="utf-8"
)

print(f"Generated: {OUTPUT}")
print()
print(f"Total contributions : {total_contributions}")
print(f"Commits             : {commits}")
print(f"Pull requests       : {pull_requests}")
print(f"Issues              : {issues}")
print(f"Top language        : {top_language}")