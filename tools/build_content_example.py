"""Build the Content Example prototypes from reference/audit.md.

Usage, from the site root:
    python3 tools/build_content_example.py .

Steps
  A. Parse the audit's two tables into prototypes/content-example/data/examples.json,
     adding TCC curation (paraphrase only) from the CURATION table below.
  B. Write static HTML for three player models (stage/, canvas/, spec/):
     a library page (messenger and curator views), one detail page per
     example and one page per contrast pair.
  C. Write the compare page (prototypes/content-example/index.html) and the
     page-weight block in the README.

Python 3 standard library only. Overwrites only generated files: the JSON,
every *.html in the three model folders, the compare page, and the block
between the "weights" markers in README.md. Hand-written files (CSS, JS,
schema.md, the rest of README.md) are never touched.

Rights: nothing here copies the originals. Each artifact is drawn as an
HTML/CSS stand-in filled with TCC paraphrase from the audit, plus at most
one short quote (under 15 words) that the audit itself already quotes.
"""
import html, json, pathlib, re, sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
OUT = ROOT / "prototypes" / "content-example"
AUDIT = ROOT / "reference" / "audit.md"

AUDIT_DATE = "2026-11-06"
TAXONOMY = "prototype-0 (Nov 2026)"
RUBRIC = "TCC segment audit first-pass screen, Nov 6, 2026"

PRIN = [
    ("P1", "Personal"), ("P2", "Accessible"), ("P3", "Empowering"), ("P4", "Doable"),
    ("P5", "Collective"), ("P6", "Normal"), ("P7", "Trustworthy"), ("P8", "For everyone"),
]
PNAME = dict(PRIN)
GRADE = {"+": ("strong", "+"), "~": ("mixed", "~"), "–": ("weak", "–"), "·": ("not in play", "·"), "": ("not graded", "—")}
VERDICT_SLUG = {"Good example": "good", "So-so": "soso", "Not yet usable": "not"}

# Controlled content-type list (IN-2). Slug -> label.
TYPES = {
    "short-video": "Short video", "long-video": "Long video", "social-post": "Social post",
    "news-article": "News article", "op-ed": "Op-ed", "blog-post": "Blog post",
    "news-release": "News release", "testimony": "Testimony recap", "profile": "Profile",
    "roster": "Roster page",
}
TOPICS = {
    "heat": "Heat", "wildfire-smoke": "Wildfire smoke", "air-quality": "Air quality",
    "clinical-care": "Clinical care", "voting": "Voting", "clean-transport": "Clean transport",
    "waste": "Plastic and compost", "winter": "Winter and snow", "public-lands": "Public lands",
    "policy": "Policy",
}
SEGMENTS = {"health": "Health professionals", "athlete": "Outdoor and athlete voices"}

# ---------------------------------------------------------------------------
# TCC curation, keyed by source URL (the audit's link). Paraphrase only.
# notes: (principle, "working" | "improve", one-line note, region key)
# regions: (key, short label, TCC paraphrase shown in the stand-in)
# Fields marked draft below (structure, doable_step, topics, geography,
# timeliness, audience) are derived from the audit text for prototyping.
# ---------------------------------------------------------------------------
CURATION = {
"https://www.youtube.com/watch?v=3SnN9aQxQpE": dict(
    id="lawson-heat-dome-speech", type="long-video", format="long-video",
    venue="CAPE (Canadian Association of Physicians for the Environment)", platform="YouTube",
    role="Doctor (per the video's title on YouTube)", affil="Speaking at a CAPE event",
    authors=["CAPE"], topics=["heat"], geo=("Vancouver, BC, Canada", "regional"),
    timeliness="Anniversary of the 2021 BC heat dome", audience=["public"],
    why="She starts from what she saw working downtown Vancouver during the 2021 heat dome, so the story is personal and local. She moves from grief to a hopeful turn toward cheaper, cleaner energy, then asks for one thing anyone can do: check on isolated seniors.",
    watch="A few phrases could be plainer (P2 mixed), and it doesn't yet show others already acting (P6 mixed). It had 20 views in our audit: strong but unseen.",
    structure=["Hook: what she saw during the 2021 heat dome", "Local link: downtown Vancouver", "Feeling: grief, named honestly", "Turn: cheaper, cleaner energy", "One ask: check on isolated seniors"],
    step="Check on isolated seniors when it's hot.",
    fe="Stays on health, neighbours and energy costs; no partisan framing.",
    notes=[("P1", "working", "Opens with what she saw at work during the heat dome.", "opening"),
           ("P3", "working", "Moves from grief to a hopeful turn: cheaper, cleaner energy.", "turn"),
           ("P4", "working", "Ends with one step anyone can take: check on isolated seniors.", "ask"),
           ("P6", "improve", "Could show more people already acting, so it feels normal.", "turn")],
    regions=[("opening", "Opening", "She recalls working in downtown Vancouver during the 2021 heat dome."),
             ("turn", "Middle", "From grief to hope: cheaper, cleaner energy."),
             ("ask", "Close", "Her ask: check on isolated seniors.")],
    media=dict(platform="YouTube", url="https://www.youtube.com/watch?v=3SnN9aQxQpE", embed_id="3SnN9aQxQpE",
               duration_s=295, approx_mb="about 20–40 MB at 720p (estimate)", captions=None),
    engagement=[dict(date=AUDIT_DATE, views=20, note="In our audit")], amplify=True,
),
"https://www.youtube.com/shorts/DSOotr4ZQQk": dict(
    id="msv-healthcare-short", type="short-video", format="short-video",
    venue="Medical Society of Virginia", platform="YouTube (Shorts)",
    role="Physician (name not given)", affil="Medical Society of Virginia",
    authors=["Medical Society of Virginia"], topics=["heat", "wildfire-smoke", "clinical-care"], geo=("Virginia, US", "regional"),
    timeliness="Evergreen", audience=["peers"], institution="Medical Society of Virginia (state medical society)",
    why="A physician talks to other clinicians about routine care, not politics. The asks are small and clinical: ask older patients about heat, and ask parents of kids with asthma about smoky air.",
    watch="The speaker isn't named, and it doesn't show other practices already doing this (P5, P6 mixed). It had 55 views in our audit.",
    structure=["Frame: one clinician to another", "Health link: heat and older patients; smoke and asthma", "Step: one screening question per patient group"],
    step="Ask older patients about heat, and parents of kids with asthma about smoky air.",
    fe="Framed as routine clinical care, which keeps it out of politics.",
    notes=[("P7", "working", "A physician speaking to peers: a trusted messenger for this audience.", "opening"),
           ("P4", "working", "Two screening questions a clinician can add tomorrow.", "ask"),
           ("P5", "improve", "Could show other practices already asking these questions.", "ask")],
    regions=[("opening", "Opening", "A physician speaks to fellow clinicians about routine care."),
             ("ask", "Tip", "Ask older patients about heat, and parents of kids with asthma about smoky air.")],
    media=dict(platform="YouTube", url="https://www.youtube.com/shorts/DSOotr4ZQQk", embed_id="DSOotr4ZQQk",
               duration_s=54, approx_mb="about 5–10 MB (estimate)", captions=None),
    engagement=[dict(date=AUDIT_DATE, views=55, note="In our audit")], amplify=True,
),
"https://www.cp24.com/news/canada/2026/07/11/one-of-the-biggest-public-health-threats-why-doctors-say-you-need-to-take-wildfire-smoke-seriously/": dict(
    id="howard-wildfire-smoke", type="news-article", format="article", venue="CP24", platform="News website",
    role="Emergency physician", affil="CMA president-elect", authors=["CP24"],
    topics=["wildfire-smoke", "air-quality"], geo=("Canada", "national"), timeliness="Wildfire-smoke season", audience=["public"],
    why="She names local towns and admits her own home runs four air filters, so it feels personal, not preachy. Then she gives three steps anyone can take today.",
    watch="One slip: jargon about particle size in microns. Try “tiny particles that reach deep into the lungs.”",
    structure=["Hook: local towns under smoke", "Personal: her own home runs four air filters", "Health effect, in plain words", "Three steps for today"],
    step="Take one of the three smoke-day steps she lists (read the original for the list).",
    fe="Practical and non-partisan: it's about protecting your lungs, not about blame.",
    notes=[("P1", "working", "Names local towns, so readers see their own place.", "lede"),
           ("P7", "working", "Admits her own home runs four air filters: she walks the talk.", "p1"),
           ("P2", "improve", "Jargon about particle size in microns. Say “tiny particles” instead.", "p2"),
           ("P4", "working", "Ends with three steps anyone can take today.", "ask")],
    regions=[("headline", "Headline", None), ("lede", "Lede", "An emergency physician links wildfire smoke to health and names local towns."),
             ("p1", "Paragraph", "She mentions that her own home runs four air filters."),
             ("p2", "Paragraph", "A passage explains smoke particle size in microns."),
             ("ask", "The ask", "Three steps readers can take today.")],
),
"https://globalnews.ca/news/8366001/bc-doctor-climate-change-diagnosis": dict(
    id="merritt-climate-diagnosis", type="news-article", format="article", venue="Global News", platform="News website",
    role="Family physician", affil="Nelson, BC", authors=["Global News"],
    topics=["heat", "clinical-care"], geo=("Nelson, BC, Canada", "local"), timeliness="2021 BC heat dome", audience=["public", "peers"],
    why="He opens with a patient in her 70s during the heat dome and says plainly he is a doctor, not an activist. That protects his standing and shows climate as something he sees in clinic.",
    watch="He calls it the first time he wrote the term, which makes the practice sound rare (P6). Frame it as something more doctors are starting to do.",
    structure=["Hook: one patient during the heat dome", "Role: a doctor, not an activist", "Health link in plain words", "The practice: naming climate in the chart"],
    step="When it applies, name climate as a factor in a patient's chart.",
    fe="He separates his clinical role from activism, which keeps it cross-audience.",
    notes=[("P1", "working", "Opens with a patient in her 70s during the heat dome.", "lede"),
           ("P7", "working", "Says plainly he's a doctor, not an activist.", "p1"),
           ("P6", "improve", "“First time” framing makes the practice sound rare.", "p2")],
    regions=[("headline", "Headline", None), ("lede", "Lede", "A patient in her 70s, during the 2021 heat dome, leads the story."),
             ("p1", "Paragraph", "He says plainly that he is a doctor, not an activist."),
             ("p2", "Paragraph", "He calls it the first time he wrote the term in a chart.")],
),
"https://www.turnto23.com/news/health/doctors-are-starting-to-incorporate-climate-change-into-their-patient-care": dict(
    id="dresser-climate-patient-care", type="news-article", format="tv-story", venue="Turn to 23 (local TV)", platform="TV station website",
    role="Emergency physician", affil="Harvard Chan C-CHANGE", authors=["Turn to 23"],
    topics=["heat", "clinical-care"], geo=("United States", "local"), timeliness="Evergreen", audience=["public", "peers"],
    why="He turns climate into a clinical question: “What's your plan?” for a hot day. It's the clearest doable step in the set, and it sounds like normal care, not advocacy.",
    watch="It dates from 2021, so pair it with something current. It could show more clinicians already asking (P5, P6 mixed).",
    quote="What's your plan?",
    structure=["Frame: climate as a clinical question", "Ask the patient: what's your plan for a hot day?", "Why it matters for their health"],
    step="Ask patients: “What's your plan?” for a hot day.",
    fe="Clinical framing keeps it out of politics.",
    notes=[("P2", "working", "Plain, clinical language; no jargon.", "lede"),
           ("P4", "working", "“What's your plan?” is a step any clinician can use.", "quote"),
           ("P6", "improve", "Could show how many clinicians already ask this.", "p2")],
    regions=[("headline", "Headline", None), ("clip", "Broadcast clip", "Broadcast segment (not shown in this prototype)."),
             ("lede", "Lede", "Doctors describe bringing climate into patient visits."),
             ("quote", "Key line", "The clinical question for a hot day: “What's your plan?”"),
             ("p2", "Paragraph", "The story centers one physician; few others are shown.")],
),
"https://www.seattletimes.com/opinion/extreme-heats-impact-on-our-health-demands-we-take-action/": dict(
    id="seattle-times-heat-oped", type="op-ed", format="op-ed", venue="The Seattle Times", platform="News website",
    role="Physicians", affil="Washington Physicians for Social Responsibility (WA PSR)",
    authors=["Breck Lebegue", "Chris Covert-Bowlds", "Michael Soman"],
    topics=["heat"], geo=("Washington State, US", "regional"), timeliness="2021 heat dome, written in 2023", audience=["public", "policymakers"],
    why="Some of the most vivid patient stories in the set, such as a man who had a heart attack waiting for roadside help on I-5.",
    watch="It opens with a long list of disasters and despair, calls the science “no longer a matter of debate,” and ends with more than ten asks at once. Fix: lead with one patient, drop the debate, end with one ask.",
    quote="no longer a matter of debate",
    structure=["(As published) Opening list of disasters", "Patient stories", "Debate framing", "Ten-plus asks"],
    fe="Calling the science settled spotlights the debate it means to close (P8 mixed).",
    notes=[("P3", "improve", "Opens with a long list of disasters and despair. Lead with the patient instead.", "lede"),
           ("P1", "working", "Vivid patient story: a heart attack while waiting for help on I-5.", "p1"),
           ("P8", "improve", "“No longer a matter of debate” spotlights the debate. Skip it.", "p2"),
           ("P4", "improve", "More than ten asks at once. Pick one.", "ask")],
    regions=[("headline", "Headline", None), ("lede", "Opening", "Opens with a long list of disasters and feelings of despair."),
             ("p1", "Paragraph", "Patient story: a man had a heart attack while waiting for roadside help on I-5."),
             ("p2", "Paragraph", "A passage says the science is “no longer a matter of debate.”"),
             ("ask", "Close", "Ends with more than ten asks at once.")],
),
"https://psr.org/as-doctors-see-the-costs-of-climate-change-trump-plays-a-deadly-game-of-denial/": dict(
    id="vossler-psr-post", type="blog-post", format="blog", venue="PSR / Earthjustice", platform="Organization website",
    role="Retired cardiologist", affil="Physicians for Social Responsibility (PSR)", authors=["Mark Vossler"],
    topics=["heat", "policy"], geo=("United States", "national"), timeliness="2026 federal policy debate", audience=["public"],
    partisan="The headline frames the piece as a fight about the President.",
    why="A powerful patient story from a cardiologist's practice.",
    watch="The headline turns the story into a fight about the President, so readers who don't share that view stop reading. The excerpt we saw offers no path forward. Fix: keep the patient story, drop the partisan headline, add one step.",
    structure=["(As published) Partisan headline", "Patient story", "No step"],
    fe="Partisan headline limits reach with cross-party readers (P8 weak).",
    notes=[("P8", "improve", "Headline frames a partisan fight; many readers stop here.", "headline"),
           ("P3", "improve", "Anger is aimed at a person, not at a solution.", "lede"),
           ("P1", "working", "A powerful patient story.", "p1"),
           ("P4", "improve", "No step for readers in the excerpt we saw.", "close")],
    regions=[("headline", "Headline", None), ("lede", "Lede", "A retired cardiologist describes the costs doctors see, set against a political fight."),
             ("p1", "Paragraph", "A powerful patient story."),
             ("close", "Close", "The excerpt ends without a step for readers.")],
),
"https://www.napnap.org/nursing-leaders-taking-action-on-extreme-heat/": dict(
    id="napnap-nursing-heat", type="news-release", format="release", venue="NAPNAP / ANHE", platform="Organization website",
    role="Nursing organizations", affil="NAPNAP and the Alliance of Nurses for Healthy Environments (ANHE)", authors=["NAPNAP", "ANHE"],
    topics=["heat", "policy"], geo=("United States", "national"), timeliness="Heat season", audience=["peers", "policymakers"],
    institution="National nursing organizations",
    why="Real collective momentum: 26 organizations representing 5 million nurses, acting together on heat.",
    watch="It is buried in agency acronyms and a long list of asks with no first step. Fix: spell out names, lead with one nurse's story, and give one first step.",
    structure=["(As published) Coalition announcement", "Agency acronyms", "Long list of asks"],
    notes=[("P5", "working", "26 organizations, 5 million nurses: a strong collective signal.", "lede"),
           ("P2", "improve", "Agency acronyms bury the message.", "p1"),
           ("P4", "improve", "A long list of asks with no first step.", "ask")],
    regions=[("headline", "Headline", None), ("lede", "Lede", "26 organizations representing 5 million nurses announce joint action on heat."),
             ("p1", "Body", "The body names programs by agency acronyms."),
             ("ask", "Asks", "A long list of asks, with no first step.")],
),
"https://www.instagram.com/p/DfQUuJvEgdL/": dict(
    id="pow-signs-everywhere", type="social-post", format="carousel", venue="Protect Our Winters", platform="Instagram",
    role="Outdoor advocacy organization", affil="Protect Our Winters (POW)", authors=["Protect Our Winters"],
    topics=["voting"], geo=("United States", "national"), timeliness="2026 election", audience=["fans"],
    quote="The signs are everywhere",
    why="It asks followers to text three friends: a small, specific step, framed as what everyone is already doing.",
    watch="Little personal story (P1 mixed), and as an organization account it speaks more as an authority than a peer (P7 mixed).",
    structure=["Hook: the signs are everywhere", "Norm: people like you are already doing this", "One small step: text three friends"],
    step="Text three friends.",
    fe="Asks people to vote without telling them how; graded + for P8 in our audit.",
    notes=[("P1", "improve", "Could add one person's own reason.", "s1"),
           ("P6", "working", "Framed as what everyone is already doing.", "s2"),
           ("P4", "working", "One small step: text three friends.", "s3")],
    regions=[("s1", "Slide 1", "“The signs are everywhere.”"),
             ("s2", "Slide 2", "Voting framed as what everyone is already doing."),
             ("s3", "Slide 3", "The ask: text three friends.")],
),
"https://www.instagram.com/p/DfNuQRAti1T/": dict(
    id="diggins-50-mile-race", type="social-post", format="photo-post", venue="Jessie Diggins", platform="Instagram",
    role="Olympic cross-country skier", affil=None, authors=["Jessie Diggins"],
    topics=["clean-transport"], geo=("United States", "national"), timeliness="Evergreen", audience=["fans"],
    sponsor="Sponsored post (Toyota)",
    why="She mentions choosing a race she can reach on electric mode, which makes clean driving feel normal without preaching.",
    watch="It is a sponsored Toyota post, so say so when you share it (P7 mixed). It doesn't ask fans to do anything.",
    structure=["Personal news: a 50-mile race", "Aside: she can get there on electric mode", "No lecture"],
    step="None asked; it models a choice (reaching the race on electric mode).",
    fe="Shows a choice, not an argument.",
    notes=[("P6", "working", "Clean driving appears as an everyday choice, not a lecture.", "caption"),
           ("P7", "improve", "Sponsored by Toyota: flag it when you share.", "sponsor")],
    regions=[("sponsor", "Sponsor label", "Paid partnership label (Toyota)."),
             ("photo", "Photo", None),
             ("caption", "Caption", "Announces a 50-mile race she chose partly because she can reach it on electric mode.")],
),
"https://www.wsls.com/news/politics/2026/06/24/in-visit-to-capitol-jessie-diggins-and-other-olympians-push-for-climate-change-solutions/": dict(
    id="diggins-capitol-hill", type="news-article", format="article", venue="AP via WSLS", platform="News website",
    role="Olympic cross-country skier, with fellow athletes", affil="Protect Our Winters",
    authors=["The Associated Press"], messenger_people=["Jessie Diggins", "Jaelin Kauf", "Brody Leven"],
    topics=["winter", "policy"], geo=("Washington, DC, US", "national"), timeliness="2026 Capitol Hill visit", audience=["public", "policymakers"],
    partisan="Coverage pulls the story into a dispute over the current EPA.",
    quote="very badly",
    why="Diggins wants future kids to ski, hike and breathe clean air. The team frame and hopeful tone are strong.",
    watch="The article then pulls the story into a fight over the current EPA (P8 mixed). There's no step for readers (P4 not in play).",
    structure=["Hook: Olympians on Capitol Hill, as a team", "Personal: future kids skiing, hiking, breathing clean air", "Hope"],
    step="None for readers; the athletes' own step is meeting lawmakers.",
    fe="The athletes stay hopeful; the coverage adds the partisan angle.",
    notes=[("P5", "working", "A team of Olympians acting together.", "lede"),
           ("P1", "working", "Wants future kids to ski, hike and breathe clean air.", "quote"),
           ("P8", "improve", "The article shifts to a fight over the current EPA.", "p2")],
    regions=[("headline", "Headline", None), ("lede", "Lede", "Olympians visit Capitol Hill as a team to push for climate solutions."),
             ("quote", "Paragraph", "Diggins wants future kids to ski, hike and breathe clean air, and says she wants that “very badly.”"),
             ("p2", "Paragraph", "Later paragraphs turn to a dispute over the current EPA.")],
),
"https://outrider.org/climate-change/articles/brent-suter-new-season-same-green-goals": dict(
    id="suter-outrider-oped", type="op-ed", format="op-ed", venue="Outrider", platform="Website",
    role="MLB pitcher", affil="EcoAthletes champion", authors=["Brent Suter"],
    topics=["waste"], geo=("Milwaukee, US", "local"), timeliness="Evergreen", audience=["fans"],
    why="He talks about learning, not lecturing: a beach cleanup changed his habits, his household now composts, and his Brewers teammates cut plastic use in half. He gives fans one concrete step and praises bipartisan action.",
    watch="It dates from 2020 and is mostly about plastic waste, with climate only at the end.",
    structure=["Learning moment: a beach cleanup", "At home: the household composts", "Team: teammates cut plastic in half", "One step for fans: try composting", "Close: bipartisan action"],
    step="Try composting (he links a how-to).",
    fe="Praises bipartisan action and speaks as a learner.",
    notes=[("P7", "working", "Speaks as a learner: a beach cleanup changed his habits.", "lede"),
           ("P6", "working", "Teammates cut plastic use in half: a group norm.", "p2"),
           ("P4", "working", "One concrete step for fans: try composting, with a how-to link.", "ask"),
           ("P8", "working", "Praises bipartisan action.", "close")],
    regions=[("headline", "Headline", None), ("lede", "Opening", "A beach cleanup changed his habits."),
             ("p1", "Paragraph", "His household now composts."),
             ("p2", "Paragraph", "His Brewers teammates cut their plastic use in half."),
             ("ask", "The ask", "One step for fans: try composting, with a how-to link."),
             ("close", "Close", "He praises bipartisan action; climate appears at the end.")],
),
"https://www.instagram.com/p/DfXab0BE4Un/": dict(
    id="pow-arctic-comment", type="social-post", format="carousel", venue="Protect Our Winters", platform="Instagram",
    role="Outdoor advocacy organization", affil="Protect Our Winters (POW)", authors=["Protect Our Winters"],
    topics=["public-lands", "policy"], geo=("Arctic, Alaska, US", "regional"), timeliness="Public comment period, Nov 2026", audience=["fans"],
    why="It gives a clear action: submit a public comment.",
    watch="It centers a place, not people, and shows no one else acting (P6 weak). Fix: show people who've already commented and say why it matters to them.",
    structure=["(As published) A place", "Why the comment period matters", "Ask: submit a comment"],
    notes=[("P1", "improve", "Centers a place, not people.", "s1"),
           ("P6", "improve", "No one else is shown acting.", "s2"),
           ("P4", "working", "A clear action: submit a public comment.", "s3")],
    regions=[("s1", "Slide 1", "A wild Arctic landscape; no people shown."),
             ("s2", "Slide 2", "Why the comment period matters."),
             ("s3", "Slide 3", "The ask: submit a public comment.")],
),
"https://www.instagram.com/p/DfVhqjoE95S/": dict(
    id="pow-post-election", type="social-post", format="carousel", venue="Protect Our Winters", platform="Instagram",
    role="Outdoor advocacy organization", affil="Protect Our Winters (POW)", authors=["Protect Our Winters"],
    topics=["voting"], geo=("United States", "national"), timeliness="2026 election results", audience=["fans"],
    partisan="Reads as a partisan win; comments filled with energy and EV arguments.",
    quote="Damn. What a feeling.",
    why="It rallies supporters with real collective energy.",
    watch="It reads as a partisan win, and its comments filled with arguments about energy and EVs (P8 weak). There's no next step (P4 weak).",
    structure=["(As published) Celebration", "Win framed for one side", "No step"],
    fe="Comment section turned into an argument; flag before sharing.",
    notes=[("P5", "working", "Rallies supporters as a group.", "s1"),
           ("P8", "improve", "Reads as a partisan win.", "s2"),
           ("P4", "improve", "No next step for readers.", "comments")],
    regions=[("s1", "Slide 1", "“Damn. What a feeling.”"),
             ("s2", "Slide 2", "Celebrates election results as a win for one side."),
             ("comments", "Comments", "Comment section: arguments about energy and EVs (not reproduced).")],
),
"https://www.instagram.com/p/De7y7JpRSOm/": dict(
    id="diggins-i-voted", type="social-post", format="photo-post", venue="Jessie Diggins", platform="Instagram",
    role="Olympic cross-country skier", affil=None, authors=["Jessie Diggins"],
    topics=["voting"], geo=("United States", "national"), timeliness="2026 election", audience=["fans"],
    why="A strong personal reason to vote and an easy step.",
    watch="It leads with 11.2 million environmentalists not voting, which tells readers the behavior is rare (P6 weak). Fix: lead with her own reason, or with how many people do vote.",
    structure=["(As published) A stat about people who don't vote", "Her personal reason", "Step: vote"],
    step="Vote.",
    notes=[("P6", "improve", "Leads with 11.2 million not voting, which signals the behavior is rare.", "stat"),
           ("P1", "working", "A strong personal reason to vote.", "caption"),
           ("P4", "working", "An easy step: go vote.", "ask")],
    regions=[("photo", "Photo", None),
             ("stat", "Opening line", "Leads with a stat: 11.2 million environmentalists didn't vote."),
             ("caption", "Caption", "Her personal reason for voting."),
             ("ask", "The ask", "The step: go vote.")],
),
"https://www.tetongravity.com/pow-athletes-just-testified-before-the-senate-on-climate-change/": dict(
    id="pow-senate-testimony", type="testimony", format="testimony", venue="Teton Gravity Research", platform="Website",
    role="Pro athletes (snowboarder, ski mountaineer, climber)", affil="Protect Our Winters", authors=["Teton Gravity Research"],
    topics=["winter", "policy"], geo=("United States", "national"), timeliness="Undated (likely 2019–20)", audience=["policymakers"],
    partisan="Mentions denial and was delivered to a single-party committee.",
    quote="field report",
    why="Vivid stories: Jones watching glaciers retreat, Caldwell in the Arctic Refuge.",
    watch="The athletes present a “field report” like experts, which Principle 7 warns against. It also mentions denial and was delivered to a single-party committee (P8 weak).",
    structure=["(As published) Testimony framed as a field report", "Vivid place stories", "Denial and politics"],
    notes=[("P7", "improve", "Athletes speak as experts; P7 favors listening and learning roles.", "lede"),
           ("P1", "working", "Vivid stories: glaciers retreating, the Arctic Refuge.", "p1"),
           ("P8", "improve", "Mentions denial, to a single-party committee.", "p2")],
    regions=[("headline", "Headline", None), ("lede", "Lede", "Three athletes testify before a Senate committee, framed as a “field report.”"),
             ("p1", "Paragraph", "Jones describes watching glaciers retreat; Caldwell describes the Arctic Refuge."),
             ("p2", "Paragraph", "The testimony addresses climate denial before a single-party committee.")],
    messenger_people=["Jeremy Jones", "Caroline Gleich", "Tommy Caldwell"],
),
"https://www.tetongravity.com/caroline-gleich-on-why-winter-matters/": dict(
    id="gleich-why-winter-matters", type="profile", format="profile", venue="Teton Gravity Research", platform="Website",
    role="Pro ski mountaineer", affil=None, authors=["Teton Gravity Research"],
    topics=["winter"], geo=("United States", "national"), timeliness="Undated", audience=["fans"],
    quote="showing up and speaking out",
    why="It's upbeat about showing up and speaking out.",
    watch="There's no personal story (P1 weak) and no specific step. She later ran for the U.S. Senate as a Democrat, which may limit her reach with conservative audiences.",
    structure=["(As published) Profile intro", "Upbeat call to speak out", "No personal story or step"],
    fe="Messenger's later run for office may limit cross-party reach.",
    notes=[("P1", "improve", "No personal story.", "lede"),
           ("P3", "working", "An upbeat call to show up and speak out.", "quote"),
           ("P4", "improve", "No specific step.", "close")],
    regions=[("headline", "Headline", None), ("lede", "Lede", "A profile of a pro skier on why winter matters."),
             ("quote", "Paragraph", "An upbeat call for “showing up and speaking out.”"),
             ("close", "Close", "No personal story or specific step in the piece.")],
),
"https://www.ecoathletes.org/athletes": dict(
    id="ecoathletes-roster", type="roster", format="roster", venue="EcoAthletes", platform="Organization website",
    role="Athlete climate network", affil="EcoAthletes", authors=["EcoAthletes"],
    topics=[], geo=("US and Canada", "national"), timeliness="Current", audience=[],
    why=None,
    watch="A roster, not a message: useful for recruiting messengers, not as a library example. Not graded.",
    notes=[(None, "improve", "A list of athletes, not a message: nothing to grade yet.", "grid"),
           (None, "working", "Useful for finding and recruiting messengers.", "intro")],
    regions=[("intro", "Intro", "A short program introduction."),
             ("grid", "Roster", "A grid of athlete profiles (names and photos not reproduced).")],
),
}

PAIRS = [
    dict(id="pair-heat-dome", title="The 2021 heat dome: a speech and an op-ed",
         strong="lawson-heat-dome-speech", weak="seattle-times-heat-oped",
         lesson="Same event, same region. One patient story and one ask lands better than a list of disasters and ten asks."),
    dict(id="pair-smoke-and-heat", title="Doctors on smoke and heat: practical or partisan",
         strong="howard-wildfire-smoke", weak="vossler-psr-post",
         lesson="Both start from health. One ends with three steps for today; the other turns into a fight about the President."),
    dict(id="pair-make-it-normal", title="Making action feel normal (Principle 6)",
         strong="suter-outrider-oped", weak="diggins-i-voted",
         lesson="Suter shows teammates already changing habits. The “I voted” post leads with millions who don't vote, which makes voting sound rare."),
]

# The presentation model a per-example page (examples/<id>.html) opens first.
# Stage vs. Canvas is still undecided; change this one value when it is.
DEFAULT_MODEL = "stage"

MODELS = [
    dict(key="stage", name="Stage", long="Model A: Stage", like="like a video site"),
    dict(key="canvas", name="Canvas", long="Model B: Canvas", like="like a map app"),
    dict(key="spec", name="Requirements only", long="Model C: Requirements only", like="no borrowed metaphor"),
]

# ---------------------------------------------------------------------------
# A. Parse the audit
# ---------------------------------------------------------------------------
def parse_audit():
    md = AUDIT.read_text()
    rows = []
    segs = [("health", "## Primary segment"), ("athlete", "## Flex segment")]
    for i, (seg, head) in enumerate(segs):
        a = md.index(head)
        b = md.index(segs[i + 1][1]) if i + 1 < len(segs) else md.index("## Patterns")
        sec = md[a:b]
        for line in sec.splitlines():
            if not re.match(r"^\| \[", line):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            m = re.match(r"\[([^\]]+)\]\(([^)]+)\)\s*(?:\((.+)\))?$", cells[0])
            title, url, venue_hint = m.group(1), m.group(2), m.group(3)
            grades = [c.replace("\\~", "~").strip() for c in cells[4:12]]
            rows.append(dict(segment=seg, title=title.strip(), raw_title=title, url=url,
                             venue_hint=venue_hint, content_type_audit=cells[1],
                             messenger=cells[2], date=cells[3], grades=grades, verdict=cells[12]))
    return rows

MONTHS = {m: i + 1 for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())}

def iso_date(d):
    m = re.match(r"([A-Z][a-z]{2})\s+(\d{1,2}),\s+(\d{4})$", d)
    if m:
        return f"{m.group(3)}-{MONTHS[m.group(1)]:02d}-{int(m.group(2)):02d}"
    m = re.match(r"([A-Z][a-z]{2})\s+(\d{4})$", d)
    if m:
        return f"{m.group(2)}-{MONTHS[m.group(1)]:02d}"
    return None

def recency(rec):
    iso = rec["published_iso"]
    if not iso:
        return "Undated" if rec["published_date"] != "Current" else "Current page"
    year = int(iso[:4])
    return f"{year}" if year >= 2026 else f"Evergreen · {year}"

def clean_title(t):
    t = t.replace("\\~", "~")
    t = re.sub(r'"([^"]*)"', "“\\1”", t)
    return t.replace("'", "’")

def build_records():
    rows = parse_audit()
    recs = []
    for r in rows:
        c = CURATION[r["url"]]
        grades = {p: g for (p, _), g in zip(PRIN, r["grades"])}
        not_graded = all(g == "" for g in r["grades"])
        people = c.get("messenger_people")
        messenger_name = r["messenger"]
        if r["messenger"].startswith("Dr. ") is False and r["segment"] == "health" and c["id"] in ("howard-wildfire-smoke", "merritt-climate-diagnosis", "dresser-climate-patient-care", "vossler-psr-post"):
            # The audit names these four as "Dr." in its messengers list.
            messenger_name = {"howard-wildfire-smoke": "Dr. Courtney Howard", "merritt-climate-diagnosis": "Dr. Kyle Merritt",
                              "dresser-climate-patient-care": "Dr. Caleb Dresser", "vossler-psr-post": "Dr. Mark Vossler"}[c["id"]]
        notes = []
        for i, (p, kind, text, region) in enumerate(c["notes"], 1):
            notes.append(dict(n=i, principle=p, principle_name=PNAME.get(p, "Overall"),
                              type="working" if kind == "working" else "could improve", note=text, anchor=region))
        rec = dict(
            id=c["id"], title=clean_title(r["title"]), source_url=r["url"], venue=c["venue"], platform=c["platform"],
            published_date=r["date"], published_iso=iso_date(r["date"]),
            content_type=TYPES[c["type"]], content_type_slug=c["type"], content_type_audit=r["content_type_audit"],
            standin_format=c["format"], language="en",
            full_text_md=None, renders=None,
            media=c.get("media"), sponsorship=c.get("sponsor"), rights_status="link-only",
            intake_date=AUDIT_DATE, update_log=[dict(date="2026-11-11", author="Prototype generator", reason="Record created from the Nov 6, 2026 audit for prototyping")],
            provenance="Curator: TCC segment audit (Nov 6, 2026)",
            authors=c.get("authors"), messenger_name=messenger_name, messenger_people=people,
            messenger_role=c.get("role"), messenger_affiliation=c.get("affil"),
            messenger_avatar=dict(kind="initial", initial=initial(messenger_name)),
            communicator_segment=r["segment"], communicator_segment_label=SEGMENTS[r["segment"]],
            audience_segment=c.get("audience") or None,
            topics=c["topics"], topic_labels=[TOPICS[t] for t in c["topics"]],
            geography=dict(place=c["geo"][0], scope=c["geo"][1]),
            timeliness=c.get("timeliness"), partisan_framing=c.get("partisan"),
            taxonomy_version=TAXONOMY,
            principle_grades=None if not_graded else grades,
            grading_analysis=notes,
            verdict=r["verdict"], verdict_slug=VERDICT_SLUG[r["verdict"]],
            why_it_works=c.get("why"), what_to_watch=c.get("watch"),
            contrast_pair_id=None, contrast_role=None,
            grade_provenance=dict(graded_by="TCC Design Research", method="human, first-pass screen", date=AUDIT_DATE, rubric=RUBRIC),
            structure=c.get("structure"), doable_step=c.get("step"), for_everyone_notes=c.get("fe"),
            short_quote=c.get("quote"), model_payload=None,
            institutional_backing=c.get("institution"), sources_cited=None,
            reviewed_by=None, reviewed_date=None,
            engagement_snapshots=c.get("engagement"), amplify_candidate=c.get("amplify"),
            tcc_amplified=None, derived_from=None, contributed_by=None,
            standin_regions=[dict(key=k, label=l, text=t) for k, l, t in c["regions"]],
            prototype_curation=True,
            prototype_curation_fields=["structure", "doable_step", "topics", "geography", "timeliness", "audience_segment", "grading_analysis", "standin_regions", "for_everyone_notes"],
        )
        recs.append(rec)
    by = {r["id"]: r for r in recs}
    for p in PAIRS:
        by[p["strong"]]["contrast_pair_id"] = p["id"]; by[p["strong"]]["contrast_role"] = "strong"
        by[p["weak"]]["contrast_pair_id"] = p["id"]; by[p["weak"]]["contrast_role"] = "learning case"
    for r in recs:
        if r["verdict"] == "Good example":
            r["model_payload"] = dict(
                messenger_role=r["messenger_role"], audience=r["audience_segment"],
                structure=r["structure"], doable_step=r["doable_step"], why_it_works=r["why_it_works"],
                principle_grades=r["principle_grades"],
                analysis=[f'{n["principle"]} {n["type"]}: {n["note"]}' for n in r["grading_analysis"]],
                for_everyone_notes=r["for_everyone_notes"],
                excerpt=r["short_quote"], rights_status=r["rights_status"],
                instruction="Imitate the structure and tone of this example, not its wording. Keep the user's own voice.",
            )
    return recs, by

def initial(name):
    n = re.sub(r"^(Dr\.|Unnamed)\s+", "", name).strip()
    return (n[:1] or "?").upper()

# ---------------------------------------------------------------------------
# B. HTML helpers
# ---------------------------------------------------------------------------
def e(s):
    return html.escape(s if s is not None else "", quote=True)

NEWTAB = '<span class="sr-only"> (opens in a new tab)</span>'
ICON_V = {
    "good": '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l5 5L20 7"/></svg>',
    "soso": '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" aria-hidden="true"><path d="M5 12h14"/></svg>',
    "not": '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" aria-hidden="true"><circle cx="12" cy="12" r="7"/></svg>',
}
AV_BG = ["#F0E0B0", "#DDE4F6", "#E1F4FB", "#F2E0CE", "#ECCFAF"]

def verdict_badge(rec):
    v = rec["verdict_slug"]
    return f'<span class="verdict v-{v}">{ICON_V[v]}{e(rec["verdict"])}</span>'

def avatar(rec, size=44):
    bg = AV_BG[sum(map(ord, rec["id"])) % len(AV_BG)]
    i = e(rec["messenger_avatar"]["initial"])
    return (f'<svg class="ce-av" width="{size}" height="{size}" viewBox="0 0 44 44" aria-hidden="true">'
            f'<circle cx="22" cy="22" r="22" fill="{bg}"/><text x="22" y="29" text-anchor="middle" '
            f'font-family="Nunito, sans-serif" font-weight="900" font-size="20" fill="#1B2D5B">{i}</text></svg>')

def grades_row(rec, compact=False):
    g = rec["principle_grades"]
    if not g:
        return '<p class="ce-grades-none small">Not graded: too thin to grade (verdict “Not yet usable”).</p>'
    items = []
    for p, name in PRIN:
        sym = g[p]
        label, shown = GRADE[sym]
        cls = {"strong": "g-strong", "mixed": "g-mixed", "weak": "g-weak"}.get(label, "g-na")
        items.append(f'<li class="g {cls}"><abbr title="{name}">{p}</abbr><span class="gs" aria-hidden="true">{shown}</span>'
                     f'<span class="sr-only">{name}: {label}</span></li>')
    return f'<ul class="ce-grades{" ce-grades--compact" if compact else ""}" aria-label="Principle grades">{"".join(items)}</ul>'

def messenger_strip(rec, h="p"):
    people = rec.get("messenger_people")
    extra = f'<span class="ce-ms-people">With {e(", ".join(people))}</span>' if people else ""
    role = rec["messenger_role"] or "Role not in the audit"
    aff = f' · {e(rec["messenger_affiliation"])}' if rec["messenger_affiliation"] else ""
    return (f'<div class="ce-ms" data-part="1">{avatar(rec)}<div class="ce-ms-text">'
            f'<{h} class="ce-ms-name">{e(rec["messenger_name"])}</{h}>'
            f'<span class="ce-ms-role">{e(role)}{aff}</span>{extra}</div></div>')

def fit_tags(rec):
    tags = [f'<li class="tag">{e(t)}</li>' for t in rec["topic_labels"]]
    tags.append(f'<li class="tag tag--place">{e(rec["geography"]["place"])}</li>')
    tags.append(f'<li class="tag tag--time">{e(recency(rec))}</li>')
    tags.append(f'<li class="tag tag--type">{e(rec["content_type"])}</li>')
    flags = []
    if rec["sponsorship"]:
        flags.append(f'<li class="tag tag--flag"><span aria-hidden="true">$</span> {e(rec["sponsorship"])}</li>')
    if rec["partisan_framing"]:
        flags.append('<li class="tag tag--flag"><span aria-hidden="true">!</span> Partisan framing</li>')
    return f'<ul class="ce-tags" data-part="2" aria-label="Fit tags">{"".join(tags + flags)}</ul>'

def draft_label():
    return '<p class="ce-draft"><span aria-hidden="true">✎</span> Draft curation for prototyping: pattern, step, topics, place and notes are derived from the audit text, not a full read of the original.</p>'

SK = ["w1", "w2", "w3", "w4", "w5"]
def skel(n, seed=0):
    return '<div class="sk" aria-hidden="true">' + "".join(f'<span class="{SK[(i + seed) % 5]}"></span>' for i in range(n)) + "</div>"

def pins_for(rec, key):
    out = []
    for n in rec["grading_analysis"]:
        if n["anchor"] == key:
            sym = "✓" if n["type"] == "working" else "↗"
            out.append(f'<a class="pin pin--{"ok" if n["type"] == "working" else "fix"}" id="pin-{rec["id"]}-{n["n"]}" '
                       f'href="#note-{rec["id"]}-{n["n"]}" data-note="note-{rec["id"]}-{n["n"]}" '
                       f'aria-label="Note {n["n"]}: {e(n["principle_name"])}, {e(n["type"])}">'
                       f'<span aria-hidden="true">{n["n"]}</span></a>')
    return f'<span class="pins">{"".join(out)}</span>' if out else ""

def region(rec, key, inner, cls="", tag="div"):
    has = any(n["anchor"] == key for n in rec["grading_analysis"])
    return (f'<{tag} class="rg {cls}" id="rg-{rec["id"]}-{key}"{" data-pinned" if has else ""}>'
            f'{pins_for(rec, key)}{inner}</{tag}>')

def reg(rec, key):
    for r in rec["standin_regions"]:
        if r["key"] == key:
            return r
    return None

def para(rec, key, cls="si-p"):
    r = reg(rec, key)
    if not r:
        return ""
    return region(rec, key, f'<p class="{cls}"><span class="si-lab">{e(r["label"])}</span>{e(r["text"])}</p>')

def fmt_dur(s):
    return f"{s // 60}:{s % 60:02d}"

def video_facade(rec, vertical=False):
    m = rec["media"]
    return (f'<div class="si-video{" si-video--v" if vertical else ""}" data-yt="{e(m["embed_id"])}" data-yt-title="{e(rec["title"])}">'
            f'<div class="si-video-inner"><p class="si-video-title">{e(rec["title"])}</p>'
            f'<p class="si-video-meta">{fmt_dur(m["duration_s"])} · {e(m["approx_mb"])}</p>'
            f'<a class="btn btn-primary si-video-load" href="{e(m["url"])}" target="_blank" rel="noopener" data-yt-load>'
            f'<span aria-hidden="true">▶</span> Load video from YouTube{NEWTAB}</a>'
            f'<p class="si-video-note">Loading contacts YouTube (youtube-nocookie.com). Nothing loads until you ask. No autoplay.</p></div></div>')

def standin_alt(rec):
    kind = {"article": "news article page", "tv-story": "TV news web story", "op-ed": "opinion page",
            "blog": "blog post", "release": "news release", "photo-post": "social photo post",
            "carousel": "three-slide social carousel", "short-video": "short vertical video",
            "long-video": "video with chapter timeline", "testimony": "testimony news recap",
            "profile": "profile article", "roster": "roster web page"}[rec["standin_format"]]
    parts = "; ".join(r["text"] for r in rec["standin_regions"] if r["text"])
    return f'Illustration of a {kind} from {rec["venue"]}, titled “{rec["title"]}”. TCC paraphrase of its parts: {parts}'

def standin(rec):
    """Draw the original as an HTML/CSS stand-in. Returns <figure>."""
    f = rec["standin_format"]
    rid = rec["id"]
    date = e(rec["published_date"])
    byline = e(", ".join(rec["authors"] or []))
    body = ""
    if f in ("article", "tv-story", "op-ed", "blog", "release", "testimony", "profile"):
        kicker = {"article": "News", "tv-story": "Local TV news", "op-ed": "Opinion", "blog": "Blog",
                  "release": "News release", "testimony": "News · Testimony recap", "profile": "Profile"}[f]
        h = region(rec, "headline", f'<p class="si-kicker">{kicker}</p><p class="si-h">{e(rec["title"])}</p>', tag="header")
        meta = f'<p class="si-meta">{byline} · {date}</p>'
        seq = [k["key"] for k in rec["standin_regions"] if k["key"] != "headline"]
        chunks = []
        for i, k in enumerate(seq):
            if k == "clip":
                chunks.append(region(rec, "clip", f'<div class="si-clip"><span aria-hidden="true">▶</span> {e(reg(rec, "clip")["text"])}</div>'))
                continue
            chunks.append(para(rec, k, "si-p si-p--lede" if i == 0 else "si-p"))
            chunks.append(skel(6 if f in ("op-ed", "release", "blog", "testimony") else 4, i))
        author_box = ""
        if f == "op-ed":
            author_box = f'<div class="si-authorbox"><span class="si-lab">About the authors</span>{byline}{(" · " + e(rec["messenger_affiliation"])) if rec["messenger_affiliation"] else ""}</div>'
        body = (f'<div class="si-browser"><span class="si-dots" aria-hidden="true"><i></i><i></i><i></i></span>'
                f'<span class="si-url">{e(rec["venue"])}</span></div>'
                f'<div class="si-page si-page--{f}">{h}{meta}{"".join(chunks)}{author_box}</div>')
    elif f in ("photo-post", "carousel"):
        sponsor = ""
        if reg(rec, "sponsor"):
            sponsor = region(rec, "sponsor", f'<span class="si-sponsor">{e(reg(rec, "sponsor")["text"])}</span>')
        head = (f'<div class="si-sohead">{avatar(rec, 32)}<span><b>{e(rec["venue"])}</b><small>{date}</small></span></div>{sponsor}')
        if f == "photo-post":
            photo = region(rec, "photo", '<div class="si-photo"><span>Photo not reproduced</span></div>') if reg(rec, "photo") else ""
            rest = "".join(para(rec, k, "si-cap") for k in [r["key"] for r in rec["standin_regions"]] if k not in ("photo", "sponsor"))
            body = f'<div class="si-phone">{head}{photo}<div class="si-capwrap">{rest}</div></div>'
        else:
            slides = [r for r in rec["standin_regions"] if r["key"].startswith("s")]
            sl = "".join(region(rec, r["key"], f'<div class="si-slide"><span class="si-lab">{e(r["label"])}</span><p>{e(r["text"])}</p></div>', cls="si-slidewrap") for r in slides)
            others = "".join(para(rec, r["key"], "si-cap") for r in rec["standin_regions"] if not r["key"].startswith("s"))
            dots = "".join("<i></i>" for _ in slides)
            body = (f'<div class="si-phone">{head}<div class="si-slides">{sl}</div><div class="si-cdots" aria-hidden="true">{dots}</div>'
                    f'<div class="si-capwrap"><p class="si-cap si-cap--muted">Caption not reproduced.</p>{others}</div></div>')
    elif f in ("short-video", "long-video"):
        vert = f == "short-video"
        chapters = "".join(region(rec, r["key"], f'<div class="si-chap"><span class="si-lab">{e(r["label"])}</span>{e(r["text"])}</div>', cls="si-chapwrap") for r in rec["standin_regions"])
        body = (f'<div class="si-vid{" si-vid--v" if vert else ""}">{video_facade(rec, vert)}'
                f'<div class="si-timeline" role="group" aria-label="Order of moves in the video"><p class="si-tl-note">Order of moves (TCC paraphrase). Timestamps not yet captured.</p>'
                f'<div class="si-chaps">{chapters}</div></div></div>')
    elif f == "roster":
        tiles = "".join('<span class="si-tile" aria-hidden="true"><i></i><b></b></span>' for _ in range(8))
        intro = region(rec, "intro", '<p class="si-h">' + e(rec["title"]) + '</p>' + skel(2))
        grid = region(rec, "grid", '<p class="si-p"><span class="si-lab">Roster</span>' + e(reg(rec, "grid")["text"]) + '</p><div class="si-tiles">' + tiles + '</div>')
        body = (f'<div class="si-browser"><span class="si-dots" aria-hidden="true"><i></i><i></i><i></i></span><span class="si-url">{e(rec["venue"])}</span></div>'
                f'<div class="si-page si-page--roster">{intro}{grid}</div>')
    return (f'<figure class="si si--{f}" id="si-{rid}" aria-describedby="si-alt-{rid}">'
            f'<figcaption class="si-cap-top">Illustration of the original. <a href="{e(rec["source_url"])}" target="_blank" rel="noopener">View it at {e(rec["venue"])} <span aria-hidden="true">↗</span>{NEWTAB}</a>'
            f'<span class="si-cap-sub">Text is TCC’s paraphrase, not the original wording.</span></figcaption>'
            f'<p class="sr-only" id="si-alt-{rid}">{e(standin_alt(rec))}</p>'
            f'<div class="si-body">{body}</div></figure>')

def notes_list(rec, heading="h3"):
    items = []
    for n in rec["grading_analysis"]:
        ok = n["type"] == "working"
        sym = "✓" if ok else "↗"
        p = f'{n["principle"]} {n["principle_name"]}' if n["principle"] else "Overall"
        items.append(f'<li class="ce-note ce-note--{"ok" if ok else "fix"}" id="note-{rec["id"]}-{n["n"]}">'
                     f'<span class="ce-note-n" aria-hidden="true">{n["n"]}</span>'
                     f'<div><p class="ce-note-h"><span class="ce-note-kind"><span aria-hidden="true">{sym}</span> {"Working" if ok else "Could improve"}</span> · {e(p)}</p>'
                     f'<p class="ce-note-t">{e(n["note"])}</p>'
                     f'<a class="ce-note-jump" href="#rg-{rec["id"]}-{n["anchor"]}">Show in the content<span class="sr-only"> (note {n["n"]})</span></a></div></li>')
    return (f'<div class="ce-notes" data-notes="{rec["id"]}"><{heading} class="ce-sub">Notes on the content</{heading}>'
            f'<ol class="ce-notelist">{"".join(items)}</ol></div>')

def overlay_toggle(rec_or_id):
    i = rec_or_id if isinstance(rec_or_id, str) else rec_or_id["id"]
    return (f'<label class="ce-ov"><input type="checkbox" class="ov-toggle" id="ov-{i}" data-ov>'
            f'<span class="ce-ov-sw" aria-hidden="true"></span><span><span class="nar-sr">Show </span>why it works</span></label>')

def why_section(rec, h="h2", with_notes=True):
    if rec["verdict_slug"] == "not":
        body = f'<p>{e(rec["what_to_watch"])}</p>'
    else:
        watch_label = "What to watch (learning case)" if rec["verdict_slug"] == "soso" else "What to watch"
        body = (f'<p class="ce-why">{e(rec["why_it_works"])}</p>' +
                (f'<div class="ce-watch"><p class="ce-sub2">{watch_label}</p><p>{e(rec["what_to_watch"])}</p></div>' if rec["what_to_watch"] else ""))
    head = "Why it works" if rec["verdict_slug"] == "good" else ("What works, and what to fix" if rec["verdict_slug"] == "soso" else "Why it isn’t in the library")
    return (f'<section class="ce-part ce-part--why" data-part="4" aria-labelledby="why-{rec["id"]}">'
            f'<{h} id="why-{rec["id"]}">{head}</{h}><div class="ce-verdictline">{verdict_badge(rec)}</div>{grades_row(rec)}{body}'
            f'{notes_list(rec) if with_notes else ""}</section>')

def pattern_section(rec, h="h2"):
    if rec["verdict_slug"] == "good":
        st = "".join(f"<li>{e(s)}</li>" for s in rec["structure"] or [])
        inner = (f'<p class="ce-sub2">Structure</p><ol class="ce-structure">{st}</ol>'
                 f'<p class="ce-sub2">The one doable step</p><p class="ce-step">{e(rec["doable_step"])}</p>')
        if rec["for_everyone_notes"]:
            inner += f'<p class="ce-sub2">How it stays for everyone</p><p>{e(rec["for_everyone_notes"])}</p>'
    elif rec["verdict_slug"] == "soso":
        st = "".join(f"<li>{e(s)}</li>" for s in rec["structure"] or [])
        inner = (f'<p>This is a learning case, so there’s no pattern to borrow as is. Its structure as published:</p>'
                 f'<ol class="ce-structure ce-structure--asis">{st}</ol>')
        if rec["for_everyone_notes"]:
            inner += f'<p class="ce-sub2">For-everyone note</p><p>{e(rec["for_everyone_notes"])}</p>'
    else:
        inner = "<p>No pattern: this is a roster, not a message.</p>"
    return (f'<section class="ce-part ce-part--pattern" data-part="5" data-layer="pattern" aria-labelledby="pat-{rec["id"]}">'
            f'<{h} id="pat-{rec["id"]}">Reusable pattern</{h}>{inner}{draft_label()}</section>')

def trust_section(rec, h="h2"):
    bits = [f'<li><b>Source:</b> <a href="{e(rec["source_url"])}" target="_blank" rel="noopener">{e(rec["venue"])} <span aria-hidden="true">↗</span>{NEWTAB}</a> · {e(rec["platform"])} · {e(rec["published_date"])}</li>']
    if rec["institutional_backing"]:
        bits.append(f'<li><b>Institution:</b> {e(rec["institutional_backing"])}</li>')
    else:
        bits.append('<li><b>Institution:</b> <span class="ce-gap">Not recorded</span></li>')
    bits.append(f'<li><b>Sponsorship:</b> {e(rec["sponsorship"]) if rec["sponsorship"] else "None noted in the audit"}</li>')
    if rec["partisan_framing"]:
        bits.append(f'<li><b>Partisan framing:</b> {e(rec["partisan_framing"])}</li>')
    bits.append(f'<li><b>Graded:</b> TCC segment audit, Nov 6, 2026 (first-pass screen, human). <span class="ce-gap">Not yet reviewed by a clinician.</span></li>')
    bits.append('<li><b>Sources cited in the piece:</b> <span class="ce-gap">Not recorded</span></li>')
    return (f'<section class="ce-part ce-part--trust" data-part="6" data-layer="trust" aria-labelledby="tr-{rec["id"]}">'
            f'<{h} id="tr-{rec["id"]}">Trust line</{h}><ul class="ce-trust">{"".join(bits)}</ul>'
            f'<p class="small muted">TCC curated, not TCC endorsed. Rights: link-only, so the original isn’t reproduced here.</p></section>')

def payload_text(rec):
    return json.dumps(rec["model_payload"], indent=2, ensure_ascii=False)

def actions_section(rec, h="h2", print_label=None):
    acts = [f'<a class="btn btn-primary" href="{e(rec["source_url"])}" target="_blank" rel="noopener">View original <span aria-hidden="true">↗</span>{NEWTAB}</a>']
    model = ""
    if rec["model_payload"]:
        size = len(payload_text(rec).encode())
        model = (f'<details class="ce-model" id="use-{rec["id"]}"><summary class="btn btn-ghost">Use as a model</summary>'
                 f'<p class="small">Copy this into your AI chatbot as a model. It tells the chatbot to borrow structure and tone, not wording. '
                 f'<span class="muted">Plain text, JSON, {size:,} bytes.</span></p>'
                 f'<pre class="ce-payload" tabindex="0"><code>{e(payload_text(rec))}</code></pre>'
                 f'<button type="button" class="btn btn-ghost ce-copy" data-copy="use-{rec["id"]}" hidden>Copy</button></details>')
    elif rec["verdict_slug"] == "soso":
        acts.append(f'<a class="btn btn-ghost" href="#why-{rec["id"]}">See what to fix</a>')
    acts.append('<span class="btn btn-ghost is-off" aria-disabled="true">Save <small>(not in prototype)</small></span>')
    acts.append(f'<button type="button" class="btn btn-ghost" data-print hidden>{print_label or "Print or save as PDF"}</button>')
    return (f'<section class="ce-part ce-part--actions" data-part="7" aria-labelledby="ac-{rec["id"]}">'
            f'<{h} id="ac-{rec["id"]}" class="sr-only">Actions</{h}><div class="ce-actions">{"".join(acts)}</div>{model}</section>')

def connection_section(rec, h="h2"):
    eng = ""
    if rec["engagement_snapshots"]:
        s = rec["engagement_snapshots"][0]
        eng = f' Reach in our audit: {s["views"]} views, so it\'s a candidate for TCC to reshare.'
    return (f'<section class="ce-part ce-part--conn" data-part="8" aria-labelledby="cn-{rec["id"]}"><{h} id="cn-{rec["id"]}" class="sr-only">Connection</{h}>'
            f'<p class="ce-conn"><span aria-hidden="true">◎</span> Made with this example: <span class="ce-gap">no data yet</span>. '
            f'Reshared by TCC: <span class="ce-gap">not yet</span>.{e(eng)}</p></section>')

def jsonld(rec):
    authors = rec["authors"] or [rec["messenger_name"]]
    people = {"Brent Suter", "Mark Vossler", "Breck Lebegue", "Chris Covert-Bowlds", "Michael Soman", "Jessie Diggins"}
    data = {
        "@context": "https://schema.org", "@type": "CreativeWork", "name": rec["title"], "url": rec["source_url"],
        "author": [{"@type": "Person" if a in people else "Organization", "name": a} for a in authors],
        "publisher": {"@type": "Organization", "name": rec["venue"]},
        "inLanguage": "en", "genre": rec["content_type"],
    }
    if rec["published_iso"]:
        data["datePublished"] = rec["published_iso"]
    if rec["messenger_name"] not in authors:
        data["contributor"] = {"@type": "Person" if rec["messenger_name"].startswith("Dr.") or rec["messenger_name"] in people else "Organization", "name": rec["messenger_name"]}
    if rec["topic_labels"]:
        data["keywords"] = ", ".join(rec["topic_labels"])
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'

# ---------------------------------------------------------------------------
# Page shell
# ---------------------------------------------------------------------------
def page(title, body, model=None, depth=1, css=(), js=True, head_extra="", body_class=""):
    links = f'<link rel="stylesheet" href="{"shared/" if depth == 0 else "../shared/"}ce-core.css">' + "".join(f'<link rel="stylesheet" href="{c}">' for c in css)
    script = f'<script src="{"shared/" if depth == 0 else "../shared/"}ce-enhance.js" defer></script>' if js else ""
    compare = "index.html" if depth == 0 else "../index.html"
    site_root = "../" * (depth + 2)  # prototypes/content-example/ is two levels down
    trail = '<span class="tcc-banner__kind">Prototype</span><span>Content Example</span>'
    if model:
        trail += f'<span>{e(model["name"])}</span>'
        links_html = f'<a class="tcc-banner__back" href="{compare}">← Compare models</a>'
    else:
        trail += '<span>Compare models</span>'
        links_html = ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="robots" content="noindex">
<meta name="color-scheme" content="light dark">
<script>document.documentElement.classList.add('js')</script>
{links}
{head_extra}
{script}
</head>
<body class="{body_class}">
<a class="skip" href="#main">Skip to content</a>
<nav class="tcc-banner" aria-label="Where you are">
  <div class="tcc-banner__inner">
    <p class="tcc-banner__trail">{trail}</p>
    <p class="tcc-banner__links">{links_html}</p>
  </div>
</nav>
{body}
<!-- Overnote review layer, loaded only with ?review=1. See js/annotate.js. -->
<script type="module" src="{site_root}js/annotate.js"></script>
</body>
</html>
"""

# ---------------------------------------------------------------------------
# Library (shared markup, model CSS differs)
# ---------------------------------------------------------------------------
def related(rec, recs, n=4):
    pool = [r for r in recs if r["id"] != rec["id"] and r["verdict_slug"] == "good"]
    def score(r):
        s = 0
        s += 3 * len(set(r["topics"]) & set(rec["topics"]))
        s += 2 if r["communicator_segment"] == rec["communicator_segment"] else 0
        s += 1 if r["content_type_slug"] == rec["content_type_slug"] else 0
        return -s
    return sorted(pool, key=score)[:n]

def card(rec, view, model):
    one = rec["short_quote"] and rec["verdict_slug"] == "good" and f'“{rec["short_quote"]}”' or (rec["why_it_works"] or rec["what_to_watch"] or "")
    one = one.split(". ")[0].rstrip(".") + ("." if not one.endswith("”") else "")
    flags = []
    if rec["sponsorship"]:
        flags.append('<span class="flag"><span aria-hidden="true">$</span> Sponsored</span>')
    if rec["partisan_framing"]:
        flags.append('<span class="flag"><span aria-hidden="true">!</span> Partisan framing</span>')
    text = " ".join([rec["title"], rec["messenger_name"], rec["venue"], rec["content_type"], " ".join(rec["topic_labels"]), rec["geography"]["place"]]).lower()
    thumb = f'<div class="thumb thumb--{rec["standin_format"]}" aria-hidden="true"><span>{e(rec["content_type"])}</span></div>'
    if rec["media"]:
        thumb = thumb.replace("</span></div>", f'</span><b>{fmt_dur(rec["media"]["duration_s"])}</b></div>')
    return (f'<li class="card" data-segment="{rec["communicator_segment"]}" data-type="{rec["content_type_slug"]}" '
            f'data-verdict="{rec["verdict_slug"]}" data-topic="{" ".join(rec["topics"]) or "none"}" data-text="{e(text)}">'
            f'{thumb}<div class="card-body">'
            f'<h3 class="card-h"><a href="{rec["id"]}.html">{e(rec["title"])}</a></h3>'
            f'<div class="card-ms">{avatar(rec, 28)}<span>{e(rec["messenger_name"])}<small>{e(rec["messenger_role"] or "")}</small></span></div>'
            f'<p class="card-one">{e(one)}</p>'
            f'<div class="card-meta">{verdict_badge(rec)}<span class="tag tag--type">{e(rec["content_type"])}</span><span class="tag tag--time">{e(recency(rec))}</span>{"".join(flags)}</div>'
            f'{grades_row(rec, compact=True)}'
            f'<p class="card-trust">{e(rec["venue"])} · {e(rec["geography"]["place"])}</p></div></li>')

def pair_card(p, by):
    s, w = by[p["strong"]], by[p["weak"]]
    segs = " ".join(sorted({s["communicator_segment"], w["communicator_segment"]}))
    types = " ".join(sorted({s["content_type_slug"], w["content_type_slug"]}))
    topics = " ".join(sorted(set(s["topics"]) | set(w["topics"]))) or "none"
    text = " ".join([p["title"], s["title"], w["title"], s["messenger_name"], w["messenger_name"]]).lower()
    return (f'<li class="card card--pair" data-segment="{segs}" data-type="{types}" data-verdict="good soso" data-topic="{topics}" data-text="{e(text)}">'
            f'<div class="thumb thumb--pair" aria-hidden="true"><span>Contrast pair</span></div><div class="card-body">'
            f'<h3 class="card-h"><a href="{p["id"]}.html">{e(p["title"])}</a></h3>'
            f'<p class="card-pair"><span>{verdict_badge(s)} {e(s["messenger_name"])}, {e(s["content_type"].lower())}</span>'
            f'<span><span class="verdict v-soso">{ICON_V["soso"]}Learning case</span> {e(w["messenger_name"])}, {e(w["content_type"].lower())}</span></p>'
            f'<p class="card-one">{e(p["lesson"])}</p></div></li>')

def filter_form(recs, view):
    present = recs
    def group(name, legend, opts):
        o = [f'<label><input type="radio" name="{name}" value="" checked> All</label>']
        o += [f'<label><input type="radio" name="{name}" value="{k}"> {e(v)}</label>' for k, v in opts]
        return f'<fieldset class="fg"><legend>{legend}</legend><div class="fg-opts">{"".join(o)}</div></fieldset>'
    segs = [(k, v) for k, v in SEGMENTS.items()]
    types = [(k, v) for k, v in TYPES.items() if any(r["content_type_slug"] == k for r in present)]
    verds = [(VERDICT_SLUG[v], v) for v in ["Good example", "So-so", "Not yet usable"] if any(r["verdict"] == v for r in present)]
    tops = [(k, v) for k, v in TOPICS.items() if any(k in r["topics"] for r in present)]
    return (f'<form class="filters" method="get" action="" role="search" aria-label="Filter examples">'
            f'<div class="fsearch js-only"><label for="q">Search</label><input type="search" id="q" name="q" placeholder="Name, topic, place" autocomplete="off"></div>'
            f'{group("segment", "Segment", segs)}{group("type", "Content type", types)}{group("verdict", "Verdict", verds)}{group("topic", "Topic", tops)}'
            f'<p class="fstatus" aria-live="polite" data-fstatus></p>'
            f'<div class="fempty" data-fempty hidden><p><b>No examples match.</b> Try a nearby topic, or clear a filter.</p>'
            f'<p><a href="?">Clear all filters</a> · <span class="muted">Request an example (not in prototype)</span></p></div>'
            f'<noscript><p class="small muted">Filters apply as you choose them, in current browsers.</p></noscript></form>')

def filter_css(recs):
    """CSS :has() rules so filters work without JavaScript."""
    rules = []
    for name, vals in (("segment", SEGMENTS), ("type", TYPES), ("verdict", {"good": 1, "soso": 1, "not": 1}), ("topic", TOPICS)):
        for k in vals:
            rules.append(f'.lib:has(input[name="{name}"][value="{k}"]:checked) .card:not([data-{name}~="{k}"]){{display:none}}')
    return "<style>" + "\n".join(rules) + "</style>"

def view_switch(view):
    a = 'aria-current="page"'
    return (f'<nav class="viewswitch" aria-label="View"><a href="index.html" {a if view == "messenger" else ""}>Messenger view</a>'
            f'<a href="curator.html" {a if view == "curator" else ""}>Curator view</a></nav>')

def view_note(view):
    if view == "messenger":
        return ('<p class="small muted viewnote">Messenger view applies rules R2 and R3: only Good examples appear on their own. '
                'So-so examples appear only inside a contrast pair. Not-yet-usable examples are hidden.</p>')
    return '<p class="small muted viewnote">Curator view shows all 18 audit examples with their verdicts, so every content type can be tested.</p>'

def library(model, recs, by, view):
    shown = recs if view == "curator" else [r for r in recs if r["verdict_slug"] == "good"]
    pairs = "".join(pair_card(p, by) for p in PAIRS)
    cards = "".join(card(r, view, model) for r in shown)
    title = "Content Example library"
    intro = f'<p class="lib-intro">Real climate communication from health professionals and athletes, graded against the <i>Eight Principles for Effective and Inviting Climate Communication</i>.</p>'
    mk = model["key"]
    if mk == "canvas":
        body = canvas_library(model, recs, by, view, shown, pairs, cards, intro)
    else:
        body = (f'<main id="main" class="lib lib--{mk} wrap">'
                f'<header class="lib-head"><p class="eyebrow">{e(model["long"])} · {"Messenger" if view == "messenger" else "Curator"} view</p>'
                f'<h1>{title}</h1>{intro}{view_switch(view)}{view_note(view)}</header>'
                f'{filter_form(shown, view)}'
                f'<section aria-labelledby="pairs-h"><h2 id="pairs-h" class="lib-h2">Contrast pairs</h2><ul class="cards cards--pairs" data-cards>{pairs}</ul></section>'
                f'<section aria-labelledby="ex-h"><h2 id="ex-h" class="lib-h2">Examples <span class="muted lib-count">({len(shown)})</span></h2><ul class="cards" data-cards>{cards}</ul></section>'
                f'</main>')
    return page(f"{title} · {model['name']} · {'Messenger' if view == 'messenger' else 'Curator'} view", body, model,
                css=[f"{mk}.css"], head_extra=filter_css(recs), js=True, body_class=f"m-{mk} p-lib")

def canvas_library(model, recs, by, view, shown, pairs, cards, intro):
    # Board: clusters by segment, placed on a pannable canvas.
    cl = []
    for seg, label in SEGMENTS.items():
        cs = "".join(card(r, view, model) for r in shown if r["communicator_segment"] == seg)
        cl.append(f'<section class="cluster" aria-labelledby="cl-{seg}"><h2 id="cl-{seg}" class="cluster-h">{e(label)}</h2><ul class="cards" data-cards>{cs}</ul></section>')
    board = (f'<div class="board"><section class="cluster cluster--pairs" aria-labelledby="cl-pairs"><h2 id="cl-pairs" class="cluster-h">Contrast pairs</h2>'
             f'<ul class="cards cards--pairs" data-cards>{pairs}</ul></section>{"".join(cl)}</div>')
    return (f'<main id="main" class="lib lib--canvas cvp">'
            f'<h1 class="sr-only">Content Example library, {model["long"]}</h1>'
            f'<div class="cv" data-cv data-cv-fit=".cluster" tabindex="0" role="region" aria-label="Library board. Drag or use arrow keys to pan; plus and minus to zoom.">'
            f'<div class="cv-content" data-cv-content>{board}</div></div>'
            f'<div class="fl fl-pill"><details class="pill"><summary><span aria-hidden="true">⌕</span> Search &amp; filter <span class="muted">· {"Messenger" if view == "messenger" else "Curator"} view</span></summary>'
            f'<div class="pill-panel">{intro}{view_switch(view)}{view_note(view)}{filter_form(shown, view)}</div></details></div>'
            f'{zoom_cluster()}</main>')

def zoom_cluster():
    return ('<div class="fl fl-zoom js-only" role="group" aria-label="Zoom">'
            '<button type="button" data-zoom="in" aria-label="Zoom in">+</button>'
            '<button type="button" data-zoom="out" aria-label="Zoom out">–</button>'
            '<button type="button" data-zoom="fit" aria-label="Fit to screen"><span aria-hidden="true">⤢</span></button></div>')

# ---------------------------------------------------------------------------
# Detail pages
# ---------------------------------------------------------------------------
def state_banner(rec, by):
    if rec["verdict_slug"] == "soso":
        if rec["contrast_pair_id"]:
            return (f'<p class="ce-state"><b>Learning case.</b> For messengers, this appears only as the weaker half of a contrast pair (rule R3). '
                    f'<a href="{rec["contrast_pair_id"]}.html">See the pair</a>.</p>')
        return '<p class="ce-state"><b>Curator view only.</b> A So-so example with no contrast pair yet, so messengers don\'t see it (rule R3).</p>'
    if rec["verdict_slug"] == "not":
        return '<p class="ce-state"><b>Not yet usable.</b> Visible to curators only. Reason: it\'s a roster, not a message.</p>'
    if rec["contrast_pair_id"]:
        return f'<p class="ce-state ce-state--info">Part of a contrast pair. <a href="{rec["contrast_pair_id"]}.html">Compare it with a learning case</a>.</p>'
    return ""

def detail(model, rec, recs, by):
    mk = model["key"]
    fn = {"stage": detail_stage, "canvas": detail_canvas, "spec": detail_spec}[mk]
    body = fn(model, rec, recs, by)
    needs_js = mk != "spec" or bool(rec["media"]) or bool(rec["model_payload"])
    return page(f'{rec["title"]} · {model["name"]} · Content Example', body, model, css=[f"{mk}.css"],
                head_extra=jsonld(rec), js=needs_js, body_class=f"m-{mk} p-detail")

def back_link():
    return '<p class="ce-back"><a href="index.html">← Library</a></p>'

def detail_stage(model, rec, recs, by):
    rel = "".join(f'<li><a href="{r["id"]}.html">{avatar(r, 28)}<span><b>{e(r["title"])}</b><small>{e(r["messenger_name"])} · {e(r["content_type"])}</small></span></a></li>' for r in related(rec, recs))
    controls = (f'<div class="stage-controls" role="group" aria-label="Stage controls">{overlay_toggle(rec)}'
                f'<a class="sc-btn" href="{e(rec["source_url"])}" target="_blank" rel="noopener">Open original <span aria-hidden="true">↗</span>{NEWTAB}</a>'
                + (f'<a class="sc-btn" href="#use-{rec["id"]}" data-open-details>Use as a model</a>' if rec["model_payload"] else "") + '</div>')
    return (f'<main id="main" class="wrap st-detail">{back_link()}<h1 class="st-title">{e(rec["title"])}</h1>{state_banner(rec, by)}'
            f'<div class="st-grid">'
            f'<div class="st-a1">{messenger_strip(rec)}</div><div class="st-a2">{fit_tags(rec)}</div>'
            f'<div class="st-stage" data-part="3"><div class="stage"><div class="stage-scroll" tabindex="0" role="region" aria-label="Content stage">{standin(rec)}</div>{controls}</div></div>'
            f'<div class="st-side">{why_section(rec)}{pattern_section(rec)}{trust_section(rec)}{actions_section(rec)}{connection_section(rec)}</div>'
            f'<section class="st-related" aria-labelledby="rel-h"><h2 id="rel-h">More examples like this</h2><ol class="rel">{rel}</ol>'
            f'<p class="small muted">A short, finite list. Nothing plays next on its own.</p></section>'
            f'</div></main>')

def layers_menu(rid):
    return (f'<details class="fl fl-layers"><summary><span aria-hidden="true">◫</span> Layers</summary><div class="layers-panel">'
            f'<label><input type="checkbox" class="ov-toggle" id="ov-{rid}" data-ov> Why it works pins</label>'
            f'<label><input type="checkbox" class="layer" data-layer-toggle="pattern" checked> Reusable pattern</label>'
            f'<label><input type="checkbox" class="layer" data-layer-toggle="trust" checked> Trust details</label></div></details>')

def detail_canvas(model, rec, recs, by):
    narrow = rec["standin_format"] in ("photo-post", "carousel", "short-video")
    return (f'<main id="main" class="cvp cv-detail">'
            f'<h1 class="sr-only">{e(rec["title"])}</h1>'
            f'<div class="fl fl-card">{messenger_strip(rec)}{fit_tags(rec)}</div>'
            f'<div class="cv{" cv--narrow" if narrow else ""}" data-cv data-part="3" tabindex="0" role="region" aria-label="Content canvas. Drag or use arrow keys to pan; plus and minus to zoom; 0 to fit.">'
            f'<div class="cv-content" data-cv-content>{standin(rec)}</div></div>'
            f'<div class="fl fl-pill"><a class="pill pill--link" href="index.html"><span aria-hidden="true">⌕</span> Search &amp; filter examples</a></div>'
            f'{layers_menu(rec["id"])}{zoom_cluster()}'
            f'<aside class="sheet" data-sheet="half" aria-label="Details"><button type="button" class="sheet-handle js-only" data-sheet-handle aria-label="Resize details panel" aria-expanded="true"><span aria-hidden="true"></span></button>'
            f'<div class="sheet-body">{state_banner(rec, by)}{why_section(rec)}{pattern_section(rec)}{trust_section(rec)}{actions_section(rec)}{connection_section(rec)}</div></aside>'
            f'<div class="notecard" data-notecard hidden role="dialog" aria-modal="false" aria-labelledby="nc-h"><p class="nc-h" id="nc-h"></p><div class="nc-body"></div>'
            f'<div class="nc-nav"><button type="button" data-nc="prev">← Previous</button><span data-nc-count></span><button type="button" data-nc="next">Next →</button>'
            f'<button type="button" data-nc="close" aria-label="Close note">✕</button></div></div>'
            f'</main>')

def detail_spec(model, rec, recs, by):
    return (f'<main id="main" class="wrap sp">{back_link()}'
            f'<article class="sp-article" aria-labelledby="t-{rec["id"]}"><h1 id="t-{rec["id"]}">{e(rec["title"])}</h1>{state_banner(rec, by)}'
            f'<ol class="sp-parts">'
            f'<li><h2 class="sp-h">Messenger</h2>{messenger_strip(rec)}</li>'
            f'<li><h2 class="sp-h">Fit</h2>{fit_tags(rec)}</li>'
            f'<li data-part="3"><h2 class="sp-h">Content</h2>{overlay_toggle(rec)}{standin(rec)}{notes_list(rec)}</li>'
            f'<li>{why_section(rec, with_notes=False)}</li>'
            f'<li>{pattern_section(rec)}</li><li>{trust_section(rec)}</li><li>{actions_section(rec)}</li><li>{connection_section(rec)}</li>'
            f'</ol></article></main>')

# ---------------------------------------------------------------------------
# Pair pages
# ---------------------------------------------------------------------------
def compare_table(p, by):
    s, w = by[p["strong"]], by[p["weak"]]
    rows = []
    for code, name in PRIN:
        def cell(r):
            g = (r["principle_grades"] or {}).get(code, "")
            label, shown = GRADE[g]
            cls = {"strong": "g-strong", "mixed": "g-mixed", "weak": "g-weak"}.get(label, "g-na")
            notes = [n["note"] for n in r["grading_analysis"] if n["principle"] == code]
            return (f'<td class="g {cls}"><span class="gs" aria-hidden="true">{shown}</span><span class="gl">{label}</span>'
                    + (f'<span class="gn">{e(notes[0])}</span>' if notes else "") + "</td>")
        rows.append(f'<tr><th scope="row">{code} {name}</th>{cell(s)}{cell(w)}</tr>')
    return (f'<div class="table-scroll" tabindex="0" role="region" aria-label="Principle-by-principle comparison"><table class="cmp">'
            f'<caption class="sr-only">Principle by principle: {e(s["messenger_name"])} and {e(w["messenger_name"])}</caption>'
            f'<thead><tr><th scope="col">Principle</th><th scope="col">{e(s["messenger_name"])} <small>Good example</small></th>'
            f'<th scope="col">{e(w["messenger_name"])} <small>Learning case</small></th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>')

def pair_intro(p, by):
    s, w = by[p["strong"]], by[p["weak"]]
    return (f'<p class="pair-lesson">{e(p["lesson"])}</p>'
            f'<p class="small muted">The second piece is a learning case, not a callout of its authors (rule R4). Use this page as a draft precedent sheet: print it or save it as PDF.</p>')

def pair_item_compact(rec, role, with_standin=True):
    label = "Good example" if role == "strong" else "Learning case"
    return (f'<article class="pi" aria-labelledby="pi-{rec["id"]}"><p class="eyebrow">{label}</p>'
            f'<h2 id="pi-{rec["id"]}" class="pi-h"><a href="{rec["id"]}.html">{e(rec["title"])}</a></h2>'
            f'{messenger_strip(rec, "p")}{fit_tags(rec)}'
            + (f'<div data-part="3">{standin(rec)}</div>' if with_standin else "")
            + f'{why_section(rec, h="h3")}{trust_section(rec, h="h3")}</article>')

def pair_page(model, p, by):
    mk = model["key"]
    s, w = by[p["strong"]], by[p["weak"]]
    if mk == "stage":
        def stagebox(r):
            return (f'<div class="stage"><div class="stage-scroll" tabindex="0" role="region" aria-label="Stage: {e(r["messenger_name"])}">{standin(r)}</div>'
                    f'<div class="stage-controls"><a class="sc-btn" href="{e(r["source_url"])}" target="_blank" rel="noopener">Open original <span aria-hidden="true">↗</span>{NEWTAB}</a>'
                    f'<a class="sc-btn" href="{r["id"]}.html">Details</a></div></div>')
        def col(r, role):
            return (f'<article class="pair-col" aria-labelledby="pc-{r["id"]}"><p class="eyebrow">{"Good example" if role == "strong" else "Learning case"}</p>'
                    f'<h2 id="pc-{r["id"]}" class="pi-h">{e(r["title"])}</h2>{messenger_strip(r)}{fit_tags(r)}<div data-part="3">{stagebox(r)}</div>'
                    f'{why_section(r, h="h3")}{trust_section(r, h="h3")}</article>')
        body = (f'<main id="main" class="wrap st-pair">{back_link()}<h1>{e(p["title"])}</h1>{pair_intro(p, by)}'
                f'<div class="pair-toolbar">{overlay_toggle(p["id"])}</div>'
                f'<div class="pair-grid">{col(s, "strong")}{col(w, "weak")}</div>'
                f'<section aria-labelledby="cmp-h" class="pair-cmp"><h2 id="cmp-h">Principle by principle</h2>{compare_table(p, by)}</section></main>')
    elif mk == "canvas":
        def half(r, role):
            return (f'<div class="split-pane" data-split-pane><p class="split-label"><span class="verdict {"v-good" if role == "strong" else "v-soso"}">{ICON_V["good" if role == "strong" else "soso"]}{"Good example" if role == "strong" else "Learning case"}</span> {e(r["messenger_name"])}</p>'
                    f'<div class="cv" data-cv data-cv-sync="{p["id"]}" tabindex="0" role="region" aria-label="Canvas: {e(r["title"])}. Drag or arrow keys to pan; plus and minus to zoom.">'
                    f'<div class="cv-content" data-cv-content>{standin(r)}</div></div></div>')
        body = (f'<main id="main" class="cvp cv-pair"><h1 class="sr-only">{e(p["title"])}</h1>'
                f'<div class="split" data-split>{half(s, "strong")}'
                f'<div class="split-divider js-only" role="separator" tabindex="0" aria-orientation="vertical" aria-label="Resize split" aria-valuemin="20" aria-valuemax="80" aria-valuenow="50" data-split-divider><span aria-hidden="true"></span></div>'
                f'{half(w, "weak")}</div>'
                f'<div class="fl fl-pill"><a class="pill pill--link" href="index.html"><span aria-hidden="true">⌕</span> Search &amp; filter examples</a></div>'
                f'{layers_menu(p["id"])}{zoom_cluster()}'
                f'<aside class="sheet" data-sheet="collapsed" aria-label="Comparison"><button type="button" class="sheet-handle js-only" data-sheet-handle aria-label="Resize comparison panel" aria-expanded="false"><span aria-hidden="true"></span></button>'
                f'<div class="sheet-body"><p class="eyebrow">Contrast pair</p><h2 class="pi-h">{e(p["title"])}</h2>{pair_intro(p, by)}'
                f'<section aria-labelledby="cmp-h"><h3 id="cmp-h">Principle by principle</h3>{compare_table(p, by)}</section>'
                f'{pair_item_compact(s, "strong", False)}{pair_item_compact(w, "weak", False)}</div></aside>'
                f'<div class="notecard" data-notecard hidden role="dialog" aria-modal="false" aria-labelledby="nc-h"><p class="nc-h" id="nc-h"></p><div class="nc-body"></div>'
                f'<div class="nc-nav"><button type="button" data-nc="prev">← Previous</button><span data-nc-count></span><button type="button" data-nc="next">Next →</button>'
                f'<button type="button" data-nc="close" aria-label="Close note">✕</button></div></div></main>')
    else:
        body = (f'<main id="main" class="wrap sp sp-pair">{back_link()}<h1>{e(p["title"])}</h1>{pair_intro(p, by)}'
                f'{overlay_toggle(p["id"])}{pair_item_compact(s, "strong")}{notes_list(s)}{pair_item_compact(w, "weak")}{notes_list(w)}'
                f'<section aria-labelledby="cmp-h"><h2 id="cmp-h">Principle by principle</h2>{compare_table(p, by)}</section></main>')
    return page(f'{p["title"]} · Contrast pair · {model["name"]}', body, model, css=[f"{mk}.css"],
                js=(mk != "spec"), body_class=f"m-{mk} p-pair")

# ---------------------------------------------------------------------------
# Per-example pages: examples/<id>.html
# A stable URL per example or pair that survives the Stage vs. Canvas choice.
# It names the default model and offers the others. "#pattern" on the URL is
# carried to the reusable-pattern section (#pat-<id>) in whichever model opens.
# ---------------------------------------------------------------------------
ROUTER_JS = """<script>
(function(){var h=location.hash.slice(1);if(!h)return;var m=document.querySelector('main[data-id]');if(!m)return;var id=m.getAttribute('data-id');
var map={pattern:'pat-'+id,why:'why-'+id,notes:'why-'+id};var t=map[h];if(!t)return;
document.querySelectorAll('a[data-model]').forEach(function(a){a.href=a.getAttribute('href').split('#')[0]+'#'+t;});})();
</script>"""

def model_choice(target, label):
    ordered = sorted(MODELS, key=lambda m: m["key"] != DEFAULT_MODEL)
    first, rest = ordered[0], ordered[1:]
    btn = f'<a class="btn btn-primary" data-model="{first["key"]}" href="../{first["key"]}/{target}.html">Open {e(label)} in {e(first["name"])}</a>'
    others = " · ".join(f'<a data-model="{m["key"]}" href="../{m["key"]}/{target}.html">{e(m["long"])}</a>' for m in rest)
    return (f'<p class="ex-go">{btn}</p>'
            f'<p class="small ex-alt">Default model: {e(first["long"])}, {e(first["like"])}. The presentation model isn\'t chosen yet. Also open it in {others}, or <a href="../index.html">compare all three</a>.</p>')

def example_router(rec):
    why = rec["why_it_works"] or rec["what_to_watch"] or ""
    pair = next((p for p in PAIRS if rec["id"] in (p["strong"], p["weak"])), None)
    pair_line = f'<p class="small">Part of the contrast pair <a href="{pair["id"]}.html">{e(pair["title"])}</a>.</p>' if pair else ""
    body = f"""<main id="main" class="wrap ex-route" data-id="{rec["id"]}">
<p class="eyebrow">Content Example · {e(rec["communicator_segment_label"])}</p>
<h1>{e(rec["title"])}</h1>
{messenger_strip(rec)}
<p>{verdict_badge(rec)} <span class="small muted">{e(rec["content_type"])} · {e(rec["venue"] or "")}</span></p>
{f'<p class="lede">{e(why)}</p>' if why else ""}
{model_choice(rec["id"], "this example")}
{pair_line}
</main>"""
    return page(f'{rec["title"]} · Content Example', body + ROUTER_JS, {"name": "Example"}, depth=1, js=False,
                head_extra=f"<style>{ROUTER_CSS}</style>", body_class="p-route")

def pair_router(p, by):
    s, w = by[p["strong"]], by[p["weak"]]
    body = f"""<main id="main" class="wrap ex-route">
<p class="eyebrow">Content Example · Contrast pair</p>
<h1>{e(p["title"])}</h1>
<p class="lede">{e(p["lesson"])}</p>
<ul class="ex-pair">
<li>{verdict_badge(s)} <a href="{s["id"]}.html">{e(s["title"])}</a> <span class="small muted">{e(s["messenger_name"])}</span></li>
<li>{verdict_badge(w)} <a href="{w["id"]}.html">{e(w["title"])}</a> <span class="small muted">{e(w["messenger_name"])}</span></li>
</ul>
{model_choice(p["id"], "this pair")}
</main>"""
    return page(f'{p["title"]} · Content Example pair', body, {"name": "Pair"}, depth=1, js=False,
                head_extra=f"<style>{ROUTER_CSS}</style>", body_class="p-route")

ROUTER_CSS = """
.ex-route{max-width:760px;padding-top:32px;padding-bottom:64px}
.ex-route h1{font-size:clamp(28px,4vw,40px);line-height:1.15;margin:4px 0 16px}
.ex-route .ce-ms{margin:0 0 12px}
.ex-go{margin:24px 0 8px}
.ex-pair{list-style:none;padding:0;margin:16px 0;display:grid;gap:10px}
.ex-pair li{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
"""

# ---------------------------------------------------------------------------
# C. Compare page and weights
# ---------------------------------------------------------------------------
MATRIX = [
    ("Short-form video", ["msv-healthcare-short"]),
    ("Long-form video or speech", ["lawson-heat-dome-speech"]),
    ("Social post (text and image)", ["pow-signs-everywhere", "diggins-i-voted"]),
    ("News article or interview", ["howard-wildfire-smoke"]),
    ("Op-ed or blog post", ["seattle-times-heat-oped", "suter-outrider-oped", "vossler-psr-post"]),
    ("News release", ["napnap-nursing-heat"]),
    ("Contrast pair (two items)", [p["id"] for p in PAIRS]),
    ("Report or talking-points memo", []),
]

def measure(path):
    """Bytes for a page plus every local CSS, JS and font file it references (uncompressed)."""
    seen = set()
    total = path.stat().st_size
    src = path.read_text()
    refs = re.findall(r'(?:href|src)="([^"#?]+\.(?:css|js))"', src)
    for r in refs:
        f = (path.parent / r).resolve()
        if f in seen or not f.exists():
            continue
        seen.add(f)
        total += f.stat().st_size
        if f.suffix == ".css":
            for u in re.findall(r'url\(["\']?([^"\')]+\.woff2)', f.read_text()):
                ff = (f.parent / u).resolve()
                if ff not in seen and ff.exists():
                    seen.add(ff); total += ff.stat().st_size
    third = re.findall(r'(?:href|src)="(https?://[^"]+)"', src)
    third = [t for t in third if not re.search(r'<a [^>]*href="' + re.escape(t), src)]
    return total

def kb(n):
    return f"{n / 1024:.0f} KB"

def weights():
    out = {}
    for m in MODELS:
        d = OUT / m["key"]
        out[m["key"]] = dict(
            library=measure(d / "index.html"),
            curator=measure(d / "curator.html"),
            article=measure(d / "howard-wildfire-smoke.html"),
            video=measure(d / "lawson-heat-dome-speech.html"),
            pair=measure(d / "pair-heat-dome.html"),
            heaviest_detail=max((measure(f), f.name) for f in d.glob("*.html") if f.name not in ("index.html", "curator.html") and not f.name.startswith("pair-")),
        )
    return out

def compare_page(by, w):
    head = "".join(f'<th scope="col">{e(m["long"])}<small>{e(m["like"])}</small></th>' for m in MODELS)
    rows = []
    for label, ids in MATRIX:
        cells = []
        for m in MODELS:
            if not ids:
                cells.append('<td class="tbs">To be sourced</td>')
                continue
            links = []
            for i in ids:
                if i.startswith("pair-"):
                    p = next(p for p in PAIRS if p["id"] == i)
                    links.append(f'<a href="{m["key"]}/{i}.html">{e(by[p["strong"]]["messenger_name"].replace("Dr. ", ""))} vs. {e(by[p["weak"]]["messenger_name"].replace("Dr. ", "").split(",")[0])}</a>')
                else:
                    links.append(f'<a href="{m["key"]}/{i}.html">{e(by[i]["messenger_name"].replace("Dr. ", ""))}</a>')
            cells.append(f'<td>{"<br>".join(links)}</td>')
        ex = ", ".join(by[i]["title"] if not i.startswith("pair-") else "" for i in ids if not i.startswith("pair-")) or ("Three pairs" if ids else "None in the audit yet")
        rows.append(f'<tr><th scope="row">{e(label)}<small>{e(ex)}</small></th>{"".join(cells)}</tr>')
    def pair_links(p):
        return " · ".join('<a href="%s/%s.html">%s</a>' % (m["key"], p["id"], e(m["name"])) for m in MODELS)
    pairs = "".join(f'<li><b>{e(p["title"])}</b><span>{pair_links(p)}</span></li>' for p in PAIRS)
    wrows = []
    for m in MODELS:
        x = w[m["key"]]
        def b(n, budget):
            ok = n <= budget
            return f'<td>{kb(n)} <span class="{"ok" if ok else "over"}">{"✓ within" if ok else "✕ over"}</span></td>'
        wrows.append(f'<tr><th scope="row">{e(m["long"])}</th>{b(x["library"], 300*1024)}{b(x["article"], 500*1024)}{b(x["video"], 500*1024)}{b(x["pair"], 500*1024)}'
                     f'<td>0 <span class="ok">✓</span></td></tr>')
    libs = "".join(f'<a class="btn btn-primary" href="{m["key"]}/index.html">{e(m["long"])}</a>' for m in MODELS)
    cards = "".join(
        f'<a class="tile linkcard" href="{m["key"]}/index.html"><p class="eyebrow" style="margin:0">{e(m["long"])}</p><h3>{e(m["name"])}</h3><p>{e(desc)}</p><span class="more">Open the {e(m["name"].lower())} library</span></a>'
        for m, desc in zip(MODELS, [
            "A clear stage holds the artifact; details sit below on phones and beside it on desktop. Controls float over the stage's bottom edge. Tests: video, familiar reflow.",
            "The artifact fills the screen and pans and zooms. Details float in cards and a bottom sheet; pins open note cards. Tests: long documents, spatial annotation.",
            "No metaphor: the anatomy in order 1–8 in one readable column. Works fully without JavaScript. The baseline for weight and robustness.",
        ]))
    body = f"""<main id="main" class="wrap cmp-page">
<header class="cmp-head"><p class="eyebrow">Prototype · for testing with clinicians</p>
<h1>Content Example: compare three ways to present an example</h1>
<p class="lede">The player that shows a curated example isn't decided yet. The requirements (section 7.2) name two candidate models, a <b>Stage</b> like a video site and a <b>Canvas</b> like a map app, plus a <b>baseline</b> built only from the requirements. All three use the same 18 audit examples, the same anatomy in the same order, and the same data. Only layout and how notes are revealed differ. We'll judge them on: can Dr. Maya tell in seconds whether it's for her, on a phone (J2)? Can she find why it works without being lectured (J4)? Can she see the pattern she'd borrow (J5)? Do long documents and video work equally well (J2, J4)? Does it export cleanly to a slide or PDF page (J4, J6)? And how much does it weigh on a slow connection (J1, J2; WSG 2.17, 3.1)?</p>
</header>
<div class="grid g3 cmp-cards">{cards}</div>
<section aria-labelledby="mx-h"><h2 id="mx-h">Prototype matrix</h2>
<p>Each cell opens the matching detail page in that model. From requirements section 7.2.</p>
<div class="table-scroll" tabindex="0" role="region" aria-label="Prototype matrix"><table class="plain mx"><caption class="sr-only">Content type by model</caption>
<thead><tr><th scope="col">Content type</th>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div></section>
<section aria-labelledby="pr-h"><h2 id="pr-h">Contrast pairs in all three models</h2><ul class="cmp-pairs">{pairs}</ul></section>
<section aria-labelledby="wt-h"><h2 id="wt-h">Weight</h2>
<p>Total bytes for the page plus the CSS, script and fonts it loads, with media not loaded. Uncompressed, so real transfers with gzip or Brotli are smaller. Budgets from WS-11: library ≤ 300 KB, detail ≤ 500 KB. No page makes a third-party request on load; YouTube is contacted only after “Load video.”</p>
<div class="table-scroll" tabindex="0" role="region" aria-label="Page weight by model"><table class="plain wt"><caption class="sr-only">Page weight by model</caption>
<thead><tr><th scope="col">Model</th><th scope="col">Library</th><th scope="col">Detail: long article (Howard)</th><th scope="col">Detail: video, not loaded (Lawson)</th><th scope="col">Contrast pair (heat dome)</th><th scope="col">Third-party requests on load</th></tr></thead>
<tbody>{"".join(wrows)}</tbody></table></div></section>
<section aria-labelledby="how-h"><h2 id="how-h">How to read these prototypes</h2>
<ul class="prose">
<li><b>Stand-ins, not copies.</b> We don't have rights to reproduce the originals. Each one is drawn as an illustration of its format, filled with TCC's paraphrase and at most one short quote. Every stand-in links to the original.</li>
<li><b>Messenger and curator views.</b> Messenger view hides So-so and Not-yet-usable examples except inside contrast pairs (rules R2, R3). Curator view shows all 18.</li>
<li><b>Draft curation.</b> Pattern, step, topics, place and notes are derived from the audit for prototyping and labelled as drafts.</li>
<li><b>Gaps are shown.</b> Where the audit has no data (full text, clinician review, institution, reshare counts), the page says so.</li>
</ul></section>
</main>"""
    return page("Compare Content Example models · TCC prototype", body, None, depth=0, css=["shared/compare.css"], js=False, body_class="p-compare")

def update_readme(w):
    rd = OUT / "README.md"
    if not rd.exists():
        return
    lines = ["| Model | Library | Detail: article | Detail: video (not loaded) | Pair | Heaviest detail |", "|---|---|---|---|---|---|"]
    for m in MODELS:
        x = w[m["key"]]
        lines.append(f'| {m["long"]} | {kb(x["library"])} | {kb(x["article"])} | {kb(x["video"])} | {kb(x["pair"])} | {kb(x["heaviest_detail"][0])} ({x["heaviest_detail"][1]}) |')
    block = "<!-- weights:start -->\n" + "\n".join(lines) + "\n<!-- weights:end -->"
    t = rd.read_text()
    t = re.sub(r"<!-- weights:start -->.*?<!-- weights:end -->", lambda _: block, t, flags=re.S)
    rd.write_text(t)

# ---------------------------------------------------------------------------
def main():
    recs, by = build_records()
    (OUT / "data").mkdir(parents=True, exist_ok=True)
    data = dict(generated_by="tools/build_content_example.py", source="reference/audit.md", audit_date=AUDIT_DATE,
                note="Prototype dataset. Fields the audit doesn't support are null. prototype_curation marks TCC draft curation.",
                pairs=PAIRS, examples=recs)
    (OUT / "data" / "examples.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    count = 0
    for m in MODELS:
        d = OUT / m["key"]
        d.mkdir(parents=True, exist_ok=True)
        for old in d.glob("*.html"):
            old.unlink()
        (d / "index.html").write_text(library(m, recs, by, "messenger")); count += 1
        (d / "curator.html").write_text(library(m, recs, by, "curator")); count += 1
        for r in recs:
            (d / f'{r["id"]}.html').write_text(detail(m, r, recs, by)); count += 1
        for p in PAIRS:
            (d / f'{p["id"]}.html').write_text(pair_page(m, p, by)); count += 1
    ex = OUT / "examples"
    ex.mkdir(parents=True, exist_ok=True)
    for old in ex.glob("*.html"):
        old.unlink()
    for r in recs:
        (ex / f'{r["id"]}.html').write_text(example_router(r)); count += 1
    for p in PAIRS:
        (ex / f'{p["id"]}.html').write_text(pair_router(p, by)); count += 1
    w = weights()
    (OUT / "index.html").write_text(compare_page(by, w)); count += 1
    update_readme(w)
    print(f"Wrote {len(recs)} records and {count} pages to {OUT.relative_to(ROOT)}")
    for m in MODELS:
        x = w[m["key"]]
        print(f'  {m["name"]:<18} library {kb(x["library"]):>7}  article {kb(x["article"]):>7}  video {kb(x["video"]):>7}  pair {kb(x["pair"]):>7}')

if __name__ == "__main__":
    main()
