import heapq
import tkinter as tk
from tkinter import ttk, messagebox

# ---------------- COMMON LOCATIONS ----------------
locations = [
    "Rajiv Chowk", "Kashmere Gate", "Central Secretariat",
    "INA", "Hauz Khas", "Saket", "AIIMS", "Lajpat Nagar"
]

# ---------------- METRO GRAPH ----------------
metro_graph = {
    "Rajiv Chowk": [("Kashmere Gate", 5), ("Central Secretariat", 3)],
    "Kashmere Gate": [("Rajiv Chowk", 5), ("INA", 6)],
    "Central Secretariat": [("Rajiv Chowk", 3), ("INA", 4)],
    "INA": [("Central Secretariat", 4), ("Hauz Khas", 3), ("AIIMS", 2)],
    "Hauz Khas": [("INA", 3), ("Saket", 2)],
    "Saket": [("Hauz Khas", 2), ("Lajpat Nagar", 4)],
    "AIIMS": [("INA", 2), ("Lajpat Nagar", 3)],
    "Lajpat Nagar": [("AIIMS", 3), ("Saket", 4)]
}

# ---------------- BUS GRAPH (FIXED) ----------------
bus_graph = {
    "Rajiv Chowk": [("Kashmere Gate", 7), ("AIIMS", 6), ("Central Secretariat", 5)],
    "Kashmere Gate": [("Rajiv Chowk", 7), ("INA", 5)],
    "Central Secretariat": [("Rajiv Chowk", 5), ("INA", 4)],
    "INA": [("Kashmere Gate", 5), ("Hauz Khas", 6), ("AIIMS", 4), ("Central Secretariat", 4)],
    "Hauz Khas": [("INA", 6), ("Saket", 3)],
    "Saket": [("Hauz Khas", 3), ("Lajpat Nagar", 2)],
    "AIIMS": [("Rajiv Chowk", 6), ("INA", 4), ("Lajpat Nagar", 5)],
    "Lajpat Nagar": [("AIIMS", 5), ("Saket", 2)]
}

# ---------------- DIJKSTRA ----------------
def dijkstra(graph, start, end):
    pq = [(0, start, [])]
    visited = set()

    while pq:
        cost, node, path = heapq.heappop(pq)

        if node in visited:
            continue

        path = path + [node]

        if node == end:
            return cost, path

        visited.add(node)

        for neighbor, weight in graph.get(node, []):
            heapq.heappush(pq, (cost + weight, neighbor, path))

    return float("inf"), []

# ---------------- A* ----------------
def heuristic(a, b):
    return 1

def a_star(graph, start, end):
    pq = [(0, 0, start, [])]
    visited = set()

    while pq:
        f, g, node, path = heapq.heappop(pq)

        if node in visited:
            continue

        path = path + [node]

        if node == end:
            return g, path

        visited.add(node)

        for neighbor, weight in graph.get(node, []):
            heapq.heappush(pq, (g + weight + heuristic(node, end), g + weight, neighbor, path))

    return float("inf"), []

# ---------------- MAIN FUNCTION ----------------
def find_routes():
    start = start_var.get()
    end = end_var.get()

    if start == "" or end == "":
        messagebox.showerror("Error", "Please select locations")
        return

    if start == end:
        messagebox.showwarning("Warning", "Start and destination cannot be same")
        return

    metro_cost, metro_path = dijkstra(metro_graph, start, end)
    bus_cost, bus_path = a_star(bus_graph, start, end)

    result = f"📍 {start} → {end}\n\n"

    # METRO OUTPUT
    if metro_cost != float("inf"):
        result += f"🚇 Metro Route:\n{' → '.join(metro_path)}\nCost: ₹{metro_cost}\n\n"
    else:
        result += "🚇 Metro: Route not available\n\n"

    # BUS OUTPUT
    if bus_cost != float("inf"):
        result += f"🚌 Bus Route:\n{' → '.join(bus_path)}\nCost: ₹{bus_cost}\n\n"
    else:
        result += "🚌 Bus: Route not available\n\n"

    # COMPARISON
    if metro_cost != float("inf") and bus_cost != float("inf"):
        if metro_cost < bus_cost:
            result += f"💡 Best Choice: Metro (saves ₹{bus_cost - metro_cost})"
        elif bus_cost < metro_cost:
            result += f"💡 Best Choice: Bus (saves ₹{metro_cost - bus_cost})"
        else:
            result += "💡 Both cost the same"
    elif metro_cost != float("inf"):
        result += "💡 Only Metro available"
    elif bus_cost != float("inf"):
        result += "💡 Only Bus available"

    output_text.set(result)

# ---------------- UI ----------------
root = tk.Tk()
root.title("Smart Delhi Navigator")
root.geometry("600x550")
root.resizable(False, False)

# Gradient background
canvas = tk.Canvas(root, width=600, height=550, highlightthickness=0)
canvas.pack(fill="both", expand=True)

for i in range(550):
    r = int(60 + (i / 550) * 80)
    g = int(40 + (i / 550) * 60)
    b = int(120 + (i / 550) * 100)
    color = f"#{r:02x}{g:02x}{b:02x}"
    canvas.create_line(0, i, 600, i, fill=color)

# Card
frame = tk.Frame(canvas, bg="white")
frame.place(relx=0.5, rely=0.5, anchor="center", width=430, height=400)

# Title
tk.Label(frame, text="🚀 Smart Route Finder",
        font=("Helvetica", 18, "bold"),
        bg="white").pack(pady=15)

# Dropdowns
start_var = tk.StringVar()
end_var = tk.StringVar()

tk.Label(frame, text="📍 Where are you now?", bg="white").pack()
ttk.Combobox(frame, textvariable=start_var, values=locations, state="readonly").pack(pady=5)

tk.Label(frame, text="🎯 Your destination?", bg="white").pack()
ttk.Combobox(frame, textvariable=end_var, values=locations, state="readonly").pack(pady=5)

# Button
tk.Button(frame,
        text="✨ Find Best Route",
        command=find_routes,
        bg="#6C63FF",
        fg="white",
        font=("Arial", 12, "bold"),
        relief="flat",
        padx=15,
        pady=8).pack(pady=20)

# Output
output_text = tk.StringVar()
tk.Label(frame,
        textvariable=output_text,
        wraplength=380,
        justify="left",
        bg="white",
        font=("Arial", 10)).pack(pady=10)

root.mainloop()