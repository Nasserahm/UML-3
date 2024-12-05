import unittest
import pickle
from typing import Dict, List, Tuple
from datetime import datetime
from datetime import datetime
from typing import List
import os  


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

class User:
    def __init__(self, user_id: str, name: str, email: str, user_type: str, password: str):
        self._user_id = user_id
        self._name = name
        self._email = email
        self._user_type = user_type
        self._password = password

    # Getters
    def get_user_id(self) -> str:
        return self._user_id

    def get_name(self) -> str:
        return self._name

    def get_email(self) -> str:
        return self._email

    def get_user_type(self) -> str:
        return self._user_type

    def get_password(self) -> str:
        if self._password is None:
            raise ValueError("Password has not been set")
        return self._password

    # Setters
    def set_user_id(self, user_id: str):
        self._user_id = user_id

    def set_name(self, name: str):
        self._name = name

    def set_email(self, email: str):
        if "@" not in email or "." not in email:
            raise ValueError("Invalid email format.")
        self._email = email
    
    def set_password(self, password: str):
        if not password or len(password) < 6:  # Basic password validation
            raise ValueError("Password must be at least 6 characters long")
        self._password = password

    def set_user_type(self, user_type: str):
        if user_type not in ["Customer", "Admin"]:
            raise ValueError("Invalid user type. Must be 'Customer' or 'Admin'.")
        self._user_type = user_type

    # Method for displaying user info
    def display_info(self):
        return f"User ID: {self._user_id}, Name: {self._name}, Email: {self._email}, User Type: {self._user_type}"


class Customer(User):
    def __init__(self, user_id: str, name: str, email: str, password: str, permissions: list[str] = None):
        super().__init__(user_id, name, email, user_type="Customer", password=password)
        # Set default permissions if not provided
        self._permissions = permissions if permissions else [
            "View own account", 
            "Update account info", 
            "Place ticket orders", 
            "Cancel orders", 
            "View booking history", 
            "Browse available tickets",
            "View events and attractions"
        ]

    # Getter and Setter for permissions
    def get_permissions(self) -> list[str]:
        return self._permissions

    def set_permissions(self, permissions: list[str]):
        if not isinstance(permissions, list):
            raise ValueError("Permissions must be a list of strings.")
        self._permissions = permissions

    # Method to add a permission
    def add_permission(self, permission: str):
        if permission not in self._permissions:
            self._permissions.append(permission)

    # Method to remove a permission
    def remove_permission(self, permission: str):
        if permission in self._permissions:
            self._permissions.remove(permission)

    # Override display_info
    def display_info(self):
        base_info = super().display_info()
        permissions = ", ".join(self._permissions)
        return f"{base_info}, Permissions: [{permissions}]"


class Admin(User):
    def __init__(self, user_id: str, name: str, email: str, password: str, permissions: list[str] = None):
        super().__init__(user_id, name, email, user_type="Admin", password=password)
        # Set default permissions if not provided
        self._permissions = permissions if permissions else [
            "Create, Update, Delete users", 
            "Manage ticket bookings", 
            "Modify booking statuses", 
            "View all transactions", 
            "Generate booking reports", 
            "Manage system settings", 
            "Modify user permissions", 
            "Audit trail", 
            "Manage content"
        ]

    # Getter and Setter for permissions
    def get_permissions(self) -> list[str]:
        return self._permissions

    def set_permissions(self, permissions: list[str]):
        if not isinstance(permissions, list):
            raise ValueError("Permissions must be a list of strings.")
        self._permissions = permissions

    # Method to add a permission
    def add_permission(self, permission: str):
        if permission not in self._permissions:
            self._permissions.append(permission)

    # Method to remove a permission
    def remove_permission(self, permission: str):
        if permission in self._permissions:
            self._permissions.remove(permission)

    # Override display_info
    def display_info(self):
        base_info = super().display_info()
        permissions = ", ".join(self._permissions)
        return f"{base_info}, Permissions: [{permissions}]"

class Order:
    VALID_STATUSES = ["Pending", "Confirmed", "Cancelled"]  # Ensure "Confirmed" is included

    def __init__(self, order_id: str, user_id: str, tickets: List[Ticket]):
        self._order_id = order_id
        self._user_id = user_id
        self._tickets = tickets
        self._order_date = datetime.now()  # Automatically sets the order date
        self._status = "Pending"

    # Getters
    def get_order_id(self) -> str:
        return self._order_id

    def get_user_id(self) -> str:
        return self._user_id

    def get_tickets(self) -> List[Ticket]:
        return self._tickets

    def get_order_date(self) -> datetime:
        return self._order_date

    def get_status(self) -> str:
        return self._status

    # Setters
    def set_status(self, status: str):
        if status not in self.VALID_STATUSES:
            raise ValueError("Invalid order status.")
        self._status = status

    # Method to calculate the total price of the order
    def calculate_total_price(self) -> float:
        total = sum(ticket.calculate_discounted_price() for ticket in self._tickets)
        return total

    # Method to display order details
    def display_order_details(self) -> str:
        ticket_details = "\n".join(
            [
                f"Ticket Type: {ticket.get_ticket_type()}, Price: {ticket.calculate_discounted_price():.2f}"
                for ticket in self._tickets
            ]
        )
        return (
            f"Order ID: {self._order_id}\n"
            f"User ID: {self._user_id}\n"
            f"Order Date: {self._order_date.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Status: {self._status}\n"
            f"Tickets:\n{ticket_details}\n"
            f"Total Price: {self.calculate_total_price():.2f}"
        )

class Payment:
    def __init__(self, payment_id: str, order_id: str, user_id: str, amount: float, payment_method: str):
        self._payment_id = payment_id
        self._order_id = order_id
        self._user_id = user_id
        self._amount = amount
        self._payment_method = payment_method  # e.g., "Credit Card", "PayPal", "M-PESA"
        self._status = "Pending"  # Default payment status

    # Getters
    def get_payment_id(self) -> str:
        return self._payment_id

    def get_order_id(self) -> str:
        return self._order_id

    def get_user_id(self) -> str:
        return self._user_id

    def get_amount(self) -> float:
        return self._amount

    def get_payment_method(self) -> str:
        return self._payment_method

    def get_status(self) -> str:
        return self._status

    # Setters
    def set_status(self, status: str):
        if status not in ["Pending", "Completed", "Failed"]:
            raise ValueError("Invalid payment status.")
        self._status = status

    # Method to display payment details
    def display_payment_details(self) -> str:
        return (
            f"Payment ID: {self._payment_id}\n"
            f"Order ID: {self._order_id}\n"
            f"User ID: {self._user_id}\n"
            f"Amount: {self._amount:.2f}\n"
            f"Payment Method: {self._payment_method}\n"
            f"Status: {self._status}"
        )


class AccountManagement:
    def __init__(self):
        self._users: Dict[str, User] = {}  # Dictionary to store users by user ID
        self._active_user: User = None  # Tracks the currently logged-in user
        self.load_users()  # Load users when initializing

    USERS_FILE = "users.pkl"

    # Load users from the pickle file
    def load_users(self):
        try:
            with open(self.USERS_FILE, 'rb') as file:
                self._users = pickle.load(file)
        except FileNotFoundError:
            print("No existing user data found.")
            self._users = {}  # Initialize to empty if file not found

    # Save users to the pickle file
    def save_users(self):
        with open(self.USERS_FILE, 'wb') as file:
            pickle.dump(self._users, file)

    # Create user (either Customer or Admin)
    def create_user(self, user_id: str, name: str, email: str, user_type: str, password: str):
        if user_id in self._users:
            print("User ID already exists.")
            return
        if user_type == "Customer":
            self._users[user_id] = Customer(user_id, name, email, password)
            print(f"User '{name}' with role '{user_type}' created successfully.")
        elif user_type == "Admin":
            self._users[user_id] = Admin(user_id, name, email, password)
            print(f"User '{name}' with role '{user_type}' created successfully.")
        else:
            raise ValueError("Invalid user type.")
        
        self.save_users()  # Save users after creation

    # Login a user
    def login(self, user_id: str, password: str) -> bool:
        try:
            if user_id in self._users:
                user = self._users[user_id]
                if user.get_password() == password:
                    self._active_user = user
                    return True
                else:
                    raise ValueError("Invalid password.")
            else:
                raise ValueError("User not found.")
        except ValueError as e:
            print(e)
            return False
        
    def get_active_user(self):
        return self._active_user

    # Logout the currently logged-in user
    def logout(self):
        if self._active_user:
            self._active_user = None
        else:
            print("No user is currently logged in.")

    # CRUD Operations for User
    def get_user(self, user_id: str) -> User:
        if user_id in self._users:
            return self._users[user_id]
        else:
            print("User not found.")
            return None

    def delete_user(self, user_id: str):
        if not self._active_user:
            print("You must be logged in to delete a user.")
            return
        
        if self._active_user.get_user_type() != "Admin":
            print("Only admins can delete users.")
            return
        
        try:
            if user_id in self._users:
                del self._users[user_id]
                self.save_users()  # Save changes after deletion
                print(f"User {user_id} deleted successfully.")
            else:
                raise ValueError("User not found.")
        except ValueError as e:
            print(e)

    def update_user(self, user_id: str, **kwargs):
        if not self._active_user:
            print("You must be logged in to update your account.")
            return
        
        if user_id != self._active_user.get_user_id():
            print("You can only update your own account.")
            return
        
        if user_id not in self._users:
            raise ValueError("User not found.")
        
        user = self._users[user_id]
        
        for key, value in kwargs.items():
            if key == 'name':
                user.set_name(value)
            elif key == 'email':
                user.set_email(value)
            elif key == 'password':
                user.set_password(value)
            elif key == 'user_type':
                user.set_user_type(value)
            else:
                raise ValueError(f"Invalid attribute: {key}")
        
        self.save_users()  # Save changes after update
        print(f"User {user_id} updated successfully.")

    def display_all_users(self):
        """
        Display information for all users in the system.
        Returns a list of user information strings.
        """
        if not self._users:
            print("No users found in the system.")
            return []        
        
        for user_id, user in self._users.items():
            user_info = user.display_info()
            print(user_info)
            


class OrderPaymentManager:
    ORDERS_FILE = "orders.pkl"
    PAYMENTS_FILE = "payments.pkl"

    def __init__(self):
        self._orders: Dict[str, Order] = {}
        self._payments: Dict[str, Payment] = {}

    # Load orders from the pickle file
    def load_orders(self):
        try:
            with open(self.ORDERS_FILE, 'rb') as file:
                self._orders = pickle.load(file)
        except FileNotFoundError:
            print("No existing order data found.")

    # Save orders to the pickle file
    def save_orders(self):
        with open(self.ORDERS_FILE, 'wb') as file:
            pickle.dump(self._orders, file)

    # Load payments from the pickle file
    def load_payments(self):
        try:
            with open(self.PAYMENTS_FILE, 'rb') as file:
                self._payments = pickle.load(file)
        except FileNotFoundError:
            print("No existing payment data found.")

    # Save payments to the pickle file
    def save_payments(self):
        with open(self.PAYMENTS_FILE, 'wb') as file:
            pickle.dump(self._payments, file)

    # Add an order
    def add_order(self, order: Order):
        if order.get_order_id() in self._orders:
            print(f"Order ID {order.get_order_id()} already exists.")
            return
        self._orders[order.get_order_id()] = order
        self.save_orders()
        print(f"Order {order.get_order_id()} added successfully.")

    # Add a payment
    def add_payment(self, payment: Payment):
        if payment._payment_id in self._payments:
            print(f"Payment ID {payment._payment_id} already exists.")
            return
        self._payments[payment._payment_id] = payment
        self.save_payments()
        print(f"Payment {payment._payment_id} added successfully.")

    # Display all orders
    def display_all_orders(self):
        if not self._orders:
            print("No orders found.")
        for order_id, order in self._orders.items():
            print(order.display_order_details())

    # Display all payments
    def display_all_payments(self):
        if not self._payments:
            print("No payments found.")
        for payment_id, payment in self._payments.items():
            print(
                f"Payment ID: {payment._payment_id}, "
                f"Order ID: {payment._order_id}, "
                f"User ID: {payment._user_id}, "
                f"Amount: {payment._amount:.2f}, "
                f"Method: {payment._payment_method}"
            )

    # Add this new method
    def create_order(self, order_id: str, user_id: str, tickets: List[Ticket]):
        if order_id in self._orders:
            print(f"Order ID {order_id} already exists.")
            return
        new_order = Order(order_id, user_id, tickets)
        self._orders[order_id] = new_order
        self.save_orders()
        print(f"Order {order_id} created successfully.")

    # Add this new method
    def get_order(self, order_id: str) -> Order:
        if order_id not in self._orders:
            raise ValueError(f"Order ID {order_id} not found.")
        return self._orders[order_id]

    # Add this method too since it's used later in the code
    def get_payment(self, payment_id: str) -> Payment:
        if payment_id not in self._payments:
            raise ValueError(f"Payment ID {payment_id} not found.")
        return self._payments[payment_id]

    # And this method which is used in the test code
    def update_order_status(self, order_id: str, status: str):
        order = self.get_order(order_id)
        order.set_status(status)
        self.save_orders()

    # And this method for calculating total revenue
    def calculate_total_revenue(self) -> float:
        return sum(payment.get_amount() for payment in self._payments.values())

    # Add this new method
    def create_payment(self, payment_id: str, order_id: str, user_id: str, amount: float, payment_method: str):
        if payment_id in self._payments:
            print(f"Payment ID {payment_id} already exists.")
            return
        new_payment = Payment(payment_id, order_id, user_id, amount, payment_method)
        self._payments[payment_id] = new_payment
        self.save_payments()
        print(f"Payment {payment_id} created successfully.")


class DataManager:
    USERS_FILE = "users.pkl"
    ORDERS_FILE = "orders.pkl"
    PAYMENTS_FILE = "payments.pkl"
    TICKETS_FILE = "tickets.pkl"

    def __init__(self):
        self._users: Dict[str, User] = {}
        self._orders: Dict[str, Order] = {}
        self._payments: Dict[str, Payment] = {}
        self._tickets: Dict[str, Ticket] = {}

    # Load users from the pickle file
    def load_users(self):
        try:
            with open(self.USERS_FILE, "rb") as f:  # Open in binary mode
                self._users = pickle.load(f)
        except (FileNotFoundError, EOFError):
            self._users = {}  # Initialize to empty if file not found or empty

    # Save users to the pickle file
    def save_users(self):
        with open(self.USERS_FILE, "wb") as f:  # Open in binary mode
            pickle.dump(self._users, f)

    # Load orders from the pickle file
    def load_orders(self):
        try:
            with open(self.ORDERS_FILE, "rb") as f:  # Open in binary mode
                self._orders = pickle.load(f)
        except (FileNotFoundError, EOFError):
            self._orders = {}  # Initialize to empty if file not found or empty

    # Save orders to the pickle file
    def save_orders(self):
        with open(self.ORDERS_FILE, "wb") as f:  # Open in binary mode
            pickle.dump(self._orders, f)

    # Load payments from the pickle file
    def load_payments(self):
        try:
            with open(self.PAYMENTS_FILE, "rb") as f:  # Open in binary mode
                self._payments = pickle.load(f)
        except (FileNotFoundError, EOFError):
            self._payments = {}  # Initialize to empty if file not found or empty

    # Save payments to the pickle file
    def save_payments(self):
        with open(self.PAYMENTS_FILE, "wb") as f:  # Open in binary mode
            pickle.dump(self._payments, f)

    # Load tickets from the pickle file
    def load_tickets(self):
        try:
            with open(self.TICKETS_FILE, "rb") as f:  # Open in binary mode
                self._tickets = pickle.load(f)
        except (FileNotFoundError, EOFError):
            self._tickets = {}  # Initialize to empty if file not found or empty

    # Save tickets to the pickle file
    def save_tickets(self):
        with open(self.TICKETS_FILE, "wb") as f:  # Open in binary mode
            pickle.dump(self._tickets, f)

class TicketBookingSystem:
    def __init__(self):
        self.data_manager = DataManager()  # Use DataManager for data handling
        self.data_manager.load_users()  # Load users
        self.data_manager.load_orders()  # Load orders
        self.data_manager.load_payments()  # Load payments
        self.data_manager.load_tickets()  # Load tickets

        # Initialize orders as a list of Order objects
        self.orders = list(self.data_manager._orders.values())  # Ensure this is a list of Order objects

        # Check if tickets are loaded, if not load default tickets
        if not self.data_manager._tickets:
            self.tickets = self.load_default_tickets()
            self.data_manager._tickets = self.tickets  # Save default tickets to DataManager
            self.data_manager.save_tickets()  # Save tickets to the file
        else:
            self.tickets = self.data_manager._tickets  # Use loaded tickets

        self.current_user = None  # Track the currently logged-in user
        self.account_management = AccountManagement()  # Initialize AccountManagement

    def load_default_tickets(self):
        return {
            "Single-Day Pass": Ticket(
                "Single-Day Pass", 275, "1 day", "Access to the park for one day", "Valid only on selected date", 0.0
            ),
            "Two-Day Pass": Ticket(
                "Two-Day Pass", 480, "2 days", "Access to the park for two consecutive days", "Cannot be split over multiple trips", 0.0
            ),
            "Annual Membership": Ticket(
                "Annual Membership", 1840, "1 year", "Unlimited access for one year", "Must be used by the same person", 10.0
            ),
            "Child Ticket": Ticket(
                "Child Ticket", 185, "1 day", "Discounted ticket for children (ages 3-12)", 
                "Valid only on selected date, must be accompanied by an adult", 15.0
            ),
            "Group Ticket (10+)": Ticket(
                "Group Ticket (10+)", 220, "1 day", "Special rate for groups of 10 or more", 
                "Must be booked in advance, 20% off for groups of 10 or more", 20.0
            ),
            "VIP Experience Pass": Ticket(
                "VIP Experience Pass", 550, "1 day", "Includes expedited access and reserved seating for shows", 
                "Limited availability, must be purchased in advance", 5.0
            ),
        }

    def main_menu(self):
        while True:
            print("\n--- Main Menu ---")
            print("1. Login")
            print("2. Book Tickets")
            print("3. Orders and Payments (sub-menu)")
            print("4. Manage Accounts")
            print("5. Logout")
            print("6. Exit")
            choice = input("Choose an option: ")

            if choice == '1':
                self.login()  # Call the login method
            elif choice == '2':
                if not self.current_user:
                    print("You must be logged in to book tickets.")
                else:
                    self.book_tickets()
            elif choice == '3':
                if not self.current_user:
                    print("You must be logged in to access orders and payments.")
                else:
                    self.order_menu()  # Call the order menu
            elif choice == '4':
                if not self.current_user:
                    print("You must be logged in to manage accounts.")
                else:
                    self.manage_accounts()
            elif choice == '5':
                self.logout()
            elif choice == '6':
                print("Exiting the system.")
                break
            else:
                print("Invalid option. Please try again.")

    def order_menu(self):
        while True:
            print("\n--- Order Menu ---")
            print("1. View Orders")
            print("2. Pay for Order")
            print("3. View Order History")
            print("4. Back to Main Menu")
            choice = input("Choose an option: ")

            if choice == '1':
                self.view_user_orders()
            elif choice == '2':
                self.pay_for_order()
            elif choice == '3':
                self.view_order_history()
            elif choice == '4':
                break  # Go back to the main menu
            else:
                print("Invalid option. Please try again.")

    def view_tickets(self):
        print("\n--- Available Tickets ---")
        for ticket_name, ticket in self.tickets.items():
            print(
                f"{ticket_name}: ${ticket.get_price():.2f} - {ticket.get_description()} "
                f"(Discount: {ticket.get_discount()}%)"
            )

    def book_tickets(self):
        if not self.current_user:
            print("You must be logged in to book tickets.")
            return

        print("\n--- Book Tickets ---")
        self.view_tickets()
        ticket_name = input("Enter the name of the ticket to book: ")
        if ticket_name not in self.tickets:
            print("Invalid ticket name. Please try again.")
            return

        try:
            quantity = int(input("Enter the quantity: "))
            if quantity <= 0:
                raise ValueError("Quantity must be greater than zero.")
        except ValueError as e:
            print(f"Error: {e}")
            return

        ticket = self.tickets[ticket_name]
        discounted_price = ticket.calculate_discounted_price()
        total_price = discounted_price * quantity
        print(f"Total price: ${total_price:.2f}")

        confirmation = input("Confirm booking? (y/n): ").strip().lower()
        if confirmation == 'y':
            # Generate a unique order ID with 'ORD' prefix
            if self.orders:
                # Extract the numeric part of the last order ID
                last_order_id = self.orders[-1].get_order_id()  # Get the last order ID
                numeric_part = int(last_order_id[3:])  # Extract numeric part after 'ORD'
                order_id = f"ORD{numeric_part + 1:03d}"  # Increment and format with leading zeros
            else:
                order_id = "ORD001"  # Start with the first order ID

            order = Order(order_id, self.current_user.get_user_id(), [ticket] * quantity)
            self.orders.append(order)  # Append the new order to the orders list
            print(f"Booking successful! Order ID: {order_id}")
        else:
            print("Booking canceled.")

    def view_orders(self):
        if not self.current_user:
            print("You must be logged in to view orders.")
            return
        
        print("\n--- View Orders ---")
        user_orders = [order for order in self.orders if order.get_user_id() == self.current_user.get_user_id()]
        if not user_orders:
            print("No orders found.")
            return

        for order in user_orders:
            print(f"Order ID: {order.get_order_id()}, Tickets: {len(order.get_tickets())}, "
                  f"Date: {order.get_order_date()}, Status: {order.get_status()}")

    def manage_accounts(self):
        print("\n--- Account Management ---")
        if self.account_management.get_active_user().get_user_type() != "Admin":
            self.account_management.display_all_users()#
        
        print("1. Create User")
        print("2. Delete User")
        print("3. Update User")
        print("4. Back to Main Menu")
        choice = input("Choose an option: ")

        if choice == '1':
            # Allow user to create a new account without being logged in
            user_id = input("Enter User ID: ")
            name = input("Enter Name: ")
            email = input("Enter Email: ")
            user_type = input("Enter User Type (Customer/Admin): ")
            password = input("Enter Password: ")
            self.account_management.create_user(user_id, name, email, user_type, password)
        elif choice == '2':
            if not self.account_management.get_active_user():
                print("You must be logged in to delete a user.")
                return
            user_id = input("Enter User ID to delete: ")
            self.account_management.delete_user(user_id)  # This will now check for admin
        elif choice == '3':
            if not self.account_management.get_active_user():
                print("You must be logged in to update your account.")
                return
            user_id = self.account_management.get_active_user().get_user_id()  # Get the current user's ID
            updates = {}
            updates['name'] = input("Enter new name (leave blank to skip): ").strip() or None
            updates['email'] = input("Enter new email (leave blank to skip): ").strip() or None
            updates['password'] = input("Enter new password (leave blank to skip): ").strip() or None
            updates = {k: v for k, v in updates.items() if v}
            self.account_management.update_user(user_id, **updates)  # Update own account

    def login(self):
        print("\n--- Login ---")
        user_id = input("Enter User ID: ")
        password = input("Enter Password: ")
        success = self.account_management.login(user_id, password)  # Call the login method
        if success:
            self.current_user = self.account_management.get_user(user_id)  # Get the user object
            print(f"Login successful. Welcome, {self.current_user.get_name()}.")
        else:
            print("Login failed. Please try again.")

    def logout(self):
        if self.current_user:
            print(f"Goodbye, {self.current_user.get_name()}.")
            self.current_user = None
        else:
            print("No user is logged in.")

    def pay_for_order(self):
        if not self.current_user:
            print("You must be logged in to pay for an order.")
            return

        print("\n--- Pay for Order ---")
        user_orders = [order for order in self.orders if order.get_user_id() == self.current_user.get_user_id()]

        if not user_orders:
            print("No orders found for your account.")
            return

        for order in user_orders:
            total_price = sum(ticket.get_price() for ticket in order.get_tickets())  # Calculate total price
            print(f"Order ID: {order.get_order_id()}, Status: {order.get_status()}, Total Price: ${total_price:.2f}")

        order_id = input("Enter the Order ID you want to pay for: ")
        order = next((o for o in user_orders if o.get_order_id() == order_id), None)

        if order is None:
            print("Order not found.")
            return

        if order.get_status() != "Pending":
            print("You can only pay for orders with a status of 'Pending'.")
            return

        # Calculate total price for the selected order
        total_price = sum(ticket.get_price() for ticket in order.get_tickets())
        print(f"Total amount due for Order ID {order_id}: ${total_price:.2f}")

        # Simulate payment processing
        confirmation = input("Confirm payment? (y/n): ").strip().lower()
        if confirmation == 'y':
            print(f"Current status before payment: {order.get_status()}")  # Debugging line
            order.set_status("Confirmed")  # Update order status to confirmed
            print(f"New status after payment: {order.get_status()}")  # Debugging line
            print(f"Payment successful! Order ID: {order_id} is now confirmed.")
        else:
            print("Payment canceled.")

    def view_user_orders(self):
        if not self.current_user:
            print("You must be logged in to view your orders.")
            return

        print("\n--- Your Orders ---")
        user_orders = [order for order in self.orders if order.get_user_id() == self.current_user.get_user_id()]

        if not user_orders:
            print("No orders found for your account.")
            return

        for order in user_orders:
            print(f"Order ID: {order.get_order_id()}, Status: {order.get_status()}")

    def view_order_history(self):
        if not self.current_user:
            print("You must be logged in to view your order history.")
            return

        print("\n--- Order History ---")
        confirmed_orders = [order for order in self.orders if order.get_status() == "Confirmed" and order.get_user_id() == self.current_user.get_user_id()]

        if not confirmed_orders:
            print("No confirmed orders found.")
            return

        for order in confirmed_orders:
            print(f"Order ID: {order.get_order_id()}, Status: {order.get_status()}, Tickets: {len(order.get_tickets())}, Date: {order.get_order_date()}")

    def run(self):
        try:
            while True:
                self.main_menu()
        finally:
            self.data_manager.save_users()  # Save users on exit
            self.data_manager.save_orders()  # Save orders on exit
            self.data_manager.save_payments()  # Save payments on exit


if __name__ == "__main__":
    # Initialize the ticket booking system
    booking_system = TicketBookingSystem()
    
    # Run the system
    booking_system.run()

