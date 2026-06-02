"""
Social Media User Engagement Analytics
Main GUI Application — Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
import sqlite3
import os
from datetime import datetime

# ── local module ────────────────────────────────────────────────────────────
from database import (
    get_connection, init_db,
    sp_user_engagement_summary,
    sp_top_trending_posts,
    sp_user_feed,
    DB_PATH,
)

# ── Colour palette ──────────────────────────────────────────────────────────
BG        = "#0f1117"
CARD      = "#1a1d2e"
ACCENT    = "#6c63ff"
ACCENT2   = "#ff6584"
SUCCESS   = "#43d9ad"
WARNING   = "#ffd166"
TEXT      = "#e2e8f0"
TEXT_DIM  = "#718096"
BORDER    = "#2d3748"


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  HELPER WIDGETS                                                          ║
# ╚══════════════════════════════════════════════════════════════════════════╝

def styled_button(parent, text, command, color=ACCENT, **kw):
    btn = tk.Button(
        parent, text=text, command=command,
        bg=color, fg="white", relief="flat",
        font=("Helvetica", 10, "bold"),
        padx=14, pady=6, cursor="hand2",
        activebackground=color, activeforeground="white",
        **kw
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=_lighten(color)))
    btn.bind("<Leave>", lambda e: btn.config(bg=color))
    return btn


def _lighten(hex_color):
    """Return a slightly lighter shade of a hex colour."""
    r = min(255, int(hex_color[1:3], 16) + 30)
    g = min(255, int(hex_color[3:5], 16) + 30)
    b = min(255, int(hex_color[5:7], 16) + 30)
    return f"#{r:02x}{g:02x}{b:02x}"


def label(parent, text, size=10, bold=False, color=TEXT, **kw):
    weight = "bold" if bold else "normal"
    return tk.Label(parent, text=text, bg=CARD, fg=color,
                    font=("Helvetica", size, weight), **kw)


def card_frame(parent, **kw):
    return tk.Frame(parent, bg=CARD, relief="flat",
                    highlightbackground=BORDER, highlightthickness=1, **kw)


def build_treeview(parent, columns, height=12):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Custom.Treeview",
                    background=CARD, foreground=TEXT,
                    fieldbackground=CARD, rowheight=26,
                    font=("Helvetica", 9))
    style.configure("Custom.Treeview.Heading",
                    background=ACCENT, foreground="white",
                    font=("Helvetica", 9, "bold"), relief="flat")
    style.map("Custom.Treeview", background=[("selected", ACCENT)])

    frame = tk.Frame(parent, bg=BG)
    tree  = ttk.Treeview(frame, columns=columns, show="headings",
                          height=height, style="Custom.Treeview")

    vsb = ttk.Scrollbar(frame, orient="vertical",   command=tree.yview)
    hsb = ttk.Scrollbar(frame, orient="horizontal",  command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid (row=0, column=1, sticky="ns")
    hsb.grid (row=1, column=0, sticky="ew")
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    return frame, tree


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  MAIN APPLICATION WINDOW                                                 ║
# ╚══════════════════════════════════════════════════════════════════════════╝

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("📊  Social Media User Engagement Analytics")
        self.geometry("1200x780")
        self.minsize(900, 600)
        self.configure(bg=BG)
        self.resizable(True, True)

        init_db()

        self._build_header()
        self._build_sidebar()
        self._build_content()
        self._show_dashboard()

    # ── Layout ──────────────────────────────────────────────────────────────

    def _build_header(self):
        hdr = tk.Frame(self, bg=CARD, height=56,
                       highlightbackground=BORDER, highlightthickness=1)
        hdr.pack(fill="x", side="top")
        hdr.pack_propagate(False)

        tk.Label(hdr, text="⬡  EngageIQ", bg=CARD, fg=ACCENT,
                 font=("Helvetica", 16, "bold")).pack(side="left", padx=20, pady=12)

        self.clock_lbl = tk.Label(hdr, text="", bg=CARD, fg=TEXT_DIM,
                                   font=("Helvetica", 9))
        self.clock_lbl.pack(side="right", padx=20)
        self._update_clock()

    def _update_clock(self):
        now = datetime.now().strftime("%d %b %Y  %H:%M:%S")
        self.clock_lbl.config(text=now)
        self.after(1000, self._update_clock)

    def _build_sidebar(self):
        sb = tk.Frame(self, bg=CARD, width=200,
                      highlightbackground=BORDER, highlightthickness=1)
        sb.pack(fill="y", side="left")
        sb.pack_propagate(False)

        nav_items = [
            ("🏠  Dashboard",     self._show_dashboard),
            ("👤  Add User",       self._show_add_user),
            ("📝  Create Post",    self._show_create_post),
            ("❤️   Like / Comment", self._show_interactions),
            ("📈  Analytics",      self._show_analytics),
            ("🔍  SQL Explorer",   self._show_sql_explorer),
        ]
        self.nav_btns = []
        for text, cmd in nav_items:
            btn = tk.Button(
                sb, text=text, command=lambda c=cmd, b_text=text: self._nav(c, b_text),
                bg=CARD, fg=TEXT, relief="flat",
                font=("Helvetica", 10), anchor="w",
                padx=18, pady=10, cursor="hand2",
                activebackground=ACCENT, activeforeground="white"
            )
            btn.pack(fill="x")
            self.nav_btns.append((text, btn))

        # DB info at bottom
        tk.Frame(sb, bg=BORDER, height=1).pack(fill="x", pady=10)
        tk.Label(sb, text=f"DB: {os.path.basename(DB_PATH)}",
                 bg=CARD, fg=TEXT_DIM, font=("Helvetica", 8)).pack(padx=10)

    def _nav(self, cmd, btn_text):
        for text, btn in self.nav_btns:
            btn.config(bg=ACCENT if text == btn_text else CARD,
                       fg="white" if text == btn_text else TEXT)
        cmd()

    def _build_content(self):
        self.content = tk.Frame(self, bg=BG)
        self.content.pack(fill="both", expand=True, side="left")

    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    # ── Page: Dashboard ─────────────────────────────────────────────────────

    def _show_dashboard(self):
        self._clear_content()
        conn  = get_connection()
        cur   = conn.cursor()

        stats = {
            "Users":    cur.execute("SELECT COUNT(*) FROM Users").fetchone()[0],
            "Posts":    cur.execute("SELECT COUNT(*) FROM Posts WHERE is_deleted=0").fetchone()[0],
            "Likes":    cur.execute("SELECT COUNT(*) FROM Likes").fetchone()[0],
            "Comments": cur.execute("SELECT COUNT(*) FROM Comments").fetchone()[0],
            "Followers":cur.execute("SELECT COUNT(*) FROM Followers").fetchone()[0],
            "Hashtags": cur.execute("SELECT COUNT(*) FROM Hashtags").fetchone()[0],
        }
        icons  = {"Users":"👤","Posts":"📝","Likes":"❤️","Comments":"💬","Followers":"🔗","Hashtags":"#️⃣"}
        colors = [ACCENT, ACCENT2, SUCCESS, WARNING, "#4ecdc4", "#ff9f43"]
        conn.close()

        tk.Label(self.content, text="Dashboard Overview", bg=BG, fg=TEXT,
                 font=("Helvetica", 14, "bold")).pack(anchor="w", padx=24, pady=(20,10))

        # Stat cards
        grid = tk.Frame(self.content, bg=BG)
        grid.pack(fill="x", padx=20)
        for i, (key, val) in enumerate(stats.items()):
            c = card_frame(grid, padx=16, pady=16)
            c.grid(row=i//3, column=i%3, padx=8, pady=8, sticky="ew")
            grid.columnconfigure(i%3, weight=1)
            tk.Label(c, text=icons[key], bg=CARD, font=("Helvetica",20)).pack()
            tk.Label(c, text=str(val), bg=CARD, fg=colors[i],
                     font=("Helvetica",22,"bold")).pack()
            tk.Label(c, text=key, bg=CARD, fg=TEXT_DIM,
                     font=("Helvetica",9)).pack()

        # Top posts
        tk.Label(self.content, text="🔥  Top Trending Posts", bg=BG, fg=TEXT,
                 font=("Helvetica", 12, "bold")).pack(anchor="w", padx=24, pady=(18,6))

        cols = ("Rank","User","Post","Type","Likes","Comments","Score")
        frame, tree = build_treeview(self.content, cols, height=8)
        frame.pack(fill="x", padx=20, pady=4)

        widths = [40,100,380,60,60,80,70]
        for col, w in zip(cols, widths):
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor="center" if w < 120 else "w")

        for i, row in enumerate(sp_top_trending_posts(10), 1):
            tree.insert("", "end", values=(
                i,
                row["username"],
                row["content"][:70] + ("…" if len(row["content"])>70 else ""),
                row["post_type"].upper(),
                row["total_likes"],
                row["total_comments"],
                f'{row["engagement_score"]:.1f}',
            ))

    # ── Page: Add User ───────────────────────────────────────────────────────

    def _show_add_user(self):
        self._clear_content()
        tk.Label(self.content, text="Add New User", bg=BG, fg=TEXT,
                 font=("Helvetica",14,"bold")).pack(anchor="w", padx=24, pady=(20,10))

        c = card_frame(self.content)
        c.pack(fill="x", padx=20, pady=10)

        fields = [
            ("Username *",   "username"),
            ("Email *",      "email"),
            ("Full Name *",  "full_name"),
            ("Bio",          "bio"),
            ("Location",     "location"),
        ]
        self._user_vars = {}
        for label_text, key in fields:
            row = tk.Frame(c, bg=CARD)
            row.pack(fill="x", padx=16, pady=6)
            tk.Label(row, text=label_text, bg=CARD, fg=TEXT_DIM,
                     font=("Helvetica",9), width=14, anchor="w").pack(side="left")
            var = tk.StringVar()
            ent = tk.Entry(row, textvariable=var, bg=BG, fg=TEXT,
                           insertbackground=TEXT, relief="flat",
                           font=("Helvetica",10),
                           highlightbackground=BORDER, highlightthickness=1)
            ent.pack(side="left", fill="x", expand=True)
            self._user_vars[key] = var

        styled_button(c, "  Create User  ", self._do_add_user).pack(pady=14)

        # Existing users
        tk.Label(self.content, text="Existing Users", bg=BG, fg=TEXT,
                 font=("Helvetica",12,"bold")).pack(anchor="w", padx=24, pady=(14,4))

        cols = ("ID","Username","Full Name","Location","Joined","Active")
        frame, tree = build_treeview(self.content, cols, height=9)
        frame.pack(fill="both", expand=True, padx=20, pady=4)
        for col, w in zip(cols,[40,120,160,160,100,60]):
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor="center" if w<100 else "w")

        conn = get_connection()
        for r in conn.execute("SELECT user_id,username,full_name,location,joined_date,is_active FROM Users ORDER BY user_id"):
            tree.insert("","end", values=(r[0],r[1],r[2],r[3] or "—",r[4],"✅" if r[5] else "❌"))
        conn.close()

    def _do_add_user(self):
        v = {k: var.get().strip() for k, var in self._user_vars.items()}
        if not v["username"] or not v["email"] or not v["full_name"]:
            messagebox.showerror("Validation Error", "Username, Email and Full Name are required.")
            return
        try:
            conn = get_connection()
            conn.execute(
                "INSERT INTO Users(username,email,full_name,bio,location) VALUES(?,?,?,?,?)",
                (v["username"], v["email"], v["full_name"], v["bio"] or None, v["location"] or None)
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"User @{v['username']} created!")
            self._show_add_user()
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Duplicate", str(e))

    # ── Page: Create Post ────────────────────────────────────────────────────

    def _show_create_post(self):
        self._clear_content()
        tk.Label(self.content, text="Create Post", bg=BG, fg=TEXT,
                 font=("Helvetica",14,"bold")).pack(anchor="w", padx=24, pady=(20,10))

        c = card_frame(self.content)
        c.pack(fill="x", padx=20, pady=10)

        # User selector
        row = tk.Frame(c, bg=CARD); row.pack(fill="x", padx=16, pady=6)
        tk.Label(row, text="Author *", bg=CARD, fg=TEXT_DIM,
                 font=("Helvetica",9), width=10, anchor="w").pack(side="left")
        conn = get_connection()
        users = [(r[0],r[1]) for r in conn.execute("SELECT user_id,username FROM Users ORDER BY username")]
        conn.close()
        self._post_user = tk.StringVar()
        cb = ttk.Combobox(row, textvariable=self._post_user,
                          values=[f"{uid} — @{uname}" for uid,uname in users],
                          state="readonly", font=("Helvetica",10))
        cb.pack(side="left", fill="x", expand=True)
        if users:
            cb.current(0)

        # Post type
        row2 = tk.Frame(c, bg=CARD); row2.pack(fill="x", padx=16, pady=6)
        tk.Label(row2, text="Type *", bg=CARD, fg=TEXT_DIM,
                 font=("Helvetica",9), width=10, anchor="w").pack(side="left")
        self._post_type = tk.StringVar(value="text")
        for pt in ("text","image","video","reel"):
            tk.Radiobutton(row2, text=pt.capitalize(), variable=self._post_type, value=pt,
                           bg=CARD, fg=TEXT, selectcolor=ACCENT,
                           activebackground=CARD).pack(side="left", padx=6)

        # Content
        row3 = tk.Frame(c, bg=CARD); row3.pack(fill="x", padx=16, pady=6)
        tk.Label(row3, text="Content *", bg=CARD, fg=TEXT_DIM,
                 font=("Helvetica",9), width=10, anchor="nw").pack(side="left")
        self._post_content = tk.Text(row3, height=5, bg=BG, fg=TEXT,
                                     insertbackground=TEXT, relief="flat",
                                     font=("Helvetica",10),
                                     highlightbackground=BORDER, highlightthickness=1)
        self._post_content.pack(side="left", fill="x", expand=True)

        # Hashtag checkboxes
        row4 = tk.Frame(c, bg=CARD); row4.pack(fill="x", padx=16, pady=6)
        tk.Label(row4, text="Hashtags", bg=CARD, fg=TEXT_DIM,
                 font=("Helvetica",9), width=10, anchor="nw").pack(side="left")
        conn = get_connection()
        tags = conn.execute("SELECT hashtag_id,tag_name FROM Hashtags ORDER BY tag_name").fetchall()
        conn.close()
        self._tag_vars = {}
        tags_frame = tk.Frame(row4, bg=CARD)
        tags_frame.pack(side="left", fill="x", expand=True)
        for i, (tid, tname) in enumerate(tags):
            var = tk.BooleanVar()
            tk.Checkbutton(tags_frame, text=tname, variable=var,
                           bg=CARD, fg=TEXT_DIM, selectcolor=ACCENT,
                           activebackground=CARD, font=("Helvetica",8)).grid(
                               row=i//5, column=i%5, sticky="w", padx=4)
            self._tag_vars[tid] = var

        styled_button(c, "  Publish Post  ", self._do_create_post).pack(pady=14)

        # Recent posts
        tk.Label(self.content, text="Recent Posts", bg=BG, fg=TEXT,
                 font=("Helvetica",12,"bold")).pack(anchor="w", padx=24, pady=(14,4))
        cols = ("ID","Author","Post Preview","Type","Date","Likes","Comments")
        frame, tree = build_treeview(self.content, cols, height=7)
        frame.pack(fill="both", expand=True, padx=20, pady=4)
        for col, w in zip(cols,[40,110,320,60,130,55,75]):
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor="center" if w<100 else "w")

        conn = get_connection()
        for r in conn.execute("""
            SELECT p.post_id,u.username,p.content,p.post_type,p.created_at,
                   e.total_likes,e.total_comments
            FROM Posts p
            JOIN Users u ON p.user_id=u.user_id
            JOIN Engagement e ON p.post_id=e.post_id
            WHERE p.is_deleted=0
            ORDER BY p.created_at DESC LIMIT 20
        """):
            tree.insert("","end", values=(
                r[0], "@"+r[1], r[2][:60]+"…" if len(r[2])>60 else r[2],
                r[3].upper(), r[4][:16], r[5], r[6]
            ))
        conn.close()

    def _do_create_post(self):
        sel = self._post_user.get()
        if not sel:
            messagebox.showerror("Error","Please select an author.")
            return
        uid   = int(sel.split(" — ")[0])
        ptype = self._post_type.get()
        cont  = self._post_content.get("1.0","end-1c").strip()
        if not cont:
            messagebox.showerror("Validation","Post content cannot be empty.")
            return
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute(
            "INSERT INTO Posts(user_id,content,post_type) VALUES(?,?,?)",
            (uid, cont, ptype)
        )
        pid = cur.lastrowid
        for tid, var in self._tag_vars.items():
            if var.get():
                cur.execute("INSERT OR IGNORE INTO Post_Hashtags(post_id,hashtag_id) VALUES(?,?)",(pid,tid))
        conn.commit()
        conn.close()
        messagebox.showinfo("Published!",f"Post #{pid} published successfully.")
        self._show_create_post()

    # ── Page: Like / Comment ─────────────────────────────────────────────────

    def _show_interactions(self):
        self._clear_content()
        tk.Label(self.content, text="Like & Comment on Posts", bg=BG, fg=TEXT,
                 font=("Helvetica",14,"bold")).pack(anchor="w", padx=24, pady=(20,10))

        top = tk.Frame(self.content, bg=BG)
        top.pack(fill="x", padx=20)

        # Left — Like panel
        lc = card_frame(top)
        lc.pack(side="left", fill="both", expand=True, padx=(0,8))
        tk.Label(lc, text="❤️  Like a Post", bg=CARD, fg=ACCENT2,
                 font=("Helvetica",11,"bold")).pack(anchor="w", padx=14, pady=(10,6))

        self._like_vars = {}
        for field, lbl in [("user","Your Username"),("post_id","Post ID")]:
            r = tk.Frame(lc, bg=CARD); r.pack(fill="x", padx=14, pady=4)
            tk.Label(r, text=lbl, bg=CARD, fg=TEXT_DIM, font=("Helvetica",9), width=14, anchor="w").pack(side="left")
            var = tk.StringVar()
            tk.Entry(r, textvariable=var, bg=BG, fg=TEXT, insertbackground=TEXT,
                     relief="flat", highlightbackground=BORDER, highlightthickness=1,
                     font=("Helvetica",10)).pack(side="left", fill="x", expand=True)
            self._like_vars[field] = var

        bf = tk.Frame(lc, bg=CARD); bf.pack(pady=10)
        styled_button(bf, "❤️  Like",   self._do_like,   color=ACCENT2).pack(side="left", padx=4)
        styled_button(bf, "💔  Unlike", self._do_unlike, color=BORDER).pack(side="left", padx=4)

        # Right — Comment panel
        rc = card_frame(top)
        rc.pack(side="left", fill="both", expand=True, padx=(8,0))
        tk.Label(rc, text="💬  Add Comment", bg=CARD, fg=SUCCESS,
                 font=("Helvetica",11,"bold")).pack(anchor="w", padx=14, pady=(10,6))

        self._comment_vars = {}
        for field, lbl in [("user","Your Username"),("post_id","Post ID")]:
            r = tk.Frame(rc, bg=CARD); r.pack(fill="x", padx=14, pady=4)
            tk.Label(r, text=lbl, bg=CARD, fg=TEXT_DIM, font=("Helvetica",9), width=14, anchor="w").pack(side="left")
            var = tk.StringVar()
            tk.Entry(r, textvariable=var, bg=BG, fg=TEXT, insertbackground=TEXT,
                     relief="flat", highlightbackground=BORDER, highlightthickness=1,
                     font=("Helvetica",10)).pack(side="left", fill="x", expand=True)
            self._comment_vars[field] = var

        r = tk.Frame(rc, bg=CARD); r.pack(fill="x", padx=14, pady=4)
        tk.Label(r, text="Comment", bg=CARD, fg=TEXT_DIM,
                 font=("Helvetica",9), width=14, anchor="nw").pack(side="left")
        self._comment_text = tk.Text(r, height=3, bg=BG, fg=TEXT, insertbackground=TEXT,
                                      relief="flat", font=("Helvetica",10),
                                      highlightbackground=BORDER, highlightthickness=1)
        self._comment_text.pack(side="left", fill="x", expand=True)

        styled_button(rc, "  Post Comment  ", self._do_comment, color=SUCCESS).pack(pady=10)

        # Recent activity
        tk.Label(self.content, text="Recent Activity", bg=BG, fg=TEXT,
                 font=("Helvetica",12,"bold")).pack(anchor="w", padx=24, pady=(14,4))
        cols = ("Post ID","Post Author","Post Preview","Likes","Comments","Score")
        frame, self._act_tree = build_treeview(self.content, cols, height=10)
        frame.pack(fill="both", expand=True, padx=20, pady=4)
        for col, w in zip(cols,[60,110,340,60,80,70]):
            self._act_tree.heading(col, text=col)
            self._act_tree.column(col, width=w, anchor="center" if w<100 else "w")
        self._refresh_activity()

    def _refresh_activity(self):
        self._act_tree.delete(*self._act_tree.get_children())
        conn = get_connection()
        for r in conn.execute("""
            SELECT p.post_id,u.username,p.content,e.total_likes,e.total_comments,e.engagement_score
            FROM Posts p
            JOIN Users u ON p.user_id=u.user_id
            JOIN Engagement e ON p.post_id=e.post_id
            WHERE p.is_deleted=0
            ORDER BY e.last_updated DESC LIMIT 20
        """):
            self._act_tree.insert("","end", values=(
                r[0], "@"+r[1], r[2][:60]+"…" if len(r[2])>60 else r[2],
                r[3], r[4], f"{r[5]:.1f}"
            ))
        conn.close()

    def _resolve_user_id(self, username):
        conn = get_connection()
        r = conn.execute("SELECT user_id FROM Users WHERE username=?", (username,)).fetchone()
        conn.close()
        return r[0] if r else None

    def _do_like(self):
        uname = self._like_vars["user"].get().strip().lstrip("@")
        pid   = self._like_vars["post_id"].get().strip()
        if not uname or not pid:
            messagebox.showerror("Error","Fill in both fields."); return
        uid = self._resolve_user_id(uname)
        if not uid: messagebox.showerror("Error",f"User @{uname} not found."); return
        try:
            conn = get_connection()
            conn.execute("INSERT INTO Likes(post_id,user_id) VALUES(?,?)",(int(pid),uid))
            conn.commit(); conn.close()
            messagebox.showinfo("Liked!",f"@{uname} liked post #{pid}.")
            self._refresh_activity()
        except sqlite3.IntegrityError:
            messagebox.showwarning("Already liked",f"@{uname} already liked post #{pid}.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _do_unlike(self):
        uname = self._like_vars["user"].get().strip().lstrip("@")
        pid   = self._like_vars["post_id"].get().strip()
        uid   = self._resolve_user_id(uname)
        if not uid: messagebox.showerror("Error",f"User @{uname} not found."); return
        conn = get_connection()
        conn.execute("DELETE FROM Likes WHERE post_id=? AND user_id=?",(int(pid),uid))
        conn.commit(); conn.close()
        messagebox.showinfo("Unliked",f"@{uname} unliked post #{pid}.")
        self._refresh_activity()

    def _do_comment(self):
        uname = self._comment_vars["user"].get().strip().lstrip("@")
        pid   = self._comment_vars["post_id"].get().strip()
        txt   = self._comment_text.get("1.0","end-1c").strip()
        if not uname or not pid or not txt:
            messagebox.showerror("Error","All comment fields are required."); return
        uid = self._resolve_user_id(uname)
        if not uid: messagebox.showerror("Error",f"User @{uname} not found."); return
        conn = get_connection()
        conn.execute("INSERT INTO Comments(post_id,user_id,content) VALUES(?,?,?)",(int(pid),uid,txt))
        conn.commit(); conn.close()
        self._comment_text.delete("1.0","end")
        messagebox.showinfo("Commented!",f"Comment added to post #{pid}.")
        self._refresh_activity()

    # ── Page: Analytics ──────────────────────────────────────────────────────

    def _show_analytics(self):
        self._clear_content()
        tk.Label(self.content, text="Engagement Analytics", bg=BG, fg=TEXT,
                 font=("Helvetica",14,"bold")).pack(anchor="w", padx=24, pady=(20,10))

        nb = ttk.Notebook(self.content)
        nb.pack(fill="both", expand=True, padx=20, pady=4)
        style = ttk.Style()
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", background=CARD, foreground=TEXT,
                        font=("Helvetica",9,"bold"), padding=[12,6])
        style.map("TNotebook.Tab", background=[("selected", ACCENT)],
                  foreground=[("selected","white")])

        # Tab 1 — User Leaderboard
        t1 = tk.Frame(nb, bg=BG); nb.add(t1, text="  👑 User Leaderboard  ")
        cols = ("Rank","Username","Posts","Likes","Comments","Engagement","Followers","Following")
        frame, tree = build_treeview(t1, cols, height=16)
        frame.pack(fill="both", expand=True, padx=8, pady=8)
        for col, w in zip(cols,[50,130,60,60,80,100,80,80]):
            tree.heading(col, text=col); tree.column(col, width=w, anchor="center")
        conn = get_connection()
        for i, r in enumerate(conn.execute("""
            SELECT username,total_posts,total_likes_received,total_comments_received,
                   total_engagement,follower_count,following_count
            FROM v_user_stats ORDER BY total_engagement DESC
        """), 1):
            medal = "🥇" if i==1 else "🥈" if i==2 else "🥉" if i==3 else str(i)
            tree.insert("","end",values=(medal,r[0],r[1],r[2],r[3],f"{r[4]:.1f}",r[5],r[6]))
        conn.close()

        # Tab 2 — Post Type Breakdown
        t2 = tk.Frame(nb, bg=BG); nb.add(t2, text="  📊 Post Types  ")
        cols2 = ("Type","Count","Avg Likes","Avg Comments","Avg Score")
        frame2, tree2 = build_treeview(t2, cols2, height=6)
        frame2.pack(fill="x", padx=8, pady=8)
        for col, w in zip(cols2,[80,60,90,110,90]):
            tree2.heading(col, text=col); tree2.column(col, width=w, anchor="center")
        conn = get_connection()
        for r in conn.execute("""
            SELECT p.post_type, COUNT(p.post_id),
                   ROUND(AVG(e.total_likes),2), ROUND(AVG(e.total_comments),2),
                   ROUND(AVG(e.engagement_score),2)
            FROM Posts p JOIN Engagement e ON p.post_id=e.post_id
            WHERE p.is_deleted=0 GROUP BY p.post_type ORDER BY 5 DESC
        """):
            tree2.insert("","end",values=r)

        # Tab 3 — Hashtag Stats
        nb.add(self._build_hashtag_tab(nb), text="  # Hashtags  ")

        # Tab 4 — User Spotlight
        t4 = tk.Frame(nb, bg=BG); nb.add(t4, text="  🔍 User Spotlight  ")
        self._build_user_spotlight(t4)
        conn.close()

    def _build_hashtag_tab(self, parent):
        tab = tk.Frame(parent, bg=BG)
        cols = ("Hashtag","Posts","Total Likes","Total Comments","Total Engagement")
        frame, tree = build_treeview(tab, cols, height=16)
        frame.pack(fill="both", expand=True, padx=8, pady=8)
        for col, w in zip(cols,[110,60,100,120,130]):
            tree.heading(col,text=col); tree.column(col,width=w,anchor="center")
        conn = get_connection()
        for r in conn.execute("""
            SELECT h.tag_name, COUNT(DISTINCT ph.post_id),
                   COALESCE(SUM(e.total_likes),0),
                   COALESCE(SUM(e.total_comments),0),
                   COALESCE(SUM(e.engagement_score),0.0)
            FROM Hashtags h
            JOIN Post_Hashtags ph ON h.hashtag_id=ph.hashtag_id
            JOIN Posts         p  ON ph.post_id=p.post_id
            JOIN Engagement    e  ON p.post_id=e.post_id
            GROUP BY h.tag_name ORDER BY 5 DESC
        """):
            tree.insert("","end", values=(r[0],r[1],r[2],r[3],f"{r[4]:.1f}"))
        conn.close()
        return tab

    def _build_user_spotlight(self, parent):
        row = tk.Frame(parent, bg=BG); row.pack(fill="x", padx=8, pady=8)
        tk.Label(row,text="Enter username: ",bg=BG,fg=TEXT,font=("Helvetica",10)).pack(side="left")
        self._spotlight_var = tk.StringVar()
        tk.Entry(row,textvariable=self._spotlight_var,bg=CARD,fg=TEXT,
                 insertbackground=TEXT,relief="flat",font=("Helvetica",10),
                 highlightbackground=BORDER,highlightthickness=1,width=20).pack(side="left",padx=6)
        styled_button(row,"Search",self._do_spotlight).pack(side="left")
        self._spotlight_frame = tk.Frame(parent,bg=BG)
        self._spotlight_frame.pack(fill="both",expand=True,padx=8,pady=4)

    def _do_spotlight(self):
        for w in self._spotlight_frame.winfo_children(): w.destroy()
        uname = self._spotlight_var.get().strip().lstrip("@")
        conn = get_connection()
        r = conn.execute("SELECT user_id FROM Users WHERE username=?",(uname,)).fetchone()
        conn.close()
        if not r:
            tk.Label(self._spotlight_frame,text=f"User @{uname} not found.",
                     bg=BG,fg=ACCENT2,font=("Helvetica",11)).pack(pady=20)
            return
        data = sp_user_engagement_summary(r[0])
        info = [
            ("Username",        "@" + data.get("username","")),
            ("Full Name",       data.get("full_name","")),
            ("Total Posts",     str(data.get("total_posts",0))),
            ("Likes Received",  str(data.get("total_likes",0))),
            ("Comments Received",str(data.get("total_comments",0))),
            ("Engagement Score",f'{data.get("engagement_score",0.0):.1f}'),
            ("Followers",       str(data.get("followers",0))),
            ("Following",       str(data.get("following",0))),
        ]
        c = card_frame(self._spotlight_frame)
        c.pack(fill="x",pady=4)
        grid = tk.Frame(c,bg=CARD); grid.pack(padx=16,pady=12)
        for i,(k,v) in enumerate(info):
            tk.Label(grid,text=k+":",bg=CARD,fg=TEXT_DIM,font=("Helvetica",9),
                     anchor="e",width=20).grid(row=i,column=0,sticky="e",pady=3)
            tk.Label(grid,text=v,bg=CARD,fg=TEXT,font=("Helvetica",10,"bold"),
                     anchor="w").grid(row=i,column=1,sticky="w",padx=10)

    # ── Page: SQL Explorer ───────────────────────────────────────────────────

    def _show_sql_explorer(self):
        self._clear_content()
        tk.Label(self.content, text="SQL Explorer", bg=BG, fg=TEXT,
                 font=("Helvetica",14,"bold")).pack(anchor="w", padx=24, pady=(20,10))

        top = card_frame(self.content)
        top.pack(fill="x", padx=20, pady=6)

        tk.Label(top, text="Enter SQL Query:", bg=CARD, fg=TEXT_DIM,
                 font=("Helvetica",9)).pack(anchor="w", padx=14, pady=(8,2))

        self._sql_editor = tk.Text(top, height=5, bg=BG, fg=SUCCESS,
                                    insertbackground=TEXT, relief="flat",
                                    font=("Courier",10),
                                    highlightbackground=BORDER, highlightthickness=1)
        self._sql_editor.pack(fill="x", padx=14, pady=4)
        self._sql_editor.insert("end",
            "SELECT u.username, p.content, e.total_likes, e.engagement_score\n"
            "FROM Posts p\n"
            "JOIN Users u ON p.user_id = u.user_id\n"
            "JOIN Engagement e ON p.post_id = e.post_id\n"
            "WHERE p.is_deleted = 0\n"
            "ORDER BY e.engagement_score DESC\n"
            "LIMIT 10;"
        )

        presets = [
            ("Top Liked Posts",
             "SELECT u.username,p.content,e.total_likes FROM Posts p\nJOIN Users u ON p.user_id=u.user_id\nJOIN Engagement e ON p.post_id=e.post_id\nWHERE p.is_deleted=0 ORDER BY e.total_likes DESC LIMIT 10;"),
            ("Follower Leaders",
             "SELECT u.username,COUNT(*) as followers FROM Followers f\nJOIN Users u ON f.following_id=u.user_id\nGROUP BY u.user_id ORDER BY followers DESC LIMIT 10;"),
            ("Hashtag Stats",
             "SELECT h.tag_name,COUNT(DISTINCT ph.post_id) as posts FROM Hashtags h\nJOIN Post_Hashtags ph ON h.hashtag_id=ph.hashtag_id\nGROUP BY h.tag_name ORDER BY posts DESC;"),
            ("Avg-Breaking Posts",
             "SELECT u.username,p.content,e.total_likes FROM Posts p\nJOIN Users u ON p.user_id=u.user_id\nJOIN Engagement e ON p.post_id=e.post_id\nWHERE e.total_likes>(SELECT AVG(total_likes) FROM Engagement)\nORDER BY e.total_likes DESC;"),
        ]
        pbf = tk.Frame(top, bg=CARD); pbf.pack(fill="x", padx=14, pady=(4,10))
        tk.Label(pbf, text="Quick:", bg=CARD, fg=TEXT_DIM, font=("Helvetica",8)).pack(side="left")
        for name, sql in presets:
            styled_button(pbf, name,
                          lambda s=sql: (self._sql_editor.delete("1.0","end"),
                                         self._sql_editor.insert("end",s)),
                          color=BORDER).pack(side="left", padx=3)

        styled_button(top, "  ▶  Run Query  ", self._do_run_sql, color=SUCCESS).pack(pady=(0,12))

        self._sql_result_frame = tk.Frame(self.content, bg=BG)
        self._sql_result_frame.pack(fill="both", expand=True, padx=20, pady=4)

    def _do_run_sql(self):
        for w in self._sql_result_frame.winfo_children(): w.destroy()
        sql = self._sql_editor.get("1.0","end-1c").strip()
        if not sql: return
        try:
            conn = get_connection()
            cur  = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description] if cur.description else []
            conn.close()

            if not cols:
                tk.Label(self._sql_result_frame, text="Query executed successfully (no results).",
                         bg=BG, fg=SUCCESS, font=("Helvetica",10)).pack(pady=10)
                return

            tk.Label(self._sql_result_frame,
                     text=f"✅  {len(rows)} row(s) returned",
                     bg=BG, fg=SUCCESS, font=("Helvetica",9)).pack(anchor="w", pady=(0,4))

            frame, tree = build_treeview(self._sql_result_frame, cols, height=14)
            frame.pack(fill="both", expand=True)
            for col in cols:
                tree.heading(col, text=col)
                tree.column(col, width=120, anchor="w")
            for row in rows:
                tree.insert("","end", values=[str(v) if v is not None else "NULL" for v in row])

        except Exception as e:
            tk.Label(self._sql_result_frame, text=f"❌  Error: {e}",
                     bg=BG, fg=ACCENT2, font=("Helvetica",10),
                     wraplength=700, justify="left").pack(anchor="w", pady=10)


# ── Entry point ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()
