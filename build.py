#!/usr/bin/env python3
"""Builds the static pages of thefreedomrenaissanceproject.com from one shared template.
Run:  python3 build.py      (needs pandoc for the white paper page)"""
import html, re, subprocess, pathlib

ROOT = pathlib.Path(__file__).parent
SITE = "https://www.thefreedomrenaissanceproject.com"

ICONS = {
    "story": '<path d="M4 19.5V5a2 2 0 0 1 2-2h13v15H6a2 2 0 0 0-2 2zm0 0A2 2 0 0 0 6 22h13"/><path d="M9 7h6M9 11h6"/>',
    "idea": '<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-3.6 10.8c.8.6 1.1 1.4 1.1 2.2h5c0-.8.3-1.6 1.1-2.2A6 6 0 0 0 12 3z"/>',
    "plan": '<path d="M3 6l6-3 6 3 6-3v15l-6 3-6-3-6 3z"/><path d="M9 3v15M15 6v15"/>',
    "place": '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "white-paper": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
    "join": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M19 8v6M22 11h-6"/>',
}
NAV = [
    ("story", "The Back Story", "Why one mortgage banker started this."),
    ("idea", "The Idea", "The property tax is a tax on owning."),
    ("plan", "The Plan", "Start where change is possible: one county."),
    ("place", "The Place", "Six hints. The name comes after you register."),
    ("white-paper", "The White Paper", "The academic case, with sources."),
]

def icon(key):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[key]}</svg>'

def features(active=None, compact=False):
    out = ['<div class="features">']
    for key, title, sub in NAV:
        cls = "feature active" if key == active else "feature"
        out.append(f'''  <div class="{cls}">
    <a class="feature-icon" href="{key}.html" aria-label="{title}">{icon(key)}</a>
    <div><h3><a href="{key}.html">{title}</a></h3>{'' if compact else f'<p>{sub}</p>'}</div>
  </div>''')
    out.append("</div>")
    return "\n".join(out)

BRAND = '''<a class="brand" href="index.html" aria-label="The Freedom Renaissance Project home">
  <span class="brand-mark"><img src="assets/mark.svg" alt=""></span>
  <span><p class="brand-title">The</p><p class="brand-name">Freedom <span class="grad">Renaissance</span> Project</p></span>
</a>'''

def page(slug, title, desc, body):
    full_title = "The Freedom Renaissance Project" if slug == "index" else f"{title} | The Freedom Renaissance Project"
    url = SITE + "/" + ("" if slug == "index" else f"{slug}.html")
    ld = ""
    if slug == "index":
        ld = '''<script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization","name":"The Freedom Renaissance Project","url":"%s","logo":"%s/assets/mark.svg","description":"%s"}</script>''' % (SITE, SITE, html.escape(desc))
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{html.escape(full_title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta name="theme-color" content="#070b18">
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,500;1,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="site.css?v=1">
{ld}
</head>
<body>
<div class="page">
{body}
<footer class="page-footer">
  <div>&copy; 2026 The Freedom Renaissance Project. An idea, a plan and a place.<br>Nothing on this site is legal, tax or investment advice.</div>
  <nav aria-label="Site">
    <a href="index.html">Home</a><a href="story.html">Story</a><a href="idea.html">Idea</a><a href="plan.html">Plan</a><a href="place.html">Place</a><a href="white-paper.html">White Paper</a><a href="join.html">Register</a>
  </nav>
</footer>
</div>
<nav class="footer-bar" aria-label="Quick actions">
  <a class="footer-btn footer-cta" href="join.html">Register</a>
  <div class="fb-divider"></div>
  <a class="footer-btn footer-wp" href="white-paper.html" aria-label="Read the white paper">{icon("white-paper")}<span>White Paper</span></a>
  <div class="fb-divider"></div>
  <a class="footer-btn" href="index.html" aria-label="Home"><svg viewBox="0 0 24 24"><path d="M3 11l9-8 9 8"/><path d="M5 10v10h14V10"/></svg></a>
</nav>
<script src="site.js?v=1"></script>
</body>
</html>
'''

def inner(slug, eyebrow, heading, lede, caption, article):
    return f'''<div class="page-hero">
  <div class="hero-copy">
    {BRAND}
    <p class="eyebrow">{eyebrow}</p>
    <h1 class="page-heading">{heading}</h1>
    <p class="lede">{lede}</p>
    {features(slug, compact=True)}
  </div>
  <div class="hero-art"><img src="assets/frontier.svg" alt="Dawn breaking over open prairie and a small homestead"><div class="caption">{caption}</div></div>
</div>
<article class="article">
{article}
</article>'''

PAGES = {}

# ---------------- HOME ----------------
PAGES["index"] = ("Home",
"A movement to eliminate property taxes, starting in one small American county. An idea, a plan and a place.",
f'''<div class="hero">
  <div class="hero-copy">
    {BRAND}
    <h2 class="headline">The Wild, Wide&#8209;Open Frontier for <em class="grad">True Ownership.</em></h2>
    <p class="lede">A peaceful movement to eliminate the property tax, <strong>starting in one small American county</strong> where a few hundred committed neighbors can make it happen. Not by fighting. By moving, voting and building.</p>
    {features()}
    <div class="cta-row">
      <a class="btn btn-primary" href="join.html">Register &amp; learn the county</a>
      <a class="btn btn-ghost" href="white-paper.html">Read the white paper</a>
    </div>
  </div>
  <div class="hero-art">
    <img src="assets/frontier.svg" alt="Dawn breaking over open prairie and a small homestead">
    <div class="caption">If you have to keep paying for it,<br>do you really own it?<small>An idea &middot; A plan &middot; A place</small></div>
  </div>
</div>''')

# ---------------- STORY ----------------
PAGES["story"] = ("The Back Story", "How a San Diego mortgage banker decided to spend his second act on one idea: ending the property tax somewhere in America.",
inner("story", "The Back Story", "A second act worth <em class='grad'>more than a lake house.</em>",
"Success can conquer the economy's problems for one family. It rarely fixes them for anyone else.",
"It started with a simple question<small>What is my legacy?</small>",
'''<p>I was scrolling through social media one evening when I landed on a channel that stopped people driving exceptional cars and asked them for their keys to success. The advice was so good I went back, watched all eight of them again, and took notes.</p>
<p>Afterward something nagged at me. Every one of those people had mastered the economy. Their children and grandchildren were probably set for life. But none of them had changed the rules that make getting ahead so hard for everyone else. They had beaten the game, not fixed it.</p>
<h2>Built, lost, rebuilt</h2>
<p>Business came naturally to me early. Then the 2008 crash took down my real estate development and mortgage banking companies. The years that followed were a grind: a corporate mortgage job, an internet lending venture for a private equity firm that ended after eighteen months, and finally a new mortgage and real estate brokerage built with people I trust.</p>
<p>We kept the house, put two great kids through out-of-state colleges, and kept going. I learned to run my personal life like a business, to work the late nights and weekends, and eventually to like the grind. It made me humble and thankful. A health scare along the way reminded me what actually matters: faith, family, health, relationships. Money is the soil you work so those things can grow.</p>
<h2>The question</h2>
<p>Thinking about a second act, I pictured the usual: a lake house with a boat, a coastal cottage, a cabin in the middle of nowhere. Then I asked what the point would be. I wanted something with more meaning — a legacy for my kids and future grandkids that also made a difference for people outside my own family.</p>
<blockquote>Leaving your kids better off helps your own clan. It does nothing about why it keeps getting harder for everyone to get ahead.</blockquote>
<p>That question led me to taxes, and then to the one tax I handle every single day in my work. <a href="idea.html">That's the idea.</a></p>'''))

# ---------------- IDEA ----------------
PAGES["idea"] = ("The Idea", "Why the property tax is a regressive, recurring tax on unrealized and illiquid wealth, and why it deserves to be rethought.",
inner("idea", "The Idea", "A tax on owning <em class='grad'>is a tax on freedom.</em>",
"For most households it's the second-biggest housing cost after the mortgage. It starts the first year you own your home, and it never stops.",
"Bought is not the same as owned<small>The property tax starts the first year and never ends</small>",
'''<h2>Why it's unjust and un-American</h2>
<p>To own something is to hold it free and clear. A home bought with income that was already taxed should meet that test from the day you buy it. It does not. From the first year, and every year after, the owner must pay again to keep it, and if the payments stop, the government sells it. A mortgage has nothing to do with it: a home with no loan at all faces the same bill and the same sale. That is not ownership. It is rent owed to the state on property you already bought.</p>
<p>No other major asset is treated this way. Stocks, bonds, savings, retirement accounts, gold and art are not taxed simply for being owned; they are taxed when they are sold or when they produce income. The family home, the asset most Americans spend their working lives paying for, is taxed every year for as long as they hold it.</p>
<p>The idea is not new. In 1848, Marx and Engels's <em>Communist Manifesto</em> set out ten measures to &ldquo;centralize all instruments of production in the hands of the state.&rdquo; The first plank reads:</p>
<blockquote>&ldquo;Abolition of property in land and application of all rents of land to public purposes.&rdquo;</blockquote>
<p>The Manifesto does not call for a property tax. It calls for ending private ownership of land outright, openly describes its program as &ldquo;despotic inroads on the rights of property,&rdquo; and says the change would come &ldquo;by degree.&rdquo; A perpetual property tax does that work quietly. No law has to abolish ownership. The owner keeps the title, the state collects rent on it every year, and when the payments stop, the county sells the home.</p>
<p>That pressure falls hardest on the family estate. The Manifesto&rsquo;s third plank demands the &ldquo;abolition of all right of inheritance.&rdquo; The property tax never says that either, but it accomplishes much of it. A home left to children arrives with a bill that never ends. Heirs who cannot carry it year after year, on top of their own housing costs, must sell or risk losing it at auction, and the family&rsquo;s largest store of wealth is pried away from the next generation one tax bill at a time.</p>
<p>The enforcement is draconian. Fall behind on income taxes and the IRS has ten years to collect, can accept less than the full amount through an offer in compromise, offers payment plans, and generally needs a court order to take a primary home. Fall behind on property taxes and there is no settlement for less than what is owed, no forgiveness, and in most states the debt never expires. Penalties pile up, and after a few years of nonpayment the county can sell the home at public auction, in many states without any court judgment. The terms are simple: pay, or lose your house. Until the Supreme Court's 2023 <em>Tyler v. Hennepin County</em> ruling, some counties even kept the owner's equity above the debt.</p>
<p>It falls hardest on people whose income does not keep pace with the value of their home: young families stretching to buy their first house, workers whose pay is flat, and retirees on Social Security. The bill follows the home's value, not the owner's income, and it continues every year for as long as they own it.</p>
<h2>It also fails as a tax</h2>
<h3>1. It's regressive</h3>
<p>Because a home is a much bigger multiple of income for a working family than for a wealthy one, the property tax takes a larger share of income from people with less. Even researchers who generally favor higher taxes on the wealthy agree on this point.</p>
<h3>2. It taxes wealth you haven't realized — and can't easily sell</h3>
<p>Mention a tax on unrealized capital gains to an investor and they object instantly: the gain is only on paper, it could disappear, and you'd have to sell to pay. A market-value property tax is worse on every count. It taxes the <em>whole</em> value, not just the gain, every single year. And you can't sell one percent of your house to pay the bill.</p>
<blockquote>If you have to keep paying to keep it, do you own it — or are you renting it from the government?</blockquote>
<h2>Read the real books</h2>
<p>Every state and most cities and counties publish an audited <strong>Annual Comprehensive Financial Report</strong> (ACFR). Where the budget tells you what was spent, the ACFR shows what the government owns — land, buildings, investments, reserves — and what it owes. It's what bond buyers read before lending. Taxpayers should read it too, before anyone tells them a tax increase is unavoidable.</p>
<p class="note">The full argument, with sources and the strongest counterarguments, is in <a href="white-paper.html">the white paper</a>.</p>'''))

# ---------------- PLAN ----------------
PAGES["plan"] = ("The Plan", "The strategy: concentrate committed residents in one low-population, low-tax county and eliminate the property tax there first.",
inner("plan", "The Plan", "Don't try everywhere. <em class='grad'>Finish somewhere.</em>",
"Statewide change means persuading millions. In a county of under 2,000 people, a hundred committed neighbors can swing an election.",
"Vote with your feet,<br>your dollars and your ballot",
'''<p>Nothing can be done about property taxes in San Diego; Proposition 13 sets the rules statewide, and changing state law runs into the same wall as federal income tax. But in many states, <strong>counties</strong> set their own share of the levy, and a county is usually governed by a commission of just three to five people.</p>
<p>So the strategy is simple: start where taxes are already low, where residents already dislike them, where few people live, and where replacement revenue is easiest to find. Then don't just "get traction." Finish the job.</p>
<h2>Why small works</h2>
<p>In a county of about 2,000 people, 100 new residents are 5 percent of the population — enough to swing most local races. A few hundred are enough for newcomers to run for office themselves. A hundred people is not a mass movement. It's a team.</p>
<h2>How we do it</h2>
<div class="steps">
  <div class="step"><h4>Gather</h4><p>Register, tell us your commitment level, and help us reach critical mass before anyone buys or moves.</p></div>
  <div class="step"><h4>Open the books</h4><p>Publish a plain-language summary of the county's audited financial report: reserves, income, assets, liabilities.</p></div>
  <div class="step"><h4>Build the budget</h4><p>Show, line by line, how the sheriff, courts, roads and elections stay funded without the operating levy.</p></div>
  <div class="step"><h4>Move &amp; vote</h4><p>Make the county your real home, register, show up, and run for office.</p></div>
  <div class="step"><h4>Phase it out</h4><p>Retire the levy in stages, protecting current owners so no one is hurt along the way.</p></div>
</div>
<h2>Peaceful by design</h2>
<p>Wars have been fought over less. We don't need to fight anyone. We only need to exercise rights Americans already have: to move, to buy or rent a home, and to vote where we live. And because the county already has very low taxes, the people there are natural allies. Eliminating the tax benefits them and their grandchildren as much as us.</p>
<h2>Then it spreads</h2>
<p>Once one county shows it can be done, neighbors notice. Several of the nine states without a broad income tax are among the fastest-growing in the country. In 2010 only a few states allowed permitless carry; today more than half do. Good ideas that work spread on their own. We just have to prove it once.</p>
<p class="note"><strong>Residency is real residency.</strong> Voting rights follow genuine domicile. Participants should plan to make the county their principal home; registering to vote at a property you don't actually live in can be a crime. We'll share the specific state rules with registered members.</p>'''))

# ---------------- PLACE ----------------
PAGES["place"] = ("The Place", "Hints about the first Freedom Renaissance county. Register to learn which county it is.",
inner("place", "The Place", "So where is it? <em class='grad'>Not yet.</em>",
"Our forefathers crossed an ocean for freedom. This trip is a lot shorter — and it's in the lower 48.",
"Wide-open land<br>Wide-open future<small>Hints below</small>",
'''<p>You can build a good community almost anywhere: a dream house, good neighbors, family and friends. What you can't build is freedom where the rules won't let you. So we chose the place by its rules first.</p>
<p>It's in America, it's not Alaska or Hawaii, and you can fly to anywhere in the lower 48 in under five hours. We're keeping the name private until enough people have registered, to protect the effort from land speculators and early opposition.</p>
<div class="hints">
  <div class="hint"><b>Hint 1</b><span>A county of fewer than 2,000 people.</span></div>
  <div class="hint"><b>Hint 2</b><span>No state income tax.</span></div>
  <div class="hint"><b>Hint 3</b><span>A town, but no city government — no city taxes or ordinances.</span></div>
  <div class="hint"><b>Hint 4</b><span>No zoning or building permits. Build faster, cheaper, your way.</span></div>
  <div class="hint"><b>Hint 5</b><span>Homes from about $100,000 to $400,000.</span></div>
  <div class="hint"><b>Hint 6</b><span>Land around $500–$1,000 an acre. Forty acres for $20,000–$40,000.</span></div>
  <div class="hint"><b>Bonus</b><span>A constitutional-carry state. Freedom-minded already.</span></div>
</div>
<h2>Freedom over scenery</h2>
<p>This asks something real of you: to put liberty ahead of climate, views, restaurants and stadiums. That's exactly the trade our ancestors made. We're not asking for donations. We're asking for commitment and community.</p>
<p>Once you register, we'll tell you the county and walk you through what it takes to become a genuine full-time resident there.</p>
<p><a class="btn btn-primary" href="join.html" style="text-decoration:none;color:#0b1124">Register to learn the county</a></p>'''))

# ---------------- JOIN ----------------
STATES = "Alabama Alaska Arizona Arkansas California Colorado Connecticut Delaware Florida Georgia Hawaii Idaho Illinois Indiana Iowa Kansas Kentucky Louisiana Maine Maryland Massachusetts Michigan Minnesota Mississippi Missouri Montana Nebraska Nevada New_Hampshire New_Jersey New_Mexico New_York North_Carolina North_Dakota Ohio Oklahoma Oregon Pennsylvania Rhode_Island South_Carolina South_Dakota Tennessee Texas Utah Vermont Virginia Washington West_Virginia Wisconsin Wyoming Outside_the_U.S.".split()
state_opts = "".join(f'<option>{s.replace("_", " ")}</option>' for s in STATES)
inv = ["Move there full time", "Buy land or a home", "Run for local office", "Volunteer or organize",
       "Research and policy", "Spread the word online"]
inv_html = "".join(f'<label class="check"><input type="checkbox" name="involvement" value="{v}"> {v}</label>' for v in inv)
PAGES["join"] = ("Register", "Join the Freedom Renaissance Project. Register to learn the first county and how to get involved.",
inner("join", "Join the Movement", "You're part of a <em class='grad'>Movement</em> now.",
"Register, tell us how committed you are, and we'll tell you where the first county is when we reach critical mass.",
"Step one is<br>raising your hand",
f'''<div class="steps">
  <div class="step"><h4>Register</h4><p>Tell us your commitment level and how you'd like to help. Registered members learn the county.</p></div>
  <div class="step"><h4>Do your own research</h4><p>Read the white paper, check the sources, and look up your own county's financial report.</p></div>
  <div class="step"><h4>Dream the possibilities</h4><p>Picture a county where the day you buy your home, it's truly yours.</p></div>
</div>
</article>
<form class="form-card" id="register-form" action="/api/register" method="post" novalidate>
  <h2>Register</h2>
  <p>No donations. Just commitment and community. We'll never sell your information.</p>
  <div class="form-grid">
    <div class="field"><label for="f-name">Full name *</label><input id="f-name" name="name" autocomplete="name" required></div>
    <div class="field"><label for="f-email">Email *</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
    <div class="field"><label for="f-phone">Mobile (optional)</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
    <div class="field"><label for="f-state">Where do you live now?</label><select id="f-state" name="state"><option value="">Choose a state</option>{state_opts}</select></div>
    <div class="field"><label for="f-commit">Commitment level *</label>
      <select id="f-commit" name="commitment" required>
        <option value="">Choose one</option>
        <option>All in — ready to move</option>
        <option>Seriously considering a move</option>
        <option>Would buy land or a second home</option>
        <option>Supporter — can't move, want to help</option>
        <option>Just curious for now</option>
      </select></div>
    <div class="field"><label for="f-time">Possible timeline</label>
      <select id="f-time" name="timeline"><option value="">Choose one</option><option>Within 6 months</option><option>6–12 months</option><option>1–2 years</option><option>Not sure yet</option></select></div>
    <fieldset class="field full"><legend>How would you like to be involved?</legend><div class="checks">{inv_html}</div></fieldset>
    <div class="field full"><label for="f-msg">Anything you'd like us to know?</label><textarea id="f-msg" name="message"></textarea></div>
    <label class="check updates"><input type="checkbox" name="updates" value="yes" checked> Send me updates, including the county reveal.</label>
    <input class="hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
  </div>
  <div class="form-foot">
    <small>By registering you agree we may email you about the project. Unsubscribe any time.</small>
    <button class="btn btn-primary" type="submit">Register</button>
  </div>
  <div class="form-status" id="form-status" role="status" aria-live="polite"></div>
</form>
<article class="article" style="margin-top:0">'''))

# ---------------- WHITE PAPER ----------------
def white_paper():
    md = (ROOT / "paper.md").read_text()
    body = subprocess.run(["pandoc", "-f", "markdown", "-t", "html5"],
                          input=md, capture_output=True, text=True, check=True).stdout
    body = re.sub(r"<table>", '<div class="table-wrap"><table>', body).replace("</table>", "</table></div>")
    body = body.replace('<a href="http', '<a target="_blank" rel="noopener" href="http')
    heads = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body)
    toc = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in heads)
    article = f'''<p class="paper-meta"><span>A White Paper of The Freedom Renaissance Project</span><span>November 2026</span><span>~6,000 words &middot; 21 references</span></p>
<nav class="toc" aria-label="Contents"><h4>Contents</h4><ol>{toc}</ol></nav>
{body}'''
    return ("The White Paper", "Rethinking the Property Tax: Ownership, Regressivity, and a County-Level Path to Reform. A white paper with sources and counterarguments.",
            inner("white-paper", "White Paper", "Rethinking the <em class='grad'>Property Tax</em>",
                  "Ownership, regressivity, and a county-level path to reform — the academic case, with sources and the strongest counterarguments.",
                  "Evidence,<br>not just argument", article))

if __name__ == "__main__":
    PAGES["white-paper"] = white_paper()
    for slug, (title, desc, body) in PAGES.items():
        (ROOT / f"{slug}.html").write_text(page(slug, title, desc, body))
        print("wrote", slug + ".html")
