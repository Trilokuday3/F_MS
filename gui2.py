import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv
import random
from email.mime.text import MIMEText
from Backened_code import (
    get_current_date,
    display_available_flights,
    save_booking_to_file,
    read_booked_tickets_from_file,
    write_booked_tickets_to_file,
    cancel_ticket,
    send_feedback_email,
    send_thank_you_email,
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
        self.feedback_text = None

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
        # Retrieve user inputs from GUI
        user_input_date = self.user_input3.get()
        user_input_source = self.user_input1.get()
        user_input_destination = self.user_input2.get()
        user_name = self.user_name.get()
        user_phone = self.user_phone.get()

        # Retrieve available flights from the CSV file based on user inputs
        rows = self.retrieve_available_flights_from_database(user_input_date, user_input_source, user_input_destination)

        # Display available flights
        if rows:
            flight_info = "\n".join(
                f"{count}) {row[4]}\n   Date of the journey: {row[1]}\n   Flight ID: {row[11]}\n   Arrival Time: {row[5]}\n   Departure Time: {row[6]}\n   No of Stops: {row[8]}\n   No of Seats: {row[10]}\n   Price: {row[9]}"
                for count, row in enumerate(rows, start=1)
            )
            messagebox.showinfo("Available Flights", f"The routes from {user_input_source} to {user_input_destination} are:\n{flight_info}")
            found = True
        else:
            messagebox.showinfo("No Flights Found", "No available flights found for the specified criteria.")
            found = False

            booking_details = "" 
        if found:
            FID = simpledialog.askinteger("Enter Flight ID", "Enter your Flight ID:")
            num_seats = simpledialog.askinteger("Enter Number of Seats", "Enter the number of seats you want to book:")

            # Modified the loop condition to compare only source, destination, and Flight ID
            for row in rows:
                if row[2] == user_input_source and row[3] == user_input_destination and int(row[11]) == FID:
                    available_seats = int(row[10])
                    if num_seats <= available_seats:
                        row[11] = str(int(row[11]) - 1)
                        found = True
                        ticket_id = random.randint(100000, 999999)
                        booked_tickets = read_booked_tickets_from_file()
                        booked_tickets[ticket_id] = {
                            'user_input1': user_input_source,
                            'user_input2': user_input_destination,
                            'FID': FID,
                            'num_seats': num_seats,
                            'user_name': user_name,
                            'user_phone': user_phone,
                            'booking_time': get_current_date()
                        }
                        messagebox.showinfo("Booking Successful", f"Booking Successful of {num_seats} seat(s) for the flight from {user_input_source} to {user_input_destination} in {row[0]} flight\nFlight ID: {FID}\nTicket ID: {ticket_id}\nThanks for visiting\nAerobook")
                        write_booked_tickets_to_file(booked_tickets)  # Update the file after booking

                        booking_details = f"\nSource: {user_input_source}\nDestination: {user_input_destination}\nFlight ID: {FID}\nNumber of Seats: {num_seats}\nBooking Time: {get_current_date()}"
                        flight_details = f"\nFlight Information:\nFlight Name: {row[0]}\nDate: {row[1]}\nArrival Time: {row[5]}\nDeparture Time: {row[6]}\nNo of Stops: {row[8]}\nPrice: {row[9]}"

                        user_email = simpledialog.askstring("Enter Email", "Enter the passenger's email address:")
                        send_confirmation_email(user_email, "sender_email@gmail.com", "app_password", booking_details, flight_details, user_name, user_phone, ticket_id)
                        send_thank_you_email(user_email, "sender_email@gmail.com", "app_password", is_feedback=True)

                    else:
                        messagebox.showinfo("Not Enough Seats", f"Not enough seats available for the requested number. Available seats: {available_seats}")
                    break

            if not found:
                messagebox.showinfo("Invalid Flight ID", "Invalid Flight ID or no matching flight found.")

            # Display available flights
            self.display_available_flights(rows, user_input_source, user_input_destination)

        # Send confirmation email and create PDF
        send_confirmation_email(
            to_email=user_name,
            sender_email="sender_email@gmail.com",  # Replace with actual sender email
            app_password="app_password",  # Replace with actual app password
            booking_details=booking_details,
            flight_details="Flight details placeholder",
            user_name=user_name,
            user_phone=user_phone,
            ticket_no=ticket_id,
        )

    def retrieve_available_flights_from_database(self, date, source, destination):
        # Replace 'flights.csv' with the actual name of your CSV file
        with open('flights.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)  # Skip the header row

            # Assuming the columns in your CSV file are in a specific order
            # Adjust the indices accordingly based on your actual CSV file structure
            available_flights = [row for row in reader]

        # Filter flights based on user inputs
        filtered_flights = [flight for flight in available_flights
                            if flight[1] == date and flight[2] == source and flight[3] == destination]

        return filtered_flights

    def display_available_flights(self, rows, source, destination):
        print(f"\nThe routes from {source} to {destination} on {rows[0][1]} are:")
        for count, row in enumerate(rows, start=1):
            print(
                f"{count}) {row[4]}\n   Date of the journey: {row[1]}\n   Flight ID: {row[11]}\n   Arrival Time: {row[5]}\n   Departure Time: {row[6]}\n   No of Stops: {row[8]}\n   No of Seats: {row[10]}\n   Price: {row[9]}")

    def view_flights(self):
        view_flights_window = tk.Toplevel(self.root)
        view_flights_window.title("View Flights")

        ttk.Label(view_flights_window, text="Enter Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
        date_entry = ttk.Entry(view_flights_window)
        date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(view_flights_window, text="Enter Source Station:").grid(row=1, column=0, padx=5, pady=5)
        source_entry = ttk.Entry(view_flights_window)
        source_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(view_flights_window, text="Enter Destination:").grid(row=2, column=0, padx=5, pady=5)
        destination_entry = ttk.Entry(view_flights_window)
        destination_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(view_flights_window, text="Submit", command=lambda: self.handle_view_flights(date_entry.get(), source_entry.get(), destination_entry.get())).grid(row=3, column=1, pady=10)

    def handle_view_flights(self, date, source, destination):
        # Retrieve available flights based on user inputs
        rows = self.retrieve_available_flights_from_database(date, source, destination)

        # Display available flights
        if rows:
            self.display_available_flights(rows, source, destination)
        else:
            messagebox.showinfo("No Flights Found", "No available flights found for the specified criteria.")

    def provide_feedback(self):
        feedback_window = tk.Toplevel(self.root)
        feedback_window.title("Provide Feedback")

        # Create and place relevant widgets for providing feedback
        ttk.Label(feedback_window, text="Email Address:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(feedback_window, textvariable=self.user_input1).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(feedback_window, text="Feedback:").grid(row=1, column=0, padx=5, pady=5)
        self.feedback_text = tk.Text(feedback_window, wrap=tk.WORD, width=50, height=10)
        self.feedback_text.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(feedback_window, text="Submit", command=self.submit_feedback).grid(row=2, column=1, pady=10)

    def submit_feedback(self):
        # Simulate feedback submission (placeholder)
        user_email = self.user_input1.get()
        feedback = self.feedback_text.get("1.0", tk.END)

        # Create a new window to get the email and password
        credentials_window = tk.Toplevel(self.root)
        credentials_window.title("Enter Email and Password")

        ttk.Label(credentials_window, text="Email:").grid(row=0, column=0, padx=5, pady=5)
        email_entry = ttk.Entry(credentials_window)
        email_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(credentials_window, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        password_entry = ttk.Entry(credentials_window, show="*")  # Mask the password
        password_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(credentials_window, text="Submit", command=lambda: self.send_feedback_with_credentials(feedback, user_email, email_entry.get(), password_entry.get(), credentials_window)).grid(row=2, column=1, pady=10)
        

    def send_feedback_with_credentials(self, feedback, user_email, sender_email, app_password, window):
        # Display a confirmation message
        messagebox.showinfo("Feedback Submitted", f"Feedback submitted successfully!\n\nUser Email: {user_email}")

        # Call the function to send feedback email
        send_feedback_email(feedback, user_email, sender_email, app_password)

        # Close the credentials window
        window.destroy()

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

        # Create a new window to get the user's email
        user_email_window = tk.Toplevel(self.root)
        user_email_window.title("Enter User Email")

        ttk.Label(user_email_window, text="User Email:").grid(row=0, column=0, padx=5, pady=5)
        user_email_entry = ttk.Entry(user_email_window)
        user_email_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(user_email_window, text="Submit", command=lambda: self.complete_cancellation(ticket_id, user_email_entry.get(), user_email_window)).grid(row=1, column=1, pady=10)

    def complete_cancellation(self, ticket_id, user_email, window):
        # Call the function to cancel the ticket
        ticket_found, canceled_details = cancel_ticket(
            read_booked_tickets_from_file(), ticket_id, "aerobookmrt@gmail.com", "wxpq hciv lkjt zmjf")

        # Display a confirmation message
        if ticket_found:
            messagebox.showinfo("Ticket Cancellation", f"Ticket ID {ticket_id} canceled successfully.")
            # Call the function to send cancellation email
            send_cancelation_email(
                to_email=user_email,  # Use the user's email obtained from the entry
                sender_email="aerobookmrt@gmail.com",  # Replace with actual sender email
                app_password="wxpq hciv lkjt zmjf",  # Replace with actual app password
                ticket_id=ticket_id,
                canceled_details=canceled_details,
            )
        else:
            messagebox.showinfo("Ticket Cancellation", f"Ticket ID {ticket_id} not found in the booked tickets.")

        # Close the user_email_window
        window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AerobookGUI(root)
    root.mainloop()

