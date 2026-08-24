# 🏅Turtle9000
A free &amp; open graphical programming environment for Pythoneers, **Turtle9000** sports a split-screen editor and emulator combination designed to supercharge our Turtle Graphics demonstrations. 

The full set of programming buttons (Open, Save, Copy, Run) permits the sharing, execution as well as real-time reviewing of professional, pragmatic Pythoneering 'ponderables.

## Overview

**Turtle9000** bridges the gap between coding and execution by providing a real-time, split-screen environment specifically optimized for Python's standard `turtle` graphics. Built on top of customized Tkinter and Turtle abstractions, it provides enhanced state management and framework extensions to track execution conditions seamlessly. The **split-screen interface** permits 'Pythoneers to write code and view visual execution with a touch of a button.

# 🏅Lessons
We'll be sharing a complete set of programs, demonstrations &amp; lessons on [rumble](https://rumble.com/user/Nagy9000) soon. Stay tuned?

## Geeky Details
Managing long-winded executions of our programs was not an easy operation - at the time of this crafting even A.I was not able to get there, so we've checked in the three-step saga for your educational enjoyment. 😇

### Main Classes
*   **`Screen9000(cv)`**: Extends the default Turtle canvas screen layer, ready for custom update cycles.
*   **`Bot9000(canvas)`**: The primary actor class. 
    *   `_set_notify(callback)`: Registers a function to fire on state alterations.
    *   `run(bool)`: Helper mnemonic to quickly switch between execution flags.
    *   `_state(which)`: Internal state machine switcher.
    *   `is_running()`: Returns a boolean indicating if active rendering tasks exist.
