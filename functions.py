# functions.py

import tkinter as tk
from tkinter import ttk, messagebox
from data_store import team_data, team_players,reset_team_data,reset_team_players

# --- Shared Frame Reference ---
main_frame = None

def set_main_frame(frame):
    global main_frame
    main_frame = frame

def clear_main_frame():
    for widget in main_frame.winfo_children():
        widget.destroy()

# ------------------ YOUR FUNCTIONS -------------------

def bowl(a):
    return round((((a-int(a))*10)/6)+int(a),2)

def analyze_info():
    clear_main_frame()

    # Title
    tk.Label(main_frame, text="Analyze the Information", font=("Arial", 20, "bold"), bg="lightyellow").pack(pady=10)

    # Dropdowns
    select_frame = tk.Frame(main_frame, bg="white")
    select_frame.pack(pady=10)

    tk.Label(select_frame, text="Select Team:",font=("Arial", 16), bg="white").grid(row=0, column=0, padx=5)
    team_choice = ttk.Combobox(select_frame, values=["team1", "team2"], state="readonly")
    team_choice.grid(row=0, column=1, padx=5)

    tk.Label(select_frame, text="Select Type:", font=("Arial", 16), bg="white").grid(row=0, column=2, padx=5)
    type_choice = ttk.Combobox(select_frame, values=["Batsman", "Bowler"], state="readonly")
    type_choice.grid(row=0, column=3, padx=5)

    # Table frame
    table_frame = tk.Frame(main_frame, bg="white")
    table_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    # Button frame
    button_frame = tk.Frame(main_frame, bg="white")
    button_frame.pack(pady=10)

    def show_table():
        # clear old table if any
        for widget in table_frame.winfo_children():
            widget.destroy()

        team_key = team_choice.get()
        data_type = type_choice.get()
        if not team_key or not data_type:
            messagebox.showerror("Error", "Select both team and type")
            return

        # Create table
        columns = []
        if data_type == "Batsman":
            columns = ("Name", "Runs", "Balls", "Strike Rate")
        else:
            columns = ("Name", "Overs", "Maidens", "Runs", "Wickets", "Economy")

        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=100)
        tree.pack(fill=tk.BOTH, expand=True)

        # Populate table from saved data
        if data_type == "Batsman":
            for p in team_players[team_key]["batsmen"]:
                sr = (p["runs"] / bowl(p["balls"]) * 100) if p["balls"] > 0 else 0
                tree.insert("", tk.END, values=(p["name"], p["runs"], p["balls"], f"{sr:.2f}"))
        else:
            for p in team_players[team_key]["bowlers"]:
                eco = (p["runs"] / bowl(p["overs"])) if p["overs"] > 0 else 0
                tree.insert("", tk.END, values=(p["name"], p["overs"], p["maidens"], p["runs"], p["wickets"], f"{eco:.2f}"))

        # Add Best and Less buttons
        for widget in button_frame.winfo_children():
            widget.destroy()

        def best_player():
            if data_type == "Batsman":
                best = max(team_players[team_key]["batsmen"], key=lambda x: (x["runs"]/bowl(x["balls"])*100 if x["balls"] else 0), default=None)
                if best:
                    messagebox.showinfo("Best Batsman", f"{best['name']} with SR {(best['runs']/bowl(best['balls'])*100):.2f}")
            else:
                best = min(team_players[team_key]["bowlers"], key=lambda x: (x["runs"]/bowl(x["overs"]) if x["overs"] else float('inf')), default=None)
                if best:
                    messagebox.showinfo("Best Bowler", f"{best['name']} with Economy {(best['runs']/bowl(best['overs'])):.2f}")

        def less_player():
            if data_type == "Batsman":
                worst = min(team_players[team_key]["batsmen"], key=lambda x: (x["runs"]/bowl(x["balls"])*100 if x["balls"] else 0), default=None)
                if worst:
                    messagebox.showinfo("Less Batsman", f"{worst['name']} with SR {(worst['runs']/bowl(worst['balls'])*100):.2f}")
            else:
                worst = max(team_players[team_key]["bowlers"], key=lambda x: (x["runs"]/x["overs"] if x["overs"] else 0), default=None)
                if worst:
                    messagebox.showinfo("Less Bowler", f"{worst['name']} with Economy {(worst['runs']/worst['overs']):.2f}")

        tk.Button(button_frame, text="Best Player", bg="green", fg="white", command=best_player).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Less Player", bg="red", fg="white", command=less_player).pack(side=tk.LEFT, padx=10)

    # Search button
    tk.Button(select_frame, text="Show Table", bg="blue", fg="white", command=show_table).grid(row=0, column=4, padx=10)

def run_rate_page():
    clear_main_frame()

    # Title
    tk.Label(main_frame, text="Run Rate", font=("Arial", 20, "bold"), bg="lightyellow").pack(pady=10)

    # Dropdown frame
    select_frame = tk.Frame(main_frame, bg="white")
    select_frame.pack(pady=10)

    tk.Label(select_frame, text="Select Team:", font=("Arial", 16), bg="white").grid(row=0, column=0, padx=5)
    team_choice = ttk.Combobox(select_frame, values=["team1", "team2"], state="readonly")
    team_choice.grid(row=0, column=1, padx=5)

    # Output label
    result_label = tk.Label(main_frame, text="", font=("Arial", 16), bg="white", fg="blue")
    result_label.pack(pady=20)

    def calculate_nrr():
        team_key = team_choice.get()
        if not team_key:
            messagebox.showerror("Error", "Select a team first")
            return

        # Ensure team info exists
        if team_data[team_key]["name"] == "" or team_data[team_key]["overs"] <= 0:
            messagebox.showerror("Error", f"No valid information for {team_key}. Please add team info first.")
            return

        runs = team_data[team_key]["runs"]
        overs = team_data[team_key]["overs"]
        rr = runs / bowl(overs)

        result_label.config(text=f"Run Rate of {team_key}: {rr:.2f}")

    # Button
    tk.Button(select_frame, text="Show Net Run Rate", bg="blue", fg="white", command=calculate_nrr).grid(row=0, column=2, padx=10)

    
def required_run_rate_menu():
    clear_main_frame()

    # Title
    title = tk.Label(main_frame, text="Required Run Rate",font=("Arial", 20, "bold"), bg="lightyellow")
    title.pack(pady=10)

    # Dropdown to select Team 2 progress type
    info_frame = tk.Frame(main_frame, bg="white")
    info_frame.pack(pady=20)

    tk.Label(info_frame, text="Select information type:", bg="white", font=("Arial", 16)).grid(row=0, column=0, padx=10)
    info_type = tk.StringVar(value="Second innings is not started")
    info_dropdown = ttk.Combobox(info_frame, textvariable=info_type, state="readonly",
                                 values=["Second innings is not started", "Second innings start"])
    info_dropdown.grid(row=0, column=1, padx=10)

    # Label to display result
    result_label = tk.Label(main_frame, text="", font=("Arial", 16, "bold"), bg="white", fg="blue")
    result_label.pack(pady=20)

    def calculate_rrr():
        try:
            # Make sure Team1 data is complete
            # t1 = team_data[]
            if team_data["team1"]["runs"] == "" or team_data["team1"]["total_overs"] <= 0:
                messagebox.showerror("Error", "Please enter full Team 1 information first.")
                return
            
            target_runs = team_data["team1"]["runs"] + 1
            total_overs =team_data["team1"]["total_overs"]

            # Check game over
            if team_data["team2"].get("game_over", False):
                result_label.config(text="Match already over. No required run rate.")
                return
            
            if info_type.get() == "Second innings is not started":
                rrr = target_runs / bowl(total_overs)

            else:  # partial_info
                runs_scored = team_data["team2"]["runs"]
                overs_played = team_data["team2"]["overs"]
                remaining_runs = target_runs - runs_scored
                remaining_overs = bowl(total_overs) - bowl(overs_played)

                if remaining_overs <= 0:
                    result_label.config(text="No overs remaining.")
                    return

                rrr = remaining_runs / remaining_overs

            result_label.config(text=f"Required Run Rate: {rrr:.2f}")
        
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for runs/overs.")

    # Button to calculate
    tk.Button(main_frame, text="Calculate RRR", bg="blue", fg="white",
              command=calculate_rrr).pack(pady=10)


def create_dls_table(overs_max, wickets_max):
        """
        Generates a DLS-like table by calculating resource values based on
        overs remaining and wickets lost.

        The formula used is an approximation and is not the official DLS algorithm.
        It aims to "slightly match" the provided ICC DLS table values.

        Args:
            overs_max (int): The maximum number of overs in a full innings.
            wickets_max (int): The maximum number of wickets (typically 10, meaning 0-9 wickets lost).

        Returns:
            dict: A dictionary representing the DLS table, where keys are overs left
                  and values are lists of resource percentages for 0 to 9 wickets lost.
        """
        dls_table = {}

        # Parameters tuned to approximate the DLS table
        OVERS_CURVE_EXPONENT = 0.6
        EFFECTIVE_MAX_WICKETS = 14.0 # Conceptual value for wicket penalty scaling
        WICKET_PENALTY_EXPONENT = 2.2

        for overs_left in range(overs_max, -1, -1):
            dls_table[overs_left] = []
            for wickets_lost in range(wickets_max):  # Calculate for 0 to (wickets_max-1) wickets lost
                resource_val = 0.0

                if overs_left == 0:
                    # If no overs are left, resource is 0% regardless of wickets.
                    resource_val = 0.0
                else:
                    # Base resource from overs (e.g., if no wickets lost)
                    base_resource_from_overs = 100.0 * ((overs_left / overs_max) ** OVERS_CURVE_EXPONENT)

                    # Reduction multiplier due to wickets lost
                    # This makes later wickets more impactful
                    wicket_reduction_multiplier = ((EFFECTIVE_MAX_WICKETS - wickets_lost) / EFFECTIVE_MAX_WICKETS) ** WICKET_PENALTY_EXPONENT

                    # Combine both factors
                    resource_val = base_resource_from_overs * wicket_reduction_multiplier
                    resource_val = max(0.0, resource_val) # Ensure resource doesn't go negative

                dls_table[overs_left].append(round(resource_val, 1))

        # Explicitly set the row for 0 overs to all 0s for clarity
        if 0 in dls_table:
            dls_table[0] = [0.0 for _ in range(wickets_max)]

        return dls_table

def create_gui():
    clear_main_frame()
    
    title = tk.Label(main_frame, text="Duckworth-Lewis Method Score ",font=("Arial", 20, "bold"), bg="lightyellow")
    title.pack(pady=10)
    input_container = tk.Frame(main_frame)
    input_container.pack(fill="x", pady=10)

    # Inputs always visible
    tk.Label(input_container, text="Score to chase for Second Team :").pack(pady=(5,0))
    entry_S = tk.Entry(input_container)
    entry_S.pack()
    tk.Label(input_container, text="Total overs in a full innings :").pack(pady=(5,0))
    entry_O = tk.Entry(input_container)
    entry_O.pack()
    tk.Label(input_container, text="Total wickets for calculating D/L table :").pack(pady=(5,0))
    entry_W = tk.Entry(input_container)
    entry_W.pack()

    # Checkbox control
    checkbox_var = tk.IntVar()
    checkbox = tk.Checkbutton(input_container, text="Match interrupted in first innings?",
                              variable=checkbox_var, command=lambda: toggle_input())
    checkbox.pack(pady=10)

    # --- Hidden input section (inside its own frame) ---
    hidden_frame = tk.Frame(input_container)
    hidden_frame.pack(fill="x")

    input_frame1 = tk.Frame(hidden_frame, pady=10, bg="white", bd=2, relief="groove")
    tk.Label(input_frame1, text="Wickets lost by First Team before interruption :", bg="white").pack(side="left")
    entry_r1w = tk.Entry(input_frame1)
    entry_r1w.pack(side="left", padx=5)

    input_frame2 = tk.Frame(hidden_frame, pady=10, bg="white", bd=2, relief="groove")
    tk.Label(input_frame2, text="Overs remaining for First Team before interruption:", bg="white").pack(side="left")
    entry_r1ob = tk.Entry(input_frame2)
    entry_r1ob.pack(side="left", padx=5)

    input_frame3 = tk.Frame(hidden_frame, pady=10, bg="white", bd=2, relief="groove")
    tk.Label(input_frame3, text="Overs remaining for First Team interruption :", bg="white").pack(side="left")
    entry_r1oa = tk.Entry(input_frame3)
    entry_r1oa.pack(side="left", padx=5)

    def toggle_input():
        if checkbox_var.get():
            input_frame1.pack(pady=5)
            input_frame2.pack(pady=5)
            input_frame3.pack(pady=5)
        else:
            input_frame1.pack_forget()
            input_frame2.pack_forget()
            input_frame3.pack_forget()

    # Always visible inputs after hidden section
    tk.Label(input_container, text="Wickets lost by Second Team after interruption :").pack(pady=(5,0))
    entry_r2w = tk.Entry(input_container)
    entry_r2w.pack()
    tk.Label(input_container, text="Overs remaining for Second Team after interruption :").pack(pady=(5,0))
    entry_r2o = tk.Entry(input_container)
    entry_r2o.pack()

    # --- Bottom container for result + button ---
    bottom_container = tk.Frame(main_frame)
    bottom_container.pack(fill="x", pady=15)

    result_label = tk.Label(bottom_container, text="", font=("Arial", 12, "bold"), fg="blue", pady=10)
    result_label.pack()



    def calculate_target():
        """
        Calculates the DLS target score for Team 2 based on user inputs
        and the generated DLS table. Displays the result or an error message.
        """
        try:
            # Retrieve inputs and convert to integers
            S = int(entry_S.get())
            O = int(entry_O.get())
            W = int(entry_W.get()) # Total wickets for table generation
            r2w = int(entry_r2w.get())
            r2o = int(entry_r2o.get())

            # Input validation
            if not (1 <= O <= 50): # Assuming realistic overs range for DLS
                raise ValueError("Total overs (O) must be between 1 and 50.")
            if not (1 <= W <= 10): # Wickets for table generation, typically 10 (0-9 lost)
                raise ValueError("Total wickets (W) must be between 1 and 10.")
            if not (0 <= r2w <= 9): # Wickets lost by team 2 can be 0-9
                raise ValueError("Wickets lost by Team 2 (r2w) must be between 0 and 9.")
            if not (0 <= r2o <= O): # Overs remaining for team 2 cannot exceed total overs
                raise ValueError(f"Overs remaining for Team 2 (r2o) must be between 0 and {O}.")

            # Generate the DLS table based on total overs and wickets
            table = create_dls_table(O, W)

            if checkbox_var.get():  # Match interrupted in first innings
                r1w = int(entry_r1w.get())
                r1ob = int(entry_r1ob.get()) # Overs remaining before interruption
                r1oa = int(entry_r1oa.get()) # Overs remaining after interruption (new total for Team 1)

                # Validate interruption-specific inputs
                if not (0 <= r1w <= 9):
                    raise ValueError("Wickets lost by First Team must be between in proper a range.")
                if not (0 <= r1ob <= O):
                    raise ValueError(f"Overs remaining for First Team before interruption must be between 0 and {O}.")
                if not (0 <= r1oa <= O):
                    raise ValueError(f"Overs remaining for First Team after interruption must be between 0 and {O}.")
                if r1oa > r1ob:
                     raise ValueError("Overs remaining for First Team after interruption cannot be more than overs before interruption.")


                # R2: Resources available to Team 2 for their innings
                # Based on overs remaining and wickets lost by Team 2
                r2 = table[r2o][r2w]

                # R1: Resources available to Team 1 for their innings
                # This is calculated as the full initial resource minus the resource lost due to interruption.
                # 'table[O][0]' represents the total resource for 'O' overs with 0 wickets lost.
                # The resource lost by Team 1 is the difference between resources they *would have had*
                # if there was no interruption (at r1ob) and what they *actually have* (at r1oa).
                r1_full_innings_resource = table[O][0]
                resource_lost_by_team1_due_to_interruption = table[r1ob][r1w] - table[r1oa][r1w]
                r1 = r1_full_innings_resource - resource_lost_by_team1_due_to_interruption

                # Ensure r1 is not zero to prevent division by zero
                if r1 == 0:
                    result_label.config(text="Error: First Team resource value is zero, cannot calculate target. Check inputs.", fg="red")
                    return

                # Calculate target using the DLS formula: T = S * (R2 / R1) + 1
                T = round(S * (r2 / r1) + 1)

            else:  # Normal match (no interruption in first innings)
                # R2: Resources available to Team 2 for their innings
                r2 = table[r2o][r2w]
                # R1: Resources available to Team 1 for their full innings (total resource for 'O' overs)
                r1 = table[O][0]

                # Ensure r1 is not zero
                if r1 == 0:
                    result_label.config(text="Error: First Team resource value is zero, cannot calculate target. Check inputs.", fg="red")
                    return

                # Calculate target
                T = round(S * (r2 / r1) + 1)

            result_label.config(text=f"The target for Second Team is {T} in {r2o} overs", fg="blue")

        # Error handling for invalid inputs or calculation issues
        except ValueError as ve:
            result_label.config(text=f"Input Error: Please enter valid numbers. {ve}", fg="red")
        except KeyError as ke:
            result_label.config(text=f"Data Error: Overs or wickets out of table range. Ensure 'Total overs' and 'Total wickets' are correctly set. {ke}", fg="red")
        except Exception as e:
            result_label.config(text=f"An unexpected error occurred: {e}", fg="red")

    # Button to trigger target calculation
    tk.Button(bottom_container, text="Show Result", command=calculate_target,
              bg="green", fg="white", font=("Arial", 10, "bold"), width=15).pack(pady=10)

    # Call toggle function once to set the initial state (hidden)
    # toggle_interrupt_section()

    # Start the Tkinter event loop
    main_frame.mainloop()

def show_about_window():
    clear_main_frame()
    # Title label
    title_label = ttk.Label(
        main_frame, 
        text="Cricket Analysis Tool", 
        font=("Helvetica", 20, "bold")
    )
    title_label.pack(pady=(15, 5))

    # Separator
    ttk.Separator(main_frame, orient="horizontal").pack(fill="x", pady=5)

    # About text
    about_text = (
        "This application is designed to simplify cricket match analysis by allowing you to:\n\n"
        "• Add and manage team information (runs, overs, wickets, players)\n"
        "• Analyze batting and bowling performance automatically\n"
        "• Calculate match metrics such as Net Run Rate (NRR) and Required Run Rate (RRR)\n"
        "• Plan for rain interruptions with an upcoming DLS prediction feature\n\n"
        "How to use:\n"
        "- Use the toolbar to input team details and stats\n"
        "- Use the menu to access analysis tools\n"
        "- Results are shown interactively in tables and summaries\n\n"
        "Developed as a utility for quick cricket insights."
        "Developed and Designed by Amit Paul"
    )

    about_label = ttk.Label(
        main_frame, 
        text=about_text, 
        font=("Helvetica", 10, "bold"),
        wraplength=360, 
        justify="left"
    )
    about_label.pack(padx=15, pady=5)

    # Close button
    

def team_info(team_key):
    clear_main_frame()
    
    # Heading
    title = tk.Label(main_frame, text=f"{team_key.upper()} Information", font=("Arial", 18, "bold"), bg="white")
    title.pack(pady=10)

    # ====== Batsman Section ======
    batsman_frame = tk.LabelFrame(main_frame, text="Batsman Information", font=("Arial", 14), bg="lightblue", padx=10, pady=10)
    batsman_frame.pack(fill=tk.X, padx=20, pady=10)

    tk.Label(batsman_frame, text="Batsman Name:", bg="lightblue").grid(row=0, column=0, sticky="w", pady=5)
    batsman_name = tk.Entry(batsman_frame, width=20)
    batsman_name.grid(row=0, column=1, pady=5)

    tk.Label(batsman_frame, text="Runs:", bg="lightblue").grid(row=1, column=0, sticky="w", pady=5)
    batsman_runs = tk.Entry(batsman_frame, width=20)
    batsman_runs.grid(row=1, column=1, pady=5)

    tk.Label(batsman_frame, text="Balls Faced:", bg="lightblue").grid(row=2, column=0, sticky="w", pady=5)
    batsman_balls = tk.Entry(batsman_frame, width=20)
    batsman_balls.grid(row=2, column=1, pady=5)

    def save_batsman():
        if len(team_players[team_key]["batsmen"]) >= 11:
            messagebox.showerror("Error", "Maximum 11 batsmen already added.")
            return
        try:
            name = batsman_name.get()
            runs = int(batsman_runs.get())
            balls = float(batsman_balls.get())
            # Check team total run limit
            total_runs = team_data[team_key]["runs"]
            current_sum = sum(p["runs"] for p in team_players[team_key]["batsmen"])
            if current_sum + runs > total_runs:
                messagebox.showerror("Error", f"Total batsman runs exceed {total_runs}")
                return
            team_players[team_key]["batsmen"].append({"name": name, "runs": runs, "balls": balls})
            messagebox.showinfo("Success", f"Batsman '{name}' saved.")
            batsman_name.delete(0, tk.END)
            batsman_runs.delete(0, tk.END)
            batsman_balls.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Enter valid numbers for runs and balls.")

    tk.Button(batsman_frame, text="Submit Batsman", bg="blue", fg="white", command=save_batsman).grid(row=3, column=0, columnspan=2, pady=10)

    # ====== Bowler Section ======
    bowler_frame = tk.LabelFrame(main_frame, text="Bowler Information", font=("Arial", 14), bg="lightgreen", padx=10, pady=10)
    bowler_frame.pack(fill=tk.X, padx=20, pady=10)

    tk.Label(bowler_frame, text="Bowler Name:", bg="lightgreen").grid(row=0, column=0, sticky="w", pady=5)
    bowler_name = tk.Entry(bowler_frame, width=20)
    bowler_name.grid(row=0, column=1, pady=5)

    tk.Label(bowler_frame, text="Overs Bowled:", bg="lightgreen").grid(row=1, column=0, sticky="w", pady=5)
    bowler_overs = tk.Entry(bowler_frame, width=20)
    bowler_overs.grid(row=1, column=1, pady=5)

    tk.Label(bowler_frame, text="Maidens:", bg="lightgreen").grid(row=2, column=0, sticky="w", pady=5)
    bowler_maidens = tk.Entry(bowler_frame, width=20)
    bowler_maidens.grid(row=2, column=1, pady=5)

    tk.Label(bowler_frame, text="Runs Conceded:", bg="lightgreen").grid(row=3, column=0, sticky="w", pady=5)
    bowler_runs = tk.Entry(bowler_frame, width=20)
    bowler_runs.grid(row=3, column=1, pady=5)

    tk.Label(bowler_frame, text="Wickets:", bg="lightgreen").grid(row=4, column=0, sticky="w", pady=5)
    bowler_wickets = tk.Entry(bowler_frame, width=20)
    bowler_wickets.grid(row=4, column=1, pady=5)

    def save_bowler():
        if len(team_players[team_key]["bowlers"]) >= 11:
            messagebox.showerror("Error", "Maximum 11 bowlers already added.")
            return
        try:
            name = bowler_name.get()
            overs = float(bowler_overs.get())
            maidens = int(bowler_maidens.get())
            conceded = int(bowler_runs.get())
            wickets = int(bowler_wickets.get())
            # Check team total conceded run limit
            opponect_key  = "team1" if team_key =="team2" else "team2" 
            total_runs = team_data[opponect_key]["runs"]
            current_sum = sum(p["runs"] for p in team_players[team_key]["bowlers"])
            if current_sum + conceded > total_runs:
                messagebox.showerror("Error", f"Total bowler conceded runs exceed {total_runs}")
                return
            team_players[team_key]["bowlers"].append({
                "name": name, "overs": overs, "maidens": maidens,
                "runs": conceded, "wickets": wickets
            })
            messagebox.showinfo("Success", f"Bowler '{name}' saved.")
            bowler_name.delete(0, tk.END)
            bowler_overs.delete(0, tk.END)
            bowler_maidens.delete(0, tk.END)
            bowler_runs.delete(0, tk.END)
            bowler_wickets.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Enter valid numbers for overs, maidens, runs, and wickets.")

    tk.Button(bowler_frame, text="Submit Bowler", bg="green", fg="white", command=save_bowler).grid(row=5, column=0, columnspan=2, pady=10)

    
def add_team_info():
    clear_main_frame()
    
    # Title at top center
    title = tk.Label(main_frame, text="Add Team Information", font=("Arial", 18, "bold"), bg="white")
    title.pack(pady=10)

    # Create container for left and right sections
    content_frame = tk.Frame(main_frame, bg="white")
    content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # ---- LEFT PANEL (Team 1) ----
    left_frame = tk.Frame(content_frame, bg="lightblue", bd=2, relief=tk.GROOVE)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

    tk.Label(left_frame, text="Team 1 Information", font=("Arial", 14, "bold"), bg="lightblue").pack(pady=10)

    tk.Label(left_frame, text="Team Name:", bg="lightblue").pack(anchor="w", padx=10, pady=5)
    team1_name = tk.Entry(left_frame, width=25)
    team1_name.pack(padx=10)

    tk.Label(left_frame, text="Total Runs:", bg="lightblue").pack(anchor="w", padx=10, pady=5)
    team1_runs = tk.Entry(left_frame, width=25)
    team1_runs.pack(padx=10)

    tk.Label(left_frame, text="Overs Played:", bg="lightblue").pack(anchor="w", padx=10, pady=5)
    team1_overs = tk.Entry(left_frame, width=25)
    team1_overs.pack(padx=10)

    tk.Label(left_frame, text="Total Overs :", bg="lightblue").pack(anchor="w", padx=10, pady=5)
    total_overs = tk.Entry(left_frame, width=25)
    total_overs.pack(padx=10)
    
    tk.Label(left_frame, text="Total Wickets:", bg="lightblue").pack(anchor="w", padx=10, pady=5)
    team1_wickets = tk.Entry(left_frame, width=25)
    team1_wickets.pack(padx=10)
    
    submit1 = tk.Button(left_frame, text="Submit Team 1", bg="blue", fg="white",
                        command=lambda: save_team1(team1_name, team1_runs, team1_overs,total_overs , team1_wickets))
    submit1.pack(pady=10)

    # ---- RIGHT PANEL (Team 2) ----
    right_frame = tk.Frame(content_frame, bg="lightgreen", bd=2, relief=tk.GROOVE)
    right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

    tk.Label(right_frame, text="Team 2 Information", font=("Arial", 14, "bold"), bg="lightgreen").pack(pady=10)

    tk.Label(right_frame, text="Team Name:", bg="lightgreen").pack(anchor="w", padx=10, pady=5)
    team2_name = tk.Entry(right_frame, width=25)
    team2_name.pack(padx=10)

    tk.Label(right_frame, text="Total Runs:", bg="lightgreen").pack(anchor="w", padx=10, pady=5)
    team2_runs = tk.Entry(right_frame, width=25)
    team2_runs.pack(padx=10)

    tk.Label(right_frame, text="Overs Played:", bg="lightgreen").pack(anchor="w", padx=10, pady=5)
    team2_overs = tk.Entry(right_frame, width=25)
    team2_overs.pack(padx=10)
    
    tk.Label(right_frame, text="Total Overs:", bg="lightgreen").pack(anchor="w", padx=10, pady=5)
    total_overs2 = tk.Entry(right_frame, width=25)
    total_overs2.pack(padx=10)

    tk.Label(right_frame, text="Total Wickets:", bg="lightgreen").pack(anchor="w", padx=10, pady=5)
    team2_wickets = tk.Entry(right_frame, width=25)
    team2_wickets.pack(padx=10)

    game_over_var = tk.BooleanVar()
    game_over_check = tk.Checkbutton(right_frame, text="Game Over", variable=game_over_var, bg="lightgreen")
    game_over_check.pack(pady=5)

    submit2 = tk.Button(right_frame, text="Submit Team 2", bg="green", fg="white",
                        command=lambda: save_team2(team2_name, team2_runs, team2_overs, total_overs2, team2_wickets, game_over_var))
    submit2.pack(pady=10)
    

def save_team1(name_entry, runs_entry, overs_entry,total_overs_entry, wickets_entry):
    try:
        team_data["team1"]["name"] = name_entry.get()
        team_data["team1"]["runs"] = int(runs_entry.get())
        team_data["team1"]["overs"] = float(overs_entry.get())
        team_data["team1"]["total_overs"] = float(total_overs_entry.get())
        team_data["team1"]["wickets"] = int(wickets_entry.get())
        messagebox.showinfo("Success", "Team 1 information saved!")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values for runs, overs, and wickets.")

def save_team2(name_entry, runs_entry, overs_entry, total_overs_entry, wickets_entry, game_over_var):
    try:
        team_data["team2"]["name"] = name_entry.get()
        team_data["team2"]["runs"] = int(runs_entry.get())
        team_data["team2"]["overs"] = float(overs_entry.get())
        team_data["team2"]["total_overs"] = float(total_overs_entry.get())  # fixed typo
        team_data["team2"]["wickets"] = int(wickets_entry.get())
        team_data["team2"]["game_over"] = game_over_var.get()  # <-- store checkbox state

        messagebox.showinfo("Success", "Team 2 information saved!")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values for runs, overs, and wickets.")

def refresh_info():
    clear_main_frame()

    # Title
    title = tk.Label(main_frame, text="Refresh Information",font=("Arial", 20, "bold"), bg="lightyellow")
    title.pack(pady=10)

    # Dropdown to select Team 2 progress type
    info_frame1 = tk.Frame(main_frame, bg="white")
    info_frame1.pack(pady=20)

    tk.Label(info_frame1, text="Select information type:", bg="white", font=("Arial", 16)).grid(row=0, column=0, padx=10)
    info_type = tk.StringVar(value="")
    info_dropdown = ttk.Combobox(info_frame1, textvariable=info_type, state="readonly",
                                 values=["Refresh Team Information", "Refresh Players Information"])
    info_dropdown.grid(row=0, column=1, padx=10)
    def refresh():
        try:
            
            if info_type.get() == "Refresh Team Information":
                reset_team_data() 
                messagebox.showinfo("Team Data Reset", "All team data has been reset successfully!")
                clear_main_frame()
                tk.Label(main_frame, text="@Cricket Analyzer", font=("Arial", 16), bg="white").pack(pady=20)

            else:
                reset_team_players() 
                messagebox.showinfo("Players Data Reset", "All players data has been reset successfully!")
                clear_main_frame()
                tk.Label(main_frame, text="@Cricket Analyzer", font=("Arial", 16), bg="white").pack(pady=20)
                
        
        except ValueError:
            messagebox.showerror("Error", "Refresh no work")

    # Label to display result
    tk.Button(main_frame, text="RESET", bg="blue", fg="white",
              command=refresh).pack(pady=10)
    result_label = tk.Label(main_frame, text="", font=("Arial", 16, "bold"), bg="white", fg="blue")
    result_label.pack(pady=20)
