"""
Vidya Academy of Science & Technology
Department of Computer Science & Engineering
Lab Manual Download Portal (Streamlit)

Run:  streamlit run app.py
"""

import io
import zipfile
from pathlib import Path

import streamlit as st

# ----------------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent
MANUAL_DIR = BASE_DIR / "manuals"
LOGO_PATH = BASE_DIR / "assets" / "logo.png"
THUMB_DIR = BASE_DIR / "assets" / "thumbs"

# ----------------------------------------------------------------------------
# Lab manual catalogue
# To add a new manual: drop the PDF into /manuals and add one entry here.
# ----------------------------------------------------------------------------
MANUALS = [
    # ---------------- 2024 Scheme ----------------
    {"file": "python_UPDATED.pdf", "code": "UCEST105", "title": "Algorithmic Thinking with Python Lab",
     "scheme": "2024", "semester": "S1/S2", "author": "Dr. Sanaj M S"},
    {"file": "C_Manual_2024.pdf", "code": "GXEST204", "title": "Programming in C Lab",
     "scheme": "2024", "semester": "S2", "author": "Ms. Neethu George"},
    {"file": "IT_Workshop_2024_Scheme_new.pdf", "code": "GXESL208", "title": "IT Workshop",
     "scheme": "2024", "semester": "S2", "author": "Ms. Remya K R"},
    {"file": "DS_2024Scheme_new.pdf", "code": "PCCSL307", "title": "Data Structures Lab",
     "scheme": "2024", "semester": "S3", "author": "Ms. Remya K R"},
    {"file": "os_lab_manual_2024_new.pdf", "code": "PCCSL407", "title": "Operating Systems Lab",
     "scheme": "2024", "semester": "S4", "author": "Ms. Ramya Raj K P"},
    {"file": "dbms_Manual2024.pdf", "code": "PCCSL408", "title": "Database Management Systems Lab",
     "scheme": "2024", "semester": "S4", "author": "Ms. Anitha L"},
    {"file": "network_lab_manual2024new.pdf", "code": "PCCSL507", "title": "Networks Lab",
     "scheme": "2024", "semester": "S5", "author": "Ms. Jucy Vareed"},
    {"file": "ML-Manual.pdf", "code": "PCCSL508", "title": "Machine Learning Lab",
     "scheme": "2024", "semester": "S5", "author": "Dr. Arjun K P"},

    # ---------------- 2019 Scheme ----------------
    {"file": "C_Manual_2019.pdf", "code": "EST102", "title": "Programming in C Lab",
     "scheme": "2019", "semester": "S1/S2", "author": "Ms. Neethu George"},
    {"file": "DS_Lab_Manual_2019_new.pdf", "code": "CSL201", "title": "Data Structures Lab",
     "scheme": "2019", "semester": "S3", "author": "Ms. Remya K R"},
    {"file": "oops_lab_new.pdf", "code": "CSL203", "title": "Object Oriented Programming Lab",
     "scheme": "2019", "semester": "S3", "author": "Ms. Athulya Bhaskar K R"},
    {"file": "os_2019_new.pdf", "code": "CSL204", "title": "Operating Systems Lab",
     "scheme": "2019", "semester": "S4", "author": "Ms. Athulya Bhaskar K R"},
    {"file": "SSMP_2019.pdf", "code": "CSL331", "title": "System Software & Microprocessors Lab",
     "scheme": "2019", "semester": "S5", "author": "Ms. Prajitha M V"},
    {"file": "DBMS-2019.pdf", "code": "CSL333", "title": "Database Management Systems Lab",
     "scheme": "2019", "semester": "S5", "author": "Ms. Anitha L"},
    {"file": "Networks_Lab_Manual_2019_new.pdf", "code": "CSL332", "title": "Networking Lab",
     "scheme": "2019", "semester": "S6", "author": "Mr. Sivadasan E T"},
    {"file": "COMPILER_LAB_new.pdf", "code": "CSL411", "title": "Compiler Lab",
     "scheme": "2019", "semester": "S7", "author": "Ms. Delmy David V"},

    # ---------------- Common documents ----------------
    {"file": "EXP_MAPPED_WITH_CO.pdf", "code": "CO-MAP", "title": "List of Experiments Mapped with COs (All Labs)",
     "scheme": "Common", "semester": "All", "author": "Department of CSE"},
]

# ----------------------------------------------------------------------------
# Page setup & styling
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Lab Manuals | Vidya Academy of Science & Technology",
    page_icon=str(LOGO_PATH) if LOGO_PATH.exists() else "📘",
    layout="wide",
)

BROWN = "#7B3F00"
BROWN_DARK = "#5A2D00"
CREAM = "#FFF8EF"

st.markdown(
    f"""
    <style>
      .block-container {{ padding-top: 1.5rem; max-width: 1250px; }}
      .hero {{
          background: linear-gradient(135deg, {BROWN_DARK} 0%, {BROWN} 60%, #A0612A 100%);
          border-radius: 18px; padding: 1.4rem 1.8rem; color: #fff;
          margin-bottom: 1.2rem; box-shadow: 0 6px 20px rgba(90,45,0,.25);
      }}
      .hero h1 {{ color: #fff; font-size: 2.0rem; margin: 0; line-height: 1.2; }}
      .hero .sub {{ opacity: .9; font-size: .95rem; margin-top: .2rem; }}
      .hero .dept {{ margin-top: .7rem; font-weight: 700; letter-spacing: .5px;
                     font-size: 1.05rem; color: #FFE2BF; }}
      .badge {{ display:inline-block; padding: 2px 10px; border-radius: 999px;
                font-size: .72rem; font-weight: 700; margin-right: 6px; }}
      .b2024 {{ background:#E8F5E9; color:#1B5E20; }}
      .b2019 {{ background:#E3F2FD; color:#0D47A1; }}
      .bCommon {{ background:#FFF3E0; color:#E65100; }}
      .bcode {{ background:{CREAM}; color:{BROWN}; border:1px solid #E9CFAF; }}
      .mtitle {{ font-weight: 700; font-size: 1.02rem; margin: .45rem 0 .2rem 0;
                 min-height: 2.6em; color: inherit; }}
      .meta {{ font-size: .82rem; opacity: .75; line-height: 1.5; }}
      div[data-testid="stImage"] img {{ border-radius: 8px; border: 1px solid #e5d6c4; }}
      .footer {{ text-align:center; opacity:.65; font-size:.8rem; margin-top: 2rem; }}
      .stDownloadButton button {{ width: 100%; }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def read_bytes(path: str) -> bytes:
    return Path(path).read_bytes()


@st.cache_data(show_spinner=False)
def pdf_page_count(path: str) -> int | None:
    """Best-effort page count without extra dependencies."""
    try:
        data = Path(path).read_bytes()
        count = data.count(b"/Type /Page") - data.count(b"/Type /Pages")
        if count <= 0:
            count = data.count(b"/Type/Page") - data.count(b"/Type/Pages")
        return count if count > 0 else None
    except Exception:
        return None


def human_size(n: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if n < 1024:
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


@st.cache_data(show_spinner="Preparing ZIP…")
def build_zip(files: tuple[str, ...]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            p = MANUAL_DIR / f
            if p.exists():
                zf.write(p, arcname=f)
    return buf.getvalue()


# Keep only manuals whose PDF actually exists
available = [m for m in MANUALS if (MANUAL_DIR / m["file"]).exists()]
missing = [m for m in MANUALS if not (MANUAL_DIR / m["file"]).exists()]

# ----------------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------------
with st.container():
    c_logo, c_text = st.columns([1, 4], vertical_alignment="center")
    with c_logo:
        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), width="stretch")
    with c_text:
        st.markdown(
            """
            <div class="hero">
              <h1>Vidya Academy of Science &amp; Technology</h1>
              <div class="sub">A unit of Vidya International Charitable Trust · Approved by AICTE &amp;
              Affiliated to APJ Abdul Kalam Technological University</div>
              <div class="dept">DEPARTMENT OF COMPUTER SCIENCE &amp; ENGINEERING — LAB MANUALS</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ----------------------------------------------------------------------------
# Sidebar filters
# ----------------------------------------------------------------------------
with st.sidebar:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width="stretch")
    st.markdown("### 🔎 Find a manual")
    query = st.text_input("Search by course name, code or faculty", placeholder="e.g. PCCSL407, Python, Compiler")
    scheme = st.radio("KTU Scheme", ["All", "2024", "2019", "Common"], horizontal=True)
    semesters = sorted({m["semester"] for m in available})
    sem_pick = st.multiselect("Semester", semesters)
    show_covers = st.toggle("Show cover pages", value=True)
    st.divider()
    st.caption(f"📚 {len(available)} manuals available")


def matches(m: dict) -> bool:
    if scheme != "All" and m["scheme"] != scheme:
        return False
    if sem_pick and m["semester"] not in sem_pick:
        return False
    if query:
        hay = f'{m["code"]} {m["title"]} {m["author"]} {m["scheme"]}'.lower()
        return all(tok in hay for tok in query.lower().split())
    return True


filtered = [m for m in available if matches(m)]

# ----------------------------------------------------------------------------
# Summary stats + bulk download
# ----------------------------------------------------------------------------
s1, s2, s3, s4 = st.columns(4)
s1.metric("Total manuals", len(available))
s2.metric("2024 Scheme", sum(m["scheme"] == "2024" for m in available))
s3.metric("2019 Scheme", sum(m["scheme"] == "2019" for m in available))
s4.metric("Showing", len(filtered))

if filtered:
    zip_name = "VAST_CSE_Lab_Manuals" + ("" if scheme == "All" else f"_{scheme}") + ".zip"
    st.download_button(
        f"⬇️  Download all {len(filtered)} shown manuals as ZIP",
        data=build_zip(tuple(m["file"] for m in filtered)),
        file_name=zip_name,
        mime="application/zip",
        type="primary",
        width="stretch",
    )

st.write("")

# ----------------------------------------------------------------------------
# Manual cards
# ----------------------------------------------------------------------------
if not filtered:
    st.info("No manuals match your filters. Try clearing the search or changing the scheme.")
else:
    order = {"2024": 0, "2019": 1, "Common": 2}
    groups = {}
    for m in sorted(filtered, key=lambda x: (order.get(x["scheme"], 9), x["code"])):
        groups.setdefault(m["scheme"], []).append(m)

    for grp, items in groups.items():
        label = "Common Documents" if grp == "Common" else f"KTU {grp} Scheme"
        st.subheader(f"📘 {label}")
        cols_per_row = 4
        for i in range(0, len(items), cols_per_row):
            cols = st.columns(cols_per_row)
            for col, m in zip(cols, items[i:i + cols_per_row]):
                path = MANUAL_DIR / m["file"]
                size = human_size(path.stat().st_size)
                pages = pdf_page_count(str(path))
                with col:
                    with st.container(border=True):
                        thumb = THUMB_DIR / (Path(m["file"]).stem + ".png")
                        if show_covers and thumb.exists():
                            st.image(str(thumb), width="stretch")
                        st.markdown(
                            f"""
                            <span class="badge b{m['scheme']}">{m['scheme']}</span>
                            <span class="badge bcode">{m['code']}</span>
                            <div class="mtitle">{m['title']}</div>
                            <div class="meta">👤 {m['author']}<br>
                            🎓 Semester: {m['semester']}<br>
                            📄 {f"{pages} pages · " if pages else ""}{size}</div>
                            """,
                            unsafe_allow_html=True,
                        )
                        st.download_button(
                            "Download PDF",
                            data=read_bytes(str(path)),
                            file_name=m["file"],
                            mime="application/pdf",
                            key=f"dl_{m['file']}",
                            width="stretch",
                        )
        st.write("")

if missing:
    with st.expander(f"⚠️ {len(missing)} catalogue entries have no PDF in /manuals"):
        for m in missing:
            st.write(f"- {m['code']} – {m['title']} (`{m['file']}`)")

# ----------------------------------------------------------------------------
# Footer
# ----------------------------------------------------------------------------
st.markdown(
    """
    <div class="footer">
      © Vidya Academy of Science &amp; Technology · Department of Computer Science &amp; Engineering<br>
      <i>Progress Through Education</i>
    </div>
    """,
    unsafe_allow_html=True,
)
