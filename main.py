from tkinter import *
from tkinter import ttk, messagebox
root = Tk()
root.title("Optimal Caching Algorithm Visualizer")
root.attributes('-fullscreen', True)

welcome = ttk.Label(root, text="Welcome to the Optimal Caching Algorithm Visualizer", font=("Helvetica", 24))
welcome.pack(pady=20)

canvas = None
RECT_SIZE = 75
MAX_RECTS = root.winfo_screenwidth() // RECT_SIZE - 2

cache_input_label = ttk.Label(root, text="Enter cache size:", font=("Helvetica", 16))
cache_input_label.pack(pady=(20, 0))
cache_input = ttk.Entry(root, width=10)
cache_input.pack(pady=(5, 0))

access_input_label = ttk.Label(root, text="Enter number access sequence size:", font=("Helvetica", 16))
access_input_label.pack(pady=(20, 0))
access_input = ttk.Entry(root, width=10)
access_input.pack(pady=(5, 0))

def random_char_list(n):
    import random
    import string
    return [random.choice(string.ascii_uppercase) for _ in range(n)]

def draw_lists(cache, access_sequence):
    global canvas
    canvas = Canvas(root, height=600, bg="#3F3F3F")
    canvas.pack(fill=BOTH, expand=True)

    x_offset = root.winfo_screenwidth() // 2 - (len(cache) * RECT_SIZE) // 2
    print(x_offset)
    y_offset = 75
    for idx, c in enumerate(cache):
        x1 = x_offset + idx * RECT_SIZE
        x2 = x1 + RECT_SIZE
        y1 = y_offset
        y2 = y1 + RECT_SIZE
        canvas.create_rectangle(x1, y1, x2, y2, outline="white")
        canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=c, fill="white", font=("Helvetica", 20))

    # TODO (For Mohsen): draw access requests list
    # Maybe use different rect_size for this list?
    # because it has more elements


def on_start_viz():
    cache_size = cache_input.get()
    try:
        cache_size = int(cache_size)
        if cache_size <= 0 or cache_size > MAX_RECTS:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", f"Please enter a valid positive integer larger than 0 and less than or equal to {MAX_RECTS} for cache size.")
        return

    num_requests = access_input.get()
    try:
        num_requests = int(num_requests)
        if num_requests <= 0 or num_requests > MAX_RECTS:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", f"Please enter a valid positive integer larger than 0 and less than or equal to {MAX_RECTS} for number of access requests.")
        return
    
    welcome.destroy()
    cache_input_label.destroy()
    cache_input.destroy()
    access_input_label.destroy()
    access_input.destroy()
    start_button.destroy()

    cache = random_char_list(cache_size)
    access_sequence = None
    # TODO (For Mohsen): generate access requests list
    # I wonder how???
    draw_lists(cache, access_sequence)
    


start_button = ttk.Button(root, text="Start Visualization", command=on_start_viz)
start_button.pack(pady=20)

root.mainloop()
