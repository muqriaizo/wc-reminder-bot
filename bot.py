"""
⚽ WC 2026 Fixture Reminder Bot
- Checks every 5 minutes for upcoming matches
- Opens a thread + pings @everyone when kickoff is within 1 hour
"""

import discord
from discord.ext import tasks
from datetime import datetime, timezone, timedelta
import os

# ──────────────────────────────────────────────
#  YOUR SETTINGS  (edit these two lines)
# ──────────────────────────────────────────────
TOKEN      = os.environ.get("DISCORD_TOKEN",  "PASTE_BOT_TOKEN_HERE")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "PASTE_CHANNEL_ID_HERE"))

# ──────────────────────────────────────────────
#  TIMEZONE  — Malaysia Time = UTC+8
# ──────────────────────────────────────────────
MYT = timezone(timedelta(hours=8))

def t(month, day, hour, minute=0):
    """Shortcut to create a MYT datetime for 2026."""
    return datetime(2026, month, day, hour, minute, tzinfo=MYT)

# ──────────────────────────────────────────────
#  ALL 72 GROUP STAGE FIXTURES  (MYT)
# ──────────────────────────────────────────────
FLAGS = {
    "Mexico":"🇲🇽","South Korea":"🇰🇷","South Africa":"🇿🇦","Czechia":"🇨🇿",
    "Canada":"🇨🇦","Switzerland":"🇨🇭","Qatar":"🇶🇦","Bosnia & Herzegovina":"🇧🇦",
    "Brazil":"🇧🇷","Morocco":"🇲🇦","Scotland":"🏴󠁧󠁢󠁳󠁣󠁴󠁿","Haiti":"🇭🇹",
    "USA":"🇺🇸","Australia":"🇦🇺","Paraguay":"🇵🇾","Turkey":"🇹🇷",
    "Germany":"🇩🇪","Ecuador":"🇪🇨","Ivory Coast":"🇨🇮","Curacao":"🇨🇼",
    "Netherlands":"🇳🇱","Japan":"🇯🇵","Tunisia":"🇹🇳","Sweden":"🇸🇪",
    "Belgium":"🇧🇪","Iran":"🇮🇷","Egypt":"🇪🇬","New Zealand":"🇳🇿",
    "Spain":"🇪🇸","Uruguay":"🇺🇾","Saudi Arabia":"🇸🇦","Cape Verde":"🇨🇻",
    "France":"🇫🇷","Senegal":"🇸🇳","Norway":"🇳🇴","Iraq":"🇮🇶",
    "Argentina":"🇦🇷","Austria":"🇦🇹","Algeria":"🇩🇿","Jordan":"🇯🇴",
    "Portugal":"🇵🇹","Colombia":"🇨🇴","Uzbekistan":"🇺🇿","DR Congo":"🇨🇩",
    "England":"🏴󠁧󠁢󠁥󠁮󠁧󠁿","Croatia":"🇭🇷","Panama":"🇵🇦","Ghana":"🇬🇭",
}

MATCHES = [
    # ── Group A ─────────────────────────────────────────────────────
    {"id":"m1",  "t1":"Mexico",          "t2":"South Africa",        "grp":"A","venue":"Mexico City",   "ko":t(6,12, 3, 0)},
    {"id":"m2",  "t1":"South Korea",     "t2":"Czechia",             "grp":"A","venue":"Guadalajara",   "ko":t(6,12,10, 0)},
    {"id":"m25", "t1":"Czechia",         "t2":"South Africa",        "grp":"A","venue":"Atlanta",       "ko":t(6,19, 0, 0)},
    {"id":"m28", "t1":"Mexico",          "t2":"South Korea",         "grp":"A","venue":"Guadalajara",   "ko":t(6,19, 9, 0)},
    {"id":"m53", "t1":"South Africa",    "t2":"South Korea",         "grp":"A","venue":"Monterrey",     "ko":t(6,25, 9, 0)},
    {"id":"m54", "t1":"Czechia",         "t2":"Mexico",              "grp":"A","venue":"Mexico City",   "ko":t(6,25, 9, 0)},
    # ── Group B ─────────────────────────────────────────────────────
    {"id":"m3",  "t1":"Canada",          "t2":"Bosnia & Herzegovina","grp":"B","venue":"Toronto",       "ko":t(6,13, 3, 0)},
    {"id":"m5",  "t1":"Qatar",           "t2":"Switzerland",         "grp":"B","venue":"San Francisco", "ko":t(6,14, 3, 0)},
    {"id":"m26", "t1":"Switzerland",     "t2":"Bosnia & Herzegovina","grp":"B","venue":"Los Angeles",   "ko":t(6,19, 3, 0)},
    {"id":"m27", "t1":"Canada",          "t2":"Qatar",               "grp":"B","venue":"Vancouver",     "ko":t(6,19, 6, 0)},
    {"id":"m49", "t1":"Switzerland",     "t2":"Canada",              "grp":"B","venue":"Vancouver",     "ko":t(6,25, 3, 0)},
    {"id":"m50", "t1":"Bosnia & Herzegovina","t2":"Qatar",           "grp":"B","venue":"Seattle",       "ko":t(6,25, 3, 0)},
    # ── Group C ─────────────────────────────────────────────────────
    {"id":"m6",  "t1":"Brazil",          "t2":"Morocco",             "grp":"C","venue":"New Jersey",    "ko":t(6,14, 6, 0)},
    {"id":"m7",  "t1":"Haiti",           "t2":"Scotland",            "grp":"C","venue":"Boston",        "ko":t(6,14, 9, 0)},
    {"id":"m30", "t1":"Scotland",        "t2":"Morocco",             "grp":"C","venue":"Boston",        "ko":t(6,20, 6, 0)},
    {"id":"m31", "t1":"Brazil",          "t2":"Haiti",               "grp":"C","venue":"Philadelphia",  "ko":t(6,20, 8,30)},
    {"id":"m51", "t1":"Morocco",         "t2":"Haiti",               "grp":"C","venue":"Atlanta",       "ko":t(6,25, 6, 0)},
    {"id":"m52", "t1":"Scotland",        "t2":"Brazil",              "grp":"C","venue":"Miami",         "ko":t(6,25, 6, 0)},
    # ── Group D ─────────────────────────────────────────────────────
    {"id":"m4",  "t1":"USA",             "t2":"Paraguay",            "grp":"D","venue":"Los Angeles",   "ko":t(6,13, 9, 0)},
    {"id":"m8",  "t1":"Australia",       "t2":"Turkey",              "grp":"D","venue":"Vancouver",     "ko":t(6,14,12, 0)},
    {"id":"m29", "t1":"USA",             "t2":"Australia",           "grp":"D","venue":"Seattle",       "ko":t(6,20, 3, 0)},
    {"id":"m32", "t1":"Turkey",          "t2":"Paraguay",            "grp":"D","venue":"San Francisco", "ko":t(6,20,11, 0)},
    {"id":"m59", "t1":"Turkey",          "t2":"USA",                 "grp":"D","venue":"Los Angeles",   "ko":t(6,26,10, 0)},
    {"id":"m60", "t1":"Paraguay",        "t2":"Australia",           "grp":"D","venue":"San Francisco", "ko":t(6,26,10, 0)},
    # ── Group E ─────────────────────────────────────────────────────
    {"id":"m9",  "t1":"Germany",         "t2":"Curacao",             "grp":"E","venue":"Houston",       "ko":t(6,15, 1, 0)},
    {"id":"m10", "t1":"Ivory Coast",     "t2":"Ecuador",             "grp":"E","venue":"Philadelphia",  "ko":t(6,15, 7, 0)},
    {"id":"m34", "t1":"Germany",         "t2":"Ivory Coast",         "grp":"E","venue":"Toronto",       "ko":t(6,21, 4, 0)},
    {"id":"m35", "t1":"Ecuador",         "t2":"Curacao",             "grp":"E","venue":"Kansas City",   "ko":t(6,21, 8, 0)},
    {"id":"m55", "t1":"Curacao",         "t2":"Ivory Coast",         "grp":"E","venue":"Philadelphia",  "ko":t(6,26, 4, 0)},
    {"id":"m56", "t1":"Ecuador",         "t2":"Germany",             "grp":"E","venue":"New Jersey",    "ko":t(6,26, 4, 0)},
    # ── Group F ─────────────────────────────────────────────────────
    {"id":"m11", "t1":"Netherlands",     "t2":"Japan",               "grp":"F","venue":"Dallas",        "ko":t(6,15, 4, 0)},
    {"id":"m12", "t1":"Sweden",          "t2":"Tunisia",             "grp":"F","venue":"Monterrey",     "ko":t(6,15,10, 0)},
    {"id":"m33", "t1":"Netherlands",     "t2":"Sweden",              "grp":"F","venue":"Houston",       "ko":t(6,21, 1, 0)},
    {"id":"m36", "t1":"Tunisia",         "t2":"Japan",               "grp":"F","venue":"Monterrey",     "ko":t(6,21,12, 0)},
    {"id":"m57", "t1":"Tunisia",         "t2":"Netherlands",         "grp":"F","venue":"Kansas City",   "ko":t(6,26, 7, 0)},
    {"id":"m58", "t1":"Japan",           "t2":"Sweden",              "grp":"F","venue":"Dallas",        "ko":t(6,26, 7, 0)},
    # ── Group G ─────────────────────────────────────────────────────
    {"id":"m13", "t1":"Belgium",         "t2":"Egypt",               "grp":"G","venue":"Seattle",       "ko":t(6,16, 3, 0)},
    {"id":"m15", "t1":"Iran",            "t2":"New Zealand",         "grp":"G","venue":"Los Angeles",   "ko":t(6,16, 9, 0)},
    {"id":"m38", "t1":"Belgium",         "t2":"Iran",                "grp":"G","venue":"Los Angeles",   "ko":t(6,22, 3, 0)},
    {"id":"m40", "t1":"New Zealand",     "t2":"Egypt",               "grp":"G","venue":"Vancouver",     "ko":t(6,22, 9, 0)},
    {"id":"m65", "t1":"Belgium",         "t2":"New Zealand",         "grp":"G","venue":"Seattle",       "ko":t(6,27, 9, 0)},
    {"id":"m66", "t1":"Egypt",           "t2":"Iran",                "grp":"G","venue":"Los Angeles",   "ko":t(6,27, 9, 0)},
    # ── Group H ─────────────────────────────────────────────────────
    {"id":"m14", "t1":"Spain",           "t2":"Cape Verde",          "grp":"H","venue":"Atlanta",       "ko":t(6,16, 0, 0)},
    {"id":"m16", "t1":"Saudi Arabia",    "t2":"Uruguay",             "grp":"H","venue":"Miami",         "ko":t(6,16, 6, 0)},
    {"id":"m37", "t1":"Spain",           "t2":"Saudi Arabia",        "grp":"H","venue":"Atlanta",       "ko":t(6,22, 0, 0)},
    {"id":"m39", "t1":"Uruguay",         "t2":"Cape Verde",          "grp":"H","venue":"Miami",         "ko":t(6,22, 6, 0)},
    {"id":"m63", "t1":"Spain",           "t2":"Uruguay",             "grp":"H","venue":"Kansas City",   "ko":t(6,27, 6, 0)},
    {"id":"m64", "t1":"Cape Verde",      "t2":"Saudi Arabia",        "grp":"H","venue":"Miami",         "ko":t(6,27, 6, 0)},
    # ── Group I ─────────────────────────────────────────────────────
    {"id":"m17", "t1":"France",          "t2":"Senegal",             "grp":"I","venue":"New Jersey",    "ko":t(6,17, 3, 0)},
    {"id":"m18", "t1":"Iraq",            "t2":"Norway",              "grp":"I","venue":"Boston",        "ko":t(6,17, 6, 0)},
    {"id":"m42", "t1":"France",          "t2":"Iraq",                "grp":"I","venue":"Philadelphia",  "ko":t(6,23, 5, 0)},
    {"id":"m43", "t1":"Norway",          "t2":"Senegal",             "grp":"I","venue":"New Jersey",    "ko":t(6,23, 8, 0)},
    {"id":"m61", "t1":"Norway",          "t2":"France",              "grp":"I","venue":"Boston",        "ko":t(6,27, 3, 0)},
    {"id":"m62", "t1":"Senegal",         "t2":"Iraq",                "grp":"I","venue":"Toronto",       "ko":t(6,27, 3, 0)},
    # ── Group J ─────────────────────────────────────────────────────
    {"id":"m19", "t1":"Argentina",       "t2":"Algeria",             "grp":"J","venue":"Kansas City",   "ko":t(6,17, 9, 0)},
    {"id":"m20", "t1":"Austria",         "t2":"Jordan",              "grp":"J","venue":"San Francisco", "ko":t(6,17,12, 0)},
    {"id":"m41", "t1":"Argentina",       "t2":"Austria",             "grp":"J","venue":"Dallas",        "ko":t(6,23, 1, 0)},
    {"id":"m44", "t1":"Jordan",          "t2":"Algeria",             "grp":"J","venue":"San Francisco", "ko":t(6,23,11, 0)},
    {"id":"m67", "t1":"Argentina",       "t2":"Jordan",              "grp":"J","venue":"Kansas City",   "ko":t(6,28, 3, 0)},
    {"id":"m68", "t1":"Algeria",         "t2":"Austria",             "grp":"J","venue":"Dallas",        "ko":t(6,28, 3, 0)},
    # ── Group K ─────────────────────────────────────────────────────
    {"id":"m21", "t1":"Portugal",        "t2":"DR Congo",            "grp":"K","venue":"Houston",       "ko":t(6,18, 1, 0)},
    {"id":"m24", "t1":"Uzbekistan",      "t2":"Colombia",            "grp":"K","venue":"Mexico City",   "ko":t(6,18,10, 0)},
    {"id":"m45", "t1":"Portugal",        "t2":"Uzbekistan",          "grp":"K","venue":"Houston",       "ko":t(6,24, 1, 0)},
    {"id":"m48", "t1":"Colombia",        "t2":"DR Congo",            "grp":"K","venue":"Guadalajara",   "ko":t(6,24,10, 0)},
    {"id":"m69", "t1":"Portugal",        "t2":"Colombia",            "grp":"K","venue":"Philadelphia",  "ko":t(6,28, 6, 0)},
    {"id":"m70", "t1":"DR Congo",        "t2":"Uzbekistan",          "grp":"K","venue":"Atlanta",       "ko":t(6,28, 6, 0)},
    # ── Group L ─────────────────────────────────────────────────────
    {"id":"m22", "t1":"England",         "t2":"Croatia",             "grp":"L","venue":"Dallas",        "ko":t(6,18, 4, 0)},
    {"id":"m23", "t1":"Ghana",           "t2":"Panama",              "grp":"L","venue":"Toronto",       "ko":t(6,18, 7, 0)},
    {"id":"m46", "t1":"England",         "t2":"Ghana",               "grp":"L","venue":"Boston",        "ko":t(6,24, 4, 0)},
    {"id":"m47", "t1":"Panama",          "t2":"Croatia",             "grp":"L","venue":"Toronto",       "ko":t(6,24, 7, 0)},
    {"id":"m71", "t1":"England",         "t2":"Panama",              "grp":"L","venue":"New York/NJ",   "ko":t(6,28, 9, 0)},
    {"id":"m72", "t1":"Croatia",         "t2":"Ghana",               "grp":"L","venue":"Vancouver",     "ko":t(6,28, 9, 0)},
]

# ──────────────────────────────────────────────
#  BOT SETUP
# ──────────────────────────────────────────────
intents = discord.Intents.default()
client  = discord.Client(intents=intents)

# Tracks match IDs we've already pinged so we don't double-ping
already_notified = set()

# ──────────────────────────────────────────────
#  BACKGROUND TASK — runs every 5 minutes
# ──────────────────────────────────────────────
@tasks.loop(minutes=5)
async def check_fixtures():
    now     = datetime.now(MYT)
    channel = client.get_channel(CHANNEL_ID)

    if channel is None:
        print("⚠️  Channel not found — check your CHANNEL_ID")
        return

    for m in MATCHES:
        mid  = m["id"]
        diff = (m["ko"] - now).total_seconds()   # seconds until kickoff

        # Skip: already done OR match already started OR more than 1 hour away
        if mid in already_notified:
            continue
        if diff <= 0:
            already_notified.add(mid)             # past match, mark done silently
            continue
        if diff > 3600:
            continue                               # too early, check again later

        # ── Within 1 hour → fire the reminder! ──────────────────────
        mins      = int(diff // 60)
        f1        = FLAGS.get(m["t1"], "")
        f2        = FLAGS.get(m["t2"], "")
        ko_str    = m["ko"].strftime("%H:%M")

        # 1) Post the announcement message with @everyone
        msg = await channel.send(
            f"@everyone\n"
            f"# ⚽  {f1} {m['t1']}  VS  {m['t2']} {f2}\n"
            f"🕐  Kickoff in **{mins} minutes** — {ko_str} MYT\n"
            f"📍  {m['venue']}  ·  Group {m['grp']}"
        )

        # 2) Open a thread from that message
        thread_name = f"{m['t1']} VS {m['t2']}"
        await msg.create_thread(
            name   = thread_name,
            auto_archive_duration = 1440   # auto-close thread after 24 hours
        )

        already_notified.add(mid)
        print(f"✅ Notified: {thread_name} ({mins} min to kickoff)")

# ──────────────────────────────────────────────
#  STARTUP
# ──────────────────────────────────────────────
@client.event
async def on_ready():
    print(f"⚽ WC 2026 Reminder Bot is online as {client.user}")
    print(f"   Watching {len(MATCHES)} fixtures in MYT")
    check_fixtures.start()

client.run(TOKEN)
