import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Backened_code import (
    get_current_date,
    display_available_flights,
    save_booking_to_file,
    read_booked_tickets_from_file,
    write_booked_tickets_to_file,
    cancel_ticket,
    display_booked_tickets,
    send_feedback_email,
    send_thank_you_email,
    create_pdf,
    send_confirmation_email,
    send_cancelation_email,
)


class AerobookGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Aerobook GUI")

        # Variables
        self.user_input1 = tk.StringVar()
        self.user_input2 = tk.StringVar()
        self.user_input3 = tk.StringVar()
        self.user_name = tk.StringVar()
        self.user_phone = tk.StringVar()

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Main Menu
        menu_label = tk.Label(self.root, text="Main Menu", font=("Helvetica", 16))
        menu_label.grid(row=0, column=1, pady=10)

        # Options
        options_frame = ttk.LabelFrame(self.root, text="Options")
        options_frame.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(options_frame, text="Book a Ticket", command=self.book_ticket).grid(row=0, column=0, padx=5)
        ttk.Button(options_frame, text="View Available Flights", command=self.view_flights).grid(row=0, column=1, padx=5)
        ttk.Button(options_frame, text="Provide Feedback", command=self.provide_feedback).grid(row=0, column=2, padx=5)
        ttk.Button(options_frame, text="Cancel Ticket", command=self.cancel_ticket).grid(row=0, column=3, padx=5)

    def book_ticket(self):
        book_ticket_window = tk.Toplevel(self.root)
        book_ticket_window.title("Book a Ticket")

        # Create and place relevant widgets for booking a ticket
        ttk.Label(book_ticket_window, text="Source Station:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(book_ticket_window, textvariable=self.user_input1).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(book_ticket_window, text="Destination:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(book_ticket_window, textvariable=self.user_input2).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(book_ticket_window, text="Date (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(book_ticket_window, textvariable=self.user_input3).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(book_ticket_window, text="Passenger Name:").grid(row=3, column=0, padx=5, pady=5)
        ttk.Entry(book_ticket_window, textvariable=self.user_name).grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(book_ticket_window, text="Passenger Phone:").grid(row=4, column=0, padx=5, pady=5)
        ttk.Entry(book_ticket_window, textvariable=self.user_phone).grid(row=4, column=1, padx=5, pady=5)

        ttk.Button(book_ticket_window, text="Submit", command=self.submit_booking).grid(row=5, column=1, pady=10)
    def submit_booking(self):
        # Simulate booking logic (placeholder)
        booking_details = (
            f"Source: {self.user_input1.get()}\n"
            f"Destination: {self.user_input2.get()}\n"
            f"Date: {self.user_input3.get()}\n"
            f"Passenger Name: {self.user_name.get()}\n"
            f"Passenger Phone: {self.user_phone.get()}"
        )

        # Display a confirmation message
        messagebox.showinfo("Booking Successful", f"Ticket booked successfully!\n\n{booking_details}")


    def view_flights(self):
        view_flights_window = tk.Toplevel(self.root)
        view_flights_window.title("View Available Flights")

        # Simulate available flights (placeholder)
        available_flights = [
            "Flight 1 - ABC Airlines\n   Date: 2023-11-10\n   Flight ID: 123\n   Price: $200",
            "Flight 2 - XYZ Airways\n   Date: 2023-11-15\n   Flight ID: 456\n   Price: $150",
            "Flight 3 - MNO Airlines\n   Date: 2023-11-20\n   Flight ID: 789\n   Price: $180",
        ]

        # Create a text widget to display available flights
        flights_text = tk.Text(view_flights_window, wrap=tk.WORD, width=50, height=15)
        flights_text.grid(row=0, column=0, padx=10, pady=10)

        # Insert available flights into the text widget
        for flight in available_flights:
            flights_text.insert(tk.END, f"{flight}\n\n")
        flights_text.config(state=tk.DISABLED)

    def provide_feedback(self):
        feedback_window = tk.Toplevel(self.root)
        feedback_window.title("Provide Feedback")

        # Create and place relevant widgets for providing feedback
        ttk.Label(feedback_window, text="Email Address:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(feedback_window, textvariable=self.user_input1).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(feedback_window, text="Feedback:").grid(row=1, column=0, padx=5, pady=5)
        feedback_text = tk.Text(feedback_window, wrap=tk.WORD, width=50, height=10)
        feedback_text.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(feedback_window, text="Submit", command=self.submit_feedback).grid(row=2, column=1, pady=10)

    def submit_feedback(self):
        # Simulate feedback submission (placeholder)
        user_email = self.user_input1.get()
        feedback = self.feedback_text.get("1.0", tk.END)

        # Display a confirmation message
        messagebox.showinfo("Feedback Submitted", f"Feedback submitted successfully!\n\nUser Email")

    def cancel_ticket(self):
        cancel_ticket_window = tk.Toplevel(self.root)
        cancel_ticket_window.title("Cancel Ticket")

        # Create and place relevant widgets for canceling a ticket
        ttk.Label(cancel_ticket_window, text="Ticket ID:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(cancel_ticket_window, textvariable=self.user_input1).grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(cancel_ticket_window, text="Submit", command=self.submit_cancellation).grid(row=1, column=1, pady=10)

    def submit_cancellation(self):
        # Simulate cancellation logic (placeholder)
        ticket_id = self.user_input1.get()

        # Display a confirmation message
        messagebox.showinfo("Ticket Cancellation", f"Ticket ID {ticket_id} canceled successfully.")


if __name__ == "__main__":
    root = tk.Tk()
    app = AerobookGUI(root)
    root.mainloop()
