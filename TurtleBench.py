# MISSION: Create a split-screen editor + emulator for Turtle Graphics
# STATUS: Alpha release
# VERSION: 2026.08.24
# NOTES: Looks good!
# DATE: 2026-08-23 05:32:42
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

RUN_DIRTY  = 9
STOP_DIRTY = 8
RUN_SEEN  = 1
STOP_SEEN = 3

class Screen9000(turtle.TurtleScreen):
    ''' A place to add experience enhancers '''
    def __init__(self, cv, mode='standard', colormode=1.0, delay=10):
        self._running = STOP_DIRTY
        super().__init__(cv, mode, colormode, delay)

    def _update(self):
        # ... we've other things planned ...
        super()._update()

class Bot9000(turtle.RawTurtle):
    ''' A place to add framework enhancements '''
    def __init__(self, canvas=None, shape='classic', undobuffersize=1000, visible=True):
        self.callback = None
        super().__init__(canvas, shape, undobuffersize, visible)

    def _set_notify(self, callback):
        ''' The way to signal state changes. '''
        self.callback = callback

    def run(self, run=True):
        ''' Classic mnemonics - easier for some to remember. '''
        if run:
            self.getscreen()._running = RUN_DIRTY
        else:
            self.getscreen()._running = STOP_DIRTY
        if self.callback:
            self.callback()

    def _state(self, which = None)->int:
        ''' Manage the 'dirty' state. Returns the present state
        by default, else returns previous state when changing. '''
        if not which:
            return self.getscreen()._running
        state = self.getscreen()
        prev = state._running
        state._running = which
        return prev
        
    def is_running(self)->bool:
        ''' See if THE USER is running anything. '''
        state = self._state()
        return (state == RUN_SEEN) or (state == RUN_DIRTY)

    def is_seen(self)->bool:
        state = self._state()
        return (state == RUN_SEEN) or (state == STOP_SEEN)

    def is_dirty(self)->bool:
        state = self._state()
        return (state == RUN_DIRTY) or (state == STOP_DIRTY)
    
    def showrun(self):
        ''' Show -n- Tell what YOUR state is. '''
        state = '' if self.is_running() else 'not '
        messagebox.showinfo("Run State", f"{id(self)} is {state}running.")


class SplitScreenEditor:
    def __init__(self, root):
        self.root = root
        self.in_service = tk.BooleanVar(value=False)
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
        tk.Button(self.button_frame, text="ℹ ABOUT", command=self.show_about_art, bg="#6c5ce7", fg="white", font=("Arial", 10, "bold"), bd=0, padx=4).pack(side=tk.LEFT, padx=2, pady=8)
        self.run_button = tk.Button(
            self.button_frame,
            text="▶ RUN",
            command=self.run_code_pressed,
            bg="#007acc",
            fg="white",
            font=("Arial", 11, "bold"), bd=0, padx=10, pady=4)
        self.run_button.pack(side=tk.RIGHT, padx=6, pady=8)

        # Editor Frame Space Input
        self.editor_frame = tk.Frame(root, bg="#1e1e1e")
        self.editor_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.code_text = tk.Text(self.editor_frame, wrap=tk.WORD, bg="#1e1e1e", fg="#d4d4d4", insertbackground="white", font=("Consolas", self.current_font_size), bd=0, padx=10, pady=10)
        self.code_text.pack(fill=tk.BOTH, expand=True)

        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-o>", lambda e: self.open_file())

        # Inject Default Start Script
        self.code_text.insert(tk.END, "t.speed(0)\nt.pencolor('cyan')\nt.width(2)\n\nfor i in range(120):\n    t.forward(i)\n    t.left(91)\n")
        self.t._set_notify(self.do_notify)

    def do_notify(self):
        self.AFTER(500, self.run_code_pressed)

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

    def run_code_pressed(self):
        self.run_button.config(state="disabled")
        self.turtle_screen.clear(); self.turtle_screen.bgcolor("black")
        self.t.clear()
        self.t.hideturtle()
        del self.t        
        self.t = Bot9000(self.turtle_screen); self.t.hideturtle()
        self.AFTER(500, self.__toggle_run_state)
           
    def __show_run_state(self):
        if self.t.is_running():
            self.t._state(RUN_SEEN) # WE ARE RUNNING
            self.run_button.config(state="disabled") 
        else:
            self.t._state(STOP_SEEN)# WE ARE NOT RUNNING
            self.run_button.config(state="normal")
            
    def __toggle_run_state(self):
        if self.t.is_running():
            self.t._state(STOP_DIRTY)
            self.AFTER(500, self.__show_run_state)
        else:
            self.t._state(RUN_DIRTY)
            self.AFTER(500, self.__run_the_code)
        
    def __run_the_code(self):
        try:
            self.in_service.set(True)
            exec(self.code_text.get("1.0", tk.END), {}, {"t": self.t, 'root': self.root})
            self.in_service.set(False)
        except KeyboardInterrupt as ex:
            messagebox.showinfo("Stop", "Run Terminated")
        except Exception as ex:
            messagebox.showinfo("Error", ex)
        self.AFTER(500, self.__toggle_run_state())

    def show_about_art(self):
        self.turtle_screen.clear(); self.turtle_screen.bgcolor("black")
        w = turtle.RawTurtle(self.turtle_screen); w.hideturtle(); w.speed(0); w.penup()
        w.goto(-2, 42); w.color("#ff5ce7"); w.write(ZNAME, align="center", font=("Consolas", 20, "bold"))
        w.goto(0, 40); w.color("#6c5ce7"); w.write(ZNAME, align="center", font=("Consolas", 20, "bold"))
        w.goto(0, 0); w.color("white"); w.write(ZVERSION, align="center", font=("Consolas", 12))
        w.goto(-2, 82); w.color("gray"); w.write(ZAUTHOR, align="center", font=("Stencil", 24))
        w.goto(0, 80); w.color("blue"); w.write(ZAUTHOR, align="center", font=("Stencil", 24))

    def AFTER(self, a, b):
        if not self.in_service.get():
            self.root.after(a, b)

    def on_closing(self):
        #self.root.wait_variable(self.in_service)
        if self.in_service.get():
            self.root.after(1000, self.on_closing)
        else:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SplitScreenEditor(root)
    try:
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        roow.mainloop()
    except:
        pass

