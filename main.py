from tkinter import *
from tkinter import ttk, messagebox

# ---------------- ROOT ----------------
root = Tk()
root.title("Optimal Caching Algorithm Visualizer")
root.attributes('-fullscreen', True)
root.configure(bg="#1E1E2E")


# ---------------- STYLES ----------------
style = ttk.Style()
style.theme_use("clam")
style.configure("Big.TButton", font=("Segoe UI", 12), padding=10,foreground="#1E1E2E",background="#7AA2F7")
style.configure("TLabel", background="#1E1E2E", foreground="white")
style.configure("Exit.TButton", foreground="#FF0000",font=("Segoe UI", 10), padding=8)
style.configure("Next.TButton", font=("Segoe UI", 10), padding=8)
# ---------------- TITLE ----------------
welcome = ttk.Label(root, text="Welcome to the Optimal Caching Algorithm Visualizer",
     font=("Segoe UI", 34, "bold"),
    foreground="#7AA2F7")

welcome.pack(pady=(30, 10))

subtitle = ttk.Label(
    root,
    text="Greedy Replacement Visualization",
    font=("Segoe UI", 16),
    foreground="#A9B1D6"
)
subtitle.pack(pady=(0, 30))

# ---------------- GLOBAL ----------------

canvas = None
RECT_SIZE = 75
MAX_RECTS = root.winfo_screenwidth() // RECT_SIZE - 2

to_replace = None
access_sequence = []
cache = {}
driver_index = 0
driver_arrow = None

hit_count = 0
hit_label = None

miss_count = 0
miss_label = None
    
# ---------------- DRAW FUNCTIONS ----------------

def draw_cache_list(cache):
    """Draw the cache boxes centered at the top."""
    global canvas
    x_offset = root.winfo_screenwidth() // 2 - (len(cache) * RECT_SIZE) // 2
    y_offset = 175

    canvas.create_text(x_offset - 60, y_offset + RECT_SIZE / 2,
                       text="Cache:", fill="white", font=("Segoe UI", 18, "bold"))
    
    temp = None
    for idx, c in enumerate(cache):
        x1 = x_offset + idx * RECT_SIZE
        x2 = x1 + RECT_SIZE
        y1 = y_offset
        y2 = y1 + RECT_SIZE
        canvas.create_rectangle(x1, y1, x2, y2, outline="white",width=3)
        canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=c, fill="white", font=("Segoe UI", 20))
        # draw cache element's LRU value above it
        canvas.create_text((x1 + x2) / 2, y1 - 15, text=f"freq={cache[c]}", fill="yellow", font=("Segoe UI", 12))
        if to_replace and c == to_replace[0]:
            temp = (x1, y1, x2, y2)
    if temp:
        canvas.create_rectangle(temp[0], temp[1], temp[2], temp[3], outline="red", width=3)


def draw_access_sequence(access):
    """Draw the access sequence centered lower on screen."""
    global canvas
    x_offset = root.winfo_screenwidth() // 2 - (len(access) * RECT_SIZE) // 2
    y_offset = 350

    canvas.create_text(x_offset - 120, y_offset + RECT_SIZE / 2,
                       text="Access Sequence:", fill="white", font=("Segoe UI", 18, "bold"))
    for idx, c in enumerate(access):
        x1 = x_offset + idx * RECT_SIZE
        x2 = x1 + RECT_SIZE
        y1 = y_offset
        y2 = y1 + RECT_SIZE
        canvas.create_rectangle(x1, y1, x2, y2, outline="#7AA2F7", width=3)
        canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=c, fill="#7AA2F7", font=("Segoe UI", 20))

def draw_driver(index):
    """Draw the arrow pointing to the current element in access sequence."""
    global canvas, access_sequence, driver_arrow
    global hit_count, hit_label
    global miss_count, miss_label
    global cache
    global to_replace

    if driver_arrow:
        canvas.delete(driver_arrow)

    if index >= len(access_sequence):
        return

    x_offset = root.winfo_screenwidth() // 2 - (len(access_sequence) * RECT_SIZE) // 2
    box_x = x_offset + index * RECT_SIZE + RECT_SIZE // 2
    arrow_y = 320

    # Hit check
    if access_sequence[index] in cache:
        color = "#9ECE6A"
        cache[access_sequence[index]] += 1
        hit_count += 1
        hit_label.config(text=f"Hits: {hit_count}")
    else:
        # MISS case
        color = "#F7768E"
        miss_count += 1
        miss_label.config(text=f"Misses: {miss_count}")

        # OPTIMAL ALGORITHM to find the victim
        LRU_val = min(cache.values())

        # o(n)
        for i in cache:
            if(cache[i] == LRU_val):
                to_replace = (i, access_sequence[index])
                break
        # Redraw updated cache
        canvas.delete("all")
        draw_cache_list(cache)
        draw_access_sequence(access_sequence)

    driver_arrow = canvas.create_text(box_x, arrow_y, text="↓", fill=color, font=("Segoe UI", 30, "bold"))

# ---------------- LOGIC ----------------
def next_step():
    """Move the driver arrow 1 step to the right."""
    global driver_index, access_sequence, to_replace

    if to_replace:
        del cache[to_replace[0]]
        cache[to_replace[1]] = 0
        to_replace = None
        canvas.delete("all")
        draw_cache_list(cache)
        draw_access_sequence(access_sequence)
    elif driver_index < len(access_sequence):
        driver_index += 1
        draw_driver(driver_index)


def draw_lists(cache, access_sequence):
    global canvas
    canvas = Canvas(root, height=700, bg="#24283B", highlightthickness=0)
    canvas.pack(fill=BOTH, expand=True)

    draw_cache_list(cache)
    draw_access_sequence(access_sequence)
    # draw_driver(0)


# ---------------- INPUT UI ----------------
cache_input_label = ttk.Label(root, text="Enter cache elements:", font=("Segoe UI", 30))
cache_input_label.pack(pady=(150, 25))
cache_input = ttk.Entry(root, width=35)
cache_input.pack(pady=(5, 0))

access_input_label = ttk.Label(root, text="Enter your access sequence:", font=("Segoe UI", 30))
access_input_label.pack(pady=(40, 25))
access_input = ttk.Entry(root, width=35)
access_input.pack(pady=(5, 100))

# ---------------- START ----------------
def on_start_viz():
    global cache, access_sequence, cache_elements, access_sequence_elements
    global driver_index, hit_label, miss_label, miss_count

    cache_elements = cache_input.get()
    try:
        if len(cache_elements) <= 0 or len(cache_elements) > MAX_RECTS:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input",
                             f"Limit cache to between 1 and {MAX_RECTS} elements")
        return

    access_sequence_elements = access_input.get()
    try:
        if len(access_sequence_elements) <= 0 or len(access_sequence_elements) > MAX_RECTS:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input",
                             f"Limit access sequence to between 1 and {MAX_RECTS} elements")
        return

    # Create miss/hit labels
    miss_label = ttk.Label(root, text=f"Misses: {miss_count}", font=("Segoe UI", 20))
    miss_label.pack(pady=(10, 0))

    hit_label = ttk.Label(root, text=f"Hits: {hit_count}", font=("Segoe UI", 20))
    hit_label.pack(pady=(0, 10))

    
    # Remove init UI
    welcome.destroy()
    subtitle.destroy()
    cache_input_label.destroy()
    cache_input.destroy()
    access_input_label.destroy()
    access_input.destroy()
    start_button.destroy()

    # Init simulation
    cache = {c: 0 for c in cache_elements}
    access_sequence = list(access_sequence_elements)
    driver_index = -1

    exit_button = ttk.Button(root, text="Exit", command=root.destroy, style="Exit.TButton")
    exit_button.pack(side=BOTTOM, pady=(0, 8))

    step_button = ttk.Button(root, text="Next Step", command=next_step, style="Next.TButton")    
    step_button.pack(side=BOTTOM, pady=18)
    
    

    legend_label = ttk.Label(
    root,
    text="Legend: \nGreen ↓ = Hit \nRed ↓ = Miss \nRed Box = Evicted",
    font=("Segoe UI", 13),
    foreground="#A9B1D6",
    background="#1E1E2E"
    )
    legend_label.place(relx=0.93, rely=0.93, anchor="center")
    draw_lists(cache, access_sequence)


start_button = ttk.Button(root, text="Start Visualization", command=on_start_viz, style="Big.TButton")
start_button.pack(pady=(10, 40))


root.mainloop()
