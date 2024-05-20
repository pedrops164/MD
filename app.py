
import tkinter as tk
import os
import threading

class TravelGuideApp(tk.Tk):
    def __init__(self, agent):
        super().__init__()
        self.agent = agent
        self.title("Travel Guide")
        self.geometry("700x500")
        self.msg_count = 0

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

        self.configure_styles()

    
    def send_query(self):
        self.msg_count += 1
        query = self.query_entry.get("1.0", tk.END).strip()
        if query:
            self.display_message("User", query)
            self.query_entry.delete("1.0", tk.END)
            threading.Thread(target=self.process_query, args=(query, self.msg_count)).start()

    def process_query(self, query, msg_num):
        trip_suggestion, list_of_places, validation_result = self.agent.build_itinerary(query)
        if trip_suggestion:
            self.display_message("TravelAgent", trip_suggestion)
        else:
            self.display_message("TravelAgent", "Sorry, your request could not be processed.")
        self.log_to_file(query, trip_suggestion, list_of_places, validation_result, msg_num)

    def display_message(self, sender, message):
        self.chat_text.config(state=tk.NORMAL)
        if sender.lower() == "user":
            self.chat_text.insert(tk.END, f"{sender}: \n{message}\n\n", "user_message")
        else:
            self.chat_text.insert(tk.END, f"{sender}: \n{message}\n\n", "agent_message")
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.yview(tk.END)

    def configure_styles(self):
        self.chat_text.tag_configure("user_message", font=("Helvetica", 10), foreground="blue")
        self.chat_text.tag_configure("agent_message", font=("Helvetica", 10), foreground="green")

    def log_to_file(self, query, trip_suggestion, list_of_places, validation_result, msg_num):
        os.makedirs("output", exist_ok=True)
        with open("output/debug.txt", "a", encoding="utf-8") as file:
            file.write(f"\n\n\n--------------------------------------------------\nMessage: #{msg_num}\n")
            file.write(f"--------------------------------------------------\nUser Query: {query}\n")
            file.write(f"--------------------------------------------------\nTrip Suggestion: {trip_suggestion}\n")
            file.write(f"--------------------------------------------------\nList of Places: {list_of_places}\n")
            file.write(f"--------------------------------------------------\nValidation Result: {validation_result}\n")
