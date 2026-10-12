#!/usr/bin/env python3

import tkinter as tk
from pylogix import PLC
import threading
import time

# Handle both old and new pymodbus versions
try:
    # Try new version first (pymodbus >= 3.0)
    from pymodbus.client import ModbusTcpClient
except ImportError:
    try:
        # Fall back to old version (pymodbus < 3.0)
        from pymodbus.client.sync import ModbusTcpClient
    except ImportError:
        ModbusTcpClient = None
        print("ERROR: pymodbus not installed properly")

# CHANGE: your PLC IP and prefix
PLC_IP = "192.168.3.8"
PREFIX = "STN41"

# Modbus configuration for safety feature
MODBUS_IP = "192.168.7.5"
MODBUS_PORT = 502
MODBUS_SLAVE_ID = 1
SAFETY_COIL_ADDRESS = 10  # M10 - Safety feature toggle (True=OFF, False=ON)

# Modbus configuration for M30 and M31 coils
M30_COIL_ADDRESS = 30     # M30 - Custom control coil
M31_COIL_ADDRESS = 31     # M31 - Custom control coil

RECONNECT_DELAY = 3    # seconds between reconnect attempts
POLL_INTERVAL   = 1    # seconds between tag polls

UNLOAD_SEQ = [
    ("PLC_UNLOAD_REQ",           "plc", "1. PLC requests unload"),
    ("AMR_UNLOAD_ACCEPTED",      "amr", "2. AMR accepted"),
    ("AMR_DOCK_COMPLETE_UNLOAD", "amr", "3. AMR docked"),
    ("PLC_START_TRANSFER",       "plc", "4. PLC start transfer"),
    ("AMR_TRANSFER_ACCEPTED",    "amr", "5. AMR transfer accepted"),
    ("PLC_TRANSFER_COMPLETE",    "plc", "6. PLC transfer complete"),
    ("AMR_TRANSFER_ACK_UNLOAD",  "amr", "7. AMR acknowledged"),
]

LOAD_SEQ = [
    ("PLC_LOAD_REQ",             "plc", "1. PLC requests load"),
    ("AMR_LOAD_ACCEPTED",        "amr", "2. AMR accepted"),
    ("AMR_DOCK_COMPLETE_LOAD",   "amr", "3. AMR docked"),
    ("AMR_START_TRANSFER",       "amr", "4. AMR start transfer"),
    ("PLC_TRANSFER_ACCEPTED",    "plc", "5. PLC transfer accepted"),
    ("AMR_TRANSFER_COMPLETE",    "amr", "6. AMR transfer complete"),
    ("PLC_PALLET_RECEIVED",      "plc", "7. PLC pallet received"),
    ("AMR_TRANSFER_ACK_LOAD",    "amr", "8. AMR acknowledged"),
]

ALL_SEQ = UNLOAD_SEQ + LOAD_SEQ

COLOR_TRUE    = "#4CAF50"
COLOR_FALSE   = "#F44336"
COLOR_WARN    = "#FFA726"
COLOR_BG      = "#1e1e1e"
COLOR_PANEL   = "#2b2b2b"
COLOR_BORDER  = "#3a3a3a"
COLOR_PLC     = "#1565C0"
COLOR_AMR     = "#6A1B9A"
COLOR_PLC_LT  = "#1976D2"
COLOR_AMR_LT  = "#7B1FA2"


class PLCMonitor:

    def __init__(self, root):
        self.root     = root
        self.root.title(f"PLC Monitor — {PREFIX}  |  LOAD & UNLOAD Sequence")
        self.root.configure(bg=COLOR_BG)
        self.root.resizable(False, False)

        self.plc          = None
        self.plc_lock     = threading.Lock()

        self.modbus_client = None
        self.modbus_lock  = threading.Lock()

        self.connected         = False
        self.safety_state      = False  # False = safety ON, True = safety OFF
        self.m30_state         = False  # M30 state
        self.m31_state         = False  # M31 state
        self.state             = {tag: False for tag, _, _ in ALL_SEQ}
        self.indicators        = {}
        self.val_labels        = {}
        self.safety_indicator  = None
        self.safety_btn_text   = None
        self.m30_indicator     = None  # M30 indicator
        self.m31_indicator     = None  # M31 indicator
        self.m30_status_label  = None  # M30 status label
        self.m31_status_label  = None  # M31 status label
        self.running           = True

        self._build_ui()
        self._start_connection_thread()

    # ── UI BUILD ──────────────────────────────────────────────────────────────

    def _build_ui(self):
        MONO    = ("Courier New", 10)
        MONO_SM = ("Courier New", 9)

        # header
        hdr = tk.Frame(self.root, bg=COLOR_BG, pady=10, padx=16)
        hdr.pack(fill="x")

        self.status_dot = tk.Label(hdr, text="●", fg=COLOR_FALSE,
                                   bg=COLOR_BG, font=("Courier New", 14))
        self.status_dot.pack(side="left")

        self.status_txt = tk.Label(hdr, text="  Connecting...",
                                   fg=COLOR_WARN, bg=COLOR_BG,
                                   font=("Courier New", 11))
        self.status_txt.pack(side="left")

        tk.Label(hdr, text=f"  {PREFIX}  {PLC_IP}",
                 fg="#555555", bg=COLOR_BG,
                 font=("Courier New", 10)).pack(side="left")

        self.ts_lbl = tk.Label(hdr, text="--:--:--", fg="#555555",
                               bg=COLOR_BG, font=MONO)
        self.ts_lbl.pack(side="right")

        tk.Button(hdr, text="RECONNECT", font=("Courier New", 8),
                  bg="#333333", fg="#aaaaaa", relief="flat",
                  padx=8, pady=2, cursor="hand2",
                  command=self._manual_reconnect).pack(side="right", padx=8)

        tk.Frame(self.root, bg=COLOR_BORDER, height=1).pack(fill="x")

        # Safety feature panel
        safety_panel = tk.Frame(self.root, bg=COLOR_PANEL, padx=16, pady=10)
        safety_panel.pack(fill="x")

        safety_label_frame = tk.Frame(safety_panel, bg=COLOR_PANEL)
        safety_label_frame.pack(fill="x", pady=(0, 8))

        tk.Label(safety_label_frame, text="⚠ SAFETY FEATURE", fg="#FF9800", bg=COLOR_PANEL,
                 font=("Courier New", 10, "bold")).pack(side="left")

        self.safety_indicator = tk.Label(safety_label_frame, text=" ●", fg=COLOR_FALSE, bg=COLOR_PANEL,
                                        font=("Courier New", 12))
        self.safety_indicator.pack(side="left", padx=4)

        self.safety_status_label = tk.Label(safety_label_frame, text="Safety ON (M10=0)", fg=COLOR_TRUE, 
                                           bg=COLOR_PANEL, font=("Courier New", 9))
        self.safety_status_label.pack(side="left", padx=4)

        safety_btn_frame = tk.Frame(safety_panel, bg=COLOR_PANEL)
        safety_btn_frame.pack(fill="x")

        tk.Button(safety_btn_frame, text="Turn OFF (Disable Safety)", font=("Courier New", 9),
                  bg=COLOR_FALSE, fg="white", relief="flat",
                  padx=12, pady=6, cursor="hand2",
                  command=lambda: self._write_safety(True)).pack(side="left", padx=(0, 6))

        tk.Button(safety_btn_frame, text="Turn ON (Enable Safety)", font=("Courier New", 9),
                  bg=COLOR_TRUE, fg="white", relief="flat",
                  padx=12, pady=6, cursor="hand2",
                  command=lambda: self._write_safety(False)).pack(side="left", padx=0)

        tk.Frame(self.root, bg=COLOR_BORDER, height=1).pack(fill="x")

        # M30 Control Panel
        m30_panel = tk.Frame(self.root, bg=COLOR_PANEL, padx=16, pady=10)
        m30_panel.pack(fill="x")

        m30_label_frame = tk.Frame(m30_panel, bg=COLOR_PANEL)
        m30_label_frame.pack(fill="x", pady=(0, 8))

        tk.Label(m30_label_frame, text="M30 CONTROL", fg="#2196F3", bg=COLOR_PANEL,
                 font=("Courier New", 10, "bold")).pack(side="left")

        self.m30_indicator = tk.Label(m30_label_frame, text=" ●", fg=COLOR_FALSE, bg=COLOR_PANEL,
                                     font=("Courier New", 12))
        self.m30_indicator.pack(side="left", padx=4)

        self.m30_status_label = tk.Label(m30_label_frame, text="M30 = 0 (OFF)", fg=COLOR_TRUE, 
                                        bg=COLOR_PANEL, font=("Courier New", 9))
        self.m30_status_label.pack(side="left", padx=4)

        m30_btn_frame = tk.Frame(m30_panel, bg=COLOR_PANEL)
        m30_btn_frame.pack(fill="x")

        tk.Button(m30_btn_frame, text="M30 → FALSE", font=("Courier New", 9),
                  bg=COLOR_FALSE, fg="white", relief="flat",
                  padx=12, pady=6, cursor="hand2",
                  command=lambda: self._write_m30_m31(M30_COIL_ADDRESS, False)).pack(side="left", padx=(0, 6))

        tk.Button(m30_btn_frame, text="M30 → TRUE", font=("Courier New", 9),
                  bg=COLOR_TRUE, fg="white", relief="flat",
                  padx=12, pady=6, cursor="hand2",
                  command=lambda: self._write_m30_m31(M30_COIL_ADDRESS, True)).pack(side="left", padx=0)

        tk.Frame(self.root, bg=COLOR_BORDER, height=1).pack(fill="x")

        # M31 Control Panel
        m31_panel = tk.Frame(self.root, bg=COLOR_PANEL, padx=16, pady=10)
        m31_panel.pack(fill="x")

        m31_label_frame = tk.Frame(m31_panel, bg=COLOR_PANEL)
        m31_label_frame.pack(fill="x", pady=(0, 8))

        tk.Label(m31_label_frame, text="M31 CONTROL", fg="#9C27B0", bg=COLOR_PANEL,
                 font=("Courier New", 10, "bold")).pack(side="left")

        self.m31_indicator = tk.Label(m31_label_frame, text=" ●", fg=COLOR_FALSE, bg=COLOR_PANEL,
                                     font=("Courier New", 12))
        self.m31_indicator.pack(side="left", padx=4)

        self.m31_status_label = tk.Label(m31_label_frame, text="M31 = 0 (OFF)", fg=COLOR_TRUE, 
                                        bg=COLOR_PANEL, font=("Courier New", 9))
        self.m31_status_label.pack(side="left", padx=4)

        m31_btn_frame = tk.Frame(m31_panel, bg=COLOR_PANEL)
        m31_btn_frame.pack(fill="x")

        tk.Button(m31_btn_frame, text="M31 → FALSE", font=("Courier New", 9),
                  bg=COLOR_FALSE, fg="white", relief="flat",
                  padx=12, pady=6, cursor="hand2",
                  command=lambda: self._write_m30_m31(M31_COIL_ADDRESS, False)).pack(side="left", padx=(0, 6))

        tk.Button(m31_btn_frame, text="M31 → TRUE", font=("Courier New", 9),
                  bg=COLOR_TRUE, fg="white", relief="flat",
                  padx=12, pady=6, cursor="hand2",
                  command=lambda: self._write_m30_m31(M31_COIL_ADDRESS, True)).pack(side="left", padx=0)

        tk.Frame(self.root, bg=COLOR_BORDER, height=1).pack(fill="x")

        # legend
        leg = tk.Frame(self.root, bg=COLOR_BG, padx=16, pady=5)
        leg.pack(fill="x")
        tk.Label(leg, text="■", fg=COLOR_PLC_LT, bg=COLOR_BG,
                 font=("Courier New", 12)).pack(side="left")
        tk.Label(leg, text=" PLC tag  ", fg="#666666", bg=COLOR_BG,
                 font=MONO_SM).pack(side="left")
        tk.Label(leg, text="■", fg=COLOR_AMR_LT, bg=COLOR_BG,
                 font=("Courier New", 12)).pack(side="left")
        tk.Label(leg, text=" AMR tag", fg="#666666", bg=COLOR_BG,
                 font=MONO_SM).pack(side="left")

        tk.Frame(self.root, bg=COLOR_BORDER, height=1).pack(fill="x")

        # two columns
        body = tk.Frame(self.root, bg=COLOR_BG, padx=12, pady=10)
        body.pack(fill="both")

        left  = tk.Frame(body, bg=COLOR_BG)
        sep   = tk.Frame(body, bg=COLOR_BORDER, width=1)
        right = tk.Frame(body, bg=COLOR_BG)

        left.pack(side="left",  fill="both", expand=True, padx=(0, 8))
        sep.pack(side="left",   fill="y",    padx=4)
        right.pack(side="left", fill="both", expand=True, padx=(8, 0))

        # UNLOAD
        self._col_header(left, "UNLOAD", "Station → AMR", "#EF6C00")
        for i, (tag, side, label) in enumerate(UNLOAD_SEQ):
            self._seq_row(left, tag, side, label, i + 1, MONO, MONO_SM)
        bf = tk.Frame(left, bg=COLOR_BG, pady=8)
        bf.pack(fill="x")
        self._bulk_btn(bf, "Reset UNLOAD", lambda: self._reset_seq(UNLOAD_SEQ), COLOR_FALSE)

        # LOAD
        self._col_header(right, "LOAD", "AMR → Station", "#2E7D32")
        for i, (tag, side, label) in enumerate(LOAD_SEQ):
            self._seq_row(right, tag, side, label, i + 1, MONO, MONO_SM)
        bf2 = tk.Frame(right, bg=COLOR_BG, pady=8)
        bf2.pack(fill="x")
        self._bulk_btn(bf2, "Reset LOAD", lambda: self._reset_seq(LOAD_SEQ), COLOR_FALSE)

        tk.Frame(self.root, bg=COLOR_BORDER, height=1).pack(fill="x")

        # log
        lf = tk.Frame(self.root, bg=COLOR_BG, padx=16, pady=8)
        lf.pack(fill="x")
        tk.Label(lf, text="LOG", fg="#555555", bg=COLOR_BG,
                 font=("Courier New", 9, "bold")).pack(anchor="w")
        self.log_box = tk.Text(lf, height=5, bg=COLOR_PANEL, fg="#aaaaaa",
                               font=("Courier New", 9), relief="flat",
                               bd=0, state="disabled", wrap="none")
        self.log_box.pack(fill="x")
        self.log_box.tag_config("ok",   foreground=COLOR_TRUE)
        self.log_box.tag_config("err",  foreground=COLOR_FALSE)
        self.log_box.tag_config("warn", foreground=COLOR_WARN)
        self.log_box.tag_config("inf",  foreground="#888888")

    def _col_header(self, parent, title, subtitle, color):
        f = tk.Frame(parent, bg=COLOR_BG, pady=6)
        f.pack(fill="x")
        tk.Label(f, text=title, fg=color, bg=COLOR_BG,
                 font=("Courier New", 13, "bold")).pack(side="left")
        tk.Label(f, text=f"  {subtitle}", fg="#555555", bg=COLOR_BG,
                 font=("Courier New", 9)).pack(side="left")

    def _seq_row(self, parent, tag, side, label, step, mono, mono_sm):
        color = COLOR_PLC_LT if side == "plc" else COLOR_AMR_LT
        panel = "#1a2a3a"    if side == "plc" else "#2a1a3a"

        row = tk.Frame(parent, bg=panel, pady=5, padx=10,
                       highlightthickness=1, highlightbackground=COLOR_BORDER)
        row.pack(fill="x", pady=2)

        tk.Label(row, text=f"{step}", fg=color, bg=panel,
                 font=("Courier New", 11, "bold"), width=2).pack(side="left")

        ind = tk.Label(row, text=" ●", fg=COLOR_FALSE, bg=panel,
                       font=("Courier New", 12))
        ind.pack(side="left")
        self.indicators[tag] = ind

        tk.Label(row, text=f"  {label}", fg="#cccccc", bg=panel,
                 font=("Courier New", 10), anchor="w", width=26).pack(side="left")

        val = tk.Label(row, text="False", fg=COLOR_FALSE, bg=panel,
                       font=("Courier New", 9, "bold"), width=5)
        val.pack(side="right", padx=4)
        self.val_labels[tag] = val

        btn_color = COLOR_PLC if side == "plc" else COLOR_AMR
        tk.Button(row, text="CLR", font=("Courier New", 8),
                  bg="#333333", fg="#aaaaaa", relief="flat",
                  padx=6, pady=1, cursor="hand2",
                  command=lambda t=tag: self._write(t, False)).pack(side="right", padx=2)
        tk.Button(row, text="SET", font=("Courier New", 8),
                  bg=btn_color, fg="white", relief="flat",
                  padx=6, pady=1, cursor="hand2",
                  command=lambda t=tag: self._write(t, True)).pack(side="right", padx=2)

    def _bulk_btn(self, parent, text, cmd, color):
        tk.Button(parent, text=text, font=("Courier New", 9),
                  bg=color, fg="white", relief="flat",
                  padx=10, pady=4, cursor="hand2",
                  command=cmd).pack(side="left", padx=(0, 6))

    # ── SAFETY FEATURE ────────────────────────────────────────────────────────

    def _write_safety(self, value):
        """Write safety feature state via Modbus (True=OFF, False=ON)"""
        if not self.modbus_client or not self.modbus_client.is_socket_open():
            self._log("Cannot write safety — Modbus not connected", "err")
            return
        
        def do():
            try:
                with self.modbus_lock:
                    result = self.modbus_client.write_coil(
                        address=SAFETY_COIL_ADDRESS,
                        value=value,
                        slave=MODBUS_SLAVE_ID
                    )
                
                if not result.isError():
                    self.safety_state = value
                    self.root.after(0, self._update_safety_ui)
                    status_text = "Safety OFF (M10=1)" if value else "Safety ON (M10=0)"
                    self._log(f"SAFETY WRITE SUCCESS  {status_text}", "ok")
                else:
                    self._log(f"Safety write failed  {result}", "err")
            except Exception as e:
                self._log(f"Safety write error: {e}", "err")
        
        threading.Thread(target=do, daemon=True).start()

    def _poll_safety(self):
        """Poll safety feature state via Modbus"""
        if not self.modbus_client or not self.modbus_client.is_socket_open():
            return
        
        try:
            with self.modbus_lock:
                result = self.modbus_client.read_coils(
                    address=SAFETY_COIL_ADDRESS,
                    count=1,
                    slave=MODBUS_SLAVE_ID
                )
            
            if not result.isError() and result.bits:
                new_state = result.bits[0]
                if new_state != self.safety_state:
                    self.safety_state = new_state
                    self.root.after(0, self._update_safety_ui)
        except Exception as e:
            self._log(f"Safety poll error: {e}", "warn")

    def _update_safety_ui(self):
        """Update safety indicator and status label"""
        if self.safety_state:  # True = Safety OFF
            self.safety_indicator.config(fg=COLOR_FALSE)
            self.safety_status_label.config(text="Safety OFF (M10=1)", fg=COLOR_FALSE)
        else:  # False = Safety ON
            self.safety_indicator.config(fg=COLOR_TRUE)
            self.safety_status_label.config(text="Safety ON (M10=0)", fg=COLOR_TRUE)

    # ── M30 & M31 CONTROLS ────────────────────────────────────────────────────

    def _write_m30_m31(self, coil_address, value):
        """Write M30 or M31 coil state via Modbus"""
        coil_name = f"M{coil_address}"
        if not self.modbus_client or not self.modbus_client.is_socket_open():
            self._log(f"Cannot write {coil_name} — Modbus not connected", "err")
            return
        
        def do():
            try:
                with self.modbus_lock:
                    result = self.modbus_client.write_coil(
                        address=coil_address,
                        value=value,
                        slave=MODBUS_SLAVE_ID
                    )
                
                if not result.isError():
                    # Update state based on coil address
                    if coil_address == M30_COIL_ADDRESS:
                        self.m30_state = value
                        self.root.after(0, self._update_m30_ui)
                    elif coil_address == M31_COIL_ADDRESS:
                        self.m31_state = value
                        self.root.after(0, self._update_m31_ui)
                    
                    status_text = f"{coil_name} = {1 if value else 0} ({value})"
                    self._log(f"WRITE SUCCESS  {status_text}", "ok")
                else:
                    self._log(f"{coil_name} write failed  {result}", "err")
            except Exception as e:
                self._log(f"{coil_name} write error: {e}", "err")
        
        threading.Thread(target=do, daemon=True).start()

    def _poll_m30_m31(self):
        """Poll M30 and M31 states via Modbus"""
        if not self.modbus_client or not self.modbus_client.is_socket_open():
            return
        
        try:
            # Poll M30
            with self.modbus_lock:
                result_m30 = self.modbus_client.read_coils(
                    address=M30_COIL_ADDRESS,
                    count=1,
                    slave=MODBUS_SLAVE_ID
                )
            
            if not result_m30.isError() and result_m30.bits:
                new_state = result_m30.bits[0]
                if new_state != self.m30_state:
                    self.m30_state = new_state
                    self.root.after(0, self._update_m30_ui)
            
            # Poll M31
            with self.modbus_lock:
                result_m31 = self.modbus_client.read_coils(
                    address=M31_COIL_ADDRESS,
                    count=1,
                    slave=MODBUS_SLAVE_ID
                )
            
            if not result_m31.isError() and result_m31.bits:
                new_state = result_m31.bits[0]
                if new_state != self.m31_state:
                    self.m31_state = new_state
                    self.root.after(0, self._update_m31_ui)
        except Exception as e:
            self._log(f"M30/M31 poll error: {e}", "warn")

    def _update_m30_ui(self):
        """Update M30 indicator and status label"""
        if self.m30_state:  # True = ON
            self.m30_indicator.config(fg=COLOR_TRUE)
            self.m30_status_label.config(text="M30 = 1 (ON)", fg=COLOR_TRUE)
        else:  # False = OFF
            self.m30_indicator.config(fg=COLOR_FALSE)
            self.m30_status_label.config(text="M30 = 0 (OFF)", fg=COLOR_FALSE)

    def _update_m31_ui(self):
        """Update M31 indicator and status label"""
        if self.m31_state:  # True = ON
            self.m31_indicator.config(fg=COLOR_TRUE)
            self.m31_status_label.config(text="M31 = 1 (ON)", fg=COLOR_TRUE)
        else:  # False = OFF
            self.m31_indicator.config(fg=COLOR_FALSE)
            self.m31_status_label.config(text="M31 = 0 (OFF)", fg=COLOR_FALSE)

    def _start_connection_thread(self):
        threading.Thread(target=self._connection_loop, daemon=True).start()

    def _connection_loop(self):
        while self.running:
            if not self.connected:
                self._try_connect()
            else:
                self._poll_tags()
                self._poll_safety()
                self._poll_m30_m31()
            time.sleep(POLL_INTERVAL)

    def _try_connect(self):
        self.root.after(0, self._set_status, False, "Connecting...")
        self._log(f"Connecting to PLC  {PLC_IP} ...", "warn")
        
        # Connect to Modbus for safety feature
        try:
            if ModbusTcpClient is None:
                self._log("Modbus not available - install with: pip install pymodbus", "err")
            else:
                with self.modbus_lock:
                    if self.modbus_client:
                        try:
                            self.modbus_client.close()
                        except Exception:
                            pass
                    
                    # Support both old and new pymodbus versions
                    try:
                        # New version (pymodbus >= 3.0)
                        self.modbus_client = ModbusTcpClient(host=MODBUS_IP, port=MODBUS_PORT)
                    except TypeError:
                        # Old version (pymodbus < 3.0)
                        self.modbus_client = ModbusTcpClient(MODBUS_IP, port=MODBUS_PORT)
                    
                    if self.modbus_client.connect():
                        self._log(f"Modbus connected  {MODBUS_IP}:{MODBUS_PORT}", "ok")
                    else:
                        self._log(f"Modbus connection failed  {MODBUS_IP}:{MODBUS_PORT}", "warn")
                        self.modbus_client = None
        except Exception as e:
            self._log(f"Modbus connection error: {e}", "warn")
            self.modbus_client = None
        
        # Connect to PLC via Pylogix
        try:
            with self.plc_lock:
                if self.plc:
                    try:
                        self.plc.Close()
                    except Exception:
                        pass
                self.plc = PLC()
                self.plc.IPAddress = PLC_IP

            # test with a single read
            ret = self.plc.Read(f"{PREFIX}.PLC_LOAD_REQ")
            if ret.Status == "Success":
                self.connected = True
                self.root.after(0, self._set_status, True, f"Connected  {PLC_IP}")
                self._log(f"PLC connected  {PLC_IP}", "ok")
            else:
                self.connected = False
                self.root.after(0, self._set_status, False, f"No response  ({ret.Status})")
                self._log(f"PLC not responding  status={ret.Status}  retrying in {RECONNECT_DELAY}s", "err")
                time.sleep(RECONNECT_DELAY)

        except Exception as e:
            self.connected = False
            self.root.after(0, self._set_status, False, "Connection failed")
            self._log(f"Connection error: {e}  retrying in {RECONNECT_DELAY}s", "err")
            time.sleep(RECONNECT_DELAY)

    def _poll_tags(self):
        all_tags = list({tag for tag, _, _ in ALL_SEQ})
        failed   = 0
        with self.plc_lock:
            for tag in all_tags:
                try:
                    ret = self.plc.Read(f"{PREFIX}.{tag}")
                    if ret.Status == "Success":
                        if ret.Value != self.state[tag]:
                            self.state[tag] = ret.Value
                            self.root.after(0, self._update_ui, tag)
                    else:
                        failed += 1
                except Exception:
                    failed += 1

        if failed > len(all_tags) // 2:
            self.connected = False
            self.root.after(0, self._set_status, False, "Connection lost")
            self._log("PLC connection lost — reconnecting...", "err")

        self.root.after(0, self._tick)

    def _manual_reconnect(self):
        self.connected = False
        self._log("Manual reconnect triggered", "warn")

    def _set_status(self, ok, text):
        color = COLOR_TRUE if ok else (COLOR_WARN if "Connecting" in text else COLOR_FALSE)
        self.status_dot.config(fg=color)
        self.status_txt.config(text=f"  {text}", fg=color)

    # ── WRITE ─────────────────────────────────────────────────────────────────

    def _write(self, tag, value):
        if not self.connected:
            self._log("Cannot write — PLC not connected", "err")
            return
        def do():
            full = f"{PREFIX}.{tag}"
            try:
                with self.plc_lock:
                    ret = self.plc.Write(full, value)
                if ret.Status == "Success":
                    self.state[tag] = value
                    self.root.after(0, self._update_ui, tag)
                    self._log(f"WRITE  {full} = {value}", "ok")
                else:
                    self._log(f"WRITE FAILED  {full}  status={ret.Status}", "err")
                    if ret.Status in ("Unknown Device", "No route to target", "timeout"):
                        self.connected = False
                        self.root.after(0, self._set_status, False, "Connection lost")
            except Exception as e:
                self._log(f"WRITE ERROR  {full}  {e}", "err")
                self.connected = False
                self.root.after(0, self._set_status, False, "Connection lost")
        threading.Thread(target=do, daemon=True).start()

    def _reset_seq(self, seq):
        for tag, _, _ in seq:
            self._write(tag, False)

    # ── UI UPDATE ─────────────────────────────────────────────────────────────

    def _update_ui(self, tag):
        v     = self.state[tag]
        color = COLOR_TRUE if v else COLOR_FALSE
        self.indicators[tag].config(fg=color)
        self.val_labels[tag].config(text="True" if v else "False", fg=color)

    def _tick(self):
        self.ts_lbl.config(text=time.strftime("%H:%M:%S"))

    def _log(self, msg, kind="inf"):
        ts   = time.strftime("%H:%M:%S")
        line = f"[{ts}]  {msg}\n"
        self.root.after(0, self._append_log, line, kind)

    def _append_log(self, line, kind):
        self.log_box.config(state="normal")
        self.log_box.insert("end", line, kind)
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def stop(self):
        self.running = False
        if self.plc:
            try:
                self.plc.Close()
            except Exception:
                pass
        if self.modbus_client:
            try:
                self.modbus_client.close()
            except Exception:
                pass


if __name__ == "__main__":
    root = tk.Tk()
    app  = PLCMonitor(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.stop(), root.destroy()))
    root.mainloop()