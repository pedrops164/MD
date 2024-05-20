
import tkinter as tk
from tkinter import ttk
import os

class TravelGuideApp(tk.Tk):
    def __init__(self, agent):
        super().__init__()
        self.agent = agent
        self.title("Travel Guide")
        self.geometry("700x500")

        self.chat_frame = tk.Frame(self)
        self.chat_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.chat_text = tk.Text(self.chat_frame, state='disabled', width=80, height=20, wrap='word', bg="#F0F0F0", font=("Helvetica", 10))
        self.chat_text.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        self.scrollbar = tk.Scrollbar(self.chat_frame, command=self.chat_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_text['yscrollcommand'] = self.scrollbar.set

        self.entry_frame = tk.Frame(self)
        self.entry_frame.pack(pady=10, fill=tk.X, expand=True)

        self.query_entry = tk.Text(self.entry_frame, width=70, height=4, font=("Helvetica", 12))
        self.query_entry.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        self.send_button = tk.Button(self.entry_frame, text="Send", command=self.send_query, font=("Helvetica", 12))
        self.send_button.pack(side=tk.RIGHT)

    def send_query(self):
        query = self.query_entry.get("1.0", tk.END).strip()
        if query:
            self.display_message("User", query)
            self.query_entry.delete("1.0", tk.END)
            #try:
            trip_suggestion, list_of_places, validation_result = self.agent.build_itinerary(query)
            if trip_suggestion:
                self.display_message("TravelAgent", trip_suggestion)
            else:
                self.display_message("TravelAgent", "Sorry, your request could not be processed.")
            self.log_to_file(query, trip_suggestion, list_of_places, validation_result)
            #except Exception as e:
            #    self.display_message("Error", str(e))

    def display_message(self, sender, message):
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(tk.END, f"{sender}: {message}\n", sender.lower())
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.yview(tk.END)

    def log_to_file(self, query, trip_suggestion, list_of_places, validation_result):
        os.makedirs("output", exist_ok=True)
        with open("output/debug.txt", "a") as file:
            file.write(f"User Query: {query}\n")
            file.write(f"Trip Suggestion: {trip_suggestion}\n")
            file.write(f"List of Places: {list_of_places}\n")
            file.write(f"Validation Result: {validation_result}\n")
            file.write("-" * 50 + "\n")
