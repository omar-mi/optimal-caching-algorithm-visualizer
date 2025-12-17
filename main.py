from tkinter import *
from tkinter import ttk, messagebox

root = Tk()
root.title("Optimal Caching Algorithm Visualizer")
root.attributes('-fullscreen', True)
welcome = ttk.Label(root, text="Welcome to the Optimal Caching Algorithm Visualizer", font=("Helvetica", 34))
welcome.pack(pady=20)

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
    
def draw_cache_list(cache):
    """Draw the cache boxes centered at the top."""
    global canvas
    x_offset = root.winfo_screenwidth() // 2 - (len(cache) * RECT_SIZE) // 2
    y_offset = 175

    canvas.create_text(x_offset - 50, y_offset + RECT_SIZE / 2,
                       text="Cache:", fill="white", font=("Helvetica", 18))
    
    temp = None
    for idx, c in enumerate(cache):
        x1 = x_offset + idx * RECT_SIZE
        x2 = x1 + RECT_SIZE
        y1 = y_offset
        y2 = y1 + RECT_SIZE
        canvas.create_rectangle(x1, y1, x2, y2, outline="white")
        canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=c, fill="white", font=("Helvetica", 20))
        # draw cache element's LRU value above it
        canvas.create_text((x1 + x2) / 2, y1 - 15, text=str(cache[c]), fill="yellow", font=("Helvetica", 14))
        if to_replace and c == to_replace[0]:
            temp = (x1, y1, x2, y2)
    if temp:
        canvas.create_rectangle(temp[0], temp[1], temp[2], temp[3], outline="red", width=3)


def draw_access_sequence(access):
    """Draw the access sequence centered lower on screen."""
    global canvas
    x_offset = root.winfo_screenwidth() // 2 - (len(access) * RECT_SIZE) // 2
    y_offset = 350

    canvas.create_text(x_offset - 100, y_offset + RECT_SIZE / 2,
                       text="Access Sequence:", fill="white", font=("Helvetica", 18))
    for idx, c in enumerate(access):
        x1 = x_offset + idx * RECT_SIZE
        x2 = x1 + RECT_SIZE
        y1 = y_offset
        y2 = y1 + RECT_SIZE
        canvas.create_rectangle(x1, y1, x2, y2, outline="lightblue")
        canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=c, fill="lightblue", font=("Helvetica", 20))

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
        color = "green"
        cache[access_sequence[index]] += 1
        hit_count += 1
        hit_label.config(text=f"Hits: {hit_count}")
    else:
        # write miss check here bby
        # MISS case
        color = "red"
        miss_count += 1
        miss_label.config(text=f"Misses: {miss_count}")

        # TODO: Apply OPTIMAL ALGORITHM to find the victim
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

    driver_arrow = canvas.create_text(box_x, arrow_y, text="↓", fill=color, font=("Helvetica", 30))


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
    canvas = Canvas(root, height=700, bg="#3F3F3F")
    canvas.pack(fill=BOTH, expand=True)

    draw_cache_list(cache)
    draw_access_sequence(access_sequence)
    # draw_driver(0)



cache_input_label = ttk.Label(root, text="Enter cache elements:", font=("Helvetica", 26))
cache_input_label.pack(pady=(150, 20))
cache_input = ttk.Entry(root, width=30)
cache_input.pack(pady=(5, 0))

access_input_label = ttk.Label(root, text="Enter your access sequence:", font=("Helvetica", 26))
access_input_label.pack(pady=(40, 20))
access_input = ttk.Entry(root, width=30)
access_input.pack(pady=(5, 20))


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
    miss_label = ttk.Label(root, text=f"Misses: {miss_count}", font=("Helvetica", 20))
    miss_label.pack(pady=(0, 10))

    hit_label = ttk.Label(root, text=f"Hits: {hit_count}", font=("Helvetica", 20))
    hit_label.pack(pady=(0, 10))

    # Remove init UI
    welcome.destroy()
    cache_input_label.destroy()
    cache_input.destroy()
    access_input_label.destroy()
    access_input.destroy()
    start_button.destroy()

    # Init simulation
    cache = {c: 0 for c in cache_elements}
    access_sequence = list(access_sequence_elements)
    driver_index = -1

    draw_lists(cache, access_sequence)

    step_button = ttk.Button(root, text="Next Step", command=next_step)
    step_button.pack(pady=20)


start_button = ttk.Button(root, text="Start Visualization", command=on_start_viz, style="Big.TButton")
start_button.pack(pady=(20, 60))
style = ttk.Style()
style.configure("Big.TButton", font=("Helvetica", 14))

root.mainloop()
