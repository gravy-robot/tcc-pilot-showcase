# Content Example: Component Requirements

**Project:** TCC Curated Content Platform, health professionals pilot
**Author:** TCC Design Research
**Date:** November 9, 2026 (v3: adds alignment with the W3C Web Sustainability Guidelines)
**Status:** Draft for review
**Derived from:** `content-example-jtbd.md` (in this folder)

**Framework:** Rare's *Eight Principles for Effective and Inviting Climate Communication* (P1 Make it personal · P2 Make it accessible · P3 Make it empowering · P4 Make it doable · P5 Make it collective · P6 Make it normal · P7 Make it trustworthy · P8 Make it for everyone). Use this exact title everywhere.

**Web sustainability:** aligned with the W3C *Web Sustainability Guidelines (WSG)*, Group Note Draft of 16 October 2026 (https://www.w3.org/TR/web-sustainability-guidelines/). WSG numbers are cited as "WSG 2.9" etc. See section 12.

---

## 0. How to read this document

**Traceability.** Every requirement traces to at least one job.

| Job | Stage | Short name |
|---|---|---|
| J1 | Notice | Give her permission |
| J2 | Explore | Signal fit fast |
| J3 | Join | Preview the value |
| J4 | Learn | Make "good" visible |
| J5 | Create | Be a model she can borrow |
| J6 | Share | Provide cover |
| J7 | Return and connect | Connect her to peers and credit her work |

**Scope.** Each requirement is marked:
- **Pilot:** needed for the health-professionals pilot.
- **Later:** a planned capability, built only when users ask for it *and* it serves TCC's Theory of Change. Section 14 lists these with the signal that would trigger them.

The bias is to deliver less until users show they need more.

---

## 1. Design principle

**One record, many renderings.** Each Content Example is a single structured record. Every touchpoint renders a variant of that record: a social post, the library, a chatbot, a training module, a deck or the messenger's own post. Curation happens once and is reused across the journey, and every variant stays traceable to the original. (This is also the WSG's "reuse over recreation" idea: WSG 2.7, 3.4.)

The system has four layers:
1. **Intake:** how examples get in (section 2).
2. **Record:** what is stored about each one (section 3).
3. **Access:** who and what can read, add or edit (section 4).
4. **Presentation:** how examples appear across the journey (sections 5–8).

---

## 2. Intake

### 2.1 Content types

| ID | Requirement | Trace | Scope |
|---|---|---|---|
| IN-1 | Accept these content types: short-form video, long-form video, social post (text and/or images), article or op-ed, blog post, press release, report, talking points or briefing memo, interview (video, audio or text), example conversation (video or transcript). | J2, J4, J5 | Pilot: types found in the audit (short and long video, social post, article/op-ed, news story, blog post, news release, testimony recap, profile). Later: the rest. |
| IN-2 | `content_type` uses a controlled list that curators can extend without code changes. | J2 | Pilot |

### 2.2 Capture

| ID | Requirement | Trace | Scope |
|---|---|---|---|
| IN-3 | Capture the full text as formatted Markdown: article text, video transcript, or post text. Four of 11 audit sources gave only an excerpt through public pages, so the platform can't depend on the original staying available. | J4, J5 | Pilot |
| IN-4 | Capture rendered images of how the content looks as published: desktop browser, phone browser, and the intended app (e.g., a social feed). These are the *whole artifact*, not just images inside it. Store them in efficient formats at the sizes variants need (WSG 2.9). | J1, J4, J6 | Pilot: phone rendering plus one other. Later: all three for every item. |
| IN-5 | Before storing rendered images, remove or blur third parties: commenters' names, faces and avatars, and people in a conversation who haven't consented. | J6 | Pilot |
| IN-6 | Record provenance: who nominated the example and how it came in (curator, messenger submission, partner, automated). | J7 | Pilot |
| IN-7 | Detect duplicates (same URL, or same text from another outlet) and link reposts to the original record. | J2 | Later |
| IN-8 | Record `intake_date`, and keep an update log of every later change with date, author and reason (e.g., "engagement rose materially," "original removed," "grade revised"). | J4, J6 | Pilot |
| IN-9 | Example conversations with private individuals require recorded consent and de-identification before intake. | J6 | Later (no conversations in the pilot) |

### 2.3 Engagement

Engagement shows **reach, not quality**. In our audit, the strongest health videos had 20 and 55 views, and TCC's survey does not measure which efforts succeed. So engagement is stored and used for amplification decisions, never for grading or ranking quality.

| ID | Requirement | Trace | Scope |
|---|---|---|---|
| IN-10 | Store engagement as dated snapshots: views, reactions, comments, reposts or shares, plus the messenger's follower count at that date where available. Refresh on a defined schedule (at intake, then quarterly) rather than continuously (WSG 4.7). | J7 | Pilot |
| IN-11 | Flag "strong but unseen" examples (verdict = Good example, low engagement relative to followers) as candidates for TCC to reshare. | J1, J7 | Pilot (manual curator flag) |
| IN-12 | Engagement never affects the verdict, the grades or default sort order in the library. | J2, J4 | Pilot |
| IN-13 | Summarize comments: counts of favorable, unfavorable and neutral comments, plus a few descriptive words for each. Store aggregates only, never commenters' names or comment text (WSG 5.18). Useful for P8 (does a piece polarize?). | J4, J6 | Later |

---

## 3. The record (data model)

"Req." means required to publish.

### 3.1 Identity and source
| Field | Req. | Notes | Trace | Scope |
|---|---|---|---|---|
| `id` | ✓ | Stable slug | All | Pilot |
| `title` | ✓ | Plain-language title written by TCC | J2 | Pilot |
| `source_url` | ✓ | Opens in a new tab | J2, J6 | Pilot |
| `venue` | ✓ | Where it was published (outlet, organization, event) | J2, J6 | Pilot |
| `platform` | ✓ | Where it was distributed (e.g., a social network, website, video site), as text | J2, J5 | Pilot |
| `published_date` | ✓ | Exact or approximate; "undated" allowed with a note | J2 | Pilot |
| `content_type` | ✓ | From the controlled list (IN-2) | J2, J5 | Pilot |
| `language` | ✓ | The survey covered the U.S. and Canada | J2 | Pilot |
| `full_text_md` | ✓ | IN-3 | J4, J5 | Pilot |
| `renders` | ✓ | Rendered images, IN-4 | J1, J4, J6 | Pilot |
| `media` | | For video or audio: duration and approximate data size, so the player can tell users before loading (WSG 2.9) | J2 | Pilot |
| `sponsorship` | | Whether the original is sponsored, and by whom (the audit found sponsored athlete posts) | J6 | Pilot |
| `rights_status` | ✓ | Permission granted / link-only / pending. Controls which variants may show text, renders or media | All | Pilot |
| `intake_date`, `update_log` | ✓ | IN-8 | J4, J6 | Pilot |
| `provenance` | ✓ | IN-6 | J7 | Pilot |

### 3.2 Messenger
"Author" and "messenger" are separate: credibility comes from the messenger's role, and the author may be a ghostwriter or organization.

| Field | Req. | Notes | Trace | Scope |
|---|---|---|---|---|
| `authors` | ✓ | Who wrote or produced it | J6 | Pilot |
| `messenger_name` | ✓ | Who is speaking | J1, J6 | Pilot |
| `messenger_role` | ✓ | e.g., emergency physician, family doctor, nurse | J1, J2 | Pilot |
| `messenger_affiliation` | | Institution or society | J6 | Pilot |
| `messenger_avatar` | | Illustrated initial by default; real photos only with rights | J1 | Pilot |

### 3.3 Tags (controlled and versioned)
Each tag stores the **taxonomy version** it was assigned under, so records can be re-indexed when a model changes.

| Field | Req. | Notes | Trace | Scope |
|---|---|---|---|---|
| `communicator_segment` | ✓ | From the communicator segmentation model (health professionals, outdoor/athletes…) | J2 | Pilot |
| `audience_segment` | | From the audience segmentation model, which cross-references the communicator model | J2, J5 | Pilot: simple list (patients, peers, public, policymakers, fans). Later: full model. |
| `topics` | ✓ | e.g., heat, wildfire smoke, air quality | J2 | Pilot |
| `geography` | ✓ | Place it speaks to, plus scope (local, regional, national) | J2 | Pilot |
| `timeliness` | | Seasonal or event hook, or "evergreen" | J2 | Pilot |
| `partisan_framing` | | Flag for pieces framed around a partisan fight, so messengers can choose cross-audience pieces (an audit finding) | J2, J6 | Pilot |
| `taxonomy_version` | ✓ | Stamped per tag | J2 | Pilot |
| `estimated_reach` | | From a probabilistic model; shown as a range with model version; internal only | J7 | Later |

### 3.4 Grading and analysis (the learning layer)
| Field | Req. | Notes | Trace | Scope |
|---|---|---|---|---|
| `principle_grades` | ✓ | P1–P8 on the audit's scale: **+** strong · **~** mixed · **–** weak (works against the principle) · **·** not in play for this piece | J4, J5 | Pilot |
| `grading_analysis_md` | ✓ | Markdown record that, for each principle, names what's working and what could improve, **anchored to specific passages or timestamps** in the content. Powers overlays (7.3) | J4, J5 | Pilot |
| `verdict` | ✓ | Good example (mostly +, no –) / So-so (useful to teach a fix) / Not yet usable (too thin to grade) | J4 | Pilot |
| `why_it_works` | ✓ | Two or three plain sentences for messengers, distilled from the analysis | J1, J4, J5 | Pilot |
| `what_to_watch` | | Where it misses and how to fix it. Required for the weaker half of a contrast pair | J4 | Pilot |
| `contrast_pair_id` | | Links a strong and a weaker example on the same topic | J4 | Pilot |
| `grade_provenance` | ✓ | Who graded it, human or AI-assisted, date, and the version of the principle definitions and rubric used | J4, J6 | Pilot |

### 3.5 Reusable pattern (the borrowing layer)
| Field | Req. | Notes | Trace | Scope |
|---|---|---|---|---|
| `structure` | ✓ for Good example | Ordered moves, e.g., hook → local link → health effect → one doable step → hope | J5 | Pilot |
| `doable_step` | ✓ for Good example | The single action it asks for (P4, a common miss in the audit) | J1, J5 | Pilot |
| `for_everyone_notes` | | How it stays non-partisan (P8, the other common miss) | J5, J6 | Pilot |
| `short_quote` | | One line, under 15 words, credited and linked | J1, J3 | Pilot |
| `model_payload` | ✓ for Good example | Structured bundle for AI tools (section 8) | J5 | Pilot |

### 3.6 Safety and approval
| Field | Req. | Notes | Trace | Scope |
|---|---|---|---|---|
| `institutional_backing` | | Published by a hospital, society or public-health body | J6 | Pilot |
| `sources_cited` | | Whether claims are sourced, with links | J6 | Pilot |
| `reviewed_by`, `reviewed_date` | ✓ | TCC curator, plus a clinician reviewer for health claims | J6 | Pilot |

### 3.7 Reach and connection
| Field | Req. | Notes | Trace | Scope |
|---|---|---|---|---|
| `engagement_snapshots` | | IN-10 | J7 | Pilot |
| `amplify_candidate` | | IN-11 | J1, J7 | Pilot |
| `tcc_amplified` | | Whether TCC reshared it, with link | J7 | Pilot |
| `derived_from` | | IDs of examples a messenger's piece credits ("made with") | J7 | Pilot |
| `contributed_by` | | Set when a messenger or partner submits a piece | J7 | Pilot |

---

## 4. Storage, interoperability and access

### 4.1 Who needs to sign in

**Messengers reading and using examples do not need to sign in.** Dr. Maya must be able to see examples at Notice, Explore and Join (J1–J3) before she commits to anything. The "Join" sign-up is for the starter pack and digest, not a gate on the library.

**Authentication applies to contributors and third-party systems** that read from or write to the database of examples.

| Role | Signs in? | Can do | Trace | Scope |
|---|---|---|---|---|
| Messenger (reader) | No | Browse, filter, view, export, copy the model payload, for all rights-cleared records | J1–J6 | Pilot |
| Contributor (messenger or partner org) | Yes | Read; **append** new records; edit metadata on **their own** records only; cannot grade their own work | J7 | Pilot (TCC-invited contributors only) |
| Curator / reviewer | Yes | Grade, write analysis, set the verdict, approve, edit any record | J4, J6 | Pilot |
| Admin | Yes | Manage taxonomies, rubrics, roles and system clients | All | Pilot |
| System client (read) | Yes (API credential) | Read-only access to a defined scope, e.g., TCC's site, an AI integration, a training platform. The most common system role | J2, J5 | Pilot: TCC's own site. Later: partners. |
| System client (append) | Yes (API credential) | Submit new records into the review queue | J7 | Later |

### 4.2 Storage and interoperability

| ID | Requirement | Trace | Scope |
|---|---|---|---|
| ST-1 | Store records in a structured, documented, open format (e.g., JSON with Markdown fields and image files), exportable in full (WSG 2.7). | All | Pilot |
| ST-2 | Expose records through a read API that touchpoints can call, with filters for segment, topic, geography, timeliness and verdict. Each variant requests only the fields it renders (WSG 3.11, 3.16). | J2, J5 | Pilot: read API used by TCC's own pages |
| ST-3 | Apply `rights_status` at the API: records or fields without permission are returned as link-only. | All | Pilot |
| ST-4 | Contributor submissions enter a review queue and are not visible to readers until a curator approves them. | J6, J7 | Pilot |
| ST-5 | Support re-indexing: when a taxonomy, segmentation model or rubric version changes, list affected records and allow batch re-tagging, with each change written to the update log. | J2, J4 | Pilot: version stamps only (manual re-tagging). Later: batch tooling. |
| ST-6 | Log every write by user or system client. | J6 | Pilot |
| ST-7 | Publish each example with schema.org structured data (JSON-LD) so search engines and AI tools can read who said it, when and where (WSG 3.8). | J2, J5 | Pilot |
| ST-8 | Define retention for renders, media and engagement snapshots: keep what variants need, and delete superseded sizes (WSG 2.9 media management, 4.12). | All | Pilot |

---

## 5. Anatomy

Each variant uses a subset of these parts, always in this order so messengers learn to read them.

1. **Messenger strip:** avatar, name, role, affiliation. *Who is speaking.*
2. **Fit tags:** topic, place, recency, content type. *Is this for me.*
3. **Content:** the original (render, media or text) or a preview.
4. **Why it works:** principle tags plus the plain summary; optionally, overlays on the content (7.1).
5. **Reusable pattern:** structure and doable step.
6. **Trust line:** source, institution, sponsorship if any, "Reviewed by TCC on [date]."
7. **Actions:** view original · use as a model · save · export · share.
8. **Connection line:** "Made with this example: 3 clinicians" or "Reshared by TCC."

---

## 6. Variants across the journey

| # | Variant | Stage / job | Where it appears | Parts | Delivery | Scope |
|---|---|---|---|---|---|---|
| 6.1 | **Spotlight** | 1 Notice / J1 | TCC social post, newsletter | 1, 3 (quote), 4 (tags), 7 (CTA) | Static export (image card) | Pilot |
| 6.2 | **Library card** | 2 Explore / J2 | Health library list | 1, 2, 3 (one line), 4 (tags), 6 (short) | Rendered in TCC's site | Pilot |
| 6.3 | **Starter-pack item** | 3 Join / J3 | Sign-up offer and welcome email | 1, 3, 4 (one line) | Rendered or email | Pilot |
| 6.4 | **Detail view** | 2–5 / J2, J4, J5 | Library item page | All | Player (section 7) | Pilot |
| 6.5 | **Contrast pair** | 4 Learn / J4 | Library, training module | Two detail views aligned by principle; `what_to_watch` on the weaker one | Player | Pilot |
| 6.6 | **Model reference** | 5 Create / J5 | Messenger's AI chatbot, Canva template | No visual UI | Payload (section 8) | Pilot |
| 6.7 | **Precedent sheet** | 6 Share / J6 | For an employer's comms office | 1, 3, 6, `for_everyone_notes`, sources | HTML page with print stylesheet, plus PDF (WSG 2.13) | Pilot |
| 6.8 | **Attribution badge** | 6–7 / J6, J7 | The messenger's own post | "Made with TCC's health examples" plus library link | Text snippet and image | Pilot |
| 6.9 | **Contribution card** | 7 Return / J7 | Digest, library | Library card with "contributed by" | Rendered | Pilot |
| 6.10 | **Training, deck and report export** | 4 Learn / J4 | Training modules, presentations, reports | Content with overlays, why it works, source | Slide image, PDF page, Markdown | Pilot: slide image and PDF. Later: native slide formats. |

**Variant rules**
- **R1.** Every variant links to the detail view (6.4). The detail view always links to the original.
- **R2.** Spotlight and Starter-pack items use only examples with verdict "Good example."
- **R3.** A "So-so" or "Not yet usable" example appears only as the weaker half of a contrast pair, never on its own. Curators can see all records.
- **R4.** The weaker half of a contrast pair is framed as a learning case, never as a callout of its author. Prefer institutional examples for the weaker half, or get permission.
- **R5.** Social platforms don't run embeds, so variants headed to social (6.1, 6.8) are delivered as static exports.
- **R6.** Before any download, show the file name, format, size and a one-line summary (WSG 2.13).

---

## 7. Presentation: the player

### 7.1 Requirements for any player
| ID | Requirement | Trace | Scope |
|---|---|---|---|
| PR-1 | One configurable component renders the detail view (6.4) and the contrast pair (6.5) for every content type. | J2, J4, J5 | Pilot |
| PR-2 | Responsive in interactive UIs: phone web first (390px), then desktop. Most first encounters happen on a phone. | J1, J2 | Pilot |
| PR-3 | Shows the **original artifact** (render, media or text) as the dominant element. | J1, J4 | Pilot |
| PR-4 | Shows the original **with overlays** of the grading analysis: numbered pins anchored to passages or timestamps, each opening its note. Overlays are off by default and toggled with "Show why it works" (WSG 2.5). | J4, J5 | Pilot |
| PR-5 | The plain "why it works" summary and the doable step are readable without opening any overlay. | J1, J5 | Pilot |
| PR-6 | Embeddable on TCC-owned pages. | J2 | Pilot |
| PR-7 | Embeddable on partner sites and apps via a script or iframe, using a read-only system credential; the embed loads lazily (WSG 3.5). | J2 | Later |
| PR-8 | Video and other third-party media load only when the user asks: show a static preview with duration and approximate data use, and no autoplay (WSG 2.9, 3.5). | J1, J2 | Pilot |
| PR-9 | Related examples are a short, finite list. No infinite scroll and no auto-advance to the next example (WSG 2.5). | J2, J4 | Pilot |

### 7.2 Two candidate models, to prototype before deciding

The model is **not decided**. Both will be prototyped across content types before choosing a direction, and the final player may borrow from each. A third prototype built only from these requirements, with neither metaphor, serves as a baseline.

| | **Stage model** (like a video site) | **Canvas model** (like a map app) |
|---|---|---|
| Layout | A clear stage holds the content; details sit below or beside it | The content fills the view; details open in floating cards and panels |
| Controls | Float over the stage | Float over the content |
| Overlays | Pins on the stage; notes below or in a side panel | Pins on the content; notes in floating cards |
| Likely strengths | Video; phone layouts that reflow; familiar | Long documents (reports, op-eds) you pan and zoom into; spatial annotation |
| Likely risks | Long documents become a tall scroll | Floating panels crowd a phone screen; pan and zoom cost more to render (WSG 3.1) |

**Prototype matrix.** Build each cell with audit examples.

| Content type | Stage | Canvas | Requirements-only | Example to use |
|---|---|---|---|---|
| Short-form video | ☐ | ☐ | ☐ | Medical Society of Virginia short |
| Long-form video or speech | ☐ | ☐ | ☐ | Lawson's heat-dome speech |
| Social post (text and image) | ☐ | ☐ | ☐ | POW "signs are everywhere"; Diggins "I voted" |
| News article or interview | ☐ | ☐ | ☐ | Howard on wildfire smoke |
| Op-ed or blog post | ☐ | ☐ | ☐ | Seattle op-ed; Suter op-ed; Vossler post |
| News release | ☐ | ☐ | ☐ | Nursing leaders on extreme heat |
| Contrast pair (two items) | ☐ | ☐ | ☐ | Lawson vs. Seattle op-ed; Howard vs. Vossler; Suter vs. Diggins "I voted" |
| Report or talking-points memo | ☐ | ☐ | ☐ | To be sourced |

**Decision criteria** (each traces to a job):
- Can Dr. Maya tell in seconds whether it's for her, on a phone? (J2)
- Can she find why it works without being lectured? (J4)
- Can she see the pattern she'd borrow? (J5)
- Does it handle long documents and video equally well? (J2, J4)
- Does it export cleanly to a slide or PDF page? (J4, J6)
- How much does it weigh, and does it stay usable on a slow connection? (J1, J2; WSG 2.17, 3.1)

---

## 8. Model reference payload (6.6)

So an example can act as a model inside an AI tool (J5), the platform exposes a payload per "Good example." It can be copied from the detail view and read by system clients.

The payload contains:
- messenger role and audience
- `structure` (ordered moves) and `doable_step`
- `why_it_works`, principle grades and the relevant parts of `grading_analysis_md`
- `for_everyone_notes`
- an excerpt within rights limits (full text only if `rights_status` allows)
- an instruction to imitate structure and tone, **not wording**, and keep the user's own voice

A contrast pair can be loaded as one payload with "do this / avoid this" framing. Keep payloads small: only the fields the model needs (WSG 3.11, 5.19). (Trace: J5. Scope: Pilot.)

---

## 9. Content rules

| ID | Rule | Trace |
|---|---|---|
| CR-1 | Plain language in every TCC-written field, following the *Eight Principles for Effective and Inviting Climate Communication*. | J1, J4 |
| CR-2 | At most one quote per source, under 15 words, credited and linked. | J1, J3 |
| CR-3 | No real photos of messengers without rights; default to an illustrated initial. | J1 |
| CR-4 | Say "TCC curated," never "TCC endorsed," and never imply the messenger's institution endorses TCC. | J6 |
| CR-5 | Show recency; label older pieces "evergreen" rather than dropping them. | J2 |
| CR-6 | No platform logos in TCC-rendered variants; name platforms in text. | J2 |
| CR-7 | Third parties are removed from renders (IN-5). | J6 |
| CR-8 | Flag sponsorship and partisan framing on the card, not only in the detail view. | J2, J6 |

---

## 10. States

| State | Behavior | Trace |
|---|---|---|
| Loading | Skeleton matching the variant | J2 |
| Link-only (`rights_status`) | Metadata, why it works and pattern; no text, renders or media; prominent "View original" | All |
| Original removed | Keep the record, captured text and renders; label "Original no longer online," with capture date | J4, J6 |
| Outdated | Notice that guidance is superseded; link a replacement or retire it | J6 |
| Pending review | Visible to curators and the contributor only | J7 |
| Not yet usable | Visible to curators only, with the reason | J4 |
| No results (library filters) | Suggest the nearest match by topic or place; offer "Request an example" | J2 |
| Offline or slow connection | Text and why-it-works still render; media shows its preview and size (WSG 2.17, 4.2) | J1, J2 |

---

## 11. Accessibility and inclusion

- Verdicts and grades use text and symbols, never color alone. (J4)
- Video carries captions; transcripts come from `full_text_md`. (J2, J4)
- Overlay pins are keyboard-reachable, and every note is also available as a list below the content. (J4)
- Renders have alt text summarizing the artifact. (J1, J4)
- Semantic headings, visible focus states and WCAG 2.2 AA contrast in every variant. (All)
- Respect `prefers-reduced-motion`, `prefers-color-scheme` and `prefers-contrast` (WSG 2.10, 3.9). (All)
- Core content works without JavaScript; scripts only enhance (WSG 3.10 progressive enhancement). (J1, J2)
- Usable on older phones and slow or unstable connections (WSG 2.17). (J1, J2)

---

## 12. Web sustainability (W3C WSG)

TCC's credibility depends on practicing what it promotes, so the platform should be light by design. These requirements apply the WSG to this component. We claim **alignment**, not conformance: the WSG warns against presenting partial improvements as proof of sustainability (WSG 1.4.3), and greenwashing would undercut trust (J6).

### 12.1 User experience design
| ID | Requirement | WSG | Trace | Scope |
|---|---|---|---|---|
| WS-1 | Keep journeys short: from a Spotlight to a detail view in one tap, and from filters to a result in seconds. | 2.4 | J1, J2 | Pilot |
| WS-2 | Overlays, notes and secondary panels stay collapsed until asked for; no pop-ups on arrival. | 2.5 | J4 | Pilot |
| WS-3 | No deceptive patterns in sign-up (Join); analytics only with consent and only what the pilot signals need (section 15). | 2.6 | J3 | Pilot |
| WS-4 | Build every variant from the TCC design system's tokens and components; load only the components a page uses. | 2.8 | All | Pilot |
| WS-5 | Media: include renders only where they aid understanding; serve responsive sizes in modern formats (AVIF/WebP with fallback); lazy-load anything below the first screen. | 2.9 | J1, J2, J4 | Pilot |
| WS-6 | Animation only when it explains something (e.g., moving to a pin); honor reduced motion. | 2.10 | J4 | Pilot |
| WS-7 | Limit web fonts to the design system's two families and the weights used, self-hosted and subset, with system-font fallbacks. | 2.11, 3.5 | All | Pilot |
| WS-8 | Downloads (precedent sheet, exports) prefer HTML with a print stylesheet; PDFs are compressed and generated once, then reused. | 2.13 | J4, J6 | Pilot |
| WS-9 | Test prototypes with clinicians before building production code; the three prototypes exist for this reason. | 2.3, 2.14, 2.16 | All | Pilot |
| WS-10 | Notifications (digest, starter pack) are opt-in with easy unsubscribe. | 2.12 | J3, J7 | Pilot |

### 12.2 Web development
| ID | Requirement | WSG | Trace | Scope |
|---|---|---|---|---|
| WS-11 | Set a performance budget per variant and check it on every release. Proposed starting budgets, to confirm in prototyping: library page ≤ 300 KB and detail view ≤ 500 KB before media is requested. | 3.1, 5.24 | J1, J2 | Pilot |
| WS-12 | Prefer static pages generated from the records over dynamic rendering. | 3.14 | All | Pilot |
| WS-13 | Plain HTML, CSS and minimal JavaScript; no framework unless a need is shown; keep a dependency inventory. | 3.6, 3.12 | All | Pilot |
| WS-14 | No third-party requests on page load; third-party media loads only on user action. | 3.5 | J1, J2 | Pilot |
| WS-15 | Include schema.org structured data (ST-7) and expected files (sitemap, robots.txt, carbon.txt). | 3.8, 3.13 | J2, J5 | Pilot |
| WS-16 | Support dark mode, reduced data, reduced motion and print through media queries. | 3.9 | All | Pilot |

### 12.3 Hosting and data
| ID | Requirement | WSG | Trace | Scope |
|---|---|---|---|---|
| WS-17 | Choose hosting that discloses its energy sources and efficiency. | 4.1 | All | Pilot (decision), ongoing |
| WS-18 | Cache static pages and assets with versioned file names; keep the library readable during brief outages. | 4.2 | J2 | Pilot: caching. Later: offline mode. |
| WS-19 | Engagement refresh on a schedule (IN-10); no continuous polling. | 4.7 | J7 | Pilot |
| WS-20 | Store only the data the jobs need; aggregate comments; de-identify third parties. | 4.12, 5.18 | J6, J7 | Pilot |

### 12.4 Strategy and governance
| ID | Requirement | WSG | Trace | Scope |
|---|---|---|---|---|
| WS-21 | Mark AI-assisted grading and keep a human reviewer (GV-4). | 5.19 | J4, J6 | Pilot |
| WS-22 | Name a sustainability advocate on the build team. | 5.2 | All | Pilot |
| WS-23 | Review planet, people and prosperity impacts at the start and at regular intervals, and publish a short sustainability statement. | 2.1, 5.6 | All | Later |

---

## 13. Governance

| ID | Requirement | Trace | Scope |
|---|---|---|---|
| GV-1 | A TCC curator grades P1–P8, writes the analysis and sets the verdict. A clinician reviewer checks health claims before publishing. | J4, J6 | Pilot |
| GV-2 | A written rubric defines each grade level for each principle, with versioning. | J4 | Pilot |
| GV-3 | Calibrate graders: a sample of records is graded independently by two curators and differences resolved. | J4 | Pilot (light) |
| GV-4 | AI-assisted grades are marked as such until a curator reviews them. | J4, J6 | Pilot, if AI assistance is used |
| GV-5 | Request permission from creators for text, render or media reuse; record it in `rights_status`. | All | Pilot |
| GV-6 | Re-check links and recency at least twice a year, and before seasonal hooks (e.g., smoke season). | J2, J6 | Pilot |
| GV-7 | Contributions go through the same review as curated examples. | J7 | Pilot |

---

## 14. Future capabilities (not required now)

Build these only when users ask for them *and* they serve TCC's Theory of Change.

| Capability | Why it might matter | Signal that would trigger it | Trace |
|---|---|---|---|
| **Five-level grading plus "not applicable"** | Finer distinctions for analysis and AI tools | Curators or AI-tool users find the pilot scale too coarse to separate examples | J4, J5 |
| **Estimated reach model** | Helps TCC prioritize amplification | TCC needs to compare reach across platforms for funders or for reshare decisions | J7 |
| **Comment summaries** (IN-13) | Shows whether a piece polarized its audience (P8) | Curators find P8 hard to grade without audience reaction | J4, J6 |
| **Full audience segmentation model** | Better matching of examples to audiences | Messengers ask for examples by audience, not just topic | J2, J5 |
| **Batch re-indexing tooling** (ST-5) | Keeps tags current as models change | The library outgrows manual re-tagging | J2 |
| **Partner embeds and system write access** | Distribution beyond TCC's site | A partner asks to embed the library or submit records | J2, J7 |
| **Remaining content types** (IN-1) | Broader library | Messengers ask for formats the pilot lacks | J2, J5 |
| **Example conversations** (IN-9) | Models for one-to-one talk, which TCC's research says invites people in | Messengers ask how to *talk*, not just post | J5 |
| **Native slide formats** (6.10) | Easier reuse in decks | Exports are reused often enough that image slides become friction | J4 |
| **Offline library** (WS-18) | Access in clinics with poor signal | Messengers report using the library where connections fail | J2 |
| **Sustainability statement** (WS-23) | Transparency for funders and partners | TCC or funders ask for reporting | All |

---

## 15. How we'll know it works

Directional signals for the pilot, not targets. Collect them with consent and aggregated (WS-3).

| Job | Signal |
|---|---|
| J1 Permission | Click-through from Spotlight to the library |
| J2 Fit | Time to first opened or saved example after filtering |
| J3 Value | Starter-pack sign-up rate |
| J4 Good is visible | Messengers can explain why one example in a pair is stronger; overlay use |
| J5 Borrowable | "Use as a model" actions; principle grades of drafts made with examples vs. without |
| J6 Cover | Messengers report easier approval; precedent sheet downloads |
| J7 Connection | "Made with" posts; contributions; reach of TCC-reshared pieces vs. their earlier engagement snapshots |
| All (WSG) | Page weight per variant against budget; share of pages loading no third-party resources |

---

## 16. Open questions to test

1. **Stage, Canvas or neither?** Which model, or which mix, works across content types on a phone? (Section 7.2)
2. **Overlays on others' work:** Do messengers trust annotations on someone else's content, and do creators accept them?
3. **Pair or single?** Do clinicians learn more from a contrast pair, or does the weaker example feel like a lecture?
4. **How much "why"?** Is two or three sentences right, or does she skip it?
5. **Badge willingness:** Will messengers add a "made with TCC" link to their post?
6. **Gatekeeper fit:** What does a hospital comms office need on a precedent sheet?
7. **Engagement for messengers:** Does showing engagement help or distract? (Pilot keeps it internal.)
8. **Contributors' grades:** Should contributors see how their own pieces were graded?
9. **AI handoff:** Can messengers easily get the payload into the chatbot they already use?
10. **Weight vs. richness:** Does the Canvas model's extra rendering cost buy enough understanding to justify it? (WSG 3.1)
