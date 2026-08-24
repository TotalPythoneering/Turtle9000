# MISSION: Create a split screen editor + emulator for Turtle Graphics
# STATUS: R&D
# VERSION: 2026.08.22
# NOTES: Needs exit & support for programatic 'ops.
# DATE: 2026-08-22 20:40:45
# FILE: TurtleBench.py
# AUTHOR: Total Pythoneering
#
import tkinter as tk
from tkinter import messagebox, filedialog
import turtle
import os

ZNAME       = "WARP SPEED"
ZVERSION    = "Turtle9000 v1.5.0"
ZAUTHOR     = "TOTAL PYTHONEERING"

class Screen9000(turtle.TurtleScreen):
    def __init__(self, cv, mode='standard', colormode=1.0, delay=10):
        self.running = False
        super().__init__(cv, mode, colormode, delay)

    def _update(self):
        if self.running:
            print('.')
        super()._update()

class Bot9000(turtle.RawTurtle):
    def __init__(self, canvas=None, shape='classic', undobuffersize=1000, visible=True):
        super().__init__(canvas, shape, undobuffersize, visible)

    def run(self, run=True):
        if run:
            self.start()
        else:
            self.stop()

    def start(self):
        self.getscreen().running = True

    def stop(self):
        self.getscreen().running = False

    def running(self):
        return self.getscreen().running

    def is_running(self):
        state = '' if self.getscreen().running else 'not '
        messagebox.showinfo("is_running", f"{id(self)} is {state}running.")



class SplitScreenEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Workbench")
        self.root.geometry("500x800")
        self.root.configure(bg="#1e1e1e")

        self.current_font_size = 14
        self.current_filepath = None

        # Canvas for Drawing Artwork
        self.canvas_frame = tk.Frame(root, width=500, height=400, bg="black")
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, width=500, height=400, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.turtle_screen = Screen9000(self.canvas)
        self.turtle_screen.bgcolor("black")
        self.t = Bot9000(self.turtle_screen)
        self.t.hideturtle()
        # Control Buttons Bar Row
        self.button_frame = tk.Frame(root, bg="#2d2d2d", height=45)
        self.button_frame.pack(side=tk.TOP, fill=tk.X)

        # Utility Buttons Pack Layout
        tk.Button(self.button_frame, text=" A − ", command=self.decrease_font, bg="#3e3e42", fg="white", font=("Arial", 10, "bold"), bd=0, padx=4).pack(side=tk.LEFT, padx=(6,2), pady=8)
        tk.Button(self.button_frame, text=" A + ", command=self.increase_font, bg="#3e3e42", fg="white", font=("Arial", 10, "bold"), bd=0, padx=4).pack(side=tk.LEFT, padx=2, pady=8)
        tk.Button(self.button_frame, text="📁 OPEN", command=self.open_file, bg="#3a3a3a", fg="white", font=("Arial", 10, "bold"), bd=0, padx=4).pack(side=tk.LEFT, padx=2, pady=8)
        tk.Button(self.button_frame, text="💾 SAVE", command=self.save_file, bg="#2d7d46", fg="white", font=("Arial", 10, "bold"), bd=0, padx=4).pack(side=tk.LEFT, padx=2, pady=8)
        tk.Button(self.button_frame, text="📋 COPY", command=self.copy_to_clipboard, bg="#d24d57", fg="white", font=("Arial", 10, "bold"), bd=0, padx=4).pack(side=tk.LEFT, padx=2, pady=8)
        tk.Button(self.button_frame, text="ℹ️ ABOUT", command=self.show_about_art, bg="#6c5ce7", fg="white", font=("Arial", 10, "bold"), bd=0, padx=4).pack(side=tk.LEFT, padx=2, pady=8)
        tk.Button(self.button_frame, text="▶ RUN", command=self.run_code, bg="#007acc", fg="white", font=("Arial", 11, "bold"), bd=0, padx=10, pady=4).pack(side=tk.RIGHT, padx=6, pady=8)

        # Editor Frame Space Input
        self.editor_frame = tk.Frame(root, bg="#1e1e1e")
        self.editor_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.code_text = tk.Text(self.editor_frame, wrap=tk.WORD, bg="#1e1e1e", fg="#d4d4d4", insertbackground="white", font=("Consolas", self.current_font_size), bd=0, padx=10, pady=10)
        self.code_text.pack(fill=tk.BOTH, expand=True)

        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-o>", lambda e: self.open_file())

        # Inject Default Start Script
        self.code_text.insert(tk.END, "t.speed(0)\nt.pencolor('cyan')\nt.width(2)\n\nfor i in range(120):\n    t.forward(i)\n    t.left(91)\n")

    def increase_font(self):
        if self.current_font_size < 40: self.current_font_size += 2; self.code_text.configure(font=("Consolas", self.current_font_size))

    def decrease_font(self):
        if self.current_font_size > 8: self.current_font_size -= 2; self.code_text.configure(font=("Consolas", self.current_font_size))

    def copy_to_clipboard(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.code_text.get("1.0", tk.END).strip())
        messagebox.showinfo("Clipboard", "Code Copied!")

    def open_file(self):
        fp = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if fp:
            with open(fp, "r") as f: self.code_text.delete("1.0", tk.END); self.code_text.insert(tk.END, f.read())
            self.current_filepath = fp; self.root.title(f"Editor — {os.path.basename(fp)}")

    def save_file(self):
        self.current_filepath = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py")])
        if self.current_filepath:
            with open(self.current_filepath, "w") as f:
                f.write(self.code_text.get("1.0", tk.END))
            self.root.title(f"Editor — {os.path.basename(self.current_filepath)}")

    def run_code(self):
        self.turtle_screen.clear(); self.turtle_screen.bgcolor("black")
        self.t = Bot9000(self.turtle_screen); self.t.hideturtle()
        try:
            exec(self.code_text.get("1.0", tk.END), {}, {"t": self.t, 'root': self.root})
            self.t.start()
        except KeyboardInterrupt as ex:
            messagebox.showinfo("Stop", "Run Terminated")
        except Exception as ex:
            messagebox.showinfo("Error", ex)

    def show_about_art(self):
        self.turtle_screen.clear(); self.turtle_screen.bgcolor("black")
        w = turtle.RawTurtle(self.turtle_screen); w.hideturtle(); w.speed(0); w.penup()
        w.goto(-2, 42); w.color("#ff5ce7"); w.write(ZNAME, align="center", font=("Consolas", 20, "bold"))
        w.goto(0, 40); w.color("#6c5ce7"); w.write(ZNAME, align="center", font=("Consolas", 20, "bold"))
        w.goto(0, 0); w.color("white"); w.write(ZVERSION, align="center", font=("Consolas", 12))
        w.goto(-2, 82); w.color("gray"); w.write(ZAUTHOR, align="center", font=("Stencil", 24))
        w.goto(0, 80); w.color("blue"); w.write(ZAUTHOR, align="center", font=("Stencil", 24))

if __name__ == "__main__":
    window = tk.Tk()
    app = SplitScreenEditor(window)
    window.mainloop()

