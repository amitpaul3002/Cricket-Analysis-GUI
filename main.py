# main.py

import tkinter as tk
from functions import (
    analyze_info,run_rate_page, required_run_rate_menu, 
    create_gui, team_info, add_team_info, set_main_frame,show_about_window,refresh_info
)

root = tk.Tk()
root.title("Cricket Analysis GUI")
root.geometry("1100x600")

# ---- MENU BAR ----
menubar = tk.Menu(root)
menubar.add_command(label="Analyze", command=analyze_info)
menubar.add_command(label="Run Rate", command=run_rate_page)
menubar.add_command(label="Required Run Rate", command=required_run_rate_menu)
menubar.add_command(label="D/L Prediction", command=create_gui)
menubar.add_command(label="About", command=show_about_window)
root.config(menu=menubar)

# ---- TOOLBAR ----
toolbar = tk.Frame(root, bd=1, relief=tk.RAISED, bg="lightgray")
toolbar.pack(side=tk.LEFT, fill=tk.Y)

btn1 = tk.Button(toolbar, text="Add team information", width=20, command=add_team_info)
btn1.pack(pady=5, padx=5)

btn2 = tk.Button(toolbar, text="Team 1 information", width=20, command=lambda: team_info("team1"))
btn2.pack(pady=5, padx=5)

btn3 = tk.Button(toolbar, text="Team 2 information", width=20, command=lambda: team_info("team2"))
btn3.pack(pady=5, padx=5)

btn4 = tk.Button(toolbar, text="Reset Information", width=20, command=refresh_info)
btn4.pack(pady=5, padx=5)
# ---- MAIN FRAME ----
main_frame = tk.Frame(root, bg="white")
main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
set_main_frame(main_frame)  # Pass main_frame reference to functions.py

label = tk.Label(main_frame, text="@Cricket Analyzer", font=("Arial", 16), bg="white")
label.pack(pady=20)

# ---- START GUI ----
root.mainloop()
