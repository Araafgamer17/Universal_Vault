#Made by Araaf

global volume_level
global is_muted
global is_dragging
global seek_frame
import base64
import os
import sys
import io
import cv2
import pygame
import time
import subprocess
import shutil
import zipfile
import tempfile
import uuid
import atexit
import threading
import signal
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog as sd
from tkinterdnd2 import DND_FILES, TkinterDnD
from moviepy.video.io.VideoFileClip import VideoFileClip
import re
import numpy as np
from tkinterweb import HtmlFrame
import random
from PIL import Image, ImageTk
from cryptography.fernet import Fernet
import hashlib
from tkinter import ttk, messagebox, filedialog, simpledialog as sd
TEMP_TRACKER = []
def cleanup_all_temps(*args):
    """Forcefully removes all tracked temp files and directories"""
    for path in TEMP_TRACKER:
        try:
            if os.path.exists(path):
                if os.path.isdir(path):
                    shutil.rmtree(path, ignore_errors=True)
                else:
                    os.remove(path)
        except:
            pass
    if args:
        sys.exit(0)
atexit.register(cleanup_all_temps)
if sys.platform != 'win32':
    signal.signal(signal.SIGTERM, cleanup_all_temps)
    signal.signal(signal.SIGHUP, cleanup_all_temps)
signal.signal(signal.SIGINT, cleanup_all_temps)
def ensure_binary(data):
    # irreducible cflow, using cdg fallback
    """Shields binary files from corruption and decodes Vault files"""
    # ***<module>.ensure_binary: Failure: Compilation Error
    if not data:
        return b''
    binary_headers = (b'ftyp', b'\xff\xd8', b'\x89PNG', b'GIF8', b'BM', b'PK', b'\x00\x00\x00', b'\x1aE\xdf\xa3', b'ID3')
    if any((data.startswith(h) for h in binary_headers)) and (not <code object get_temp_path at 0x76025ed06f50, file "player.py", line 106>(<code object ThemedProperties at 0x760246b9d9b0, file "player.py", line 112>)):
        return data
    else:
        try:
            candidate = data.strip().strip(b'"').strip(b"'")
            return base64.b64decode(candidate)
        except:
            return data
def smart_decode(file_path):
    # irreducible cflow, using cdg fallback
    """Safely reads the file as raw binary without modification"""
    # ***<module>.smart_decode: Failure: Compilation Error
    with open(file_path, 'rb') as f:
        return f.read()
                except Exception as e:
                        print(f'Read Error: {e}')
                            return b''
def show_themed_error(parent, title, message):
    """Displays a cyberpunk-themed error overlay."""
    err_win = tk.Toplevel(parent)
    err_win.overrideredirect(True)
    err_win.attributes('-topmost', True)
    err_win.configure(bg='#0a0a0a', highlightbackground='#00FF41', highlightthickness=2)
    parent.update_idletasks()
    x = parent.winfo_x() + parent.winfo_width() // 2 - 150
    y = parent.winfo_y() + parent.winfo_height() // 2 - 75
    err_win.geometry(f'300x150+{x}+{y}')
    tk.Label(err_win, text=f' ⚠ {title} ', bg='#00FF41', fg='#000', font=('Consolas', 10, 'bold')).pack(fill='x')
    tk.Label(err_win, text=message, bg='#0a0a0a', fg='#00FF41', font=('Consolas', 10), wraplength=250, pady=20).pack()
    btn = tk.Label(err_win, text='[ DISMISS ]', bg='#0a0a0a', fg='#00FF41', font=('Consolas', 10, 'bold'), cursor='hand2')
    btn.pack(pady=5)
    btn.bind('<Button-1>', lambda e: err_win.destroy())
def get_temp_path(ext):
    """Generates a tracked temporary file path for media playback"""
    temp_file = os.path.join(tempfile.gettempdir(), f'{uuid.uuid4()}{ext}')
    TEMP_TRACKER.append(temp_file)
    return temp_file
class ThemedProperties(tk.Toplevel):
    def __init__(self, parent, title, stats_dict):
        super().__init__(parent)
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.configure(bg='#000000', highlightthickness=0)
        w, h = (420, 320)
        px, py = (parent.winfo_x(), parent.winfo_y())
        self.geometry(f'{w}x{h}+{px + 50}+{py + 50}')
        self._drag_data = {'x': 0, 'y': 0}
        header = tk.Frame(self, bg='#0a0a0a', height=35)
        header.pack(fill='x', side='top')
        header.pack_propagate(False)
        self.exit_btn = tk.Label(header, text='✕', bg='#0a0a0a', fg='#ff4141', font=('Consolas', 12, 'bold'), cursor='hand2', width=4)
        self.exit_btn.pack(side='right', fill='y')
        self.exit_btn.bind('<Button-1>', lambda e: self.destroy())
        title_lbl = tk.Label(header, text=f' 📂 PROPERTIES {title.upper()}', bg='#0a0a0a', fg='#00FF41', font=('Consolas', 10, 'bold'))
        title_lbl.pack(side='left', padx=10)
        header.bind('<ButtonPress-1>', self.start_move)
        header.bind('<B1-Motion>', self.do_move)
        title_lbl.bind('<ButtonPress-1>', self.start_move)
        title_lbl.bind('<B1-Motion>', self.do_move)
        content = tk.Frame(self, bg='#000000', padx=20, pady=20)
        content.pack(fill='both', expand=True)
        for key, value in stats_dict.items():
            row = tk.Frame(content, bg='#000000')
            row.pack(fill='x', pady=2)
            tk.Label(row, text=f'> {key.ljust(12)}:', bg='#000000', fg='#00FF41', font=('Consolas', 10)).pack(side='left')
            tk.Label(row, text=str(value), bg='#000000', fg='#00FF41', font=('Consolas', 10, 'bold')).pack(side='left', padx=10)
        self.grab_set()
    def start_move(self, event):
        self._drag_data['x'] = event.x
        self._drag_data['y'] = event.y
    def do_move(self, event):
        deltax = event.x - self._drag_data['x']
        deltay = event.y - self._drag_data['y']
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f'+{x}+{y}')
class VaultResizer:
    def __init__(self, target_window, color='#00FF41'):
        self.target = target_window
        self.grip = tk.Label(self.target, text='◢', bg='#000', fg=color, font=('Consolas', 10), cursor='size_nw_se')
        self.grip.place(relx=1.0, rely=1.0, anchor='se')
        self.grip.bind('<Button-1>', self.start_resize)
        self.grip.bind('<B1-Motion>', self.do_resize)
    def start_resize(self, event):
        self.start_w = self.target.winfo_width()
        self.start_h = self.target.winfo_height()
        self.start_x = event.x_root
        self.start_y = event.y_root
    def do_resize(self, event):
        new_w = max(300, self.start_w + (event.x_root - self.start_x))
        new_h = max(200, self.start_h + (event.y_root - self.start_y))
        self.target.geometry(f'{new_w}x{new_h}')
        self.target.update_idletasks()
SELECT_RECT_FILL = '#00FF41'
SELECT_RECT_OUTLINE = '#00FF41'
SELECT_OPACITY = 0.3
class VaultBrowser:
    def __init__(self, raw_data=None):
        self.root = TkinterDnD.Tk()
        self.root.title('Universal Vault Archive Manager')
        self.root.overrideredirect(False)
        self.root.withdraw()
        self.root.after(10, self.root.deiconify)
        self.root.geometry('850x500')
        self.root.configure(bg='#000000')
        self.current_dir = ''
        self.raw = raw_data
        self.active_procs = {}
        self.clipboard = None
        self.header = tk.Frame(self.root, bg='#0a0a0a', height=30)
        self.header.pack(side='top', fill='x')
        self.title_label = tk.Label(self.header, text=' 📂 Universal Vault Archive Manager', bg='#0a0a0a', fg='#00FF41', font=('Consolas', 10))
        self.title_label.pack(side='left', padx=10)
        exit_btn = tk.Label(self.header, text='✕', bg='#0a0a0a', fg='#ff4141', font=('Consolas', 12, 'bold'), cursor='hand2')
        exit_btn.pack(side='right', padx=10)
        exit_btn.bind('<Button-1>', lambda e: self.root.destroy())
        self.header.bind('<ButtonPress-1>', self.start_move)
        self.header.bind('<B1-Motion>', self.do_move)
        self.title_label.bind('<ButtonPress-1>', self.start_move)
        self.title_label.bind('<B1-Motion>', self.do_move)
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.bind('<Escape>', lambda e: self.root.attributes('-fullscreen', False))
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.drop_to_open)
        self.setup_ui()
        self.pulse_state = 0
        self.system_pulse()
        if self.raw:
            self.refresh_view()
    def start_move(self, event):
        """Captures the initial mouse position when clicking the header"""
        self.x = event.x
        self.y = event.y
    def do_move(self, event):
        """Calculates the offset and moves the window"""
        deltax = event.x - self.x
        deltay = event.y - self.y
        new_x = self.root.winfo_x() + deltax
        new_y = self.root.winfo_y() + deltay
        self.root.geometry(f'+{new_x}+{new_y}')
    def setup_ui(self):
        # ***<module>.VaultBrowser.setup_ui: Failure: Different bytecode
        bg_main = '#000000'
        bg_header = '#0a0a0a'
        fg_neon = '#00FF41'
        accent_blue = '#003366'
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview', background=bg_main, foreground=fg_neon, fieldbackground=bg_main, rowheight=25, borderwidth=0, font=('Consolas', 10))
        style.configure('Treeview.Heading', background=bg_header, foreground='#888888', relief='flat', font=('Consolas', 10, 'bold'))
        style.map('Treeview', background=[('selected', accent_blue)])
        toolbar = tk.Frame(self.root, bg=bg_header, bd=0)
        btn_params = {'bg': '#111111', 'fg': '#aaaaaa', 'activebackground': fg_neon, 'activeforeground': 'black', 'relief': 'flat', 'padx': 15, 'pady': 5}
        tk.Button(toolbar, text='SELECT ALL', **btn_params, command=self.toggle_all).pack(side='left', padx=1)
        tk.Button(toolbar, text='EXTRACT', **btn_params, command=self.extract_selected).pack(side='left', padx=1)
        tk.Button(toolbar, text='UP', **btn_params, command=lambda: self.navigate_to('..')).pack(side='left', padx=1)
        self.status_label = tk.Label(toolbar, text='[ SYSTEM ACTIVE ]', bg=bg_header, fg=fg_neon, font=('Consolas', 9))
        self.status_label.pack(side='right', padx=10)
        self.help_btn = tk.Button(self.header, text=' [?] HELP ', command=self.show_help, bg='#000', fg='#aaaaaa', font=('Consolas', 9, 'bold'), activebackground='#00FF41', activeforeground='#000', bd=1, relief='flat')
        self.help_btn.pack(side='right', padx=10, pady=5)
        self.tree = ttk.Treeview(self.root, columns=('size', 'packed', 'type'), show='tree headings', selectmode='extended')
        self.tree.heading('#0', text='NAME', anchor='w')
        self.tree.heading('size', text='SIZE', anchor='e')
        self.tree.heading('packed', text='PACKED', anchor='e')
        self.tree.heading('type', text='TYPE', anchor='w')
        self.tree.column('#0', width=350)
        self.tree.column('size', width=100)
        self.tree.column('packed', width=100)
        self.tree.column('type', width=150)
        self.tree.pack(fill='both', expand=True)
        self.tree.bind('<Button-3>', lambda e: self.context_menu.post(e.x_root, e.y_root))
        self.address_frame = tk.Frame(self.root, bg='#000000', pady=5)
        self.address_frame.pack(side='top', fill='x')
        self.address_var = tk.StringVar(value='Vault:/')
        self.address_bar = tk.Entry(self.address_frame, textvariable=self.address_var, bg='#0a0a0a', fg='#00FF41', insertbackground='#00FF41', relief='flat', font=('Consolas', 10))
        self.address_bar.pack(side='left', fill='x', expand=True, padx=5)
        self.context_menu = tk.Menu(self.root, tearoff=0, bg=bg_header, fg=fg_neon, activebackground=fg_neon, activeforeground='black', font=('Consolas', 10))
        self.context_menu = tk.Menu(self.root, tearoff=0, bg=bg_header, fg=fg_neon, activebackground=fg_neon, activeforeground='black', font=('Consolas', 10))
        self.context_menu.add_command(label=' RUN / OPEN', command=self.run_selected_ctx)
        self.context_menu.add_command(label=' IMPORT FILE...', command=self.import_external_file)
        self.context_menu.add_command(label=' REFRESH VIEW', command=self.refresh_view)
        self.context_menu.add_separator()
        self.new_submenu = tk.Menu(self.context_menu, tearoff=0, bg=bg_header, fg=fg_neon, activebackground=fg_neon, activeforeground='black', font=('Consolas', 10))
        self.new_submenu.add_command(label='Folder', command=self.add_folder)
        self.new_submenu.add_command(label='Encrypted Text Document (.AXT)', command=self.add_text_file)
        self.new_submenu.add_command(label='Text Document (.txt)', command=lambda: self.create_new_doc('.txt'))
        self.context_menu.add_cascade(label='> NEW', menu=self.new_submenu)
        self.context_menu.add_separator()
        self.org_submenu = tk.Menu(self.context_menu, tearoff=0, bg='#0a0a0a', fg='#00FF41', activebackground='#00FF41', activeforeground='#000', font=('Consolas', 9))
        self.org_submenu.add_command(label=' COPY DATA', command=lambda: self.copy_entry(move=False))
        self.org_submenu.add_command(label=' CUT DATA', command=lambda: self.copy_entry(move=True))
        self.org_submenu.add_command(label=' PASTE DATA', command=self.paste_entry)
        self.org_submenu.add_separator(background='#1a1a1a')
        self.context_menu.add_cascade(label='> MANAGE DATA', menu=self.org_submenu)
        self.crypto_menu = tk.Menu(self.context_menu, tearoff=0, bg='#0a0a0a', fg='#00FF41', activebackground='#00FF41', activeforeground='#000', font=('Consolas', 9))
        self.crypto_menu.add_command(label=' Base64 CONVERT', command=self.secure_convert_entry)
        self.crypto_menu.add_command(label=' LOCK FILE (AES)', command=lambda: self.process_crypto(True))
        self.crypto_menu.add_command(label=' UNLOCK FILE', command=lambda: self.process_crypto(False))
        self.crypto_menu.add_separator(background='#1a1a1a')
        self.context_menu.add_cascade(label='> ENCRYPTION', menu=self.crypto_menu)
        self.context_menu.add_command(label=' OPEN CMD', command=self.open_terminal)
        self.context_menu.add_command(label=' EXPORT TO DISK...', command=self.export_selected)
        self.context_menu.add_separator(background='#1a1a1a')
        self.context_menu.add_command(label=' RENAME', command=self.rename_entry)
        warn_red = '#ff4141'
        self.context_menu.add_command(label=' DELETE SELECTED', command=self.delete_selected, foreground=warn_red, activebackground=warn_red, activeforeground='white')
        self.context_menu.add_separator()
        self.context_menu.add_command(label=' PROPERTIES', command=self.view_properties)
        self.context_menu.add_command(label=' SAVE VAULT AS...', command=self.save_vault_as)
        self.tree.bind('<Button-3>', self.show_context_menu)
        self.tree.bind('<Double-1>', self.on_double_click)
        self.tree.tag_configure('green_text', foreground=fg_neon)
    def system_pulse(self):
        if not self.root.winfo_exists():
            return None
        else:
            current_text = self.title_label.cget('text').split('[')[0].strip()
            if not current_text:
                current_text = '📂 Universal Vault Archive Manager'
            self.pulse_state = (self.pulse_state + 1) % 4
            chars = ['—', '\\', '|', '/']
            self.title_label.config(text=f' {current_text} [{chars[self.pulse_state]}]')
            self.root.after(500, self.system_pulse)
    def run_selected_ctx(self):
        item_id = self.tree.selection()
        if not item_id:
            return None
        else:
            name = self.tree.item(item_id[0])['text']
            vals = self.tree.item(item_id[0])['values']
            if vals[2] == 'Folder' or name == '..':
                self.navigate_to(name)
                return None
            else:
                ext = os.path.splitext(name)[1].lower()
                full_path = os.path.join(self.current_dir, name).replace('\\', '/')
                if ext in ('.exe', '.bat', '.wrun'):
                    temp_dir = os.path.join(tempfile.gettempdir(), f'vrun_{uuid.uuid4().hex[:6]}')
                    os.makedirs(temp_dir, exist_ok=True)
                    TEMP_TRACKER.append(temp_dir)
                    with zipfile.ZipFile(io.BytesIO(self.raw), 'r') as z:
                        for info in z.infolist():
                            if info.filename.startswith(self.current_dir):
                                rel_path = info.filename[len(self.current_dir):].lstrip('/')
                                if rel_path and '/' not in rel_path:
                                        target_p = os.path.join(temp_dir, rel_path)
                                        with open(target_p, 'wb') as f:
                                            f.write(z.read(info.filename))
                    def monitor_thread():
                        exec_path = os.path.join(temp_dir, name)
                        self.status_label.config(text=f'[ DATA STREAM ACTIVE: {name} ]')
                        try:
                            if ext == '.bat' or ext == '.wrun':
                                p = subprocess.Popen(f'start /wait cmd /c \"{exec_path}\"', shell=True, cwd=temp_dir)
                            else:
                                p = subprocess.Popen([exec_path], creationflags=subprocess.CREATE_NEW_CONSOLE, cwd=temp_dir)
                            self.active_procs[p.pid] = {'name': name, 'proc': p, 'start': time.time()}
                            p.wait()
                        except Exception as e:
                            self.show_themed_error('EXEC_FAIL', f'Vault execution failed: {e}')
                        finally:
                            if p.pid in self.active_procs:
                                del self.active_procs[p.pid]
                            self.status_label.config(text='[ SYSTEM ACTIVE ]')
                    threading.Thread(target=monitor_thread, daemon=True).start()
                else:
                    full_path = os.path.join(self.current_dir, name).replace('\\', '/')
                    with zipfile.ZipFile(io.BytesIO(self.raw), 'r') as z:
                        raw_data = z.read(full_path)
                        clean_data = ensure_binary(raw_data)
                        if ext == '.dfil':
                            self.raw = clean_data
                            self.current_dir = ''
                            self.refresh_view()
                        else:
                            handle_media(name, ext, clean_data, self)
    def copy_entry(self, move=False):
        item_id = self.tree.selection()
        if not item_id:
            return None
        else:
            name = self.tree.item(item_id[0])['text']
            if name == '..':
                return None
            else:
                full_path = os.path.join(self.current_dir, name).replace('\\', '/')
                self.clipboard = {'path': full_path, 'action': 'move' if move else 'copy'}
                mode = 'CUT' if move else 'COPIED'
                self.status_label.config(text=f'[ DATA {mode}: {name} ] -> READY FOR RELOCATION')
    def paste_entry(self):
        if not self.clipboard:
            return None
        else:
            old_path = self.clipboard['path']
            filename = os.path.basename(old_path)
            dest_dir = self.current_dir
            selection = self.tree.selection()
            if selection:
                sel_vals = self.tree.item(selection[0])['values']
                if sel_vals[2] == 'Folder':
                    sel_name = self.tree.item(selection[0])['text']
                    dest_dir = os.path.join(self.current_dir, sel_name).replace('\\', '/')
            new_path = os.path.join(dest_dir, filename).replace('\\', '/')
            if old_path == new_path and self.clipboard['action'] == 'copy':
                    name_part, ext_part = os.path.splitext(filename)
                    new_path = os.path.join(dest_dir, f'{name_part}_Copy{ext_part}').replace('\\', '/')
            try:
                old_buffer = io.BytesIO(self.raw)
                new_buffer = io.BytesIO()
                with zipfile.ZipFile(old_buffer, 'r') as zin, zipfile.ZipFile(new_buffer, 'w', zipfile.ZIP_DEFLATED) as zout:
                        for item in zin.infolist():
                            if item.filename == new_path:
                                continue
                            else:
                                if self.clipboard['action'] == 'move' and item.filename == old_path:
                                        continue
                                zout.writestr(item, zin.read(item.filename))
                        zout.writestr(new_path, zin.read(old_path))
                self.raw = new_buffer.getvalue()
                if self.clipboard['action'] == 'move':
                    self.clipboard = None
                self.refresh_view()
                self.status_label.config(text='[ SECTOR STREAMS UPDATED ]')
            except Exception as e:
                show_themed_error(self.root, 'VAULT ERROR', f'Paste failed: {e}')
    def rename_entry(self):
        # irreducible cflow, using cdg fallback
        # ***<module>.VaultBrowser.rename_entry: Failure: Compilation Error
        item_id = self.tree.selection()
        if not item_id:
            return None
        else:
            old_name = self.tree.item(item_id[0])['text']
            if old_name == '..':
                return None
            else:
                dialog = ThemedDialog(self.root, 'SYSTEM RENAME', f'ENTER NEW IDENTITY FOR {old_name}:')
                self.root.wait_window(dialog)
                new_name = dialog.result
                if not new_name or new_name == old_name:
                    return None
                else:
                    old_path = os.path.join(self.current_dir, old_name).replace('\\', '/')
                    new_path = os.path.join(self.current_dir, new_name).replace('\\', '/')
        old_buf = io.BytesIO(self.raw)
        new_buf = io.BytesIO()
        with zipfile.ZipFile(old_buf, 'r') as zin:
            if new_path in zin.namelist():
                show_themed_error(self.root, 'FILE CONFLICT', 'A file with that name already exists.')
                return
                with zipfile.ZipFile(new_buf, 'w', zipfile.ZIP_DEFLATED) as zout:
                    for item in zin.infolist():
                        if item.filename == old_path:
                            zout.writestr(new_path, zin.read(item.filename))
                        else:
                            zout.writestr(item, zin.read(item.filename))
                                self.raw = new_buf.getvalue()
                                self.refresh_view()
                        except Exception as e:
                                show_themed_error(self.root, 'RENAME ERROR', f'System could not rename: {str(e)}')
    def get_crypto_key(self):
        dialog = ThemedDialog(self.root, 'ENCRYPTION KEY', 'ENTER MASTER PASS-PHRASE:')
        self.root.wait_window(dialog)
        pwd = dialog.result
        if not pwd:
            return None
        else:
            import base64
            key = base64.urlsafe_b64encode(hashlib.sha256(pwd.encode()).digest())
            return Fernet(key)
    def process_crypto(self, encrypt=True):
        # irreducible cflow, using cdg fallback
        # ***<module>.VaultBrowser.process_crypto: Failure: Compilation Error
        item_id = self.tree.selection()
        if not item_id:
            return None
        else:
            name = self.tree.item(item_id[0])['text']
            if name == '..':
                return None
            else:
                if encrypt and name.endswith('.lock'):
                    show_themed_error(self.root, 'SECURITY_OVERLAP', 'SECTOR IS ALREADY ENCRYPTED. MULTIPLE LOCKS NOT PERMITTED.')
                    return None
                else:
                    f_key = self.get_crypto_key()
                    if not f_key:
                        return None
                    else:
                        old_path = os.path.join(self.current_dir, name).replace('\\', '/')
                        if encrypt:
                            new_name = name + '.lock'
                        else:
                            new_name = name.replace('.lock', '')
                        new_path = os.path.join(self.current_dir, new_name).replace('\\', '/')
        old_buffer = io.BytesIO(self.raw)
        new_buffer = io.BytesIO()
        with zipfile.ZipFile(old_buffer, 'r') as zin:
            data = zin.read(old_path)
            with zipfile.ZipFile(new_buffer, 'w', zipfile.ZIP_DEFLATED) as zout:
                for item in zin.infolist():
                    if item.filename == old_path:
                        continue
                    else:
                        zout.writestr(item, zin.read(item.filename))
                if encrypt:
                    processed_bytes = f_key.encrypt(data)
                    processed_bytes = f_key.decrypt(data)
                        zout.writestr(new_path, processed_bytes)
                            self.raw = new_buffer.getvalue()
                            self.refresh_view()
                            self.status_label.config(text=f'[ CRYPTO_OP COMPLETE: {new_name} ]')
                        show_themed_error(self.root, 'DECRYPTION_FAILURE', 'ACCESS DENIED: THE PROVIDED PASS-PHRASE DOES NOT MATCH THE ENCRYPTION HASH.')
                            return
                            except Exception as e:
                                    show_themed_error(self.root, 'SYSTEM ERROR', f'Crypto Failed: {e}')
    def secure_convert_entry(self):
        item_id = self.tree.selection()
        if not item_id:
            return None
        else:
            old_name = self.tree.item(item_id[0])['text']
            if old_name == '..':
                return None
            else:
                ext = os.path.splitext(old_name)[1].lower()
                base = os.path.splitext(old_name)[0]
                mapping = {'.mp4': '.video', '.avi': '.video', '.mkv': '.video', '.jpg': '.pic', '.png': '.pic', '.bmp': '.pic', '.exe': '.rxe', '.bat': '.wrun', '.cmd': '.wrun', '.zip': '.dfil', '.7z': '.dfil', '.rar': '.dfil', '.txt': '.axt', '.mp3': '.audio', '.wav': '.audio', '.flac': '.audio', '.html': '.web', '.secret': '.glitch', '.raw': '.hex'}
                target_ext = mapping.get(ext, '.dfil')
                new_name = base + target_ext
                old_path = os.path.join(self.current_dir, old_name).replace('\\', '/')
                new_path = os.path.join(self.current_dir, new_name).replace('\\', '/')
                try:
                    old_buf = io.BytesIO(self.raw)
                    new_buf = io.BytesIO()
                    with zipfile.ZipFile(old_buf, 'r') as zin:
                        data = zin.read(old_path)
                        secure_data = base64.b64encode(data)
                        with zipfile.ZipFile(new_buf, 'w', zipfile.ZIP_DEFLATED) as zout:
                            for item in zin.infolist():
                                if item.filename == old_path:
                                    continue
                                else:
                                    zout.writestr(item, zin.read(item.filename))
                            zout.writestr(new_path, secure_data)
                    self.raw = new_buf.getvalue()
                    self.refresh_view()
                    self.status_label.config(text=f'[ SECURE ] CONVERTED & ENCODED: {new_name}')
                except Exception as e:
                    show_themed_error(self.root, 'SECURE CONVERSION FAILURE', f'System could not process: {e}')
    def export_selected(self):
        # irreducible cflow, using cdg fallback
        # ***<module>.VaultBrowser.export_selected: Failure: Compilation Error
        item_id = self.tree.selection()
        if not item_id:
            return None
        else:
            name = self.tree.item(item_id[0])['text']
            if name == '..':
                return None
            else:
                suggested_name = name
                if name.endswith('.slides'):
                    suggested_name = name.replace('.slides', '.pptx')
                else:
                    if name.endswith('.video'):
                        suggested_name = name.replace('.video', '.mp4')
                    else:
                        if name.endswith('.pic'):
                            suggested_name = name.replace('.pic', '.png')
                        else:
                            if name.endswith('.axt'):
                                suggested_name = name.replace('.axt', '.txt')
                export_path = filedialog.asksaveasfilename(initialfile=suggested_name, title='EXPORT SECTOR', filetypes=[('Original Format', f'*{os.path.splitext(suggested_name)[1]}'), ('Vault Format', f'*{os.path.splitext(name)[1]}'), ('All Files', '*.*')])
                if not export_path:
                    return None
        full_path = os.path.join(self.current_dir, name).replace('\\', '/')
        with zipfile.ZipFile(io.BytesIO(self.raw), 'r') as zin:
            data = zin.read(full_path)
        standard_exts = ['.pptx', '.ppt', '.mp4', '.png', '.jpg', '.txt', '.exe']
        is_standard = any((export_path.lower().endswith(ext) for ext in standard_exts))
                            secure_exts = ['.slides', '.video', '.pic', '.axt', '.rxe', '.wrun']
                            is_secure_source = any((name.lower().endswith(ext) for ext in secure_exts))
                                                if is_standard and is_secure_source:
                                                        try:
                                                            data = base64.b64decode(data)
                                                            self.status_label.config(text='[ SYSTEM ] DECRYPTING FOR EXTERNAL USE...')
                                                        except:
                                                            pass
                                                with open(export_path, 'wb') as f:
                                                    f.write(data)
                                                self.status_label.config(text=f'[ SUCCESS ] EXPORTED: {os.path.basename(export_path)}')
                                                except Exception as e:
                                                        show_themed_error(self.root, 'EXPORT ERROR', f'System failed to export: {e}')
    def create_new_doc(self, extension):
        dialog = ThemedDialog(self.root, 'NEW DATA', f'NAME YOUR {extension.upper()} FILE:')
        self.root.wait_window(dialog)
        filename = dialog.result
        if not filename:
            return None
        else:
            if not filename.endswith(extension):
                filename += extension
            initial_content = f'--- VAULT DOCUMENT ---\nCREATED: {time.ctime()}\n----------------------\n'
            data = initial_content.encode('utf-8')
            if extension == '.axt':
                data = base64.b64encode(data)
            target_path = os.path.join(self.current_dir, filename).replace('\\', '/')
            try:
                new_buf = io.BytesIO()
                if not self.raw:
                    with zipfile.ZipFile(new_buf, 'w', zipfile.ZIP_DEFLATED) as zout:
                        zout.writestr(target_path, data)
                else:
                    with zipfile.ZipFile(io.BytesIO(self.raw), 'r') as zin, zipfile.ZipFile(new_buf, 'w', zipfile.ZIP_DEFLATED) as zout:
                            for item in zin.infolist():
                                if item.filename == target_path:
                                    continue
                                else:
                                    zout.writestr(item, zin.read(item.filename))
                            zout.writestr(target_path, data)
                self.raw = new_buf.getvalue()
                self.refresh_view()
                self.status_label.config(text=f'[ SYSTEM ] CREATED {extension.upper()}: {filename}')
            except Exception as e:
                show_themed_error(self.root, 'SYSTEM WRITE FAILURE', f'System could not create file: {str(e)}')
    def show_help(self):
        """Displays the Vault System Manual with Dragging Enabled"""
        help_top = tk.Toplevel(self.root)
        help_top.overrideredirect(True)
        help_top.geometry('500x400')
        help_top.configure(bg='#000000', highlightbackground='#00FF41', highlightthickness=1)
        help_top.attributes('-topmost', True)
        help_top._drag_data = {'x': 0, 'y': 0}
        def start_move(event):
            help_top._drag_data['x'] = event.x
            help_top._drag_data['y'] = event.y
        def do_move(event):
            deltax = event.x - help_top._drag_data['x']
            deltay = event.y - help_top._drag_data['y']
            x = help_top.winfo_x() + deltax
            y = help_top.winfo_y() + deltay
            help_top.geometry(f'+{x}+{y}')
        head = tk.Frame(help_top, bg='#0a0a0a', height=30)
        head.pack(side='top', fill='x')
        head.bind('<ButtonPress-1>', start_move)
        head.bind('<B1-Motion>', do_move)
        title_lbl = tk.Label(head, text=' 📂 SYSTEM_MANUAL.txt', bg='#0a0a0a', fg='#00FF41', font=('Consolas', 9, 'bold'))
        title_lbl.pack(side='left', padx=10)
        title_lbl.bind('<ButtonPress-1>', start_move)
        title_lbl.bind('<B1-Motion>', do_move)
        close_btn = tk.Label(head, text='✕', bg='#0a0a0a', fg='#ff4141', font=('Consolas', 12, 'bold'), cursor='hand2')
        close_btn.pack(side='right', padx=10)
        close_btn.bind('<Button-1>', lambda e: help_top.destroy())
        text_area = tk.Text(help_top, bg='#000', fg='#00FF41', font=('Consolas', 10), padx=15, pady=15, bd=0, highlightthickness=0, insertbackground='#00FF41')
        text_area.pack(fill='both', expand=True)
        text_area.config(state='normal')
        manual_text = '\n> VAULT OS v1.60 - HELP COMMANDS\n---------------------------------------\n[ FILE Base64 CONVART ]\n- .MP4 , .MKV , .avi  : .VIDEO\n- .MP3 , .WAV , .FLAC : .AUDIO\n- .PNG , .JPG , .BMP  : .PIC\n- .TXT                : .AXT\n- .ZIP , .7Z , .RAR   : .DFILL\n- .HTML               : .WEB\n- .EXE                : .RXE\n- .BAT , .CMD         : .WRUN\n\n[ MEDIA PLAYER ]\n- TRYS TO PLAYS ALL THE MEDIA\n\n[ FEATURE ]\n- RIGHT CLICK TO OPEN THE RIGHT MENU.\n- YOU CAN LOCK ANY FILE.\n- PRESS F11 TO FULLSCREEN.\n----------------------------------------\n          MADE BY ARAAF\n----------------------------------------\n'
        def type_text(index=0):
            if not help_top.winfo_exists():
                return None
            else:
                if index < len(manual_text):
                    text_area.config(state='normal')
                    text_area.insert('end', manual_text[index])
                    text_area.config(state='disabled')
                    text_area.see('end')
                    help_top.after(5, lambda: type_text(index + 1))
        type_text()
    def toggle_fullscreen(self, event=None):
        """Toggles Fullscreen mode (F11) while handling override-redirect"""
        is_fullscreen = self.root.attributes('-fullscreen')
        new_state = not is_fullscreen
        self.root.overrideredirect(False)
        self.root.attributes('-fullscreen', new_state)
        self.root.overrideredirect(False)
        self.root.focus_force()
        return 'break'
    def open_terminal(self):
        """Opens a standard CMD window in the current vault directory"""
        try:
            subprocess.Popen('start cmd /k \"title VAULT_TERMINAL && @echo off && color 0A && echo JUST TYPE THE COMMANDS \"', shell=True)
        except Exception as e:
            show_themed_error(self.root, 'EXECUTION ERROR', f'Could not initialize CMD: {e}')
    def show_in_taskbar(self, window):
        """Forces a tkinter window to appear in the taskbar."""
        window.withdraw()
        window.after(10, window.deiconify)
        window.attributes('-alpha', 1.0)
        show_in_taskbar(root)
        exit_button = tk.Button(root, text='X', command=root.destroy, bg='red', fg='white')
        exit_button.pack(anchor='ne')
    def refresh_view(self):
        """Clears the treeview and repopulates it with the current directory contents."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        if not self.raw:
            return None
        else:
            try:
                with zipfile.ZipFile(io.BytesIO(self.raw), 'r') as z:
                    all_files = z.namelist()
                    if self.current_dir:
                        self.tree.insert('', 'end', text='..', values=('', '', 'Folder'), tags=('green_text',))
                    display_items = []
                    seen_folders = set()
                    for f in all_files:
                        if f.startswith(self.current_dir):
                            rel_path = f[len(self.current_dir):]
                            if not rel_path:
                                continue
                            else:
                                parts = rel_path.split('/')
                                name = parts[0]
                                if len(parts) > 1 or f.endswith('/'):
                                    if name not in seen_folders:
                                        display_items.append({'name': name, 'is_dir': True, 'size': 0, 'packed': 0, 'type': 'Folder'})
                                        seen_folders.add(name)
                                else:
                                    info = z.getinfo(f)
                                    display_items.append({'name': name, 'is_dir': False, 'size': info.file_size, 'packed': info.compress_size, 'type': os.path.splitext(name)[1].upper() or 'FILE'})
                    display_items.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))
                    self.animate_entry(display_items, 0)
            except zipfile.BadZipFile:
                self.status_label.config(text='[ ERR: INVALID VAULT FORMAT ]', fg='#ff4141')
            count = len(self.tree.get_children())
            self.status_label.config(text=f' [ ACTIVE_STREAMS: {count} ] | [ SECTOR: {self.current_dir or 'ROOT'} ]')
    def animate_entry(self, items, index):
        if index < len(items):
            item = items[index]
            s = f'{item['size']:,}' if not item['is_dir'] else ''
            p = f'{item['packed']:,}' if not item['is_dir'] else ''
            self.tree.insert('', 'end', text=item['name'], values=(s, p, item['type']), tags=('green_text',))
            self.root.after(25, lambda: self.animate_entry(items, index + 1))
    def show_context_menu(self, event):
        """Selects the item under the mouse and shows the menu."""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
        self.context_menu.post(event.x_root, event.y_root)
    def rename_selected(self):
        sel = self.tree.selection()
        if not sel:
            return None
        else:
            old_name = self.tree.item(sel[0])['text']
            new_name = sd.askstring('Rename', f'Rename \'{old_name}\' to:', initialvalue=old_name, parent=self.root)
            if new_name and new_name != old_name:
                    with zipfile.ZipFile(io.BytesIO(self.raw), 'r') as old_z:
                        in_mem = io.BytesIO()
                        with zipfile.ZipFile(in_mem, 'w', zipfile.ZIP_DEFLATED) as new_z:
                            old_path = os.path.join(self.current_dir, old_name).replace('\\', '/')
                            new_path = os.path.join(self.current_dir, new_name).replace('\\', '/')
                            for item in old_z.infolist():
                                content = old_z.read(item.filename)
                                name = item.filename.replace(old_path, new_path, 1) if item.filename.startswith(old_path) else item.filename
                                new_z.writestr(name, content)
                    self.raw = in_mem.getvalue()
                    self.refresh_view()
    def view_properties(self):
        """Displays terminal-style metadata using the ThemedProperties overlay."""
        sel = self.tree.selection()
        if not sel or not self.raw:
            return None
        else:
            item_data = self.tree.item(sel[0])
            name = item_data['text']
            values = item_data['values']
            if name == '..':
                return None
            else:
                ext = os.path.splitext(name)[1].lower()
                encrypted_exts = ['.rxe', '.wrun', '.pic', '.video', '.audio', '.axt', '.dfil', '.web', '.glitch']
                if values[2] == 'Folder':
                    status_msg = 'DIRECTORY_NODE'
                else:
                    status_msg = 'ENCRYPTED_ARCHIVE' if ext in encrypted_exts else 'STANDARD_DATA_NODE'
                full_path = os.path.join(self.current_dir, name).replace('\\', '/')
                if values[2] == 'Folder' and (not full_path.endswith('/')):
                        full_path += '/'
                with zipfile.ZipFile(io.BytesIO(self.raw), 'r') as z:
                    try:
                        info = z.getinfo(full_path)
                        comp_pct = 0
                        if info.file_size > 0:
                            comp_pct = round((1 - info.compress_size / info.file_size) * 100, 1)
                        type_map = {'.exe': 'EXECUTABLE_BIN', '.rxe': 'ENCRYPTED_EXEC', '.axt': 'ENCRYPTED_TEXT', '.pic': 'ENCRYPTED_IMAGE', '.png': 'IMAGE_RASTER', '.video': 'ENCRYPTED_VIDEO', '.mp4': 'VIDEO_STREAM', '.dfil': 'DATABASE_FILE'}
                        file_type = type_map.get(ext, f'{ext[1:].upper()}_FILE' if ext else 'UNKNOWN_NODE')
                        stats = {'NAME': name.upper(), 'TYPE': file_type, 'RAW_SIZE': f'{info.file_size:,} bits', 'COMP_EFF': f'{comp_pct}% optimized', 'TIMESTAMP': f'{info.date_time[0]}.{info.date_time[1]:02}.{info.date_time[2]:02}', 'OS_KERNEL': 'WIN_NT' if info.create_system == 0 else 'UNIX_CORE', 'STATUS': status_msg}
                        ThemedProperties(self.root, name, stats)
                    except Exception as e:
                        self.status_label.config(text=f'[ ERR: SECTOR_READ_FAIL - {str(e)[:10]} ]', fg='#ff4141')
    def import_external_file(self):
        paths = filedialog.askopenfilenames(title='Select files to import into Vault')
        if not paths:
            return None
        else:
            for p in paths:
                with open(p, 'rb') as f:
                    self.import_raw_data(os.path.basename(p), f.read())
            ThemedNotify(self.root, 'Vault', f'IMPORTED {len(paths)} FILES SUCCESSFULLY.')
    def delete_selected_by_name(self, name):
        if not self.raw:
            return None
        else:
            with zipfile.ZipFile(io.BytesIO(self.raw), 'r') as old_z:
                in_mem = io.BytesIO()
                with zipfile.ZipFile(in_mem, 'w', zipfile.ZIP_DEFLATED) as new_z:
                    target = os.path.join(self.current_dir, name).replace('\\', '/')
                    for item in old_z.infolist():
                        if item.filename != target:
                            new_z.writestr(item, old_z.read(item.filename))
            self.raw = in_mem.getvalue()
            self.root.after(0, self.refresh_view)
    def read_text(self, name, raw_bytes):
        top = tk.Toplevel(self.root)
        top.overrideredirect(True)
        top.geometry('800x500')
        top.configure(bg='#000000')
        top.attributes('-topmost', True)
        def start_move(event):
            top.x, top.y = (event.x, event.y)
        def do_move(event):
            deltax, deltay = (event.x - top.x, event.y - top.y)
            top.geometry(f'+{top.winfo_x() + deltax}+{top.winfo_y() + deltay}')
        header = tk.Frame(top, bg='#0a0a0a', height=30)
        header.pack(side='top', fill='x')
        lbl_title = tk.Label(header, text=f' 📂 EDITING: {name}', bg='#0a0a0a', fg='#00FF41', font=('Consolas', 10))
        lbl_title.pack(side='left', padx=10)
        def save_content():
            new_text = txt.get('1.0', 'end-1c')
            if name.lower().endswith('.axt'):
                save_data = base64.b64encode(new_text.encode('utf-8'))
            else:
                save_data = new_text.encode('utf-8')
            self.import_raw_data(name, save_data)
            self.status_label.config(text=f'[ DATA COMMITTED: {name} ]')
            save_btn.config(text='✓ SAVED', fg='#00FF41')
            top.after(1000, lambda: save_btn.config(text='💾 SAVE', fg='#aaaaaa'))
        save_btn = tk.Label(header, text='💾 SAVE', bg='#111111', fg='#aaaaaa', font=('Consolas', 9, 'bold'), cursor='hand2', padx=10)
        save_btn.pack(side='right', padx=5)
        save_btn.bind('<Button-1>', lambda e: save_content())
        exit_btn = tk.Label(header, text='✕', bg='#0a0a0a', fg='#ff4141', font=('Consolas', 12, 'bold'), cursor='hand2')
        exit_btn.pack(side='right', padx=10)
        exit_btn.bind('<Button-1>', lambda e: top.destroy())
        for widget in (header, lbl_title):
            widget.bind('<ButtonPress-1>', start_move)
            widget.bind('<B1-Motion>', do_move)
        txt = tk.Text(top, bg='#000000', fg='#00FF41', insertbackground='#00FF41', font=('Consolas', 12), borderwidth=0, padx=10, pady=10)
        txt.pack(expand=True, fill='both')
        try:
            if name.lower().endswith('.axt'):
                display_data = base64.b64decode(raw_bytes).decode('utf-8')
            else:
                display_data = raw_bytes.decode('utf-8')
        except Exception:
            display_data = raw_bytes.decode('utf-8', errors='ignore')
        txt.insert('1.0', display_data)
        VaultResizer(top)
    def navigate_to(self, name):
        if name == '..':
            parts = self.current_dir.strip('/').split('/')
            self.current_dir = '/'.join(parts[:(-1)]) + ('/' if len(parts) > 1 else '')
        else:
            self.current_dir += name + '/'
        self.address_var.set(f'Vault:/{self.current_dir}')
        self.refresh_view()
    def on_double_click(self, event):
        self.run_selected_ctx()
    def drop_to_open(self, event):
        path = event.data.strip('{}')
        threading.Thread(target=start_player, args=(path, self), daemon=True).start()
    def add_folder(self):
        if self.raw is None:
            in_mem = io.BytesIO()
            zipfile.ZipFile(in_mem, 'w').close()
            self.raw = in_mem.getvalue()
        dialog = ThemedDialog(self.root, 'Create Directory', 'ENTER FOLDER NAME:')
        self.root.wait_window(dialog)
        n = dialog.result
        if n:
            self.import_raw_data(os.path.join(self.current_dir, n).replace('\\', '/') + '/', b'')
    def add_text_file(self):
        if self.raw is None:
            in_mem = io.BytesIO()
            zipfile.ZipFile(in_mem, 'w').close()
            self.raw = in_mem.getvalue()
        dialog = ThemedDialog(self.root, 'NEW SECTOR', 'NAME FOR SECURE DOCUMENT (.axt):')
        self.root.wait_window(dialog)
        name = dialog.result
        if not name:
            return None
        else:
            if not name.lower().endswith('.axt'):
                name += '.axt'
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            header = f'--- [ SECURE SECTOR ] ---\nCREATED: {timestamp}\n------------------------\n\n'
            secure_data = base64.b64encode(header.encode('utf-8'))
            try:
                old_buf = io.BytesIO(self.raw)
                new_buf = io.BytesIO()
                target_path = os.path.join(self.current_dir, name).replace('\\', '/')
                with zipfile.ZipFile(old_buf, 'r') as zin, zipfile.ZipFile(new_buf, 'w', zipfile.ZIP_DEFLATED) as zout:
                        for item in zin.infolist():
                            if item.filename == target_path:
                                continue
                            else:
                                zout.writestr(item, zin.read(item.filename))
                        zout.writestr(target_path, secure_data)
                self.raw = new_buf.getvalue()
                self.refresh_view()
                self.status_label.config(text=f'[ SYSTEM ] SECURE DOCUMENT INITIALIZED: {name}')
            except Exception as e:
                self.show_themed_error('AXT_WRITE_FAILURE', f'Failed to create .axt: {e}')
    def import_raw_data(self, name, data):
        target = os.path.join(self.current_dir, name).replace('\\', '/')
        in_mem = io.BytesIO()
        if not self.raw:
            self.raw = b'PK\x05\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        with zipfile.ZipFile(io.BytesIO(self.raw), 'r') as old_z:
            with zipfile.ZipFile(in_mem, 'w', zipfile.ZIP_DEFLATED) as new_z:
                for item in old_z.infolist():
                    if item.filename != target:
                        new_z.writestr(item, old_z.read(item.filename))
                if data or target.endswith('/'):
                    new_z.writestr(target, data)
        self.raw = in_mem.getvalue()
        self.refresh_view()
    def toggle_all(self):
        items = self.tree.get_children()
        if len(self.tree.selection()) == len(items):
            self.tree.selection_remove(items)
        else:
            self.tree.selection_set(items)
    def extract_selected(self):
        sel = self.tree.selection()
        if not sel or not self.raw:
            return None
        else:
            dest = os.path.join(os.getcwd(), 'Vault_Exports')
            if not os.path.exists(dest):
                os.makedirs(dest)
            with zipfile.ZipFile(io.BytesIO(self.raw), 'r') as z:
                for i in sel:
                    name = self.tree.item(i)['text']
                    path = os.path.join(self.current_dir, name).replace('\\', '/')
                    for m in z.namelist():
                        if m.startswith(path):
                            z.extract(m, dest)
            os.startfile(dest)
    def delete_selected(self):
        # irreducible cflow, using cdg fallback
        # ***<module>.VaultBrowser.delete_selected: Failure: Compilation Error
        sel = self.tree.selection()
        if not sel or not self.raw:
            return None
        else:
            dialog = ThemedConfirm(self.root, 'Delete', 'PERMANENTLY ERASE SELECTED DATA?')
            self.root.wait_window(dialog)
            if not dialog.result:
                return None
            else:
                with zipfile.ZipFile(io.BytesIO(self.raw), 'r') as old_z:
                    pass
        in_mem = io.BytesIO()
        with zipfile.ZipFile(in_mem, 'w', zipfile.ZIP_DEFLATED) as new_z:
            targets = [os.path.join(self.current_dir, self.tree.item(i)['text']).replace('\\', '/') for i in sel]
            for item in old_z.infolist():
                    if any((item.filename.startswith(t) for t in targets)) and (not item.filename.startswith(t)) and (not item.<code object ThemedProperties at 0x760246b9d9b0, file "player.py", line 112>(<mask_8>)):
                                            new_z.writestr(item, old_z.read(item.filename))
                    self.raw = in_mem.getvalue()
                    self.refresh_view()
    def save_vault_as(self):
        # ***<module>.VaultBrowser.save_vault_as: Failure: Compilation Error
        p = filedialog.asksaveasfilename(defaultextension='.dfil', filetypes=[('Vault', '*.dfil')])
        if p:
            with open(p, 'wb') as f, f.write(base64.b64encode(self.raw)), base64.b64encode(self.<code object VaultResizer at 0x760246b9f550, file "player.py", line 175>):
                pass
class ThemedDialog(tk.Toplevel):
    def __init__(self, parent, title, prompt):
        super().__init__(parent)
        self.result = None
        self.overrideredirect(True)
        self.configure(bg='#0a0a0a', highlightbackground='#00FF41', highlightthickness=1)
        w, h = (300, 150)
        sx = parent.winfo_x() + parent.winfo_width() // 2 - w // 2
        sy = parent.winfo_y() + parent.winfo_height() // 2 - h // 2
        self.geometry(f'{w}x{h}+{sx}+{sy}')
        header = tk.Frame(self, bg='#00FF41')
        header.pack(fill='x')
        tk.Label(header, text=title.upper(), bg='#00FF41', fg='black', font=('Consolas', 9, 'bold')).pack(side='left', padx=5)
        tk.Label(self, text=prompt, bg='#0a0a0a', fg='#00FF41', font=('Consolas', 10), pady=10).pack()
        self.entry = tk.Entry(self, bg='#000000', fg='#00FF41', insertbackground='#00FF41', relief='flat', font=('Consolas', 10), highlightthickness=1, highlightbackground='#333')
        self.entry.pack(padx=20, fill='x')
        self.entry.focus_set()
        btn_frame = tk.Frame(self, bg='#0a0a0a', pady=15)
        btn_frame.pack()
        btn_params = {'bg': '#111111', 'fg': '#00FF41', 'activebackground': '#00FF41', 'activeforeground': 'black', 'relief': 'flat', 'width': 10, 'font': ('Consolas', 9)}
        tk.Button(btn_frame, text='CONFIRM', **btn_params, command=self.on_ok).pack(side='left', padx=5)
        tk.Button(btn_frame, text='CANCEL', **btn_params, command=self.destroy).pack(side='left', padx=5)
        self.bind('<Return>', lambda e: self.on_ok())
        self.bind('<Escape>', lambda e: self.destroy())
        self.grab_set()
    def on_ok(self):
        self.result = self.entry.get()
        self.destroy()
class ThemedConfirm(tk.Toplevel):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.result = False
        self.overrideredirect(True)
        self.configure(bg='#0a0a0a', highlightbackground='#00FF41', highlightthickness=1)
        w, h = (350, 150)
        sx = parent.winfo_x() + parent.winfo_width() // 2 - w // 2
        sy = parent.winfo_y() + parent.winfo_height() // 2 - h // 2
        self.geometry(f'{w}x{h}+{sx}+{sy}')
        header = tk.Frame(self, bg='#00FF41')
        header.pack(fill='x')
        tk.Label(header, text=f' SECURITY PROMPT // {title.upper()}', bg='#00FF41', fg='black', font=('Consolas', 9, 'bold')).pack(side='left', padx=5)
        tk.Label(self, text=message, bg='#0a0a0a', fg='#00FF41', font=('Consolas', 10), pady=20, wraplength=310).pack()
        btn_frame = tk.Frame(self, bg='#0a0a0a', pady=10)
        btn_frame.pack()
        btn_params = {'bg': '#111111', 'fg': '#00FF41', 'activebackground': '#00FF41', 'activeforeground': 'black', 'relief': 'flat', 'width': 12, 'font': ('Consolas', 9)}
        tk.Button(btn_frame, text='[ YES ]', **btn_params, command=self.on_yes).pack(side='left', padx=10)
        tk.Button(btn_frame, text='[ NO ]', **btn_params, command=self.destroy).pack(side='left', padx=10)
        self.grab_set()
    def on_yes(self):
        self.result = True
        self.destroy()
    def reveal_row(self, index):
        if index < len(self.stats_list):
            key, val = self.stats_list[index]
            row = tk.Frame(self.content, bg='#000000')
            row.pack(fill='x', pady=2)
            tk.Label(row, text=f'> {key.ljust(14)}:', bg='#000000', fg='#008800', font=('Consolas', 10)).pack(side='left')
            tk.Label(row, text=str(val), bg='#000000', fg='#00FF41', font=('Consolas', 10, 'bold')).pack(side='left', padx=10)
            self.after(50, lambda: self.reveal_row(index + 1))
        else:
            tk.Label(self, text='--- SCAN COMPLETE // AUTH_KEY_VALID ---', bg='#000000', fg='#004400', font=('Consolas', 8)).pack(pady=10)
class ThemedNotify(tk.Toplevel):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.overrideredirect(True)
        self.configure(bg='#0a0a0a', highlightbackground='#00FF41', highlightthickness=1)
        w, h = (350, 120)
        sx = parent.winfo_x() + parent.winfo_width() // 2 - w // 2
        sy = parent.winfo_y() + parent.winfo_height() // 2 - h // 2
        self.geometry(f'{w}x{h}+{sx}+{sy}')
        header = tk.Frame(self, bg='#00FF41')
        header.pack(fill='x')
        tk.Label(header, text=f' SYSTEM MESSAGE // {title.upper()}', bg='#00FF41', fg='black', font=('Consolas', 9, 'bold')).pack(side='left', padx=5)
        tk.Label(self, text=message, bg='#0a0a0a', fg='#00FF41', font=('Consolas', 10), pady=15, wraplength=310).pack()
        btn = tk.Button(self, text='[ ACKNOWLEDGE ]', bg='#111111', fg='#00FF41', activebackground='#00FF41', activeforeground='black', relief='flat', font=('Consolas', 9), command=self.destroy)
        btn.pack(pady=5)
        self.bind('<Return>', lambda e: self.destroy())
        self.bind('<Escape>', lambda e: self.destroy())
        self.grab_set()
def handle_media(name, ext, data, parent_ui=None):
    """Decodes Vault files ONLY. Keeps standard files raw."""
    vault_exts = ['.axt', '.video', '.pic', '.audio', '.web', '.rxe', '.wrun', '.hex', '.glitch']
    if ext in vault_exts:
        data = ensure_binary(data)
    if ext == '.axt':
        threading.Thread(target=open_text_player, args=(name, data, parent_ui), daemon=True).start()
    else:
        if ext in ('.video', '.mp4', '.mkv', '.avi', '.wmv'):
            threading.Thread(target=play_video, args=(name, data, parent_ui), daemon=True).start()
        else:
            if ext in ('.pic', '.png', '.jpg', '.jpeg', '.gif'):
                threading.Thread(target=show_pic, args=(name, data, parent_ui), daemon=True).start()
            else:
                if ext in ('.audio', '.mp3', '.wav'):
                    threading.Thread(target=play_audio, args=(name, data, parent_ui), daemon=True).start()
                else:
                    if ext == '.web':
                        threading.Thread(target=open_web_player, args=(name, data, parent_ui), daemon=True).start()
                    else:
                        if ext == '.glitch':
                            open_glitch_vault(name, data, parent_ui)
                        else:
                            if ext in ('.cfg', '.txt'):
                                threading.Thread(target=open_text_player, args=(name, data, parent_ui), daemon=True).start()
                            else:
                                if ext in ('.exe', '.bat', '.wrun', '.rxe'):
                                    if parent_ui and parent_ui.raw:
                                        try:
                                            temp_dir = os.path.join(tempfile.gettempdir(), f'vrun_{uuid.uuid4().hex[:6]}')
                                            os.makedirs(temp_dir, exist_ok=True)
                                            TEMP_TRACKER.append(temp_dir)
                                            exec_path = os.path.join(temp_dir, name)
                                            with open(exec_path, 'wb') as f:
                                                f.write(data)
                                            if ext in ('.bat', '.wrun'):
                                                subprocess.Popen(f'start /wait cmd /c \"{exec_path}\"', shell=True, cwd=temp_dir)
                                            else:
                                                subprocess.Popen([exec_path], creationflags=subprocess.CREATE_NEW_CONSOLE, cwd=temp_dir)
                                        except Exception as e:
                                            self.show_themed_error('EXEC_CRITICAL', f'System execution failure: {e}')
                                    else:
                                        run_app(data, ext in ('.wrun', '.bat'))
def open_text_player(name, data, parent_ui):
    # ***<module>.open_text_player: Failure: Different bytecode
    if parent_ui:
        parent_ui.read_text(name, data)
        return None
    else:
        root, root = (tk.Tk(), root.title(name))
        root.geometry('600x400')
        txt = tk.Text(root, bg='black', fg='#00FF41', font=('Consolas', 11))
        txt.insert('1.0', data.decode('utf-8', errors='ignore'))
        root.mainloop()
def open_glitch_vault(name, data, parent_ui):
    top = tk.Toplevel(parent_ui.root)
    top.overrideredirect(True)
    top.geometry('600x400')
    top.configure(bg='#000000')
    def start_move(event):
        top.x, top.y = (event.x, event.y)
    def do_move(event):
        top.geometry(f'+{top.winfo_x() + (event.x - top.x)}+{top.winfo_y() + (event.y - top.y)}')
    header = tk.Frame(top, bg='#0a0a0a', height=30)
    header.pack(side='top', fill='x')
    header.pack_propagate(False)
    header.bind('<ButtonPress-1>', start_move)
    header.bind('<B1-Motion>', do_move)
    tk.Label(header, text=f' ⚠️ UNSTABLE_DATA // {name}', bg='#0a0a0a', fg='#ff4141', font=('Consolas', 9, 'bold')).pack(side='left', padx=10)
    exit_btn = tk.Label(header, text=' ✕ ', bg='#0a0a0a', fg='#ff4141', font=('Consolas', 14, 'bold'), cursor='hand2')
    exit_btn.pack(side='right')
    exit_btn.bind('<Button-1>', lambda e: top.destroy())
    txt = tk.Text(top, bg='#000000', fg='#ff4141', font=('Consolas', 11), borderwidth=0, highlightthickness=0)
    txt.pack(expand=True, fill='both', padx=20, pady=10)
    try:
        content = data.decode('utf-8', errors='ignore')
        txt.insert('1.0', content)
    except:
        txt.insert('1.0', '[DATA CORRUPTED]')
    txt.config(state='disabled')
    timer_val = 20
    timer_lbl = tk.Label(top, text=f'ERASURE IN: {timer_val}s', bg='#000000', fg='#ff4141', font=('Consolas', 14, 'bold'))
    timer_lbl.pack(side='bottom', pady=15)
    def glitch_effect():
        if top.winfo_exists():
            dx = random.randint((-4), 4)
            dy = random.randint((-4), 4)
            top.geometry(f'+{top.winfo_x() + dx}+{top.winfo_y() + dy}')
            glitch_color = random.choice(['#ff4141', '#ffffff', '#550000', '#ff0000'])
            txt.config(fg=glitch_color)
            timer_lbl.config(fg=glitch_color)
            top.after(random.randint(50, 150), glitch_effect)
    def countdown():
        nonlocal timer_val
        if not top.winfo_exists():
            return None
        else:
            if timer_val > 0:
                timer_val -= 1
                timer_lbl.config(text=f'ERASURE IN: {timer_val}s')
                top.after(1000, countdown)
                return None
            else:
                if parent_ui:
                    parent_ui.delete_selected_by_name(name)
                top.destroy()
                show_themed_error(self.root, 'SYSTEM CRITICAL', f'FILE \'{name}\' HAS BEEN PERMANENTLY ERASED.')
    glitch_effect()
    countdown()
seek_frame = (-1)
volume_level = 1.0
is_muted = False
is_dragging = False
def on_mouse_click(event, x, y, flags, param):
    global volume_level
    global is_muted
    global is_dragging
    global seek_frame
    width, total_f, height = param
    vol_start_x = width - 135
    vol_end_x = width - 35
    if event == cv2.EVENT_LBUTTONDOWN:
        if height - 40 < y < height - 30:
            seek_frame = int(x / width * total_f)
        else:
            if vol_start_x <= x <= vol_end_x and height - 26 <= y <= height - 20:
                    is_dragging = True
    else:
        if event == cv2.EVENT_MOUSEMOVE:
            if is_dragging:
                clicked_offset = x - vol_start_x
                volume_level = max(0.0, min(1.0, clicked_offset / 100))
                is_muted = False
                pygame.mixer.music.set_volume(volume_level)
        else:
            if event == cv2.EVENT_LBUTTONUP:
                is_dragging = False
volume_level = 0.5
is_muted = False
def play_audio(name, data, parent_ui=None):
    """Themed Audio Player - Optimized for Python 3.14"""
    temp_a = get_temp_path('.mp3')
    try:
        with open(temp_a, 'wb') as f:
            f.write(data)
        if not pygame.mixer.get_init():
            pygame.mixer.pre_init(44100, (-16), 2, 512)
            pygame.mixer.init()
        else:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        pygame.mixer.music.load(temp_a)
        pygame.mixer.music.set_volume(0.0 if is_muted else volume_level)
        pygame.mixer.music.play()
        audio_info = pygame.mixer.Sound(temp_a)
        duration = audio_info.get_length()
        target_root = parent_ui.root if parent_ui else tk._default_root
        target_root.after(0, lambda: create_audio_ui(name, duration, temp_a, target_root))
    except Exception as e:
        print(f'AUDIO_ENGINE_FAILURE: {e}')
def create_audio_ui(name, duration, temp_path, root_ptr):
    # ***<module>.create_audio_ui: Failure: Different bytecode
    top = tk.Toplevel(root_ptr)
    top.overrideredirect(True)
    top.geometry('450x180')
    top.configure(bg='#000000', highlightbackground='#00FF41', highlightthickness=1)
    top.attributes('-topmost', True)
    top.is_paused = False
    top.manual_offset = 0.0
    top.is_scrubbing = False
    top._drag_x, top._drag_y = (0, 0)
    def start_move(event):
        top._drag_x, top._drag_y = (event.x, event.y)
    def do_move(event):
        x = top.winfo_x() + (event.x - top._drag_x)
        y = top.winfo_y() + (event.y - top._drag_y)
        top.geometry(f'+{x}+{y}')
    header = tk.Frame(top, bg='#0a0a0a', height=30)
    header.pack(side='top', fill='x')
    header.bind('<ButtonPress-1>', start_move)
    header.bind('<B1-Motion>', do_move)
    title_lbl = tk.Label(header, text=f' 🔊 VAULT_AUDIO // {name[:25]}', bg='#0a0a0a', fg='#00FF41', font=('Consolas', 9, 'bold'))
    title_lbl.pack(side='left', padx=10)
    title_lbl.bind('<ButtonPress-1>', start_move)
    title_lbl.bind('<B1-Motion>', do_move)
    def shutdown():
        # irreducible cflow, using cdg fallback
        # ***<module>.create_audio_ui.shutdown: Failure: Compilation Error
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        top.destroy()
        if os.path.exists(temp_path):
            os.remove(temp_path)
                    return None
    exit_btn = tk.Label(header, text=' ✕ ', bg='#0a0a0a', fg='#ff4141', font=('Consolas', 12, 'bold'), cursor='hand2')
    exit_btn.pack(side='right', padx=5)
    exit_btn.bind('<Button-1>', lambda e: shutdown())
    canvas = tk.Canvas(top, width=450, height=100, bg='#000000', highlightthickness=0)
    canvas.pack(fill='x', expand=False)
    def toggle_pause(event=None):
        if not pygame.mixer.get_init():
            return None
        else:
            if top.is_paused:
                pygame.mixer.music.unpause()
                top.is_paused = False
                play_btn.config(text=' ⏸ PAUSE ', fg='#00FF41')
            else:
                pygame.mixer.music.pause()
                top.is_paused = True
                play_btn.config(text=' ▶ PLAY  ', fg='#FFFFFF')
    play_btn = tk.Label(top, text=' ⏸ PAUSE ', bg='#000000', fg='#00FF41', font=('Consolas', 10, 'bold'), cursor='hand2', highlightbackground='#00FF41', highlightthickness=1)
    play_btn.pack(pady=5)
    play_btn.bind('<Button-1>', toggle_pause)
    bar_x1, bar_y, bar_x2 = (40, 55, 410)
    def perform_seek(event):
        if bar_x1 <= event.x <= bar_x2:
            ratio = (event.x - bar_x1) / (bar_x2 - bar_x1)
            target_time = ratio * duration
            top.manual_offset = target_time
            if pygame.mixer.get_init():
                pygame.mixer.music.play(start=target_time)
                if top.is_paused:
                    pygame.mixer.music.pause()
    canvas.bind('<Button-1>', lambda e: [setattr(top, 'is_scrubbing', True), perform_seek(e)])
    canvas.bind('<B1-Motion>', lambda e: perform_seek(e) if top.is_scrubbing else None)
    canvas.bind('<ButtonRelease-1>', lambda e: setattr(top, 'is_scrubbing', False))
    def update_loop():
        if not top.winfo_exists():
            return None
        if not pygame.mixer.get_init():
            shutdown()
            return None
        else:
            if not pygame.mixer.music.get_busy() and (not top.is_scrubbing) and (not top.is_paused):
                current_pos = pygame.mixer.music.get_pos() / 1000.0 + top.manual_offset
                if current_pos >= duration - 0.2:
                    shutdown()
                    return None
            canvas.delete('all')
            current_time = pygame.mixer.music.get_pos() / 1000.0 + top.manual_offset
            canvas.create_rectangle(bar_x1, bar_y - 2, bar_x2, bar_y + 2, fill='#111111', outline='')
            prog_ratio = min(1.0, current_time / duration) if duration > 0 else 0
            px = bar_x1 + prog_ratio * (bar_x2 - bar_x1)
            canvas.create_rectangle(bar_x1, bar_y - 2, px, bar_y + 2, fill='#00FF41', outline='')
            canvas.create_oval(px - 5, bar_y - 5, px + 5, bar_y + 5, fill='#FFFFFF', outline='#00FF41')
            for i in range(25):
                is_active = pygame.mixer.music.get_busy() and (not top.is_paused)
                h = random.randint(2, 25) if is_active else 2
                canvas.create_rectangle(45 + i * 15, 95 - h, 53 + i * 15, 95, fill='#004411', outline='')
            time_str = f'{int(current_time // 60)}:{int(current_time % 60):02d} / {int(duration // 60)}:{int(duration % 60):02d}'
            canvas.create_text(40, 30, text=time_str, fill='#00FF41', font=('Consolas', 10), anchor='w')
            top.after(50, update_loop)
    update_loop()
def play_video(name, data, parent_ui):
    """Themed Video Engine - Safe Audio Extraction + Main Thread UI Guard"""
    is_wmv = data[:10].startswith(b'0&\xb2u')
    temp_v = get_temp_path('.wmv' if is_wmv else '.mp4')
    temp_a = get_temp_path('.mp3')
    try:
        with open(temp_v, 'wb') as f:
            f.write(data)
        clip = VideoFileClip(temp_v)
        duration = clip.duration
        fps = clip.fps if clip.fps and clip.fps > 0 else 30
        mixer_active = False
        if clip.audio is not None:
            try:
                clip.audio.write_audiofile(temp_a, logger=None, bitrate='128k')
                if not pygame.mixer.get_init():
                    pygame.mixer.init()
                pygame.mixer.music.load(temp_a)
                pygame.mixer.music.set_volume(0.0 if is_muted else volume_level)
                pygame.mixer.music.play()
                mixer_active = True
            except:
                pass
        clip.close()
        target_root = parent_ui.root if parent_ui and hasattr(parent_ui, 'root') else tk._default_root
        target_root.after(0, lambda: create_video_ui(name, duration, fps, temp_v, temp_a, mixer_active, target_root))
    except Exception as e:
        print(f'VIDEO_ENGINE_FAILURE: {e}')
def create_video_ui(name, duration, fps, v_path, a_path, mixer_active, root_ptr):
    """Themed Video UI - Fixed Seeker and Draggable Header"""
    from PIL import Image, ImageTk
    import cv2
    top = tk.Toplevel(root_ptr)
    top.geometry('900x650')
    top.configure(bg='#000000')
    top.attributes('-topmost', True)
    top.overrideredirect(True)
    top.is_paused = False
    top.current_frame = 0
    top.alive = True
    top._drag_data = {'x': 0, 'y': 0}
    def start_move(event):
        top._drag_data['x'] = event.x
        top._drag_data['y'] = event.y
    def do_move(event):
        x = top.winfo_x() + (event.x - top._drag_data['x'])
        y = top.winfo_y() + (event.y - top._drag_data['y'])
        top.geometry(f'+{x}+{y}')
    header = tk.Frame(top, bg='#0a0a0a', height=35)
    header.pack(side='top', fill='x')
    header.bind('<ButtonPress-1>', start_move)
    header.bind('<B1-Motion>', do_move)
    title_lbl = tk.Label(header, text=f' 🎬 {name}', bg='#0a0a0a', fg='#00FF41', font=('Consolas', 10))
    title_lbl.pack(side='left', padx=10)
    title_lbl.bind('<ButtonPress-1>', start_move)
    title_lbl.bind('<B1-Motion>', do_move)
    close_btn = tk.Label(header, text='✕', bg='#0a0a0a', fg='#ff4141', font=('Consolas', 12, 'bold'), cursor='hand2')
    close_btn.pack(side='right', padx=10)
    def on_close(e=None):
        top.alive = False
        if mixer_active:
            pygame.mixer.music.stop()
        top.destroy()
    close_btn.bind('<Button-1>', on_close)
    controls = tk.Frame(top, bg='#000000', height=70)
    controls.pack(side='bottom', fill='x')
    progress_canvas = tk.Canvas(controls, bg='#333', height=6, highlightthickness=0, cursor='hand2')
    progress_canvas.pack(fill='x', side='top', padx=10, pady=5)
    seeker_rect = progress_canvas.create_rectangle(0, 0, 0, 6, fill='#FF0000', outline='')
    btn_frame = tk.Frame(controls, bg='#000000')
    btn_frame.pack(fill='x', side='bottom', padx=10, pady=5)
    cap = cv2.VideoCapture(v_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
    def seek_video(event):
        width = progress_canvas.winfo_width()
        if width <= 0:
            return None
        else:
            target_pct = max(0, min(event.x / width, 1.0))
            target_frame = int(total_frames * target_pct)
            top.current_frame = target_frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
            if mixer_active:
                try:
                    seek_sec = target_frame / fps
                    pygame.mixer.music.play(start=seek_sec)
                    if top.is_paused:
                        pygame.mixer.music.pause()
                except:
                    pass
            progress_canvas.coords(seeker_rect, 0, 0, event.x, 6)
    progress_canvas.bind('<Button-1>', seek_video)
    def toggle_play(e=None):
        top.is_paused = not top.is_paused
        play_btn.config(text='▶' if top.is_paused else '⏸', fg='#00FF41' if top.is_paused else '#ffffff')
        if mixer_active:
            if top.is_paused:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()
    play_btn = tk.Label(btn_frame, text='⏸', bg='#000000', fg='#ffffff', font=('Consolas', 14, 'bold'), cursor='hand2')
    play_btn.pack(side='left')
    play_btn.bind('<Button-1>', toggle_play)
    def toggle_fs(e=None):
        is_fs = top.attributes('-fullscreen')
        top.overrideredirect(False)
        top.attributes('-fullscreen', not is_fs)
        top.overrideredirect(True)
        if not is_fs:
            fs_btn.config(text='❐', font=('Consolas', 14, 'bold'))
        else:
            fs_btn.config(text='⛶', font=('Consolas', 18, 'bold'))
        top.focus_force()
    fs_btn = tk.Label(btn_frame, text='⛶', bg='#000000', fg='#00FF41', font=('Consolas', 18, 'bold'), cursor='hand2', padx=10, pady=0)
    fs_btn.pack(side='left', padx=5)
    fs_btn.bind('<Button-1>', toggle_fs)
    time_label = tk.Label(btn_frame, text='00:00 / 00:00', bg='#000000', fg='#aaaaaa', font=('Consolas', 10))
    time_label.pack(side='left', padx=15)
    video_canvas = tk.Label(top, bg='black')
    video_canvas.pack(fill='both', expand=True)
    def format_time(seconds):
        mins, secs = divmod(int(max(seconds, 0)), 60)
        return f'{mins:02d}:{secs:02d}'
    def update_frame():
        if not top.alive:
            cap.release()
            return None
        else:
            if not top.is_paused:
                ret, frame = cap.read()
                if ret:
                    vw = max(top.winfo_width(), 10)
                    vh = max(top.winfo_height() - 110, 10)
                    frame = cv2.resize(frame, (vw, vh))
                    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    imgtk = ImageTk.PhotoImage(image=Image.fromarray(img))
                    video_canvas.imgtk = imgtk
                    video_canvas.configure(image=imgtk)
                    progress_pct = top.current_frame / total_frames
                    bar_width = max(progress_canvas.winfo_width(), 1)
                    progress_canvas.coords(seeker_rect, 0, 0, int(bar_width * progress_pct), 6)
                    curr_sec = top.current_frame / fps
                    time_label.config(text=f'{format_time(curr_sec)} / {format_time(duration)}')
                    top.current_frame += 1
                else:
                    on_close()
                    return None
            top.after(int(1000 / fps), update_frame)
    VaultResizer(top)
    update_frame()
def show_pic(name, raw_data, parent_ui):
    """Background loader for images"""
    from PIL import Image
    try:
        img_io = io.BytesIO(raw_data)
        pil_img = Image.open(img_io)
        pil_img.load()
        target_root = parent_ui.root if parent_ui else tk._default_root
        target_root.after(0, lambda: create_pic_ui(name, pil_img, target_root))
    except Exception as e:
        print(f'IMAGE_LOAD_ERROR for {name}: {e}')
def create_pic_ui(name, original_pil_img, root_ptr):
    """Image window with Dragging and Manual Resizing"""
    top = tk.Toplevel(root_ptr)
    top.overrideredirect(True)
    top.attributes('-topmost', True)
    top.original = original_pil_img
    w, h = top.original.size
    if w > 1100 or h > 800:
        top.original.thumbnail((1100, 800), Image.Resampling.LANCZOS)
        w, h = top.original.size
    win_w = max(w, 200)
    top.geometry(f'{win_w}x{h + 30}')
    def start_resize(e):
        top.start_w = top.winfo_width()
        top.start_h = top.winfo_height()
        top.start_x = e.x_root
        top.start_y = e.y_root
    def do_resize(e):
        new_w = max(200, top.start_w + (e.x_root - top.start_x))
        new_h = max(100, top.start_h + (e.y_root - top.start_y))
        top.geometry(f'{new_w}x{new_h}')
        img_h = max(1, new_h - 30)
        resized_pil = top.original.copy()
        resized_pil.thumbnail((new_w, img_h), Image.Resampling.NEAREST)
        new_tk = ImageTk.PhotoImage(resized_pil)
        img_lbl.config(image=new_tk)
        img_lbl.image = new_tk
    def start_move(e):
        top.drag_x, top.drag_y = (e.x, e.y)
    def do_move(e):
        top.geometry(f'+{top.winfo_x() + (e.x - top.drag_x)}+{top.winfo_y() + (e.y - top.drag_y)}')
    header = tk.Frame(top, bg='#0a0a0a', height=30)
    header.pack(side='top', fill='x')
    header.bind('<Button-1>', start_move)
    header.bind('<B1-Motion>', do_move)
    tk.Label(header, text=f' 🖼️ {name}', bg='#0a0a0a', fg='#00FF41', font=('Consolas', 9)).pack(side='left', padx=10)
    exit_btn = tk.Label(header, text=' ✕ ', bg='#0a0a0a', fg='#ff4141', font=('Consolas', 14, 'bold'), cursor='hand2')
    exit_btn.pack(side='right', padx=5)
    exit_btn.bind('<Button-1>', lambda e: top.destroy())
    img_lbl = tk.Label(top, bg='#000000', bd=0)
    img_lbl.pack(fill='both', expand=True)
    initial_tk = ImageTk.PhotoImage(top.original)
    img_lbl.config(image=initial_tk)
    img_lbl.image = initial_tk
    grip = tk.Label(top, text='◢', bg='#000', fg='#00FF41', font=('Consolas', 10), cursor='size_nw_se')
    grip.place(relx=1.0, rely=1.0, anchor='se')
    grip.bind('<Button-1>', start_resize)
    grip.bind('<B1-Motion>', do_resize)
def run_app(raw, is_bat):
    ext = '.bat' if is_bat else '.exe'
    tp = get_temp_path(ext)
    try:
        with open(tp, 'wb') as f:
            f.write(raw)
            f.flush()
            os.fsync(f.fileno())
        if is_bat:
            subprocess.Popen(f'start /wait cmd /c \"{tp}\"', shell=True)
        else:
            subprocess.Popen([tp], creationflags=subprocess.CREATE_NEW_CONSOLE)
    except Exception as e:
        self.show_themed_error('LAUNCH_FAILURE', f'System execution failed: {e}')
def open_web_player(name, data, *args):
    top = tk.Toplevel()
    top.title(f'WEB ENGINE: {name}')
    top.geometry('1000x700')
    top.configure(bg='#0a0a0a')
    top.overrideredirect(False)
    header = tk.Frame(top, bg='#0a0a0a', height=35, highlightthickness=1, highlightbackground='#333')
    header.pack(fill='x', side='top')
    header.pack_propagate(False)
    def start_move(event):
        top.x = event.x
        top.y = event.y
    def do_move(event):
        deltax = event.x - top.x
        deltay = event.y - top.y
        x = top.winfo_x() + deltax
        y = top.winfo_y() + deltay
        top.geometry(f'+{x}+{y}')
    header.bind('<Button-1>', start_move)
    header.bind('<B1-Motion>', do_move)
    tk.Label(header, text=f' 🌐 WEB ENGINE: {name}', bg='#0a0a0a', fg='#00FF41', font=('Consolas', 10, 'bold')).pack(side='left', padx=10)
    exit_btn = tk.Label(header, text='✕', bg='#0a0a0a', fg='#ff4141', font=('Consolas', 12, 'bold'), cursor='hand2', padx=10)
    exit_btn.pack(side='right')
    exit_btn.bind('<Button-1>', lambda e: top.destroy())
    exit_btn.bind('<Enter>', lambda e: exit_btn.config(bg='#330000'))
    exit_btn.bind('<Leave>', lambda e: exit_btn.config(bg='#0a0a0a'))
    browser_frame = HtmlFrame(top, messages_enabled=False)
    browser_frame.pack(fill='both', expand=True)
    try:
        content = data.decode('utf-8', errors='ignore')
        if content.strip().startswith(('http://', 'https://')):
            browser_frame.load_website(content)
        else:
            browser_frame.load_html(content)
    except Exception as e:
        browser_frame.load_html(f'<body style=\'background:#000;color:red;\'>Error loading content: {e}</body>')
def start_player(path, existing_app=None):
    # ***<module>.start_player: Failure: Different bytecode
    ext = os.path.splitext(path)[1].lower()
    raw = smart_decode(path)
    if ext == '.dfil':
        if existing_app:
            existing_app.raw = raw
            existing_app.current_dir = ''
            existing_app.root.after(0, existing_app.refresh_view)
        else:
            app = VaultBrowser(raw_data=raw)
    else:
        handle_media(os.path.basename(path), ext, raw, existing_app)
if __name__ == '__main__':
    if len(sys.argv) > 1:
        start_player(sys.argv[1])
    else:
        app = VaultBrowser()
        app.root.mainloop()f __name__ == '__main__':
    if len(sys.argv) > 1:
        start_player(sys.argv[1])
    else:
        app = VaultBrowser()
        app.root.mainloop()