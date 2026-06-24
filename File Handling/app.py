import streamlit as st
from pathlib import Path
import os
import datetime

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FileVault · File Manager",
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  

  /* Base */
  html, body, [class*="css"] {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  }

  /* Background */
  .stApp {
      background: #0A0F1E;
  }

  /* Hide default streamlit elements */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

  /* Sidebar */
  [data-testid="stSidebar"] {
      background: #0F172A !important;
      border-right: 1px solid #1E293B;
  }
  [data-testid="stSidebar"] .stRadio label {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      color: #94A3B8;
      font-size: 0.9rem;
  }

  /* Custom header card */
  .header-card {
      background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
      border: 1px solid #334155;
      border-radius: 16px;
      padding: 1.8rem 2rem;
      margin-bottom: 1.5rem;
      position: relative;
      overflow: hidden;
  }
  .header-card::before {
      content: '';
      position: absolute;
      top: -40px; right: -40px;
      width: 120px; height: 120px;
      background: radial-gradient(circle, #3B82F620 0%, transparent 70%);
      border-radius: 50%;
  }
  .header-title {
      font-size: 1.8rem;
      font-weight: 700;
      color: #F1F5F9;
      letter-spacing: -0.03em;
      margin: 0;
  }
  .header-sub {
      color: #64748B;
      font-size: 0.85rem;
      margin-top: 0.3rem;
      font-weight: 400;
  }
  .badge {
      display: inline-block;
      background: #3B82F615;
      border: 1px solid #3B82F640;
      color: #3B82F6;
      font-size: 0.7rem;
      font-weight: 600;
      padding: 0.2rem 0.6rem;
      border-radius: 20px;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      margin-bottom: 0.6rem;
  }

  /* Operation Cards */
  .op-card {
      background: #1E293B;
      border: 1px solid #334155;
      border-radius: 12px;
      padding: 1.4rem 1.6rem;
      margin-bottom: 1rem;
  }
  .op-card-title {
      font-size: 1rem;
      font-weight: 600;
      color: #E2E8F0;
      margin-bottom: 1rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
  }

  /* Terminal output */
  .terminal {
      background: #020817;
      border: 1px solid #1E293B;
      border-radius: 12px;
      padding: 1.2rem 1.4rem;
      font-family: 'Consolas', 'Courier New', monospace;
      font-size: 0.82rem;
      color: #4ADE80;
      min-height: 120px;
      line-height: 1.7;
      white-space: pre-wrap;
      word-break: break-all;
  }
  .terminal-header {
      display: flex;
      align-items: center;
      gap: 6px;
      margin-bottom: 0.8rem;
  }
  .dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
  .dot-red { background: #FF5F57; }
  .dot-yellow { background: #FEBC2E; }
  .dot-green { background: #28C840; }

  /* File list */
  .file-item {
      display: flex;
      align-items: center;
      gap: 0.7rem;
      padding: 0.6rem 0.8rem;
      border-radius: 8px;
      color: #CBD5E1;
      font-size: 0.85rem;
      font-family: 'Consolas', 'Courier New', monospace;
      border: 1px solid #1E293B;
      margin-bottom: 0.4rem;
      background: #0F172A;
  }
  .file-meta {
      color: #475569;
      font-size: 0.72rem;
      margin-left: auto;
  }

  /* Success / Error banners */
  .banner-success {
      background: #052E1620;
      border: 1px solid #16A34A40;
      border-left: 3px solid #22C55E;
      border-radius: 8px;
      padding: 0.8rem 1rem;
      color: #4ADE80;
      font-size: 0.85rem;
      margin-top: 0.8rem;
  }
  .banner-error {
      background: #7F1D1D20;
      border: 1px solid #DC262640;
      border-left: 3px solid #EF4444;
      border-radius: 8px;
      padding: 0.8rem 1rem;
      color: #FCA5A5;
      font-size: 0.85rem;
      margin-top: 0.8rem;
  }
  .banner-info {
      background: #1E3A5F20;
      border: 1px solid #3B82F640;
      border-left: 3px solid #3B82F6;
      border-radius: 8px;
      padding: 0.8rem 1rem;
      color: #93C5FD;
      font-size: 0.85rem;
      margin-top: 0.8rem;
  }

  /* Streamlit input styling */
  .stTextInput > div > div > input,
  .stTextArea > div > div > textarea {
      background: #0F172A !important;
      border: 1px solid #334155 !important;
      border-radius: 8px !important;
      color: #E2E8F0 !important;
      font-family: 'Consolas', 'Courier New', monospace !important;
      font-size: 0.85rem !important;
  }
  .stTextInput > div > div > input:focus,
  .stTextArea > div > div > textarea:focus {
      border-color: #3B82F6 !important;
      box-shadow: 0 0 0 2px #3B82F620 !important;
  }

  /* Buttons */
  .stButton > button {
      background: linear-gradient(135deg, #2563EB, #3B82F6) !important;
      color: white !important;
      border: none !important;
      border-radius: 8px !important;
      font-weight: 600 !important;
      font-size: 0.85rem !important;
      padding: 0.5rem 1.4rem !important;
      transition: all 0.2s !important;
      width: 100%;
  }
  .stButton > button:hover {
      background: linear-gradient(135deg, #1D4ED8, #2563EB) !important;
      transform: translateY(-1px) !important;
      box-shadow: 0 4px 12px #3B82F630 !important;
  }

  /* Selectbox */
  .stSelectbox > div > div {
      background: #0F172A !important;
      border: 1px solid #334155 !important;
      border-radius: 8px !important;
      color: #E2E8F0 !important;
  }

  /* Radio */
  .stRadio > div {
      gap: 0.4rem;
  }

  /* Stats */
  .stat-box {
      background: #1E293B;
      border: 1px solid #334155;
      border-radius: 10px;
      padding: 1rem;
      text-align: center;
  }
  .stat-num {
      font-size: 1.6rem;
      font-weight: 700;
      color: #3B82F6;
      font-family: 'Consolas', 'Courier New', monospace;
  }
  .stat-label {
      font-size: 0.72rem;
      color: #64748B;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-top: 0.2rem;
  }

  /* Section label */
  .section-label {
      font-size: 0.7rem;
      font-weight: 600;
      color: #475569;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      margin-bottom: 0.6rem;
      margin-top: 1.2rem;
  }
</style>
""", unsafe_allow_html=True)

# ─── Working directory ──────────────────────────────────────────────────────────
WORK_DIR = Path("filevault_storage")
WORK_DIR.mkdir(exist_ok=True)

# ─── Session state ──────────────────────────────────────────────────────────────
if "log" not in st.session_state:
    st.session_state.log = []
if "last_content" not in st.session_state:
    st.session_state.last_content = ""
if "last_status" not in st.session_state:
    st.session_state.last_status = None  # "success" | "error" | "info"
if "last_msg" not in st.session_state:
    st.session_state.last_msg = ""

def add_log(msg: str):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    st.session_state.log.append(f"[{ts}] {msg}")
    if len(st.session_state.log) > 30:
        st.session_state.log = st.session_state.log[-30:]

def set_status(status, msg):
    st.session_state.last_status = status
    st.session_state.last_msg = msg

def list_files():
    return sorted(WORK_DIR.glob("*"))

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 1rem 0 0.5rem 0;'>
        <div style='font-size:1.2rem; font-weight:700; color:#F1F5F9; letter-spacing:-0.02em;'>🗂️ FileVault</div>
        <div style='font-size:0.75rem; color:#475569; margin-top:0.2rem;'>File Manager v1.0</div>
    </div>
    <hr style='border-color:#1E293B; margin: 0.8rem 0;'>
    <div class='section-label'>Navigation</div>
    """, unsafe_allow_html=True)

    operation = st.radio(
        "",
        ["📄  Create File", "📖  Read File", "✏️  Update File", "🗑️  Delete File", "📁  All Files"],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color:#1E293B; margin: 1rem 0;'>", unsafe_allow_html=True)
    
    # Stats
    files = list_files()
    total_size = sum(f.stat().st_size for f in files if f.is_file())
    st.markdown("<div class='section-label'>Storage Stats</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class='stat-box'>
            <div class='stat-num'>{len(files)}</div>
            <div class='stat-label'>Files</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        size_str = f"{total_size}B" if total_size < 1024 else f"{total_size//1024}KB"
        st.markdown(f"""
        <div class='stat-box'>
            <div class='stat-num'>{size_str}</div>
            <div class='stat-label'>Used</div>
        </div>""", unsafe_allow_html=True)

# ─── Main Content ───────────────────────────────────────────────────────────────
# Header
st.markdown("""
<div class='header-card'>
    <div class='badge'>Python Project</div>
    <div class='header-title'>FileVault · File Manager</div>
    <div class='header-sub'>Create · Read · Update · Delete — all in one place</div>
</div>
""", unsafe_allow_html=True)

col_main, col_log = st.columns([3, 2], gap="large")

with col_main:

    # ── CREATE ──────────────────────────────────────────────────────────────
    if operation == "📄  Create File":
        st.markdown("<div class='op-card-title'>📄 Create a New File</div>", unsafe_allow_html=True)

        filename = st.text_input("File Name", placeholder="e.g. notes.txt", key="create_name")
        content  = st.text_area("File Content", placeholder="Type what you want to write inside the file...", height=160, key="create_content")

        if st.button("Create File ✦"):
            if not filename.strip():
                set_status("error", "Please enter a file name.")
                add_log("❌ Create failed — no file name provided")
            else:
                path = WORK_DIR / filename.strip()
                if path.exists():
                    set_status("error", f"'{filename}' already exists. Try a different name or use Update.")
                    add_log(f"❌ Create failed — '{filename}' already exists")
                else:
                    try:
                        path.write_text(content)
                        set_status("success", f"'{filename}' created successfully! ({len(content)} chars)")
                        add_log(f"✅ Created '{filename}' ({len(content)} chars)")
                    except Exception as e:
                        set_status("error", f"Error: {e}")
                        add_log(f"❌ Create error: {e}")

    # ── READ ────────────────────────────────────────────────────────────────
    elif operation == "📖  Read File":
        st.markdown("<div class='op-card-title'>📖 Read File Contents</div>", unsafe_allow_html=True)

        files = list_files()
        if not files:
            st.markdown("<div class='banner-info'>📂 No files yet. Create one first!</div>", unsafe_allow_html=True)
        else:
            options = [f.name for f in files]
            selected = st.selectbox("Choose a file", options, key="read_select")

            if st.button("Read File ✦"):
                path = WORK_DIR / selected
                try:
                    content = path.read_text()
                    st.session_state.last_content = content
                    set_status("success", f"'{selected}' loaded — {len(content)} chars")
                    add_log(f"📖 Read '{selected}'")
                except Exception as e:
                    set_status("error", f"Error: {e}")
                    add_log(f"❌ Read error: {e}")

            if st.session_state.last_content:
                st.markdown("<div class='section-label' style='margin-top:1rem;'>File Contents</div>", unsafe_allow_html=True)
                st.markdown(f"""
                <div class='terminal'>
                    <div class='terminal-header'>
                        <span class='dot dot-red'></span>
                        <span class='dot dot-yellow'></span>
                        <span class='dot dot-green'></span>
                        <span style='color:#475569; font-size:0.75rem; margin-left:6px;'>{selected if files else ''}</span>
                    </div>{st.session_state.last_content}</div>
                """, unsafe_allow_html=True)

    # ── UPDATE ──────────────────────────────────────────────────────────────
    elif operation == "✏️  Update File":
        st.markdown("<div class='op-card-title'>✏️ Update a File</div>", unsafe_allow_html=True)

        files = list_files()
        if not files:
            st.markdown("<div class='banner-info'>📂 No files yet. Create one first!</div>", unsafe_allow_html=True)
        else:
            options   = [f.name for f in files]
            selected  = st.selectbox("Choose a file", options, key="update_select")
            action    = st.selectbox("Operation", ["Append Content", "Overwrite Content", "Rename File"], key="update_action")

            if action == "Rename File":
                new_name = st.text_input("New File Name", placeholder="e.g. renamed_notes.txt", key="new_name")
                if st.button("Rename ✦"):
                    if not new_name.strip():
                        set_status("error", "Please enter a new name.")
                    else:
                        old_path = WORK_DIR / selected
                        new_path = WORK_DIR / new_name.strip()
                        if new_path.exists():
                            set_status("error", f"'{new_name}' already exists.")
                            add_log(f"❌ Rename failed — target exists")
                        else:
                            try:
                                old_path.rename(new_path)
                                set_status("success", f"Renamed '{selected}' → '{new_name}'")
                                add_log(f"✏️ Renamed '{selected}' → '{new_name}'")
                                st.session_state.last_content = ""
                            except Exception as e:
                                set_status("error", f"Error: {e}")

            elif action == "Append Content":
                new_data = st.text_area("Content to Append", height=130, key="append_data")
                if st.button("Append ✦"):
                    path = WORK_DIR / selected
                    try:
                        with open(path, "a") as f:
                            f.write("\n" + new_data)
                        set_status("success", f"Appended {len(new_data)} chars to '{selected}'")
                        add_log(f"✏️ Appended to '{selected}'")
                    except Exception as e:
                        set_status("error", f"Error: {e}")

            elif action == "Overwrite Content":
                new_data = st.text_area("New Content (replaces everything)", height=130, key="overwrite_data")
                if st.button("Overwrite ✦"):
                    path = WORK_DIR / selected
                    try:
                        path.write_text(new_data)
                        set_status("success", f"'{selected}' overwritten ({len(new_data)} chars)")
                        add_log(f"✏️ Overwrote '{selected}'")
                    except Exception as e:
                        set_status("error", f"Error: {e}")

    # ── DELETE ──────────────────────────────────────────────────────────────
    elif operation == "🗑️  Delete File":
        st.markdown("<div class='op-card-title'>🗑️ Delete a File</div>", unsafe_allow_html=True)

        files = list_files()
        if not files:
            st.markdown("<div class='banner-info'>📂 No files to delete.</div>", unsafe_allow_html=True)
        else:
            options  = [f.name for f in files]
            selected = st.selectbox("Choose a file to delete", options, key="del_select")

            st.markdown(f"""
            <div class='banner-error'>
                ⚠️ You are about to permanently delete <strong>'{selected}'</strong>. This cannot be undone.
            </div>""", unsafe_allow_html=True)

            if st.button("Delete Permanently 🗑️"):
                path = WORK_DIR / selected
                try:
                    path.unlink()
                    set_status("success", f"'{selected}' has been deleted.")
                    add_log(f"🗑️ Deleted '{selected}'")
                    st.session_state.last_content = ""
                except Exception as e:
                    set_status("error", f"Error: {e}")
                    add_log(f"❌ Delete error: {e}")

    # ── ALL FILES ───────────────────────────────────────────────────────────
    elif operation == "📁  All Files":
        st.markdown("<div class='op-card-title'>📁 All Files in FileVault</div>", unsafe_allow_html=True)

        files = list_files()
        if not files:
            st.markdown("<div class='banner-info'>📂 Your vault is empty. Create a file to get started!</div>", unsafe_allow_html=True)
        else:
            for f in files:
                stat    = f.stat()
                size    = stat.st_size
                modified = datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%d %b, %H:%M")
                size_str = f"{size}B" if size < 1024 else f"{size//1024}KB"
                st.markdown(f"""
                <div class='file-item'>
                    <span>📄</span>
                    <span>{f.name}</span>
                    <span class='file-meta'>{size_str} · {modified}</span>
                </div>""", unsafe_allow_html=True)

    # ── Status Banner ───────────────────────────────────────────────────────
    if st.session_state.last_status == "success":
        st.markdown(f"<div class='banner-success'>✅ {st.session_state.last_msg}</div>", unsafe_allow_html=True)
    elif st.session_state.last_status == "error":
        st.markdown(f"<div class='banner-error'>❌ {st.session_state.last_msg}</div>", unsafe_allow_html=True)
    elif st.session_state.last_status == "info":
        st.markdown(f"<div class='banner-info'>ℹ️ {st.session_state.last_msg}</div>", unsafe_allow_html=True)

# ─── Activity Log ───────────────────────────────────────────────────────────────
with col_log:
    st.markdown("<div class='section-label'>Activity Log</div>", unsafe_allow_html=True)
    
    log_text = "\n".join(st.session_state.log[-15:]) if st.session_state.log else "No activity yet...\n\nPerform any operation\nto see logs here."
    
    st.markdown(f"""
    <div class='terminal' style='min-height:300px; color: #94A3B8;'>
        <div class='terminal-header'>
            <span class='dot dot-red'></span>
            <span class='dot dot-yellow'></span>
            <span class='dot dot-green'></span>
            <span style='color:#475569; font-size:0.75rem; margin-left:6px;'>activity.log</span>
        </div>{log_text}
    </div>
    """, unsafe_allow_html=True)

    if st.button("Clear Log"):
        st.session_state.log = []
        st.rerun()

    st.markdown("<div class='section-label' style='margin-top:1.5rem;'>Quick Tips</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:#0F172A; border:1px solid #1E293B; border-radius:10px; padding:1rem; font-size:0.78rem; color:#64748B; line-height:1.9;'>
        <span style='color:#3B82F6;'>→</span> Files are stored in <code style='color:#94A3B8;'>filevault_storage/</code><br>
        <span style='color:#3B82F6;'>→</span> Use <b style='color:#94A3B8;'>All Files</b> to browse<br>
        <span style='color:#3B82F6;'>→</span> Append adds to existing content<br>
        <span style='color:#3B82F6;'>→</span> Overwrite replaces everything<br>
        <span style='color:#3B82F6;'>→</span> Delete is permanent — be careful!
    </div>
    """, unsafe_allow_html=True)
