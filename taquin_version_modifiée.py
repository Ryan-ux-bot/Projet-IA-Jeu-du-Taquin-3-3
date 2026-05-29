"""
Jeu du Taquin 3×3 - Mini Projet IA
Algorithmes: DFS, BFS, DLS (Profondeur Limitée), A*
État initial: [[1,2,7],[8,5,0],[3,5,4]] (0 = case vide)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
import tracemalloc
import heapq
from collections import deque
import threading


ETAT_INITIAL = (1, 2, 3, 8, 6, 0, 7, 5, 4)   
ETAT_FINAL   = (1, 2, 3, 8, 0, 4, 7, 6, 5)


def position_vide(etat):
    """Retourne l'index de la case vide (0)."""
    return etat.index(0)

def transitions(etat):
    """Retourne la liste des états voisins accessibles."""
    voisins = []
    idx = position_vide(etat)
    row, col = divmod(idx, 3)
    moves = []
    if row > 0: moves.append(idx - 3)  # haut
    if row < 2: moves.append(idx + 3)  # bas
    if col > 0: moves.append(idx - 1)  # gauche
    if col < 2: moves.append(idx + 1)  # droite
    for new_idx in moves:
        lst = list(etat)
        lst[idx], lst[new_idx] = lst[new_idx], lst[idx]
        voisins.append(tuple(lst))
    return voisins

def est_final(etat):
    return etat == ETAT_FINAL

# --- HEURISTIQUE SIMPLIFIÉE ---
def h_mal_places(etat):
    """Heuristique : nombre de pièces mal placées (simple)."""
    return sum(1 for i, v in enumerate(etat) if v != 0 and v != ETAT_FINAL[i])

def reconstruire_chemin(parents, etat):
    chemin = []
    while etat is not None:
        chemin.append(etat)
        etat = parents.get(etat)
    chemin.reverse()
    return chemin


def dfs(depart=ETAT_INITIAL):
    """Recherche en profondeur d'abord (DFS)."""
    tracemalloc.start()
    t0 = time.perf_counter()

    free_nodes = [depart]
    closed_nodes = set()
    parents = {depart: None}
    generes = 0

    solution = None
    while free_nodes:
        node = free_nodes.pop()  # LIFO
        if node in closed_nodes:
            continue
        closed_nodes.add(node)

        if est_final(node):
            solution = node
            break

        for s in transitions(node):
            if s not in closed_nodes and s not in parents:
                parents[s] = node
                free_nodes.append(s)
                generes += 1

    elapsed = time.perf_counter() - t0
    _, mem_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    chemin = reconstruire_chemin(parents, solution) if solution else []
    return {
        "algo": "DFS (Profondeur)",
        "noeuds_generes": generes,
        "noeuds_visites": len(closed_nodes),
        "temps": elapsed,
        "memoire": mem_peak / 1024,
        "chemin": chemin,
        "found": solution is not None
    }


def bfs(depart=ETAT_INITIAL):
    """Recherche en largeur d'abord (BFS)."""
    tracemalloc.start()
    t0 = time.perf_counter()

    free_nodes = deque([depart])
    closed_nodes = set()
    parents = {depart: None}
    generes = 0

    solution = None
    while free_nodes:
        node = free_nodes.popleft()  # FIFO
        if node in closed_nodes:
            continue
        closed_nodes.add(node)

        if est_final(node):
            solution = node
            break

        for s in transitions(node):
            if s not in closed_nodes and s not in parents:
                parents[s] = node
                free_nodes.append(s)
                generes += 1

    elapsed = time.perf_counter() - t0
    _, mem_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    chemin = reconstruire_chemin(parents, solution) if solution else []
    return {
        "algo": "BFS (Largeur)",
        "noeuds_generes": generes,
        "noeuds_visites": len(closed_nodes),
        "temps": elapsed,
        "memoire": mem_peak / 1024,
        "chemin": chemin,
        "found": solution is not None
    }


def dls(depart=ETAT_INITIAL, L=3):
    """Recherche en profondeur limitée (DLS)."""
    tracemalloc.start()
    t0 = time.perf_counter()

    generes_total = 0
    visites_total = 0
    chemin_final = []
    found = False
    L_used = L

    while not found and L_used <= 50:
        stack = [(depart, 0, [depart])]
        closed = set()
        generes = 0

        while stack:
            node, depth, path = stack.pop()
            if node in closed:
                continue
            closed.add(node)

            if est_final(node):
                found = True
                chemin_final = path
                break

            if depth < L_used:
                for s in transitions(node):
                    if s not in closed:
                        stack.append((s, depth + 1, path + [s]))
                        generes += 1

        generes_total += generes
        visites_total += len(closed)

        if not found:
            L_used += 1

    elapsed = time.perf_counter() - t0
    _, mem_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "algo": f"DLS (Prof. Limitée L={L_used})",
        "noeuds_generes": generes_total,
        "noeuds_visites": visites_total,
        "temps": elapsed,
        "memoire": mem_peak / 1024,
        "chemin": chemin_final,
        "found": found,
        "L": L_used
    }


def astar(depart=ETAT_INITIAL):
    """Algorithme A* avec heuristique simplifiée (pièces mal placées)."""
    tracemalloc.start()
    t0 = time.perf_counter()

    g_score = {depart: 0}
    parents = {depart: None}
    h0 = h_mal_places(depart)
    heap = [(h0, 0, depart)]
    closed_nodes = set()
    generes = 0

    solution = None
    while heap:
        f, g, node = heapq.heappop(heap)
        if node in closed_nodes:
            continue
        closed_nodes.add(node)

        if est_final(node):
            solution = node
            break

        for s in transitions(node):
            if s in closed_nodes:
                continue
            new_g = g + 1
            if s not in g_score or new_g < g_score[s]:
                g_score[s] = new_g
                parents[s] = node
                h = h_mal_places(s) # Utilisation exclusive de l'heuristique simple
                heapq.heappush(heap, (new_g + h, new_g, s))
                generes += 1

    elapsed = time.perf_counter() - t0
    _, mem_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    chemin = reconstruire_chemin(parents, solution) if solution else []
    return {
        "algo": "A* (Mal placées)",
        "noeuds_generes": generes,
        "noeuds_visites": len(closed_nodes),
        "temps": elapsed,
        "memoire": mem_peak / 1024,
        "chemin": chemin,
        "found": solution is not None
    }



# ─────────────────────────────────────────────
#  INTERFACE GRAPHIQUE
# ─────────────────────────────────────────────

COLORS = {
    "bg":       "#0f172a",
    "panel":    "#1e293b",
    "card":     "#334155",
    "tile":     "#3b82f6",
    "tile_fg":  "#ffffff",
    "empty":    "#1e3a5f",
    "accent":   "#38bdf8",
    "accent2":  "#f59e0b",
    "text":     "#f1f5f9",
    "subtext":  "#94a3b8",
    "success":  "#22c55e",
    "danger":   "#ef4444",
    "btn_dfs":  "#7c3aed",
    "btn_bfs":  "#0ea5e9",
    "btn_dls":  "#f59e0b",
    "btn_ast":  "#22c55e",
}


class TaquinApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Jeu du Taquin 3×3 – Mini Projet IA")
        self.configure(bg=COLORS["bg"])
        self.resizable(True, True)
        self.geometry("980x700")

        self.current_state = list(ETAT_INITIAL)
        self.solution_path = []
        self.anim_index = 0
        self.anim_running = False
        self.results = {}

        self._build_ui()
        self._draw_board(self.current_state)

    # ── UI CONSTRUCTION ──────────────────────

    def _build_ui(self):
        # ── Title bar
        title_bar = tk.Frame(self, bg=COLORS["bg"])
        title_bar.pack(fill="x", padx=20, pady=(18, 0))

        tk.Label(title_bar, text="🧩", font=("Segoe UI Emoji", 22),
                 bg=COLORS["bg"], fg=COLORS["accent"]).pack(side="left")
        tk.Label(title_bar, text="  Jeu du Taquin 3×3",
                 font=("Georgia", 22, "bold"),
                 bg=COLORS["bg"], fg=COLORS["text"]).pack(side="left")
        tk.Label(title_bar, text="   Mini Projet IA – Fondements de l'Intelligence Artificielle",
                 font=("Helvetica", 10),
                 bg=COLORS["bg"], fg=COLORS["subtext"]).pack(side="left", pady=6)

        # ── Main layout
        main = tk.Frame(self, bg=COLORS["bg"])
        main.pack(fill="both", expand=True, padx=20, pady=12)

        # Left panel
        left = tk.Frame(main, bg=COLORS["bg"])
        left.pack(side="left", fill="y", padx=(0, 16))

        self._build_board_panel(left)
        self._build_controls(left)

        # Right panel
        right = tk.Frame(main, bg=COLORS["bg"])
        right.pack(side="left", fill="both", expand=True)

        self._build_results_panel(right)
        self._build_stats_table(right)

    def _build_board_panel(self, parent):
        card = tk.Frame(parent, bg=COLORS["panel"], bd=0, relief="flat")
        card.pack(pady=(0, 12), ipadx=16, ipady=12)

        tk.Label(card, text="État courant", font=("Helvetica", 11, "bold"),
                 bg=COLORS["panel"], fg=COLORS["accent"]).pack(pady=(4, 8))

        self.board_frame = tk.Frame(card, bg=COLORS["panel"])
        self.board_frame.pack()

        self.cells = []
        for i in range(9):
            lbl = tk.Label(self.board_frame, text="", width=4, height=2,
                           font=("Georgia", 24, "bold"),
                           relief="flat", bd=0)
            lbl.grid(row=i//3, column=i%3, padx=4, pady=4)
            self.cells.append(lbl)

        # Step counter
        self.step_var = tk.StringVar(value="Étape 0 / 0")
        tk.Label(card, textvariable=self.step_var,
                 font=("Helvetica", 10), bg=COLORS["panel"],
                 fg=COLORS["subtext"]).pack(pady=(6, 2))

        # Animation speed
        spd_frame = tk.Frame(card, bg=COLORS["panel"])
        spd_frame.pack(pady=4)
        tk.Label(spd_frame, text="Vitesse :", font=("Helvetica", 9),
                 bg=COLORS["panel"], fg=COLORS["subtext"]).pack(side="left")
        self.speed_var = tk.IntVar(value=300)
        tk.Scale(spd_frame, from_=50, to=1000, orient="horizontal",
                 variable=self.speed_var, length=110, bg=COLORS["panel"],
                 fg=COLORS["text"], troughcolor=COLORS["card"],
                 highlightthickness=0, showvalue=False).pack(side="left")

    def _build_controls(self, parent):
        card = tk.Frame(parent, bg=COLORS["panel"], bd=0)
        card.pack(ipadx=16, ipady=10)

        tk.Label(card, text="Algorithmes", font=("Helvetica", 11, "bold"),
                 bg=COLORS["panel"], fg=COLORS["accent"]).pack(pady=(4, 8))

        btns = [
            ("⬇  Profondeur (DFS)",   COLORS["btn_dfs"], self._run_dfs),
            ("↔  Largeur (BFS)",       COLORS["btn_bfs"], self._run_bfs),
            ("⬇⚡ Prof. Limitée (DLS)", COLORS["btn_dls"], self._run_dls),
            ("★  A*",                  COLORS["btn_ast"], self._run_astar),
        ]
        for txt, color, cmd in btns:
            b = tk.Button(card, text=txt, command=cmd,
                          bg=color, fg="white",
                          font=("Helvetica", 10, "bold"),
                          relief="flat", bd=0, cursor="hand2",
                          activebackground=color, activeforeground="white",
                          padx=12, pady=7)
            b.pack(fill="x", pady=3, padx=8)

        sep = tk.Frame(card, bg=COLORS["card"], height=1)
        sep.pack(fill="x", padx=8, pady=8)

        nav_frame = tk.Frame(card, bg=COLORS["panel"])
        nav_frame.pack()

        self.prev_btn = tk.Button(nav_frame, text="◀ Préc", command=self._prev_step,
                                  bg=COLORS["card"], fg=COLORS["text"],
                                  font=("Helvetica", 9), relief="flat",
                                  padx=8, pady=5, cursor="hand2")
        self.prev_btn.pack(side="left", padx=4)

        self.play_btn = tk.Button(nav_frame, text="▶ Jouer", command=self._play_anim,
                                  bg=COLORS["accent"], fg=COLORS["bg"],
                                  font=("Helvetica", 9, "bold"), relief="flat",
                                  padx=8, pady=5, cursor="hand2")
        self.play_btn.pack(side="left", padx=4)

        self.next_btn = tk.Button(nav_frame, text="Suiv ▶", command=self._next_step,
                                  bg=COLORS["card"], fg=COLORS["text"],
                                  font=("Helvetica", 9), relief="flat",
                                  padx=8, pady=5, cursor="hand2")
        self.next_btn.pack(side="left", padx=4)

        tk.Button(card, text="↺ Réinitialiser", command=self._reset,
                  bg=COLORS["card"], fg=COLORS["subtext"],
                  font=("Helvetica", 9), relief="flat",
                  padx=8, pady=5, cursor="hand2").pack(pady=(8, 2))

    def _build_results_panel(self, parent):
        card = tk.Frame(parent, bg=COLORS["panel"], bd=0)
        card.pack(fill="x", pady=(0, 12), ipadx=12, ipady=10)

        tk.Label(card, text="Résultats", font=("Helvetica", 11, "bold"),
                 bg=COLORS["panel"], fg=COLORS["accent"]).pack(anchor="w", padx=8, pady=(4, 6))

        self.result_text = tk.Text(card, height=4, bg=COLORS["bg"],
                                   fg=COLORS["text"], font=("Consolas", 10),
                                   relief="flat", bd=0, state="disabled",
                                   wrap="word")
        self.result_text.pack(fill="x", padx=8, pady=(0, 4))

        # Progress bar
        self.progress = ttk.Progressbar(card, mode="indeterminate", length=300)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TProgressbar", troughcolor=COLORS["card"],
                        background=COLORS["accent"])
        self.progress.pack(padx=8, pady=2, fill="x")
        self.progress.stop()

    def _build_stats_table(self, parent):
        card = tk.Frame(parent, bg=COLORS["panel"], bd=0)
        card.pack(fill="both", expand=True, ipadx=12, ipady=10)

        tk.Label(card, text="Comparaison des algorithmes",
                 font=("Helvetica", 11, "bold"),
                 bg=COLORS["panel"], fg=COLORS["accent"]).pack(anchor="w", padx=8, pady=(4, 6))

        cols = ["Algorithme", "Nœuds générés", "Nœuds visités",
                "Temps (s)", "Mémoire (KB)", "Solution"]
        self.tree = ttk.Treeview(card, columns=cols, show="headings", height=6)

        style = ttk.Style()
        style.configure("Treeview",
                        background=COLORS["bg"],
                        foreground=COLORS["text"],
                        fieldbackground=COLORS["bg"],
                        rowheight=28,
                        font=("Consolas", 9))
        style.configure("Treeview.Heading",
                        background=COLORS["card"],
                        foreground=COLORS["accent"],
                        font=("Helvetica", 9, "bold"))
        style.map("Treeview", background=[("selected", COLORS["tile"])])

        for c in cols:
            w = 140 if c == "Algorithme" else 110
            self.tree.heading(c, text=c)
            self.tree.column(c, width=w, anchor="center")

        self.tree.tag_configure("found", foreground=COLORS["success"])
        self.tree.tag_configure("nfound", foreground=COLORS["danger"])

        scrollbar = ttk.Scrollbar(card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=(8, 0))
        scrollbar.pack(side="left", fill="y")

    # ── BOARD DRAWING ─────────────────────────

    def _draw_board(self, state):
        for i, val in enumerate(state):
            if val == 0:
                self.cells[i].config(text="", bg=COLORS["empty"],
                                     fg=COLORS["text"])
            else:
                self.cells[i].config(text=str(val), bg=COLORS["tile"],
                                     fg=COLORS["tile_fg"])

    # ── ALGORITHM RUNNERS ─────────────────────

    def _run_algo(self, fn, label):
        if self.anim_running:
            return
        self._set_result_text(f"⏳ Exécution de {label}...")
        self.progress.start(10)

        def worker():
            result = fn()
            self.after(0, lambda: self._on_result(result))

        threading.Thread(target=worker, daemon=True).start()

    def _run_dfs(self):   self._run_algo(dfs,   "DFS")
    def _run_bfs(self):   self._run_algo(bfs,   "BFS")
    def _run_dls(self):   self._run_algo(lambda: dls(L=3), "DLS")
    def _run_astar(self): self._run_algo(astar, "A*")

    def _on_result(self, result):
        self.progress.stop()
        self.results[result["algo"]] = result
        self._update_table()

        if result["found"]:
            self.solution_path = result["chemin"]
            self.anim_index = 0
            self._draw_board(self.solution_path[0])
            self.step_var.set(f"Étape 1 / {len(self.solution_path)}")
            info = (
                f"✅ {result['algo']} — Solution trouvée !\n"
                f"   Longueur du chemin : {len(result['chemin'])-1} mouvements\n"
                f"   Nœuds générés : {result['noeuds_generes']}  |  "
                f"Nœuds visités : {result['noeuds_visites']}\n"
                f"   Temps : {result['temps']:.4f}s  |  "
                f"Mémoire : {result['memoire']:.1f} KB"
            )
        else:
            info = f"❌ {result['algo']} — Solution non trouvée."

        self._set_result_text(info)

    def _update_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for algo, r in self.results.items():
            tag = "found" if r["found"] else "nfound"
            sol = f"{len(r['chemin'])-1} mvts" if r["found"] else "—"
            self.tree.insert("", "end", values=(
                r["algo"],
                r["noeuds_generes"],
                r["noeuds_visites"],
                f"{r['temps']:.4f}",
                f"{r['memoire']:.1f}",
                sol
            ), tags=(tag,))

    def _set_result_text(self, txt):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert("end", txt)
        self.result_text.config(state="disabled")

    # ── ANIMATION ────────────────────────────

    def _play_anim(self):
        if not self.solution_path:
            messagebox.showinfo("Info", "Lancez d'abord un algorithme.")
            return
        if self.anim_running:
            self.anim_running = False
            self.play_btn.config(text="▶ Jouer")
            return
        self.anim_running = True
        self.play_btn.config(text="⏸ Pause")
        self._animate()

    def _animate(self):
        if not self.anim_running or self.anim_index >= len(self.solution_path):
            self.anim_running = False
            self.play_btn.config(text="▶ Jouer")
            return
        state = self.solution_path[self.anim_index]
        self._draw_board(state)
        self.step_var.set(f"Étape {self.anim_index+1} / {len(self.solution_path)}")
        self.anim_index += 1
        self.after(self.speed_var.get(), self._animate)

    def _prev_step(self):
        if self.solution_path and self.anim_index > 1:
            self.anim_index -= 1
            self._draw_board(self.solution_path[self.anim_index - 1])
            self.step_var.set(f"Étape {self.anim_index} / {len(self.solution_path)}")

    def _next_step(self):
        if self.solution_path and self.anim_index < len(self.solution_path):
            self._draw_board(self.solution_path[self.anim_index])
            self.step_var.set(f"Étape {self.anim_index+1} / {len(self.solution_path)}")
            self.anim_index += 1

    def _reset(self):
        self.anim_running = False
        self.solution_path = []
        self.anim_index = 0
        self.current_state = list(ETAT_INITIAL)
        self._draw_board(self.current_state)
        self.step_var.set("Étape 0 / 0")
        self._set_result_text("Prêt. Choisissez un algorithme.")
        self.play_btn.config(text="▶ Jouer")


# ─────────────────────────────────────────────
#  ENTRÉE PRINCIPALE
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = TaquinApp()
    app.mainloop()