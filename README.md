Cricket Analysis GUI 🏏
This is a desktop application built with Python's Tkinter library designed to simplify cricket match analysis. It allows users to input, store and analyze match data, providing useful metrics and predictions in a user-friendly graphical interface.

Features
Team & Player Data Entry: Easily add comprehensive information for two teams, including player stats for both batsmen and bowlers.

Match Metrics Calculation: Get instant calculations for Run Rate (RR) and Required Run Rate (RRR) to track the pace of the game.

Player Performance Analysis: Analyze individual player performance with detailed tables for batsmen (Strike Rate) and bowlers (Economy). The app can also highlight the best and least effective players.

D/L Prediction: Use the built-in Duckworth-Lewis (D/L) prediction feature to calculate target scores in rain-affected matches, with options for interruptions in the first or second innings.

User-Friendly Interface: The application provides a clean and intuitive GUI with a menu bar and a toolbar for easy navigation.

How to Use
Run the Application: Execute main.py to start the program.

Add Team Information: Click "Add team information" from the toolbar to input the basic details (name, runs, overs) for both teams.

Enter Player Data: Use the "Team 1 information" and "Team 2 information" buttons on the toolbar to add individual stats for each player.

Analyze & Calculate:

Analyze: Use the "Analyze" option in the menu to view performance tables for batsmen and bowlers.

Run Rate: Select "Run Rate" to calculate the Net Run Rate (NRR) for a team.

Required Run Rate: Choose "Required Run Rate" to find the target RRR for the chasing team.

D/L Prediction: Use "D/L Prediction" to calculate a revised target score after a match interruption.

About: The "About" section provides a brief description of the application and its purpose.

File Structure
main.py: The main file that initializes the Tkinter GUI and sets up the window, menu, and toolbar.

functions.py: Contains all the core logic, including functions for clearing the frame, calculating run rates, analyzing player stats, and handling the D/L prediction.

data_store.py: Serves as a simple, in-memory database to store all match and player data using dictionaries.

Requirements
Python 3.x

Tkinter (usually comes pre-installed with Python)

To run the application, ensure all three files are in the same directory and execute main.py from your terminal.
