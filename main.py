import streamlit as st

# --- Cấu hình trang ---
st.set_page_config(
    page_title="Your Data Export Survival Guide (Now 87% More Fun!)",
    page_icon="🤪",
    layout="wide"
)

# --- CSS tùy chỉnh ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');

    body {
        font-family: 'Inter', sans-serif;
        color: #e0e0e0;
    }

    .st-emotion-cache-18ni7ap, .st-emotion-cache-h4xjwg {
        display: none;
    }

    .main-title {
        font-size: 4.0rem;
        font-weight: 900;
        text-align: center;
        background: -webkit-linear-gradient(45deg, #ff007f, #00ffcc);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 0.2em 0;
    }

    .sub-header {
        text-align: center;
        font-size: 1.15rem;
        color: #a1a1aa;
        font-weight: 400;
        max-width: 700px;
        margin: 0 auto 2rem auto;
        line-height: 1.6;
    }
    
    h2, h3 {
        font-weight: 700;
        color: #ffffff;
    }
    
    .highlight-box {
        background: linear-gradient(135deg, rgba(255, 0, 127, 0.1), rgba(0, 255, 204, 0.1));
        border-left: 4px solid #00ffcc;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.1), rgba(255, 177, 43, 0.1));
        border-left: 4px solid #ff6b6b;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .tip-box {
        background: linear-gradient(135deg, rgba(81, 207, 102, 0.1), rgba(34, 197, 94, 0.1));
        border-left: 4px solid #51cf66;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1 class='main-title'>Your Data Export Survival Guide</h1>", unsafe_allow_html=True)
st.markdown(
    """
    <div class='sub-header'>
    🎉 Congratulations! You've stumbled upon the unicorn of data exports. No more awkward begging, no more "it's still processing" nightmares, no more sad carrier pigeons to Irvine! 🐦
    <br><br>
    This guide will transform you from a confused data peasant into a CSV-wielding wizard faster than you can say "WHERE clause". Buckle up, buttercup! 🚀✨
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# --- Quick Start ---
st.header("🚀 Quick Start (For People Who Don't Read Manuals)")
st.markdown(
    """
    <div class='highlight-box'>
    <h3>🏃‍♂️ The "I Just Want My Data" Version:</h3>
    1. Pick a report from the sidebar (eeny, meeny, miny, moe works fine)<br>
    2. Enter Workspace ID + Storefront EID (yes, both are required - no, complaining won't change this)<br>  
    3. Choose dates (not your birth date, the data dates)<br>
    4. Click "Get Data" → Twiddle thumbs → Click "Export Full Data" → Download CSV<br>
    5. Do a victory dance! 💃🕺
    </div>
    """, 
    unsafe_allow_html=True
)

st.divider()

# --- The Golden Rules ---
st.header("🏆 The Sacred Commandments (Violate These and Face Digital Purgatory)")

st.subheader("👑 Commandment #1: Thou Shalt Know Thy Numbers")
st.markdown(
    """
    <div class='tip-box'>
    <strong>Workspace ID</strong> 🏢: This magical number is your VIP pass to the data kingdom. If you don't know it, you're basically trying to enter a nightclub without being on the list. Ask your team lead, check your existing reports, or consult your local data shaman.
    <br><br>
    <strong>Storefront EID</strong> 🏬: These are your shop identities (not your life crisis identities). You can juggle multiple ones, but they MUST be from the same workspace family. Don't try to create some weird data family reunion with distant cousins from other workspaces! 
    <br><br>
    <strong>Pro Tip:</strong> Use the "Storefront in Workspace" report first - it's like a dating app, but for finding your perfect storefront matches! 💕
    </div>
    """, 
    unsafe_allow_html=True
)

st.subheader("⏰ Commandment #2: The Sacred Date Range Rituals")
st.markdown(
    """
    <div class='warning-box'>
    <h4>🚨 BREAKING NEWS: Physics Still Applies to Data!</h4>
    
    <strong>1-2 storefronts:</strong> Maximum 60 days (like a good vacation)<br>
    <strong>3-5 storefronts:</strong> Maximum 30 days (like a short vacation)<br>
    <strong>More than 5:</strong> You're being greedy. Keep it under 30 days or our servers will stage a revolt! ⚔️
    <br><br>
    <strong>Why these limits exist?</strong> Because every query is like asking someone to move your entire apartment. Do it too often or ask for too much, and they'll pretend they never met you. Our servers have feelings too! 🥺💔
    </div>
    """, 
    unsafe_allow_html=True
)

st.subheader("🛡️ Commandment #3: The 50,000 Row Apocalypse Prevention Act")
st.markdown(
    """
    <div class='warning-box'>
    <h4>⚖️ This Isn't a Guideline, It's the LAW!</h4>
    
    Try to export more than <strong>50,000 rows</strong> and the system will reject you faster than a bad Tinder profile! 💔🚫
    <br><br>
    <strong>Emergency Escape Plans:</strong><br>
    • Shrink your date range (works 90% of the time, every time)<br>
    • Pick fewer storefronts (less is more, darling)<br>
    • Apply those optional filters like your life depends on it<br>
    • Offer a sincere apology to the database gods with a premium coffee sacrifice ☕🙏<br>
    <br>
    <strong>Why 50k and not 50 million?</strong> Because we learned from the Great Server Meltdown of 2023. Never forget. Never again. 🕯️
    </div>
    """, 
    unsafe_allow_html=True
)

st.divider()

# --- Advanced Features ---
st.header("🎛️ Advanced Wizardry (For Those Who've Transcended Mortal Data Needs)")

st.subheader("🔍 Optional Filters (The Secret Ingredients)")
st.markdown(
    """
    <div class='highlight-box'>
    Some reports come with fancy filters that make you feel like a data chef 👨‍🍳:
    <br><br>
    <strong>Device Type:</strong> Mobile (for thumb scrollers), Desktop (for serious business), or None (for the indecisive)<br>
    <strong>Display Type:</strong> Paid (money talks), Organic (free as a bird), Top (showing off), or None (FOMO much?)<br>
    <strong>Product Position:</strong> Specific rankings or None (because sometimes position doesn't matter 😉)<br>
    <br>
    <strong>Current Plot Twist:</strong> You can only pick one option per filter. It's like being forced to choose your favorite child, but hey, choosing "None" loves them all equally! 🤗
    </div>
    """, 
    unsafe_allow_html=True
)

st.subheader("👀 The Preview Feature (Your Crystal Ball)")
st.markdown(
    """
    <div class='tip-box'>
    ALWAYS preview before you leap! It's like checking if your parachute works before jumping out of a plane 🪂:
    <br><br>
    ✅ First 500 rows (a delicious appetizer)<br>
    ✅ Total estimated rows (the full meal deal)<br>
    ✅ Column count (how many spreadsheet columns you'll need to scroll through)<br>
    ✅ Query speed (faster than your morning coffee brewing?)<br>
    <br>
    If the preview looks suspicious, your full export will probably be a disaster movie. Trust your gut, it's usually smarter than your brain! 🧠➡️❤️
    </div>
    """, 
    unsafe_allow_html=True
)

st.divider()

# --- The Export Process ---
st.header("🎯 The Sacred Export Ritual (Follow These Steps or Face Data Chaos)")

st.markdown("### Step 1: Form Filling Like a Boss")
st.markdown("""
- **Red asterisk fields (*)** are like taxes - unavoidable and mandatory 💸
- **Optional fields** are like dessert - nice to have but you won't die without them 🍰
- **Red error messages** are like your mom telling you to clean your room - ignore them at your own peril 👩
""")

st.markdown("### Step 2: Preview Your Digital Masterpiece")
st.markdown("""
Hit that "🚀 Get Data" button and watch the magic unfold like a beautiful Excel sheet sunrise:
- Green success messages = You're winning at life ✅🎉
- Red error messages = Time to panic... just kidding, just read and fix them ❌😅
- The summary box is like a movie trailer - it tells you everything without spoilers!
""")

st.markdown("### Step 3: Export Like the Data Legend You Are")
st.markdown("""
If your preview doesn't make you cry tears of despair:
- Smash that "🚀 Export Full Data" button like it owes you money
- Practice your patience (meditation apps recommended) 🧘‍♀️
- When "📥 Download CSV Now" appears, click it faster than Black Friday shoppers
- Celebrate like you just won the lottery! 🎊🥳
""")

st.divider()

# --- Troubleshooting ---
st.header("🔧 When Everything Goes Horribly Wrong (The Murphy's Law Section)")

st.subheader("😱 Common Disasters & How to Survive Them")

with st.expander("❌ \"No data found\" (AKA The Digital Tumbleweeds)", expanded=False):
    st.markdown("""
    **Translation:** Your data is playing hide and seek, and it's really good at it.
    
    **Survival Tactics:**
    - Expand your date range (cast a wider net)
    - Remove those picky optional filters  
    - Double-check your IDs (typos happen to the best of us)
    - Try dates when you KNOW stuff happened (like Black Friday, not your cousin's birthday)
    """)

with st.expander("🚫 \"Data too large\" (AKA The Digital Buffet Overflow)", expanded=False):
    st.markdown("""
    **Translation:** You've ordered the entire restaurant menu, and the kitchen is on fire.
    
    **Damage Control (ranked by effectiveness):**
    1. **Shrink that date range** - Most effective, like Marie Kondo for data
    2. **Fewer storefronts** - Quality over quantity, my friend
    3. **Add filters** - Be pickier than a food critic
    4. **Split the export** - Divide and conquer, like Caesar (but with less stabbing)
    """)

with st.expander("⚡ \"Database Connection Error\" (AKA The Digital Apocalypse)", expanded=False):
    st.markdown("""
    **Translation:** The database is having an existential crisis.
    
    **Emergency Response Protocol:**
    - Count to 30 (slowly, with feeling)
    - Try again (maybe the database just needed a moment)
    - If it persists, alert the tech cavalry
    - Check if others are experiencing the same digital despair
    - Final resort: Sacrifice a rubber duck to the SQL gods 🦆⚡
    """)

with st.expander("🐛 \"Unexpected error\" (AKA The Plot Twist Nobody Asked For)", expanded=False):
    st.markdown("""
    **Translation:** Something so weird happened that even our error messages are confused.
    
    **Plot Armor Strategies:**
    - Hit that "🔄 Start New Export" button (the digital equivalent of turning it off and on again)
    - Try different parameters (maybe the universe just doesn't like your current choices)
    - If it keeps happening, screenshot everything and send an SOS to tech support
    - Remember: Your data is safer than your browser history!
    """)


st.divider()

# --- Support ---
st.header("🆘 SOS Protocol (When All Hope Is Lost)")

st.markdown(
    """
    <div class='warning-box'>
    <h4>🚨 Before You Disturb the Peace, Did You:</h4>
    
    1. ✅ Actually read this guide (skimming doesn't count)?<br>
    2. ✅ Try the magical "🔄 Start New Export" button?<br>
    3. ✅ Wait 30 seconds while contemplating your life choices?<br>
    4. ✅ Ask literally anyone else first (your dog doesn't count)?<br>
    5. ✅ Take three deep breaths and question your existence?<br>
    <br>
    <strong>Only if you've achieved enlightenment through all five steps,</strong> then you may summon <strong>IrvineCao</strong> from his data cave 🧙‍♂️. 
    <br><br>
    Please bring offerings:<br>
    • A detailed confession of what you were attempting<br>
    • Visual evidence (screenshots) of your digital crimes<br>
    • Your workspace ID and date range details<br>
    • A heartfelt apology letter to Irvine (bonus points for haikus) 📝<br>
    </div>
    """, 
    unsafe_allow_html=True
)

st.divider()

# --- Fun Closing ---
st.header("🎉 Congratulations, Data Padawan!")

st.markdown(
    """
    <div class='highlight-box'>
    <h3>🏆 You Have Achieved Data Export Nirvana!</h3>
    
    Your newly acquired superpowers include:
    <br>
    ✨ Exporting data faster than Irvine can debug SQL queries<br>
    ✨ Filter navigation skills that would impress a search engine<br>
    ✨ Troubleshooting abilities stronger than Google's algorithm<br>
    ✨ The power to make your colleagues both jealous and slightly afraid<br>
    <br>
    <strong>Final Words of Wisdom:</strong> With great CSV power comes great spreadsheet responsibility. Use this tool wisely, may your data always be clean, and may your exports never timeout at 99%! 📊✨🙏
    </div>
    """, 
    unsafe_allow_html=True
)

st.balloons()

# --- Easter Egg ---
if st.button("🎁 Mystery Button (Totally Not Suspicious)", help="What's the worst that could happen? 🤷‍♀️"):
    st.success("🎉 BOOM! You found the secret button! You're now officially part of the Data Export Hall of Fame!")
    st.markdown("**Conspiracy Theory:** This entire tool was built in exactly 2 weeks, fueled by an alarming amount of coffee ☕, late-night coding sessions, and the collective desperation of everyone who was tired of sliding into Irvine's DMs for data exports. True story! 😄")
    st.markdown("**Fun Fact:** You're the 47th person to click this button. You're either very curious or very bored. Either way, we appreciate you! 🤗")
    st.image("https://media.giphy.com/media/3oriNYQX2lC6dfW2Ji/giphy.gif", width=300)