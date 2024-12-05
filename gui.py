import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import datetime
import random
import pickle  # Ensure this import is at the top

class Ticket:
    def __init__(self, ticket_type: str, price: float, validity: str, description: str, restrictions: str, discount: float = 0.0):
        self._ticket_type = ticket_type
        self._price = price
        self._validity = validity
        self._description = description
        self._restrictions = restrictions
        self._discount = discount  # Default discount is 0.0

    # Getters
    def get_ticket_type(self) -> str:
        return self._ticket_type

    def get_price(self) -> float:
        return self._price

    def get_validity(self) -> str:
        return self._validity

    def get_description(self) -> str:
        return self._description

    def get_restrictions(self) -> str:
        return self._restrictions

    def get_discount(self) -> float:
        return self._discount

    # Setters
    def set_ticket_type(self, ticket_type: str):
        self._ticket_type = ticket_type

    def set_price(self, price: float):
        if price < 0:
            raise ValueError("Price cannot be negative.")
        self._price = price

    def set_validity(self, validity: str):
        self._validity = validity

    def set_description(self, description: str):
        self._description = description

    def set_restrictions(self, restrictions: str):
        self._restrictions = restrictions

    def set_discount(self, discount: float):
        if discount < 0 or discount > 100:
            raise ValueError("Discount must be between 0 and 100.")
        self._discount = discount

    # Calculate discounted price
    def calculate_discounted_price(self) -> float:
        return self._price * (1 - self._discount / 100)

class TicketBookingGUI:
    def __init__(self, master):
        self.master = master
        master.title("Ticket Booking System")
        
        # Center the main window
        self.center_window(master, 1000, 600)  # Adjust width and height as needed
        
        self.ticket_types = {
            "Single-Day Pass": Ticket("Single-Day Pass", 275.0, "1 day", 
                "Access to the park for one day", "Valid only on selected date"),
            "Two-Day Pass": Ticket("Two-Day Pass", 480.0, "2 days", 
                "Access to the park for two consecutive days", "Cannot be split over multiple trips", 10.0),
            "Annual Membership": Ticket("Annual Membership", 1840.0, "1 year", 
                "Unlimited access for one year", "Must be used by the same person", 15.0),
            "Child Ticket": Ticket("Child Ticket", 185.0, "1 day", 
                "Discounted ticket for children (ages 3-12)", "Valid only on selected date, accompanied by an adult"),
            "Group Ticket (10+)": Ticket("Group Ticket (10+)", 220.0, "1 day", 
                "Special rate for groups of 10 or more", "Must be booked in advance", 20.0),
            "VIP Experience Pass": Ticket("VIP Experience Pass", 550.0, "1 day", 
                "Includes expedited access and reserved seating", "Limited availability, must be purchased in advance")
        }
        self.create_widgets()

        # Bind tab change event to refresh orders
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_change)

        self.orders = []  # List to store booked orders

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill="both", expand=True)

        self.ticket_selection_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.ticket_selection_tab, text="Ticket Selection")
        self.create_ticket_selection_tab()

        self.account_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.account_tab, text="Account")
        self.create_account_tab()


        #Admin Tab (Password Protected)
        self.admin_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.admin_tab, text="Admin")
        self.create_admin_tab()

        # Add My Orders tab
        self.my_orders_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.my_orders_tab, text="My Orders")
        self.create_my_orders_tab()



    def create_ticket_selection_tab(self):
        # Load tickets from the .pkl file
        self.load_tickets()

        # Create frame for the table
        table_frame = ttk.Frame(self.ticket_selection_tab)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Create Treeview
        columns = ('Ticket Type', 'Price', 'Validity', 'Description', 'Restrictions')
        self.ticket_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=8)

        # Define column headings and widths
        widths = {
            'Ticket Type': 120,
            'Price': 100,
            'Validity': 100,
            'Description': 250,
            'Restrictions': 300
        }

        for col in columns:
            self.ticket_tree.heading(col, text=col)
            self.ticket_tree.column(col, width=widths[col])

        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.ticket_tree.yview)
        x_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.ticket_tree.xview)
        self.ticket_tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        # Insert ticket data
        for ticket in self.ticket_types.values():
            price_display = f"${ticket.calculate_discounted_price():.2f}"
            if ticket.get_discount() > 0:
                price_display += f" (-{ticket.get_discount()}%)"
                
            self.ticket_tree.insert('', 'end', values=(
                ticket.get_ticket_type(),
                price_display,
                ticket.get_validity(),
                ticket.get_description(),
                ticket.get_restrictions()
            ))

        # Pack the Treeview and scrollbars
        self.ticket_tree.pack(side=tk.LEFT, fill="both", expand=True)
        y_scrollbar.pack(side=tk.RIGHT, fill="y")
        x_scrollbar.pack(side=tk.BOTTOM, fill="x")

        # Create booking controls frame
        booking_frame = ttk.LabelFrame(self.ticket_selection_tab, text="Booking Details")
        booking_frame.pack(fill="x", padx=10, pady=5)

        # Ticket quantity
        ttk.Label(booking_frame, text="Quantity:").grid(row=0, column=0, padx=5, pady=5)
        self.quantity_var = tk.StringVar(value="1")
        self.quantity_spinbox = ttk.Spinbox(
            booking_frame, 
            from_=1, 
            to=20, 
            textvariable=self.quantity_var,
            width=5
        )
        self.quantity_spinbox.grid(row=0, column=1, padx=5, pady=5)

        # Visit date
        ttk.Label(booking_frame, text="Visit Date:").grid(row=0, column=2, padx=5, pady=5)
        self.date_picker = DateEntry(
            booking_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            mindate=datetime.date.today()
        )
        self.date_picker.grid(row=0, column=3, padx=5, pady=5)

        # Book button
        self.book_button = ttk.Button(
            booking_frame,
            text="Book Selected Ticket",
            command=self.book_ticket
        )
        self.book_button.grid(row=0, column=4, padx=20, pady=5)

        # Bind selection event
        self.ticket_tree.bind('<<TreeviewSelect>>', self.on_ticket_select)

    def on_ticket_select(self, event):
        """Handle ticket selection"""
        selected_items = self.ticket_tree.selection()
        if not selected_items:
            self.book_button.configure(state='disabled')
            return
        
        self.book_button.configure(state='normal')

    def book_ticket(self):
        """Handle ticket booking"""
        selected_items = self.ticket_tree.selection()
        if not selected_items:
            self.show_message("Selection Required", "Please select a ticket type first.", "warning")
            return

        try:
            selected_item = self.ticket_tree.item(selected_items[0])
            ticket_type = selected_item['values'][0]
            quantity = int(self.quantity_var.get())
            visit_date = self.date_picker.get_date()
            
            ticket = self.ticket_types[ticket_type]
            total_price = ticket.calculate_discounted_price() * quantity

            # Include discount information in the message if applicable
            discount_info = f"\nDiscount Applied: {ticket.get_discount()}%" if ticket.get_discount() > 0 else ""
            
            message = f"Booking Summary:\n\n" \
                     f"Ticket Type: {ticket_type}\n" \
                     f"Quantity: {quantity}\n" \
                     f"Visit Date: {visit_date}\n" \
                     f"Original Price: ${ticket.get_price():.2f}{discount_info}\n" \
                     f"Total Price: ${total_price:.2f}\n\n" \
                     f"Proceed with booking?"

            if self.show_message("Confirm Booking", message, "question"):
                # Generate a simple order ID (in a real app, this would come from a database)
                order_id = f"ORD{random.randint(1000, 9999)}"
                
                # Add to orders list
                self.orders.append((order_id, visit_date.strftime("%Y-%m-%d"), ticket_type, str(quantity), f"${total_price:.2f}", "Confirmed"))
                
                # Add to orders tree
                self.orders_tree.insert('', 'end', values=(
                    order_id,
                    visit_date.strftime("%Y-%m-%d"),
                    ticket_type,
                    str(quantity),
                    f"${total_price:.2f}",
                    "Confirmed"
                ))

                # Save tickets after booking
                self.save_tickets()
                
                self.show_message("Success", "Booking completed successfully!", "info")
                
        except Exception as e:
            self.show_message("Error", f"An error occurred: {str(e)}", "error")

    def create_account_tab(self):
        #Login/Registration widgets
        login_button = ttk.Button(self.account_tab, text="Login", command=self.show_login)
        login_button.pack(pady=10)
        register_button = ttk.Button(self.account_tab, text="Register", command=self.show_register)
        register_button.pack(pady=10)
        self.login_window = None
        self.register_window = None

    def show_login(self):
        if not self.login_window:
            self.login_window = tk.Toplevel(self.master)
            self.login_window.title("Login")
            self.center_window(self.login_window, 300, 200)
            self.login_window.grab_set()  # Make window modal

    def show_register(self):
        if not self.register_window:
            self.register_window = tk.Toplevel(self.master)
            self.register_window.title("Register")
            self.center_window(self.register_window, 400, 300)
            self.register_window.grab_set()  # Make window modal

    def create_admin_tab(self):
        password_label = ttk.Label(self.admin_tab, text="Password:")
        password_label.grid(row=0, column=0, sticky="w")
        self.password_entry = ttk.Entry(self.admin_tab, show="*", width=20)
        self.password_entry.grid(row=0, column=1, sticky="ew")

        login_button = ttk.Button(self.admin_tab, text="Login", command=self.check_admin_password)
        login_button.grid(row=1, column=1, sticky="e")

    def check_admin_password(self):
        password = self.password_entry.get()
        if password == "admin": #Replace with actual password checking mechanism
            #Display admin dashboard
            messagebox.showinfo("Success", "Access Granted")

        else:
            messagebox.showerror("Error", "Incorrect password")

    def center_window(self, window, width=None, height=None):
        """Center any window or toplevel widget"""
        # Get screen dimensions
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        # If width/height not provided, use window's requested size
        if width is None:
            width = window.winfo_reqwidth()
        if height is None:
            height = window.winfo_reqheight()
        
        # Calculate position coordinates
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Set window size and position
        window.geometry(f'{width}x{height}+{x}+{y}')

    def show_message(self, title, message, message_type="info"):
        """Show centered message boxes"""
        # Create a messagebox window
        if message_type == "info":
            dialog = messagebox.showinfo(title, message)
        elif message_type == "warning":
            dialog = messagebox.showwarning(title, message)
        elif message_type == "error":
            dialog = messagebox.showerror(title, message)
        elif message_type == "question":
            dialog = messagebox.askyesno(title, message)
        
        # Get the messagebox window
        for window in self.master.winfo_children():
            if isinstance(window, tk.Toplevel):
                self.center_window(window)
        
        return dialog

    def create_my_orders_tab(self):
        # Create frame for the orders table
        table_frame = ttk.Frame(self.my_orders_tab)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Create Treeview for orders
        columns = ('Order ID', 'Date', 'Ticket Type', 'Quantity', 'Total Price', 'Status')
        self.orders_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=10)

        # Define column headings and widths
        widths = {
            'Order ID': 100,
            'Date': 100,
            'Ticket Type': 200,
            'Quantity': 80,
            'Total Price': 100,
            'Status': 100
        }

        for col in columns:
            self.orders_tree.heading(col, text=col)
            self.orders_tree.column(col, width=widths[col])

        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.orders_tree.yview)
        x_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.orders_tree.xview)
        self.orders_tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        # Pack the Treeview and scrollbars
        self.orders_tree.pack(side=tk.LEFT, fill="both", expand=True)
        y_scrollbar.pack(side=tk.RIGHT, fill="y")
        x_scrollbar.pack(side=tk.BOTTOM, fill="x")

        # Add buttons frame
        button_frame = ttk.Frame(self.my_orders_tab)
        button_frame.pack(fill="x", padx=10, pady=5)

        # Add refresh button
        refresh_button = ttk.Button(
            button_frame,
            text="Refresh Orders",
            command=self.refresh_orders
        )
        refresh_button.pack(side=tk.LEFT, padx=5)

        # Add cancel order button
        cancel_button = ttk.Button(
            button_frame,
            text="Cancel Selected Order",
            command=self.cancel_order
        )
        cancel_button.pack(side=tk.LEFT, padx=5)

    def refresh_orders(self):
        """Refresh the orders list"""
        # Clear existing items
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)

        # Add booked orders to the orders tree
        for order in self.orders:
            self.orders_tree.insert('', 'end', values=order)

    def cancel_order(self):
        """Cancel the selected order"""
        selected_items = self.orders_tree.selection()
        if not selected_items:
            self.show_message("Selection Required", "Please select an order to cancel.", "warning")
            return

        selected_item = self.orders_tree.item(selected_items[0])
        order_id = selected_item['values'][0]
        
        # Confirm cancellation
        if self.show_message("Confirm Cancellation", 
                           f"Are you sure you want to cancel order {order_id}?", 
                           "question"):
            # Here you would typically update the database
            # For now, just remove from the tree
            self.orders_tree.delete(selected_items[0])
            self.show_message("Success", "Order cancelled successfully!", "info")

    def on_tab_change(self, event):
        """Handle tab change events"""
        current_tab = self.notebook.select()
        tab_name = self.notebook.tab(current_tab, "text")
        
        if tab_name == "My Orders":
            self.refresh_orders()

    def save_tickets(self):
        """Save tickets to a .pkl file."""
        try:
            with open('tickets.pkl', 'wb') as file:
                # Save only unique tickets
                unique_tickets = {ticket.get_ticket_type(): ticket for ticket in self.ticket_types.values()}
                pickle.dump(unique_tickets, file)
        except Exception as e:
            self.show_message("Error", f"Failed to save tickets: {str(e)}", "error")

    def load_tickets(self):
        """Load tickets from a .pkl file."""
        try:
            with open('tickets.pkl', 'rb') as file:
                loaded_tickets = pickle.load(file)
                for ticket_type, ticket in loaded_tickets.items():
                    if ticket_type not in self.ticket_types:
                        self.ticket_types[ticket_type] = ticket
        except FileNotFoundError:
            # If the file does not exist, we can ignore it
            pass
        except Exception as e:
            self.show_message("Error", f"Failed to load tickets: {str(e)}", "error")

# When creating the main window
if __name__ == "__main__":
    root = tk.Tk()
    gui = TicketBookingGUI(root)
    root.mainloop()
