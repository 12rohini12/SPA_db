import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import mysql.connector
import hashlib
import csv
import random

selected_role = None
current_user_id = None
current_session_username = None  # Tracks the uniquely logged-in username

# ============================================================
#  COLOUR PALETTE — Sunny Academia (Warm, Minimal, Cute)
# ============================================================
BG_MAIN       = "#fafaf7"   # Warm off-white
BG_CARD       = "#ffffff"   # Clean card white
BG_SIDEBAR    = "#f5f0e8"   # Cozy cream sidebar
YELLOW        = "#f5c518"   # Sunny gold-yellow
YELLOW_LIGHT  = "#fff8d6"   # Pale butter-yellow
GOLD          = "#c9960c"   # Deep academic gold
GREEN_LIGHT   = "#e2fbe8"   # Soft mint candy green
GREEN         = "#3dbf5a"   # Apple green
PURPLE_LIGHT  = "#ede7fd"   # Pale lilac-lavender
PURPLE        = "#8b6be8"   # Sweet lavender purple
SILVER        = "#e8e8ec"   # Ultra light aesthetic grey
SILVER_DARK   = "#9ca3af"   # Medium muted text slate
TEXT_DARK     = "#1a1a1a"   # Soft charcoal black
TEXT_MED      = "#4a4a5a"   # Smooth slate for labels
TEXT_MUTED    = "#8888a0"   # Pastel grey hints
WHITE         = "#ffffff"

BTN_YELLOW = {"bg": YELLOW,       "fg": TEXT_DARK,  "hover": GOLD}
BTN_GREEN  = {"bg": GREEN,        "fg": WHITE,      "hover": "#2da84a"}
BTN_PURPLE = {"bg": PURPLE,       "fg": WHITE,      "hover": "#7a5bd4"}
BTN_SILVER = {"bg": SILVER,       "fg": TEXT_DARK,  "hover": "#d4d4dc"}
BTN_DANGER = {"bg": "#ff6b6b",    "fg": WHITE,      "hover": "#e05555"}

F_HERO   = ("Segoe UI", 24, "bold")
F_TITLE  = ("Segoe UI", 17, "bold")
F_SUBTTL = ("Segoe UI", 12, "bold")
F_BODY   = ("Segoe UI", 11)
F_SMALL  = ("Segoe UI", 9)
F_BTN    = ("Segoe UI", 10, "bold")

SUBJECTS = ["Maths", "Science", "English"]

# ============================================================
#  DATABASE SETUP
# ============================================================
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@Rohini12@",
    database="student_performance"
)
cursor = db.cursor()

def hash_password(p):
    """Securely hashes student/user access credentials."""
    return hashlib.sha256(p.encode()).hexdigest()

def log_action(action_type, details):
    """Inserts a real-time system log track event into your audit table layout."""
    global current_user_id
    try:
        cursor.execute(
            "INSERT INTO audit_logs (user_id, action, details) VALUES (%s, %s, %s)",
            (current_user_id, action_type, details)
        )
        db.commit()
    except Exception as e:
        print(f"Audit log background trace warning: {e}")

# ============================================================
#  UI STYLING HELPERS
# ============================================================
def _hover(btn, n, h):
    btn.bind("<Enter>", lambda e: btn.config(bg=h))
    btn.bind("<Leave>", lambda e: btn.config(bg=n))

def styled_button(parent, text, palette=None, command=None, width=18, pady_inner=9):
    if palette is None: palette = BTN_YELLOW
    btn = tk.Button(parent, text=text, font=F_BTN,
        bg=palette["bg"], fg=palette["fg"],
        activebackground=palette["hover"], activeforeground=palette["fg"],
        relief="flat", bd=0, cursor="hand2",
        width=width, pady=pady_inner, command=command)
    _hover(btn, palette["bg"], palette["hover"])
    return btn

def field_label(parent, text, bg=BG_CARD):
    return tk.Label(parent, text=text, font=("Segoe UI", 10), bg=bg, fg=TEXT_MED, anchor="w")

def styled_entry(parent, show=None, width=32):
    outer = tk.Frame(parent, bg=SILVER, padx=1, pady=1)
    entry = tk.Entry(outer, width=width, font=F_BODY,
        bg="#f9f9fb", fg=TEXT_DARK, insertbackground=PURPLE,
        relief="flat", bd=7, show=show)
    entry.pack()
    return outer, entry

def styled_treeview(parent, columns, col_widths=None):
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Custom.Treeview",
        background=WHITE, foreground=TEXT_DARK,
        rowheight=34, fieldbackground=WHITE,
        borderwidth=0, font=("Segoe UI", 10))
    style.configure("Custom.Treeview.Heading",
        background=YELLOW_LIGHT, foreground=TEXT_DARK,
        font=("Segoe UI", 10, "bold"), relief="flat", padding=6)
    style.map("Custom.Treeview",
        background=[("selected", PURPLE_LIGHT)],
        foreground=[("selected", TEXT_DARK)])

    container = tk.Frame(parent, bg=SILVER, padx=1, pady=1)
    scroll = tk.Scrollbar(container, orient="vertical")
    tree = ttk.Treeview(container, columns=columns, show="headings",
        style="Custom.Treeview", yscrollcommand=scroll.set, height=10)
    scroll.config(command=tree.yview)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    for i, col in enumerate(columns):
        tree.heading(col, text=col)
        w = col_widths[i] if col_widths and i < len(col_widths) else 140
        tree.column(col, width=w, anchor="center")
    return container, tree

def card_window(title_text, w=460, h=500):
    win = tk.Toplevel(root)
    win.title(title_text)
    center_window(win, w, h)
    win.configure(bg=BG_MAIN)
    tk.Frame(win, bg=YELLOW, height=5).pack(fill=tk.X)
    inner = tk.Frame(win, bg=BG_CARD, padx=32, pady=24)
    inner.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)
    tk.Label(inner, text=title_text, font=F_TITLE, bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w", pady=(0,18))
    return win, inner

def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

# ============================================================
#  CORE OPERATIONAL ACTIONS BLOCK
# ============================================================
def view_students():
    win = tk.Toplevel(root)
    win.title("Student Records")
    center_window(win, 860, 540)
    win.configure(bg=BG_MAIN)
    tk.Frame(win, bg=YELLOW, height=5).pack(fill=tk.X)
    body = tk.Frame(win, bg=BG_MAIN, padx=24, pady=20)
    body.pack(fill=tk.BOTH, expand=True)
    tk.Label(body, text="Student Records", font=F_HERO, bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w")
    tk.Label(body, text="All currently enrolled scholars with subject spreads", font=F_SMALL, bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w", pady=(2,14))
    
    cols = ("ID", "Name", "Department", "Maths", "Science", "English", "Cumulative Average")
    container, tree = styled_treeview(body, cols, [50, 180, 160, 80, 80, 80, 140])
    container.pack(fill=tk.BOTH, expand=True)
    
    cursor.execute("SELECT id, name, department, maths, science, english FROM students ORDER BY id")
    for row in cursor.fetchall(): 
        scores = row[3:]
        avg_score = round(sum(scores) / len(scores), 1) if scores else 0
        tree.insert("", tk.END, values=row + (avg_score,))

def add_student():
    win, inner = card_window("Add Student Profile", 480, 580)
    
    canvas = tk.Canvas(inner, bg=BG_CARD, bd=0, highlightthickness=0)
    scroll_y = tk.Scrollbar(inner, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=BG_CARD)
    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

    field_label(scroll_frame, "Student Name").pack(anchor="w")
    fe1, ne = styled_entry(scroll_frame); fe1.pack(fill=tk.X, pady=(4, 12))
    field_label(scroll_frame, "Department").pack(anchor="w")
    fe2, de = styled_entry(scroll_frame); fe2.pack(fill=tk.X, pady=(4, 12))
    
    subject_entries = {}
    for sub in SUBJECTS:
        field_label(scroll_frame, f"{sub} Marks").pack(anchor="w")
        fe, en = styled_entry(scroll_frame)
        fe.pack(fill=tk.X, pady=(4, 12))
        en.insert(0, "0")
        subject_entries[sub] = en
    
    def save():
        try:
            m = int(subject_entries["Maths"].get())
            s = int(subject_entries["Science"].get())
            e = int(subject_entries["English"].get())
            calc_total_avg = (m + s + e) // 3
            
            cursor.execute(
                "INSERT INTO students(name, department, marks, maths, science, english) VALUES(%s, %s, %s, %s, %s, %s)", 
                (ne.get(), de.get(), calc_total_avg, m, s, e)
            )
            db.commit()
            
            log_action("INSERT", f"Added student: {ne.get()}")
            messagebox.showinfo("Saved ✨", "New scholastic profile cleanly created!")
            win.destroy()
        except Exception as err: 
            messagebox.showerror("Validation Error", "Ensure all marks fields contain numbers.\n" + str(err))
            
    styled_button(scroll_frame, "Save Record", BTN_GREEN, save, width=22).pack(pady=15)

def update_student():
    win, inner = card_window("Update Student Data", 480, 600)
    
    canvas = tk.Canvas(inner, bg=BG_CARD, bd=0, highlightthickness=0)
    scroll_y = tk.Scrollbar(inner, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=BG_CARD)
    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

    field_label(scroll_frame, "Target Student ID").pack(anchor="w")
    fr_id, en_id = styled_entry(scroll_frame); fr_id.pack(fill=tk.X, pady=(4, 12))
    
    field_label(scroll_frame, "New Name").pack(anchor="w")
    fr_na, en_na = styled_entry(scroll_frame); fr_na.pack(fill=tk.X, pady=(4, 12))
    
    field_label(scroll_frame, "New Department").pack(anchor="w")
    fr_dp, en_dp = styled_entry(scroll_frame); fr_dp.pack(fill=tk.X, pady=(4, 12))

    sub_entries = {}
    for sub in SUBJECTS:
        field_label(scroll_frame, f"New {sub} Marks").pack(anchor="w")
        fe, en = styled_entry(scroll_frame)
        fe.pack(fill=tk.X, pady=(4, 12))
        sub_entries[sub] = en

    def load_existing():
        try:
            cursor.execute("SELECT name, department, maths, science, english FROM students WHERE id=%s", (en_id.get(),))
            res = cursor.fetchone()
            if res:
                en_na.delete(0, tk.END); en_na.insert(0, res[0])
                en_dp.delete(0, tk.END); en_dp.insert(0, res[1])
                sub_entries["Maths"].delete(0, tk.END); sub_entries["Maths"].insert(0, res[2])
                sub_entries["Science"].delete(0, tk.END); sub_entries["Science"].insert(0, res[3])
                sub_entries["English"].delete(0, tk.END); sub_entries["English"].insert(0, res[4])
            else:
                messagebox.showwarning("Missing", "No student profile identified with this ID.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    styled_button(scroll_frame, "Fetch Existing Data", BTN_SILVER, load_existing, width=22).pack(pady=(0, 15))
        
    def save():
        try:
            m = int(sub_entries["Maths"].get())
            s = int(sub_entries["Science"].get())
            e = int(sub_entries["English"].get())
            calc_total_avg = (m + s + e) // 3

            cursor.execute(
                "UPDATE students SET name=%s, department=%s, marks=%s, maths=%s, science=%s, english=%s WHERE id=%s",
                (en_na.get(), en_dp.get(), calc_total_avg, m, s, e, en_id.get())
            )
            db.commit()
            
            log_action("UPDATE", f"Updated student: {en_na.get()}")
            messagebox.showinfo("Updated 📝", "Scholastic database profile updated seamlessly.")
            win.destroy()
        except Exception as e: 
            messagebox.showerror("Error", str(e))
            
    styled_button(scroll_frame, "Commit Update", BTN_PURPLE, save, width=22).pack(pady=10)

def delete_student():
    win, inner = card_window("Remove Record", 400, 280)
    field_label(inner, "Student ID to Remove").pack(anchor="w")
    fe, ide = styled_entry(inner); fe.pack(fill=tk.X, pady=(4, 22))
    
    def confirm():
        if not ide.get(): 
            messagebox.showerror("Missing", "Please supply a valid ID selection.")
            return
        try:
            cursor.execute("SELECT name FROM students WHERE id=%s", (ide.get(),))
            target_student = cursor.fetchone()
            student_name = target_student[0] if target_student else f"ID {ide.get()}"
            
            if messagebox.askyesno("Confirm Drop ⚠️", f"Are you absolutely sure you want to delete {student_name}?"):
                cursor.execute("DELETE FROM students WHERE id=%s", (ide.get(),))
                db.commit()
                log_action("DELETE", f"Deleted student: {student_name}")
                messagebox.showinfo("Purged", "Record cleared from database files.")
                win.destroy()
        except Exception as e: 
            messagebox.showerror("Error", str(e))
                
    styled_button(inner, "Delete Permanently", BTN_DANGER, confirm, width=22).pack()

# ============================================================
#  INTELLIGENT DYNAMIC ANALYTICS HUB
# ============================================================
def analytics():
    global selected_role, current_session_username
    
    win = tk.Toplevel(root)
    win.title("Performance Analytics Terminal Engine")
    center_window(win, 960, 680)
    win.configure(bg=BG_MAIN)
    tk.Frame(win, bg=YELLOW, height=5).pack(fill=tk.X)
    
    body = tk.Frame(win, bg=BG_MAIN, padx=24, pady=20)
    body.pack(fill=tk.BOTH, expand=True)
    
    title_prefix = f"{current_session_username.upper()}'s" if selected_role == "student" else "Global Cohort"
    tk.Label(body, text=f"{title_prefix} Analytics Dashboard", font=F_HERO, bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w")
    tk.Label(body, text="Visualizing specific performance patterns for Maths, Science, and English.", font=F_SMALL, bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w", pady=(2,14))
    
    try:
        if selected_role == "student":
            cursor.execute("SELECT maths, science, english, marks FROM students WHERE name=%s", (current_session_username,))
            res = cursor.fetchone()
            if res:
                avg_subject_scores = [float(res[0]), float(res[1]), float(res[2])]
                global_average = float(res[3])
                total_students = 1
            else:
                avg_subject_scores, global_average, total_students = [0.0, 0.0, 0.0], 0.0, 0
        else:
            cursor.execute("SELECT AVG(maths), AVG(science), AVG(english), COUNT(*) FROM students")
            raw_metrics = cursor.fetchone()
            total_students = raw_metrics[3] or 0
            avg_subject_scores = [float(x or 0) for x in raw_metrics[:3]]
            global_average = sum(avg_subject_scores) / 3 if avg_subject_scores else 0

        total_for_div = total_students if total_students > 0 else 1

        strip = tk.Frame(body, bg=BG_CARD, highlightbackground=SILVER, highlightthickness=1, padx=16, pady=12)
        strip.pack(fill=tk.X, pady=(0, 15))
        cohort_lbl = "Personal Score Matrix" if selected_role == "student" else f"Total Cohort: {total_students} Scholars"
        tk.Label(strip, text=cohort_lbl, font=F_SUBTTL, bg=BG_CARD, fg=TEXT_DARK).pack(side=tk.LEFT)
        tk.Label(strip, text=f"Composite Average Score: {round(global_average, 1)}%", font=F_SUBTTL, bg=BG_CARD, fg=PURPLE).pack(side=tk.RIGHT)

        split_frame = tk.Frame(body, bg=BG_MAIN)
        split_frame.pack(fill=tk.BOTH, expand=True)

        # 1. BAR HISTOGRAM
        left_pan = tk.LabelFrame(split_frame, text=" 📊 Subject Marks Presentation ", font=F_SUBTTL, bg=BG_CARD, fg=TEXT_DARK, bd=1, relief="solid")
        left_pan.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        can_bar = tk.Canvas(left_pan, bg=WHITE, height=340, width=400, highlightthickness=0)
        can_bar.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        bar_colors = [YELLOW, GREEN, PURPLE]
        for idx, (sub_name, score) in enumerate(zip(SUBJECTS, avg_subject_scores)):
            x0 = 60 + (idx * 110)
            y0 = 280 - int(score * 2.2)
            x1 = x0 + 70
            y1 = 280
            can_bar.create_rectangle(x0, y0, x1, y1, fill=bar_colors[idx], outline="")
            can_bar.create_text((x0+x1)//2, y0-15, text=f"{round(score,1)}%", font=F_SMALL, fill=TEXT_DARK)
            can_bar.create_text((x0+x1)//2, y1+15, text=sub_name, font=F_BTN, fill=TEXT_MED)
        can_bar.create_line(30, 280, 370, 280, fill=SILVER_DARK, width=2)

        # 2. RADIAL OR PIE DISTRIBUTOR
        right_pan = tk.LabelFrame(split_frame, text=" 🍕 Performance Distribution Breakdown ", font=F_SUBTTL, bg=BG_CARD, fg=TEXT_DARK, bd=1, relief="solid")
        right_pan.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        can_pie = tk.Canvas(right_pan, bg=WHITE, height=340, width=400, highlightthickness=0)
        can_pie.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        if selected_role == "student":
            target_color = GREEN if global_average >= 85 else (YELLOW if global_average >= 60 else "#ff6b6b")
            extent_angle = (global_average / 100.0) * 360
            can_pie.create_oval(60, 40, 260, 240, outline=SILVER, width=18)
            can_pie.create_arc(60, 40, 260, 240, start=90, extent=-extent_angle, outline=target_color, style="arc", width=18)
            can_pie.create_text(160, 140, text=f"{round(global_average)}%", font=("Segoe UI", 24, "bold"), fill=TEXT_DARK)
            status_text = "Elite Tier" if global_average >= 85 else ("Pass Standing" if global_average >= 60 else "Needs Focus")
            can_pie.create_text(160, 270, text=f"Current: {status_text}", font=F_SUBTTL, fill=TEXT_MED)
        else:
            cursor.execute("""
                SELECT SUM(CASE WHEN marks>=85 THEN 1 ELSE 0 END),
                       SUM(CASE WHEN marks BETWEEN 60 AND 84 THEN 1 ELSE 0 END),
                       SUM(CASE WHEN marks < 60 THEN 1 ELSE 0 END)
                FROM students""")
            tier_counts = [int(x or 0) for x in cursor.fetchone()]
            tier_labels = ["Elite (>=85)", "Pass (60-84)", "Needs Focus (<60)"]
            tier_colors = [GREEN, YELLOW, "#ff6b6b"]

            start_angle = 0
            for count, label, color in zip(tier_counts, tier_labels, tier_colors):
                if count == 0: continue
                extent = (count / total_for_div) * 360
                can_pie.create_arc(30, 40, 230, 240, start=start_angle, extent=extent, fill=color, outline=WHITE, width=2)
                start_angle += extent
            
            for idx, (lbl, count) in enumerate(zip(tier_labels, tier_counts)):
                pct = round((count / total_for_div) * 100)
                can_pie.create_oval(260, 70+(idx*35), 275, 85+(idx*35), fill=tier_colors[idx], outline="")
                can_pie.create_text(285, 78+(idx*35), text=f"{lbl}: {count} ({pct}%)", font=F_SMALL, fill=TEXT_DARK, anchor="w")

    except Exception as e: 
        messagebox.showerror("Dashboard Engine Error", str(e))

def leaderboard():
    win = tk.Toplevel(root)
    win.title("Academic Elite Standings")
    center_window(win, 700, 420)
    win.configure(bg=BG_MAIN)
    tk.Frame(win, bg=YELLOW, height=5).pack(fill=tk.X)
    body = tk.Frame(win, bg=BG_MAIN, padx=24, pady=20)
    body.pack(fill=tk.BOTH, expand=True)
    
    tk.Label(body, text="🏆 Academic Leaderboard", font=F_HERO, bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w")
    tk.Label(body, text="Celebrating the top 5 highest cumulative scorers across campus", font=F_SMALL, bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w", pady=(2,14))
    
    cols = ("Rank", "Name", "Department", "Composite Average Score")
    container, tree = styled_treeview(body, cols, [80, 200, 240, 160])
    container.pack(fill=tk.BOTH, expand=True)
    
    try:
        cursor.execute("SELECT name, department, marks FROM students ORDER BY marks DESC LIMIT 5")
        for rank, row in enumerate(cursor.fetchall(), 1):
            medals = {1: "🥇 First", 2: "🥈 Second", 3: "🥉 Third"}
            rank_text = medals.get(rank, f"#{rank}")
            tree.insert("", tk.END, values=(rank_text, row[0], row[1], f"{row[2]}% Composite"))
    except Exception as e: 
        messagebox.showerror("Error", str(e))

def search_department():
    win = tk.Toplevel(root)
    win.title("Departmental Lookup")
    center_window(win, 840, 540)
    win.configure(bg=BG_MAIN)
    tk.Frame(win, bg=YELLOW, height=5).pack(fill=tk.X)

    body = tk.Frame(win, bg=BG_MAIN, padx=24, pady=20)
    body.pack(fill=tk.BOTH, expand=True)

    tk.Label(body, text="Departmental Finder", font=F_HERO, bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w")
    row_bar = tk.Frame(body, bg=BG_MAIN)
    row_bar.pack(fill=tk.X, pady=10)

    fe, de = styled_entry(row_bar, width=36)
    fe.pack(side=tk.LEFT, padx=(0, 12))

    cols = ("ID", "Name", "Department", "Maths", "Science", "English")
    container, tree = styled_treeview(body, cols, [60, 210, 260, 80, 80, 80])
    container.pack(fill=tk.BOTH, expand=True, pady=8)

    def search():
        for item in tree.get_children(): tree.delete(item)
        try:
            cursor.execute("SELECT id, name, department, maths, science, english FROM students WHERE department=%s", (de.get(),))
            for r in cursor.fetchall(): tree.insert("", tk.END, values=r)
        except Exception as e: 
            messagebox.showerror("Error", str(e))

    styled_button(row_bar, "Search Space", BTN_YELLOW, search, width=14, pady_inner=6).pack(side=tk.LEFT)
    de.bind("<Return>", lambda e: search())

def view_audit_log():
    win = tk.Toplevel(root)
    win.title("System Audit Log")
    center_window(win, 920, 500)
    win.configure(bg=BG_MAIN)
    tk.Frame(win, bg=PURPLE, height=5).pack(fill=tk.X)
    body = tk.Frame(win, bg=BG_MAIN, padx=24, pady=20)
    body.pack(fill=tk.BOTH, expand=True)
    tk.Label(body, text="System Action Audit Trails", font=F_TITLE, bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w", pady=(0,10))
    
    cols = ("Log ID", "User ID", "Action", "Details Context String", "Timestamp Tracker")
    container, tree = styled_treeview(body, cols, [70, 90, 110, 420, 200])
    container.pack(fill=tk.BOTH, expand=True)
    
    try:
        cursor.execute("SELECT id, user_id, action, details, timestamp FROM audit_logs ORDER BY id DESC LIMIT 50")
        for row in cursor.fetchall():
            formatted_row = list(row)
            if formatted_row[1] is None:
                formatted_row[1] = "SYSTEM"
            tree.insert("", tk.END, values=formatted_row)
    except Exception as e:
        messagebox.showerror("Audit System Extraction Failure", str(e))

# ============================================================
#  INNOVATIVE CONNECTED SCATTER COORDINATE GRADE CURVE PREDICTOR 📉
# ============================================================
def curve_predictor_feature():
    """ADVANCED FACULTY FEATURE: Renders a true linear coordinate scattered trend wave."""
    win = tk.Toplevel(root)
    win.title("Grade Curve Predictor Workspace Engine")
    center_window(win, 740, 640)
    win.configure(bg=BG_MAIN)
    tk.Frame(win, bg=PURPLE, height=5).pack(fill=tk.X)
    
    inner = tk.Frame(win, bg=BG_CARD, padx=24, pady=20)
    inner.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)
    
    tk.Label(inner, text="Grade Curve Predictor Coordinate Wave", font=F_TITLE, bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w")
    tk.Label(inner, text="Simulate a linear curve value tracking adjustments on the fly:", font=F_SMALL, bg=BG_CARD, fg=TEXT_MUTED).pack(anchor="w", pady=(2, 10))
    
    fr, en = styled_entry(inner)
    fr.pack(fill=tk.X, pady=(4, 12))
    en.insert(0, "10") # Default testing adjustment value
    
    chart_pan = tk.LabelFrame(inner, text=" Connected Scatter Shift Projection (Gray Dotted = Current | Purple = Curved) ", font=F_SUBTTL, bg=WHITE, fg=TEXT_DARK, bd=1, relief="solid")
    chart_pan.pack(fill=tk.BOTH, expand=True, pady=10)
    
    can_sim = tk.Canvas(chart_pan, bg=WHITE, highlightthickness=0)
    can_sim.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def run_sim():
        can_sim.delete("all")
        try:
            val = int(en.get())
            
            # Fetch all individual marks sequentially to plot as points
            cursor.execute("SELECT name, marks FROM students ORDER BY marks ASC")
            records = cursor.fetchall()
            
            if not records:
                can_sim.create_text(320, 150, text="No active student marks profiles found to plot.", font=F_BODY, fill=TEXT_MUTED)
                return
                
            count = len(records)
            
            # Draw standard coordinate axes rules
            can_sim.create_line(50, 30, 50, 260, fill=SILVER_DARK, width=2)   # Y Axis
            can_sim.create_line(50, 260, 620, 260, fill=SILVER_DARK, width=2) # X Axis
            
            # Y Axis Grid Increments (Marks 0 to 100)
            for y_val in [0, 25, 50, 75, 100]:
                y_coord = 260 - int(y_val * 2.0)
                can_sim.create_line(45, y_coord, 620, y_coord, fill=SILVER, dash=(4,4))
                can_sim.create_text(25, y_coord, text=f"{y_val}", font=F_SMALL, fill=TEXT_MUTED)
            
            x_interval = 540 / count if count > 1 else 540
            
            prev_curr_coords = None
            prev_curv_coords = None
            
            # Plot Scattered Trend Dots and connecting segments
            for i, (name, marks) in enumerate(records):
                cx = 60 + int(i * x_interval)
                
                # Base Math Scores
                cy_curr = 260 - int(marks * 2.0)
                # Curve-adjusted score cap at 100
                cy_curv = 260 - int(min(marks + val, 100) * 2.0)
                
                # Plot Coordinates Dots (Scatter points)
                can_sim.create_oval(cx-3, cy_curr-3, cx+3, cy_curr+3, fill=SILVER_DARK, outline="")
                can_sim.create_oval(cx-3, cy_curv-3, cx+3, cy_curv+3, fill=PURPLE, outline="")
                
                # Connect segments dynamically across indices
                if prev_curr_coords:
                    can_sim.create_line(prev_curr_coords[0], prev_curr_coords[1], cx, cy_curr, fill=SILVER_DARK, dash=(2,2), width=1)
                if prev_curv_coords:
                    can_sim.create_line(prev_curv_coords[0], prev_curv_coords[1], cx, cy_curv, fill=PURPLE, width=2)
                    
                prev_curr_coords = (cx, cy_curr)
                prev_curv_coords = (cx, cy_curv)
                
                # Display individual labels on the axis bounds if dataset is small
                if count <= 8:
                    can_sim.create_text(cx, 275, text=name, font=F_SMALL, fill=TEXT_MED, angle=45)
                    
            # Render a summary message stamp inside chart space
            cursor.execute("SELECT COUNT(*) FROM students WHERE marks + %s >= 50", (val,))
            pass_count = cursor.fetchone()[0]
            can_sim.create_text(340, 290, text=f"✨ Simulation Projection: A +{val} shift brings {pass_count} scholars to passing bounds (>=50)", font=F_BTN, fill=GOLD)
            
        except Exception as e:
            can_sim.create_text(320, 150, text="Provide an integer configuration to update view graphics.", font=F_SMALL, fill="#ff6b6b")
            
    styled_button(inner, "Compute Scatter Wave", BTN_PURPLE, run_sim, width=22).pack(pady=5)
    run_sim()

# ============================================================
#  FIXED & STABILIZED BONUS CREDIT INGESTION ENGINE 💎
# ============================================================
def add_bonus_marks():
    """Stabilized single-statement safe transaction handler for updating subject fields and composite totals."""
    win, inner = card_window("Apply Extra Credit", 420, 300)
    field_label(inner, "Target Student ID").pack(anchor="w")
    fe1, ide = styled_entry(inner); fe1.pack(fill=tk.X, pady=(4, 12))
    field_label(inner, "Bonus Points Amount").pack(anchor="w")
    fe2, be = styled_entry(inner); fe2.pack(fill=tk.X, pady=(4, 22))
    
    def apply():
        if not ide.get() or not be.get():
            messagebox.showwarning("Incomplete Fields", "Please supply parameters.")
            return
        try:
            bonus = int(be.get())
            student_id = int(ide.get())
            
            # Step 1: Read existing row indices into local variables safely
            cursor.execute("SELECT name, maths, science, english FROM students WHERE id = %s", (student_id,))
            result = cursor.fetchone()
            
            if not result:
                messagebox.showerror("Error", "No student tracked matching this ID.")
                return
                
            s_name, current_m, current_s, current_e = result
            
            # Step 2: Calculate new capped bounds in Python environment
            new_m = min(current_m + bonus, 100)
            new_s = min(current_s + bonus, 100)
            new_e = min(current_e + bonus, 100)
            new_marks_avg = (new_m + new_s + new_e) // 3
            
            # Step 3: Write finalized variables straight back to server row cache
            cursor.execute("""
                UPDATE students SET 
                maths = %s, 
                science = %s, 
                english = %s, 
                marks = %s 
                WHERE id = %s""", (new_m, new_s, new_e, new_marks_avg, student_id))
            db.commit()
            
            log_action("BONUS_GRANT", f"Awarded +{bonus} extra credits to student: {s_name} (ID: {student_id})")
            messagebox.showinfo("Granted 🎉", f"Bonus safely applied! {s_name}'s new average is {new_marks_avg}%.")
            win.destroy()
            
        except Exception as e: 
            messagebox.showerror("Transaction Failure", str(e))
            
    styled_button(inner, "Apply Points", BTN_GREEN, apply, width=22).pack()

# ============================================================
#  REPORT CARD & AUXILIARY LEDGERS
# ============================================================
def generate_report_card_view():
    global selected_role, current_session_username
    win, inner = card_window("Academic Performance Report Card Viewer", 500, 540)
    
    f_id, e_id = styled_entry(inner)
    if selected_role == "student":
        tk.Label(inner, text=f"Logged Student Frame Access: {current_session_username.upper()}", font=F_SUBTTL, bg=BG_CARD, fg=GREEN).pack(anchor="w", pady=(0,10))
    else:
        field_label(inner, "Enter Student ID to Generate Report Card").pack(anchor="w")
        f_id.pack(fill=tk.X, pady=(4, 12))
    
    card_frame = tk.Frame(inner, bg=YELLOW_LIGHT, highlightbackground=GOLD, highlightthickness=2, padx=20, pady=20)
    card_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    lbl_title = tk.Label(card_frame, text="✨ SCHOLASTIC REPORT CARD ✨", font=F_TITLE, bg=YELLOW_LIGHT, fg=GOLD)
    lbl_title.pack(pady=(0, 10))
    
    lbl_details = tk.Label(card_frame, text="Click Generate below to track scholastic vectors.", font=F_BODY, bg=YELLOW_LIGHT, fg=TEXT_DARK, justify="left")
    lbl_details.pack(fill=tk.BOTH, expand=True)
    
    def process_card():
        try:
            if selected_role == "student":
                cursor.execute("SELECT id, name, department, maths, science, english FROM students WHERE name=%s", (current_session_username,))
            else:
                cursor.execute("SELECT id, name, department, maths, science, english FROM students WHERE id=%s", (e_id.get(),))
                
            res = cursor.fetchone()
            if res:
                s_id, name, dept, m, s, e = res
                avg = (m + s + e) / 3
                status = "Excellent Standings 🌟" if avg >= 85 else ("Passing Clear Track 👍" if avg >= 60 else "Requires Mentorship Warning ⚠️")
                
                report_text = f"Student ID: {s_id}\nName: {name}\nDepartment: {dept}\n" + "—"*32 + f"\n\n  📐 Mathematics Core: {m} pts\n  🔬 Science Matrix: {s} pts\n  📚 English Language: {e} pts\n\n" + "—"*32 + f"\n\nComposite Average Score: {round(avg,1)}%\nStatus Tracking: {status}"
                lbl_details.config(text=report_text, font=("Consolas", 11), fg=TEXT_DARK, justify="left")
            else:
                messagebox.showerror("Error", "No student tracked matching these parameters.")
        except Exception as err:
            messagebox.showerror("Error", str(err))
            
    btn_lbl = "View My Report Card" if selected_role == "student" else "Generate Report Card"
    styled_button(inner, btn_lbl, BTN_GREEN, process_card, width=22).pack()

def view_own_record():
    global current_session_username
    win = tk.Toplevel(root)
    win.title("My Academic Portfolio")
    center_window(win, 840, 400)
    win.configure(bg=BG_MAIN)
    tk.Frame(win, bg=GREEN, height=5).pack(fill=tk.X)
    
    body = tk.Frame(win, bg=BG_MAIN, padx=24, pady=20)
    body.pack(fill=tk.BOTH, expand=True)
    tk.Label(body, text=f"My Ledger ({current_session_username})", font=F_HERO, bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w")
    
    motivational_quotes = [
        "🌸 Trust the process! Continuous learning brings beautiful outcomes.",
        "📚 Small milestones every single semester build amazing journeys.",
        "🌟 You are brilliant, capable, and uniquely equipped to excel!"
    ]
    tk.Label(body, text=random.choice(motivational_quotes), font=("Segoe UI italic", 10), bg=BG_MAIN, fg=GOLD).pack(anchor="w", pady=(2, 10))
    
    cols = ("ID", "Name", "Department", "Maths", "Science", "English", "Cumulative Average")
    container, tree = styled_treeview(body, cols, [60, 180, 180, 80, 80, 80, 130])
    container.pack(fill=tk.BOTH, expand=True, pady=10)
    
    try:
        cursor.execute("SELECT id, name, department, maths, science, english FROM students WHERE name=%s", (current_session_username,))
        row = cursor.fetchone()
        if row:
            scores = row[3:]
            avg_score = round(sum(scores) / len(scores), 1) if scores else 0
            tree.insert("", tk.END, values=row + (avg_score,))
        else:
            messagebox.showwarning("Incomplete Profile", "No record entry found matching your profile username.")
    except Exception as e: 
        messagebox.showerror("Error", str(e))

def admin_password_reset():
    win, inner = card_window("Account Access Reset Tool", 440, 380)
    field_label(inner, "Target Username Profile").pack(anchor="w")
    fu, eu = styled_entry(inner); fu.pack(fill=tk.X, pady=(4, 12))
    
    field_label(inner, "Assign Platform Role").pack(anchor="w")
    rc = ttk.Combobox(inner, values=["admin", "faculty", "student"], state="readonly", font=F_BODY)
    rc.pack(fill=tk.X, pady=(4, 12)); rc.current(1)
    
    field_label(inner, "New Master Passcode").pack(anchor="w")
    fp, ep = styled_entry(inner, show="*"); fp.pack(fill=tk.X, pady=(4, 20))
    
    def execute_reset():
        if not eu.get() or not ep.get():
            messagebox.showwarning("Incomplete", "Supply all parameters before updating.")
            return
        try:
            new_hash = hash_password(ep.get())
            cursor.execute("UPDATE users SET password_hash=%s WHERE username=%s AND role=%s", (new_hash, eu.get(), rc.get()))
            db.commit()
            if cursor.rowcount > 0:
                log_action("CREDENTIAL_RESET", f"Administrative forced password override for profile user: {eu.get()}")
                messagebox.showinfo("Success Keys 🔑", f"Security password updated successfully.")
                win.destroy()
            else:
                messagebox.showerror("Failed Reset", "No matching account verified within target profile fields.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    styled_button(inner, "Reset Account Key", BTN_DANGER, execute_reset, width=22).pack()

def export_high_performers():
    try:
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV File", "*.csv")])
        if not path: return
        cursor.execute("SELECT id, name, department, maths, science, english, marks FROM students WHERE marks>=70 ORDER BY marks DESC")
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["ID", "Name", "Department", "Maths", "Science", "English", "Composite Average"])
            w.writerows(cursor.fetchall())
        messagebox.showinfo("Exported 📂", "High performers roster exported successfully!")
    except Exception as e: 
        messagebox.showerror("Error", str(e))

def manage_users():
    win, inner = card_window("Create Secure Account", 440, 440)
    field_label(inner, "New Username").pack(anchor="w")
    fe1, ue = styled_entry(inner); fe1.pack(fill=tk.X, pady=(4, 12))
    field_label(inner, "Secure Password").pack(anchor="w")
    fe2, pe = styled_entry(inner, show="*"); fe2.pack(fill=tk.X, pady=(4, 12))
    field_label(inner, "Assign Platform Role").pack(anchor="w")
    
    rc = ttk.Combobox(inner, values=["admin", "faculty", "student"], state="readonly", font=F_BODY)
    rc.pack(fill=tk.X, pady=(4, 22)); rc.current(0)
    
    def create():
        try:
            cursor.execute("INSERT INTO users(username, password_hash, role) VALUES(%s, %s, %s)",
                           (ue.get(), hash_password(pe.get()), rc.get()))
            db.commit()
            messagebox.showinfo("Created ✨", "New security role initialized successfully.")
            win.destroy()
        except Exception as e: 
            messagebox.showerror("Error", str(e))
    styled_button(inner, "Generate Access Keys", BTN_PURPLE, create, width=22).pack()

# ============================================================
#  ROBUST MULTI-ROLE INTERFACE ROUTER
# ============================================================
BUTTON_GROUPS = {
    "admin": [
        ("Add Student Profile", add_student, BTN_GREEN),
        ("View Student Roster", view_students, BTN_SILVER),
        ("Update Records Form", update_student, BTN_PURPLE),
        ("Remove Old Profile", delete_student, BTN_DANGER),
        ("Award Bonus Credit", add_bonus_marks, BTN_GREEN),
        ("Departmental Lookup", search_department, BTN_SILVER),
        ("Statistical Metrics", analytics, BTN_YELLOW),
        ("Global Leaderboard", leaderboard, BTN_YELLOW),
        ("Export Roster (.CSV)", export_high_performers, BTN_SILVER),
        ("Review Audit Trail", view_audit_log, BTN_PURPLE),
        ("Initialize User Key", manage_users, BTN_SILVER),
        ("Reset Profile Password", admin_password_reset, BTN_DANGER),
        ("Print Report Cards", generate_report_card_view, BTN_PURPLE),
    ],
    "faculty": [
        ("Add Student Profile", add_student, BTN_GREEN),
        ("View Student Roster", view_students, BTN_SILVER),
        ("Update Records Form", update_student, BTN_PURPLE),
        ("Award Bonus Credit", add_bonus_marks, BTN_GREEN),
        ("Departmental Lookup", search_department, BTN_SILVER),
        ("Statistical Metrics", analytics, BTN_YELLOW),
        ("Global Leaderboard", leaderboard, BTN_YELLOW),
        ("Simulate Grade Curve", curve_predictor_feature, BTN_PURPLE),
        ("Print Report Cards", generate_report_card_view, BTN_PURPLE),
    ],
    "student": [
        ("View My Ledger", view_own_record, BTN_GREEN),
        ("Classmate Directory", view_students, BTN_SILVER),
        ("Performance Metrics", analytics, BTN_YELLOW),
        ("Global Leaderboard", leaderboard, BTN_YELLOW),
        ("View My Report Card", generate_report_card_view, BTN_PURPLE),
    ],
}

ROLE_STRIPE = {"admin": GOLD,         "faculty": PURPLE,       "student": GREEN}
ROLE_ICON   = {"admin": "⚙️",         "faculty": "📚",         "student": "🎓"}
ROLE_BG     = {"admin": YELLOW_LIGHT, "faculty": PURPLE_LIGHT, "student": GREEN_LIGHT}

def open_dashboard(role):
    global current_session_username
    dash = tk.Toplevel(root)
    dash.title(f"{role.upper()} HUB")
    center_window(dash, 920, 720)
    dash.configure(bg=BG_MAIN)

    stripe_color = ROLE_STRIPE.get(role, YELLOW)
    tk.Frame(dash, bg=stripe_color, height=5).pack(fill=tk.X)
    outer = tk.Frame(dash, bg=BG_MAIN); outer.pack(fill=tk.BOTH, expand=True)

    sidebar = tk.Frame(outer, bg=BG_SIDEBAR, width=240, padx=16, pady=24)
    sidebar.pack(side=tk.LEFT, fill=tk.Y); sidebar.pack_propagate(False)

    logo_bg = tk.Frame(sidebar, bg=stripe_color, padx=10, pady=6)
    logo_bg.pack(fill=tk.X, pady=(0, 20))
    tk.Label(logo_bg, text="SPA PORTAL SYSTEM", font=("Segoe UI", 12, "bold"), bg=stripe_color, fg=WHITE).pack(anchor="center")

    tk.Label(sidebar, text=ROLE_ICON.get(role, ""), font=("Segoe UI", 36), bg=BG_SIDEBAR, fg=stripe_color).pack(pady=4)
    
    display_title = f"{current_session_username.upper()}" if role == "student" else role.upper()
    tk.Label(sidebar, text=display_title, font=("Segoe UI", 12, "bold"), bg=BG_SIDEBAR, fg=TEXT_DARK).pack()
    tk.Label(sidebar, text="Active Secure Link", font=F_SMALL, bg=BG_SIDEBAR, fg=TEXT_MUTED).pack(pady=(2, 0))

    tk.Frame(sidebar, bg=SILVER, height=1).pack(fill=tk.X, pady=20)
    
    btn_canvas = tk.Canvas(sidebar, bg=BG_SIDEBAR, bd=0, highlightthickness=0)
    btn_scroll = tk.Scrollbar(sidebar, orient="vertical", command=btn_canvas.yview)
    btn_frame = tk.Frame(btn_canvas, bg=BG_SIDEBAR)
    
    btn_frame.bind("<Configure>", lambda e: btn_canvas.configure(scrollregion=btn_canvas.bbox("all")))
    btn_canvas.create_window((0,0), window=btn_frame, anchor="nw", width=200)
    btn_canvas.configure(yscrollcommand=btn_scroll.set)
    btn_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    styled_button(sidebar, "🚪   Log Out Hub", BTN_DANGER, dash.destroy, width=16, pady_inner=6).pack(pady=10)

    content = tk.Frame(outer, bg=BG_MAIN, padx=24, pady=20)
    content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    hdr = tk.Frame(content, bg=ROLE_BG.get(role, YELLOW_LIGHT), padx=16, pady=12, highlightbackground=SILVER, highlightthickness=1)
    hdr.pack(fill=tk.X, pady=(0, 18))
    tk.Label(hdr, text=f"Student Performance Analyzer Dashboard", font=F_TITLE, bg=ROLE_BG.get(role, YELLOW_LIGHT), fg=TEXT_DARK).pack(anchor="w")
    tk.Label(hdr, text="Select an operations module below to execute systemic processing routines:", font=F_SMALL, bg=ROLE_BG.get(role, YELLOW_LIGHT), fg=TEXT_MED).pack(anchor="w")

    grid_canvas = tk.Canvas(content, bg=BG_MAIN, bd=0, highlightthickness=0)
    grid_scroll = tk.Scrollbar(content, orient="vertical", command=grid_canvas.yview)
    grid = tk.Frame(grid_canvas, bg=BG_MAIN)
    
    grid.bind("<Configure>", lambda e: grid_canvas.configure(scrollregion=grid_canvas.bbox("all")))
    grid_canvas.create_window((0,0), window=grid, anchor="nw", width=580)
    grid_canvas.configure(yscrollcommand=grid_scroll.set)
    
    grid_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    grid_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    items = BUTTON_GROUPS.get(role, [])
    for i, (label, cmd, palette) in enumerate(items):
        r, c = divmod(i, 2)
        grid.columnconfigure(c, weight=1)
        cell = tk.Frame(grid, bg=WHITE, highlightbackground=SILVER, highlightthickness=1)
        cell.grid(row=r, column=c, padx=6, pady=6, sticky="ew")
        
        tk.Frame(cell, bg=palette["bg"], width=4).pack(side=tk.LEFT, fill=tk.Y)
        btn = tk.Button(cell, text=label, font=F_BTN, bg=WHITE, fg=TEXT_DARK,
                        activebackground=palette["bg"], activeforeground=palette["fg"],
                        relief="flat", bd=0, cursor="hand2", height=2, command=cmd)
        btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        _hover(btn, WHITE, "#fcfcfd")

def open_login(role):
    global selected_role
    selected_role = role
    stripe = ROLE_STRIPE.get(role, YELLOW)
    icon = ROLE_ICON.get(role, "")

    win = tk.Toplevel(root)
    win.title(f"Authentication Portal")
    center_window(win, 440, 460)
    win.configure(bg=BG_MAIN)

    tk.Frame(win, bg=stripe, height=5).pack(fill=tk.X)
    body = tk.Frame(win, bg=BG_CARD, padx=36, pady=28)
    body.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

    badge = tk.Frame(body, bg=ROLE_BG.get(role, YELLOW_LIGHT), padx=12, pady=6)
    badge.pack(anchor="w", pady=(0, 10))
    tk.Label(badge, text=f"{icon}  {role.upper()} GATEWAY", font=("Segoe UI", 11, "bold"), bg=ROLE_BG.get(role, YELLOW_LIGHT), fg=TEXT_DARK).pack()

    tk.Label(body, text="Provide credentials to access system features:", font=F_SMALL, bg=BG_CARD, fg=TEXT_MUTED).pack(anchor="w", pady=(0, 18))

    field_label(body, "System Username").pack(anchor="w")
    fe1, ue = styled_entry(body); fe1.pack(fill=tk.X, pady=(4, 12))

    field_label(body, "Passcode Entry").pack(anchor="w")
    fe2, pe = styled_entry(body, show="*"); fe2.pack(fill=tk.X, pady=(4, 24))

    def role_login():
        global current_user_id, current_session_username
        hashed = hash_password(pe.get())
        
        cursor.execute("SELECT id, role, username FROM users WHERE username=%s AND password_hash=%s AND role=%s",
                       (ue.get(), hashed, selected_role))
        result = cursor.fetchone()

        if result:
            current_user_id = result[0]
            current_session_username = result[2]
            messagebox.showinfo("Access Granted 🔑", f"Successfully logged into secure session framework.")
            win.destroy()
            open_dashboard(result[1])
        else:
            messagebox.showerror("Access Denied❌", "Invalid credentials. Please re-verify spelling parameters.")

    login_btn = tk.Button(body, text="Authenticate Base Session →", font=("Segoe UI", 11, "bold"),
                          bg=stripe, fg=TEXT_DARK if stripe == YELLOW else WHITE,
                          activebackground=GOLD, relief="flat", bd=0, cursor="hand2", pady=11, command=role_login)
    login_btn.pack(fill=tk.X)
    _hover(login_btn, stripe, GOLD if stripe == YELLOW else "#6a4ec4")

    win.bind("<Return>", lambda event: role_login())

# ============================================================
#  ROOT BASE INITIALIZATION SWITCH
# ============================================================
root = tk.Tk()
root.title("Student Performance Analyzer")
center_window(root, 540, 640)
root.configure(bg=BG_MAIN)

tk.Frame(root, bg=YELLOW, height=5).pack(fill=tk.X)

hero = tk.Frame(root, bg=YELLOW_LIGHT, padx=36, pady=24)
hero.pack(fill=tk.X)
tk.Label(hero, text="🏫 SPA Analytics Core", font=("Segoe UI", 26, "bold"), bg=YELLOW_LIGHT, fg=GOLD).pack(anchor="w")
tk.Label(hero, text="The Smart Academic Performance Analytics Terminal Suite", font=("Segoe UI", 10), bg=YELLOW_LIGHT, fg=TEXT_MED).pack(anchor="w")

tk.Frame(root, bg=SILVER, height=1).pack(fill=tk.X)

mid = tk.Frame(root, bg=BG_MAIN, padx=36, pady=24)
mid.pack(fill=tk.BOTH, expand=True)

tk.Label(mid, text="Welcome! Identify Your Portal Base Role:", font=("Segoe UI", 13, "bold"), bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w")
tk.Label(mid, text="Select your corresponding access role profile tier below:", font=F_SMALL, bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w", pady=(2, 16))

role_configs = [
    ("admin",   "⚙️", "Administrator Tier", "Full infrastructure control, database, and credential parameters", YELLOW_LIGHT, GOLD),
    ("faculty", "📚", "Faculty Educator",   "Log module testing curves, marks entry, and report printing", PURPLE_LIGHT, PURPLE),
    ("student", "🎓", "Enrolled Student",    "Monitor unique scores, view performance curves and report card portfolios",  GREEN_LIGHT,  GREEN),
]

for role, icon, label, desc, bg, accent in role_configs:
    card = tk.Frame(mid, bg=bg, padx=14, pady=12, cursor="hand2", highlightbackground=SILVER, highlightthickness=1)
    card.pack(fill=tk.X, pady=6)
    
    tk.Frame(card, bg=accent, width=4).pack(side=tk.LEFT, fill=tk.Y, padx=(0, 12))
    info = tk.Frame(card, bg=bg)
    info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    tk.Label(info, text=f"{icon}  {label}", font=("Segoe UI", 11, "bold"), bg=bg, fg=TEXT_DARK, anchor="w").pack(anchor="w")
    tk.Label(info, text=desc, font=F_SMALL, bg=bg, fg=TEXT_MED, anchor="w").pack(anchor="w")
    
    arrow = tk.Label(card, text="→", font=("Segoe UI", 14, "bold"), bg=bg, fg=accent)
    arrow.pack(side=tk.RIGHT)
    
    for widget in [card, info, arrow]:
        widget.bind("<Button-1>", lambda event, r=role: open_login(r))

tk.Label(root, text="✨ Designed with Sunny Academia Aesthetic Guidelines ✨", font=F_SMALL, bg=BG_MAIN, fg=TEXT_MUTED).pack(pady=12)

root.mainloop()