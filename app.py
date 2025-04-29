# app.py

import streamlit as st

# Set page config
st.set_page_config(page_title="Canadian Election Dashboard", layout="wide")

st.title("🇨🇦 Canadian Election Dashboard: Shaping Insights Through Data")

st.markdown("""
Welcome to the **Interactive Canadian Election Dashboard**! 🎉✨

This platform is part of a growing suite of tools designed to **broaden the use of data for transparency, innovation, and discovery**. 📊🧠 Whether you're a political enthusiast, a data analyst, or a curious citizen, this dashboard gives you a front-row seat to Canada's electoral landscape.

🔍 **What you can explore:**
- 📈 Historical election trends
- 🗳️ Provincial and constituency voting patterns
- 🏛️ Party performance and shifts over time
- 🤖 Predictive models forecasting future elections
- 🌎 Geospatial and statistical deep-dives into voting behavior

---

**Built by Tyler Doiron, MSc, MQM, aCAP**  
Chief Data Officer, Astute Innovations 🚀

Tyler Doiron is a data scientist and analytics leader specializing in machine learning, statistical modeling, and building innovative data solutions. This dashboard reflects a commitment to making complex information **simple, engaging, and powerful** for everyone. 🌟

---

📚 **Interested in the source of the data? Explore these amazing Canadian open data portals:**
- [Elections Canada Official Data](https://www.elections.ca/content.aspx?section=res&dir=dat&document=index&lang=e)
- [Open Government Canada Portal](https://open.canada.ca/en/open-data)
- [Statistics Canada Open Data](https://www.statcan.gc.ca/en/start)
- [Parliament of Canada Data](https://www.ourcommons.ca/en)

These resources continue to drive accessibility, innovation, and insight across the country. 🇨🇦✨

---

👉 **Use the sidebar** to navigate between pages and start exploring the story of Canada through data!
""")

st.sidebar.success("Select a page to explore ⬆️")
