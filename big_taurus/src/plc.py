import streamlit as st
import time
import psutil
import platform
import subprocess
from pylogix import PLC
from pymodbus.client import ModbusTcpClient
from datetime import datetime

# ========================= CONFIGURATION =========================
PLC_NETWORK = {
    "Stn 1 (3.5)": {"ip": "192.168.3.5", "units": ["STN11", "STN12"], "slot": 0},
    "Stn 2 (3.6)": {"ip": "192.168.3.6", "units": ["STN21", "STN22", "STN23"], "slot": 0},
    "Stn 3 (3.7)": {"ip": "192.168.3.7", "units": ["STN31", "STN32", "STN33", "STN34"], "slot": 0},
    "Stn 4 (3.8)": {"ip": "192.168.3.8", "units": ["STN41", "STN42"], "slot": 0}
}

MODBUS_IP = "192.168.7.5"
PING_TARGET = "192.168.3.243"

TAGS = {
    "📥 UNLOAD": ["PLC_UNLOAD_REQ", "AMR_UNLOAD_ACCEPTED", "AMR_DOCK_COMPLETE_UNLOAD", "PLC_START_TRANSFER", "AMR_TRANSFER_ACCEPTED", "PLC_TRANSFER_COMPLETE", "AMR_TRANSFER_ACK_UNLOAD"],
    "📤 LOAD": ["PLC_LOAD_REQ", "AMR_LOAD_ACCEPTED", "AMR_DOCK_COMPLETE_LOAD", "AMR_START_TRANSFER", "PLC_TRANSFER_ACCEPTED", "AMR_TRANSFER_COMPLETE", "PLC_PALLET_RECEIVED", "AMR_TRANSFER_ACK_LOAD"]
}

# ====================== SESSION LOGGING (RAM ONLY) ======================
if 'app_logs' not in st.session_state:
    st.session_state.app_logs = []

def add_log(msg):
    now = datetime.now().strftime("%H:%M:%S")
    st.session_state.app_logs.insert(0, f"[{now}] {msg}")
    if len(st.session_state.app_logs) > 10: st.session_state.app_logs.pop()

# ====================== MONITORING & MODBUS ======================
def get_ping_status(ip):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    try:
        return subprocess.call(['ping', param, '1', '-w', '500', ip], 
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0
    except: return False

def op_modbus(addr, val, name):
    try:
        with ModbusTcpClient(MODBUS_IP, port=502, timeout=0.5) as c:
            if c.connect():
                c.write_coil(addr, val, slave=1)
                add_log(f"Modbus: {name} {'ON' if val else 'OFF'}")
                return True
    except: add_log(f"Error: Modbus {name} failed")
    return False

# ====================== PLC FUNCTIONS ======================
def get_data(ip, slot, prefix):
    all_t = TAGS["📥 UNLOAD"] + TAGS["📤 LOAD"]
    full = [f"{prefix}.{t}" for t in all_t]
    with PLC() as comm:
        comm.IPAddress, comm.ProcessorSlot = ip, slot
        res = comm.Read(full)
        if not res or not isinstance(res, list): return None
        return {all_t[i]: r.Value for i, r in enumerate(res) if r.Status == "Success"}

def set_plc_tag(ip, slot, pre, tag, val):
    with PLC() as comm:
        comm.IPAddress, comm.ProcessorSlot = ip, slot
        ret = comm.Write(f"{pre}.{tag}", val)
        if ret.Status == "Success":
            add_log(f"{pre}: {tag} -> {val}")

# ====================== MODERN UI ENHANCEMENTS ======================
st.set_page_config(page_title="PLC Hub Pro", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Import Modern Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    /* Global Background & Font */
    .stApp {
        background-color: #0e1117;
        font-family: 'Inter', sans-serif;
    }

    /* Modern Button Styling */
    .stButton button {
        width: 100%;
        border-radius: 6px;
        height: 2.2rem;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: all 0.2s ease;
        border: 1px solid #30363d;
        background-color: #21262d;
        color: #c9d1d9;
    }

    .stButton button:hover {
        border-color: #8b949e;
        background-color: #30363d;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }

    /* Primary Button (The "ON" or "SET" buttons) */
    button[kind="primary"] {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important;
        border: none !important;
        color: white !important;
    }

    /* Metric & Progress Bar Styling */
    .metric-text {
        font-size: 0.9rem;
        color: #8b949e;
        font-weight: 700;
        margin-bottom: 4px;
    }
    
    .stProgress > div > div > div > div {
        background-color: #388bfd;
    }

    /* Log Box Styling */
    .log-box {
        font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
        font-size: 0.8rem;
        background: #161b22;
        color: #58a6ff;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #30363d;
        line-height: 1.4;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);
    }

    /* Active Tag Highlighting */
    .active-tag {
        background: rgba(35, 134, 54, 0.15);
        color: #3fb950;
        border-left: 3px solid #3fb950;
        padding: 4px 8px;
        border-radius: 0 4px 4px 0;
        font-weight: 600;
        font-size: 0.95rem;
    }

    /* Section Headers */
    h3, h4, h5 {
        color: #f0f6fc !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
        margin-top: 20px !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }

    /* Divider */
    hr {
        border-color: #30363d !important;
    }

    /* Status Indicator Dot */
    .status-indicator {
        font-size: 1rem;
        padding: 8px;
        background: #21262d;
        border-radius: 8px;
        border: 1px solid #30363d;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. SYSTEM METRICS ---
cpu_p = psutil.cpu_percent()
ram_p = psutil.virtual_memory().percent
ping_ok = get_ping_status(PING_TARGET)

m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f"<p class='metric-text'>CPU {cpu_p}%</p>", unsafe_allow_html=True)
    st.progress(cpu_p/100)
with m2:
    st.markdown(f"<p class='metric-text'>RAM {ram_p}%</p>", unsafe_allow_html=True)
    st.progress(ram_p/100)
with m3:
    p_color = "#28a745" if ping_ok else "#dc3545"
    st.markdown(f"<p style='color:{p_color}; font-weight:bold; font-size:0.85rem; margin-top:5px;'>● Server .243</p>", unsafe_allow_html=True)

st.divider()

# --- 2. GLOBAL CONTROLS (M30/M31/Safety) ---
with st.expander("🛡️ GLOBAL MASTER CONTROLS", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        st.caption("Safety (C10)")
        if st.button("🚨 OFF", key="safe_off"): op_modbus(10, True, "Safety")
        if st.button("✅ ON", key="safe_on", type="primary"): op_modbus(10, False, "Safety")
    with c2:
        st.caption("M30 Mode")
        if st.button("M30 ON", key="m30_on"): op_modbus(30, True, "M30")
        if st.button("M30 OFF", key="m30_off"): op_modbus(30, False, "M30")
    with c3:
        st.caption("M31 Mode")
        if st.button("M31 ON", key="m31_on"): op_modbus(31, True, "M31")
        if st.button("M31 OFF", key="m31_off"): op_modbus(31, False, "M31")

# --- 3. SYSTEM LOG (RAM ONLY) ---
log_text = "<br>".join(st.session_state.app_logs) if st.session_state.app_logs else "Ready..."
st.markdown(f"<div class='log-box'>{log_text}</div>", unsafe_allow_html=True)

st.divider()

# --- 4. STATION PANEL ---
st.sidebar.header("Navigation")
sel_plc_name = st.sidebar.selectbox("Select PLC IP", list(PLC_NETWORK.keys()))
plc_cfg = PLC_NETWORK[sel_plc_name]
sel_unit = st.sidebar.radio("Active Unit", plc_cfg["units"], horizontal=True)

plc_data = get_data(plc_cfg['ip'], plc_cfg['slot'], sel_unit)

if plc_data:
    st.markdown(f"**📍 Unit: {sel_unit}** <small>({plc_cfg['ip']})</small>", unsafe_allow_html=True)
    col_u, col_l = st.columns(2)
    
    def render_tags(tag_list, title):
        st.markdown(f"##### {title}")
        for t in tag_list:
            val = plc_data.get(t, False)
            row_class = "active-tag" if val else ""
            cols = st.columns([0.7, 5, 1.4, 1.4])
            cols[0].write("🟢" if val else "⚪")
            # Clean up tag display name
            disp_name = t.split('_', 1)[-1].replace('_', ' ')
            cols[1].markdown(f"<div class='{row_class}'>{disp_name}</div>", unsafe_allow_html=True)
            
            if cols[2].button("SET", key=f"s_{sel_unit}_{t}"):
                set_plc_tag(plc_cfg['ip'], plc_cfg['slot'], sel_unit, t, True)
                st.rerun()
            if cols[3].button("CLR", key=f"c_{sel_unit}_{t}"):
                set_plc_tag(plc_cfg['ip'], plc_cfg['slot'], sel_unit, t, False)
                st.rerun()

    with col_u: render_tags(TAGS["📥 UNLOAD"], "UNLOAD")
    with col_l: render_tags(TAGS["📤 LOAD"], "LOAD")
else:
    st.warning(f"Connecting to {sel_unit}...")

# High-speed refresh
time.sleep(0.5)
st.rerun()
#streamlit run plc.py --server.port 8090 --server.headless true
