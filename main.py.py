# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 14:24:15 2023

@author: Joseph Martin Gatmaitan, Rene Allen Garcia, Oluleke John Okunade
"""

# ---- IMPORTS ----
import re
from datetime import date
# Sets the padding for all screen titles
title_padding = 40

# Initialize users_list to store registered users
users_list = []
# Initialize orders_list to store orders
orders_list = []
# Current signed in customer object 
signed_user = None 
# Current order being processed
current_order = None 
# --- CLASSES --- 

class Customers:
    fullname = ''
    mobile_no = ''
    date_of_birth = ''
    password = ''
    address = ''
    __error_msg = ''
    
    
    def __init__(self, fullname, mobile_no, date_of_birth, password):
        self.fullname = fullname
        self.mobile_no = mobile_no
        self.date_of_birth = date_of_birth
        self.password = password
        
        
    # Returns True if the format of a name is valid, else False.
    def is_valid_name(self, fullname):
        '''
        Rules: The name must at least be 2 separated names.
        '''
        name_parts = fullname.split()
        if len(name_parts) > 1:
            return True
        else:
            return False
        
    # Returns True if the format of mobile_no is valid, else False.
    def is_valid_mobile(self, mobile_no):
        '''
        Rules: The mobile number has 10 digits starting with 0.
        '''
        number_pattern = "^0\d{9}"
        is_match = bool(re.match(number_pattern, mobile_no))
        # Checks regex pattern and it has 10 digits
        if is_match and len(mobile_no) == 10:
            return True
        else:
            return False

    # Returns True if the format of date is valid, else False.
    def is_valid_birthdate(self, date):
        '''
        Rules: The date is in the format DD/MM/YYYY
        '''
        date_pattern = "^(0?[1-9]|[1-2][0-9]|3[0-1])\/(0?[1-9]|1[0-2])\/\d{4}$"
        return bool(re.match(date_pattern, date))
        

    # Returns True if the age of user is above 16 years old, else False.
    def is_valid_age(self, dob):
        '''
        Rules: 
            - The user should be at least 16 years old. 
            - The age should be calculated based on the year entered 
            in the DOB (Only consider year).
        '''
        current_year = 2023
        
        # Get birth year
        date_parts = dob.split('/')
        year = int(date_parts[2])
        
        # Calculate age of user by year
        age = current_year - year
        
        if age >= 16:
            return True
        else:
            return False

    # Returns True if the password has a valid format, else False.
    def is_valid_password(self, password):
        password_pattern = "^[a-zA-Z].*[@&].*\d$"
        match = re.match(password_pattern, password)
        return bool(match)


    def validate_signup(self):
        self.__error_msg = ""
        
        if not self.is_valid_name(self.fullname):
            self.__error_msg = self.__error_msg + "\n- Full name must at least have 2 separate names."
        
        if not self.is_valid_mobile(self.mobile_no):
            self.__error_msg = self.__error_msg + "\n- Mobile number must start with 0 and have 10 digits."
        
        if not self.is_valid_password(self.password):
            self.__error_msg = self.__error_msg + "\n- Password must start with alphabets followed by either '@' or '&' then end with numbers."
        
        if self.password != confirm_password:
            self.__error_msg = self.__error_msg + "\n- The password and confirm password did not match."
            
        if self.is_valid_birthdate(self.date_of_birth):
            if not self.is_valid_age(self.date_of_birth):
                self.__error_msg = self.__error_msg + "\n- You must be at least 16 years old to register." 
        else:
            self.__error_msg = self.__error_msg + "\n- Date of Birth must be [DD/MM/YYYY] format." 
            
        # Return True if the there is no error message, else return the error 
        if len(self.__error_msg) > 0:
            return False
        else:
            return True
        
    def get_message(self):
        return self.__error_msg


class Order:
    order_id_counter = 1  # Initialize the order ID counter
    order_id = 0
    date_ordered = ''
    customer = None
    ordered_items = []
    ordered_prices = []
    order_type = ''
    order_total = 0
    
    def __init__(self, customer, ordered_items, ordered_prices, order_type):
        today = date.today()
        self.order_id = self.generate_order_id()  # Generate unique order ID
        self.date_ordered = today.strftime("%d/%m/%Y")
        self.customer = customer
        self.ordered_items = ordered_items
        self.ordered_prices = ordered_prices  # List to store ordered items and quantities
        self.order_type = order_type
        self.order_total = 0

    def generate_order_id(self):
        order_id = Order.order_id_counter
        Order.order_id_counter += 1
        return f"A00{order_id}"

    def calc_additional_charge(self):
        raise NotImplementedError("calc_additional_charge() was not implemented")
    
    def get_grand_total(self):
        raise NotImplementedError("get_grand_total() was not implemented")
        
    def show_orders(self):
        raise NotImplementedError("show_orders() was not implemented")
        
    

class DineInOrder(Order):
    # Set service charge for 15 % of total order
    _service_charge = 0.15
    no_of_persons = 0
    visit_date = ''
    visit_time = ''
    
    def __init__(self, customer, ordered_items, ordered_prices, ):
        super().__init__(customer, ordered_items, ordered_prices, "Dine-in")  # Call the parent class constructor
        
    # Sets the dine in booking details and returns the DineInOrder object
    def set_booking_details(self, no_of_persons, visit_date, visit_time):
        self.no_of_persons = no_of_persons
        self.visit_date = visit_date
        self.visit_time = visit_time
        
        return self
    
    def show_orders(self):
        print("\n[You Ordered]:")
        for i, item in enumerate(self.ordered_items, start=0):
            print(" - " + item + "\t\t\t $" + str(self.ordered_prices[i]))
        # Get total order
        total = sum(self.ordered_prices)
        additional_charges = self.calc_additional_charge()
        grand_total = total + additional_charges
        # Prompts total orders and charges
        print(f"\nTotal price of order: ${total:.2f} \n" +
              f"Additional Charges (15%): ${additional_charges:.2f} \n" +
              f"Grand Total: ${grand_total}")
    
    # Polymorphic method
    def calc_additional_charge(self):
        return sum(self.ordered_prices) * self._service_charge
        
    def get_grand_total(self):
        return sum(self.ordered_prices) + self.calc_additional_charge()


class PickUp(Order):
    picker_name = ''
    pickup_date = ''
    pickup_time = ''
    
    def __init__(self, customer, ordered_items):
        items = []
        prices = []
        # Loop through the items
        for item in ordered_items:
            items.append(item[0]) # gets the item name
            prices.append(item[1]) # gets the item price
        super().__init__(customer, items, prices, "Pick-up")  # Call the parent class constructor
        
    # Sets the pickup details and returns the object
    def set_pickup_details(self, picker_name, pickup_date, pickup_time):
        self.picker_name = picker_name
        self.pickup_date = pickup_date
        self.pickup_time = pickup_time
        
        return self    
    
    def show_orders(self):
        print("\n[You Ordered]:")
        for i, item in enumerate(self.ordered_items, start=0):
            print(" - " + item + "\t\t\t $" + str(self.ordered_prices[i]))
        # Get total order
        total = sum(self.ordered_prices)
        additional_charges = self.calc_additional_charge()
        grand_total = total + additional_charges
        # Prompts total orders and charges
        print(f"\nTotal price of order: ${total:.2f} \n" +
              f"No Additional Charges: ${additional_charges:.2f} \n" +
              f"Grand Total: ${grand_total}")
        
    def get_grand_total(self):
        return sum(self.ordered_prices) + self.calc_additional_charge()
    
    # Polymorphic method
    def calc_additional_charge(self):
        # Pickup returns no additional charges
        return 0
    
class Deliveries(Order):
    distance = 0
    delivery_date = ''
    delivery_time = ''
    
    def __init__(self, customer, ordered_items):
        items = []
        prices = []
        # Loop through the items
        for item in ordered_items:
            items.append(item[0]) # gets the item name
            prices.append(item[1]) # gets the item price
        super().__init__(customer, items, prices, "Delivery")  # Call the parent class constructor
        
    # Sets the pickup details and returns the object
    def set_delivery_details(self, distance, delivery_date, delivery_time):
        self.distance = distance
        self.delivery_date = delivery_date
        self.delivery_time = delivery_time
        
        return self    
    
    def show_initial_order(self):
        print("\n[You Ordered]:")
        for i, item in enumerate(self.ordered_items, start=0):
            print(" - " + item + "\t\t\t $" + str(self.ordered_prices[i]))
    
    def show_orders(self):
        print("\n[You Ordered]:")
        for i, item in enumerate(self.ordered_items, start=0):
            print(" - " + item + "\t\t\t $" + str(self.ordered_prices[i]))
        # Get total order
        total = sum(self.ordered_prices)
        additional_charges = self.calc_additional_charge()
        grand_total = total + additional_charges
        # Prompts total orders and charges
        print(f"\nTotal price of order: ${total:.2f} \n" +
              f"Additional Charges based on distance of {self.distance} km.: ${additional_charges:.2f} \n" +
              f"Grand Total: ${grand_total}")
        
    def get_grand_total(self):
        return sum(self.ordered_prices) + self.calc_additional_charge()
    
    # Polymorphic method
    def calc_additional_charge(self):
        # Delivery charges depends on the distance 
        if self.distance >= 0 and self.distance <= 5:
            return 3
        elif self.distance > 5 and self.distance <= 10:
            return 6
        elif self.distance > 10 and self.distance <= 15:
            return 10
        else:
            return False
        
    
# ---- FUNCTIONS ----

# Displays the HomeScreen menu and returns the choice of the user
def show_home_screen():
    print("\n" + " Home Screen ".center(title_padding, "*") + "\n"
          "What would you like to do?\n" +
          "\t [1] - Sign up\n" + 
          "\t [2] - Sign in\n" + 
          "\t [3] - Quit Application\n")
    return int(input("Your choice [1-3]: "))

# Displays the options when user signs in and returns the choice of the user
def show_signin_screen():
    # Once signed in, show the sign in options.
    print("\n" + " Sign in Options ".center(title_padding, "*"))
    signin_input = eval(input("\t[2.1] - Start Ordering (Dine in, Self-Pickup, Delivery)\n" +
                    "\t[2.2] - Summary of Transactions \n" +
                    "\t[2.3] - Logout \n" +
                    "\t[2.4] - Reset Password \n" +
                    "Your choice [2.1-2.4]: "))
    return signin_input

# Displays the options when user selects start ordering and returns the choice of the user
def show_ordering_screen():
    # Once signed in, show the sign in options.
    print("\n" + " Start Ordering ".center(title_padding, "*"))
    selection = int(input("\t[1] - Dine in\n" +
                            "\t[2] - Order Online\n" +
                            "\t[3] - Go Back\n" +
                            "Your choice [1-3]: "))
    return selection

# Displays the options when user selects ordering online and returns the choice of the user
def show_online_screen():
    # Once signed in, show the sign in options.
    print("\n" + " Order Online ".center(title_padding, "*"))
    selection = int(input("\t[1] - Self-Pickup\n" +
                            "\t[2] - Home Delivery\n" +
                            "\t[3] - Go Back\n" +
                            "Your choice [1-3]: "))
    return selection

# Displays the options when user selects transactions history
def show_transaction_screen():
    # Once signed in, show the sign in options.
    print("\n" + " Print Statistics ".center(title_padding, "*"))
    selection = int(input("\t[1] - All Dine in Orders\n" +
                            "\t[2] - All Pick up Orders\n" +
                            "\t[3] - All Deliveries\n" +
                            "\t[4] - All Orders (Ascending Order)\n" +
                            "\t[5] - Total Amount Spent on All Orders\n" +
                            "\t[6] - Go to Previous Menu\n" +
                            "Your choice [1-6]: "))
    return selection

# Returns the complete menu in a list
def get_full_menu():
    prompts = []
    prompts.append("\n" + " Menu Choices ".center(title_padding, "*")) 
    prompts.append('Enter 1 \t Noodles    \t $2')
    prompts.append('Enter 2 \t Sandwich   \t $4')
    prompts.append('Enter 3 \t Dumpling   \t $6')
    prompts.append('Enter 4 \t Muffins    \t $8')
    prompts.append('Enter 5 \t Pasta      \t $10') 
    prompts.append('Enter 6 \t Pizza      \t $20') 
    prompts.append('Enter 7 \t Coffee     \t $2') 
    prompts.append('Enter 8 \t Cold Drink \t $4')
    prompts.append('Enter 9 \t Shake      \t $6')               
    prompts.append('Enter 10 to finish choosing meals') 
    return prompts

# Returns only the food menu in a list
def get_food_menu():
    prompts = []
    prompts.append("\n" + " Menu Choices ".center(title_padding, "*")) 
    prompts.append('Enter 1 \t Noodles    \t $2')
    prompts.append('Enter 2 \t Sandwich   \t $4')
    prompts.append('Enter 3 \t Dumpling   \t $6')
    prompts.append('Enter 4 \t Muffins    \t $8')
    prompts.append('Enter 5 \t Pasta      \t $10') 
    prompts.append('Enter 6 \t Pizza      \t $20')        
    prompts.append('Enter 7 \t for drinks menu') 
    return prompts

# Returns only the drinks menu in a list
def get_drinks_menu():
    prompts = []
    prompts.append("\n" + " Menu Choices ".center(title_padding, "*")) 
    prompts.append('Enter 1 \t Coffee     \t $2')
    prompts.append('Enter 2 \t Cold Drink \t $4')
    prompts.append('Enter 3 \t Shake      \t $6')  
    prompts.append('Enter 4 \t for Checkout') 
    return prompts

# Displays the menu and returns the chosen order in a list [item, price]
def run_select_order(prompts):
    order_selection = []
    last = int(len(prompts))
    
    # Loop until user selects the last option from list                            
    while True:
        order = []        
        # Displays the menu
        for prompt in prompts:
           print(prompt)
        
        index = eval(input("\nEnter menu choice: "))
        
        # Checks if the choice was within the menu list
        if (index >= 1) and (index < (last-1)): 
           # Record the item selected
           temp = str(prompts[index]).split("\t")
           food_name = temp[1].strip()
           order.append(food_name)
           
           # Record the price selected
           temp_price = str(prompts[index]).split("$")
           price = int(temp_price[1])
           order.append(price)
           
           # Save in order selection as a list
           order_selection.append(order)
           # Prompt order selection
           print(f"The item '{food_name}' was added to your order.")
           pass
        # Returns the order_selection if last option was selected
        elif index == (last - 1):
            return order_selection
        else:
            print("Invalid menu choice")
    
# Returns the user from the users_list when username matches 
def find_user(lookup_mobile_no):
    for user in users_list:
        
        if user.mobile_no == lookup_mobile_no:
            return user
    return False


# Returns True if reset password is valid, else the error message
# Used for validating reset password option
def is_valid_reset_password(signed_user, username, old_password, new_password):
    
    error_msg = ""
    
    # Check if username (mobile no) is valid
    if username != signed_user.mobile_no:
        error_msg = error_msg + "\nThe username you entered is not valid."
    # Check if current password is valid     
    if old_password != signed_user.password:
        error_msg = error_msg + "\nThe current password you entered is incorrect."
    # Check new password does not match current password
    if new_password == signed_user.password:
        error_msg = error_msg + "\nYour new password should not be the same from your previous password."
    
    # Return error message if not blank, else return True
    if len(error_msg) > 0:
        return error_msg
    else:
        return True

# Returns True if reset password is valid, else the error message
# Used for validating reset password with max attempts
def is_valid_dob_reset_password(signed_user, username, birth_date, new_password):
    
    error_msg = ""
    
    # Check if username (mobile no) is valid
    if username != signed_user.mobile_no:
        error_msg = error_msg + "\nThe username you entered is not valid."
    # Check if birth day matches
    if birth_date != signed_user.date_of_birth: 
        error_msg = error_msg + "\nThe birth date you entered did not match."
    # Check new password does not match current password
    if new_password == signed_user.password:
        error_msg = error_msg + "\nYour new password should not be the same from your previous password."
    
    # Return error message if not blank, else return True
    if len(error_msg) > 0:
        return error_msg
    else:
        return True
    
# Returns the user index 
def get_user_index(signed_user):
    
    found_user_index = False
    
    # Loop through the registered users to find match
    for index, user in enumerate(users_list):
        # Save index of user when match
        if user.mobile_no == signed_user.mobile_no:  # Assuming the mobile number is in the second position of the user's list
            found_user_index = index
            break
    
    return found_user_index

    
def show_orders(order_type='all'):
    print("\n" + " Print Statistics ".center(title_padding, "*"))
    print("\n\nOrder ID \t Date \t\t Total Amount Paid \t Type of Order")
    for order in orders_list:
        if order_type == 'all':
            print(f"{order.order_id} \t\t {order.date_ordered} \t\t {order.get_grand_total()} \t\t\t {order.order_type}")
        else:
            if order.order_type == order_type:
                print(f"{order.order_id} \t\t {order.date_ordered} \t\t {order.get_grand_total()} \t\t\t {order.order_type}")
    
    input("\nPress Enter to continue...")

def show_total_amount_spent():
    total = 0
    # Calculate total orders
    for order in orders_list:
       total = total + order.get_grand_total() 
    print("\nThe total Amount Spent on All orders is:  AUD ", total)
    
    input("\nPress Enter to continue...")
# ---- MAIN CODE ----

# Loops until user selects [3] to quit
while True:
    
    user_input = show_home_screen()

    # 1 - SIGN UP
    if user_input == 1:
        # Loops until sign up is successful
        while True:
            
            print("\n" + " Sign Up ".center(title_padding, "*") )
            fullname = input("Please enter your name: ")
            mobile_no = input("Please enter your mobile number [0XXXXXXXXX]: ")
            password = input("Please enter your password: ")
            confirm_password = input("Please confirm your password: ")
            date_of_birth = input("Please enter your date of birth [dd/mm/yyyy]: ")
            
            customer = Customers(fullname, mobile_no, date_of_birth, password)
            
            # If signup is valid save the user and exit loop, else display errors
            if customer.validate_signup():
                # Save the customer to users_list
                users_list.append(customer)
                print("You have successfully signed up.")
                break;
            else:
                print("\n[Invalid Input]:" + customer.get_message()  + '\nPlease start again.')
    
    # 2 - SIGN IN
    elif user_input == 2:
        
        # -- Sign-in -- 
        print("\n" + " Sign in ".center(title_padding, "*"))
        
        login_attempts = 1
        # This variable will hold the user information once signed in
        signed_user = False
        # Loop for 3 login attempts
        while login_attempts < 4:
            print("\n[Attempt "+ str(login_attempts)+"]")
            login_username = input("Please enter your username (Mobile Number):")
            login_password = input("Please enter your password:")
            
            signed_user = find_user(login_username)
            
            # If username was not found redirect to sign up 
            if signed_user == False:
                break
            
            # If password matches then show success message
            if signed_user.password == login_password:
               print("You have successfully signed in!")
               break
            else:
               print("Password did not match, please try again.")
               # increment attempt
               login_attempts = login_attempts + 1
        else:
            # RESET PASSWORD MAX ATTEMPTS
            print("You have reached the maximium login attempts. Please reset your password.")
            # Loop until user successfully resets password
            while True:
                print("\n" + " Reset Password ".center(title_padding, "*"))
                
                username = input("Please enter Username (mobile number): ")
                birth_date = input("Please enter your date of birth [dd/mm/yyyy]: ")
                new_password = input("Please enter new password: ")
                
                reset_result = is_valid_dob_reset_password(signed_user, username, birth_date, new_password)
                
                # Checks if the reset password is valid
                if reset_result == True:
                    # Lookup user index
                    found_user_index = get_user_index(signed_user)
                    #  Update users password
                    users_list[found_user_index].password = new_password
                    print("Password has been reset.")
                    break
                else:
                    # Prints the error message(s)
                    print(reset_result)      
            
        # If username does not exist, load the home screen 
        if signed_user == False:
             print("Username was not found, please sign up.")
             pass
         
        
        # LOGIN USER 
        if signed_user:
            # Initialize signin_input
            signin_input = 0
            
            # Loop until user chooses to log out
            while signin_input != 2.3:
                    
                signin_input = show_signin_screen()
                
                # 2.1 - START ORDERING
                if signin_input == 2.1:
                    order_input = 0
                    
                    # Loop until user selects option 3 to go back
                    while order_input != 3:
                        order_input = show_ordering_screen()
                        
                        # 1 - DINE IN
                        if order_input == 1:
                            # Set the menu
                            prompts = get_full_menu()
                            last = int(len(prompts))
                            # Set price and item list placeholders
                            ordered_prices = []
                            ordered_items = []
                            menu_choice = 1

                            # Loop until user selects the last option from list                            
                            while 1 <= menu_choice < (last - 1):
                                # Display the menu
                                for prompt in prompts:
                                   print(prompt)
                                menu_choice = eval(input("\nEnter menu choice: "))
                                
                                # Checks if the choice was within the menu list
                                if 1 <= menu_choice < (last - 1): 
                                   index = menu_choice 
                                   
                                   # Record the price selected
                                   temp_price = str(prompts[index]).split("$")
                                   price = int(temp_price[1])
                                   ordered_prices.append(price)
                                   
                                   # Record the item selected
                                   temp = str(prompts[index]).split("\t")
                                   food_name = temp[1].strip()
                                   ordered_items.append(food_name)
                                   
                                   # Prompt order selection
                                   print(f"The item '{food_name}' was added to your order.")
                                
                                # Calculate total charge if user chooses to checkout
                                elif menu_choice == (last - 1):
                                    print("\n[You Ordered]:")
                                    for i, item in enumerate(ordered_items, start=0):
                                        print(" - " + item + "\t\t $" + str(ordered_prices[i]))
                                    # Create DineInOrder instance
                                    dine_in_order = DineInOrder(signed_user, ordered_items, ordered_prices)
                                    # Get total amount or order
                                    total = sum(ordered_prices)
                                    additional_charges = dine_in_order.calc_additional_charge()
                                    grand_total = dine_in_order.get_grand_total()
                                    print(f"\nTotal price of order: ${total:.2f} \n" +
                                          f"Additional Charges (15%): ${additional_charges:.2f} \n" +
                                          f"Grand Total: ${grand_total}")
                                    break
                            else:
                                print("Invalid menu choice")
        
                            
                            # Prompt user to checkout
                            proceed_to_checkout = input("Proceed to checkout? (Y/N): ")
                           
                            # DINE IN CHECKOUT
                            if proceed_to_checkout.upper() == 'Y':
                                num_persons = int(input("\nPlease enter the number of persons: "))
                                date_of_visit = input("Please enter the date of booking (DD/MM/YYYY): ")
                                time_of_visit = input("Please enter the time of booking for dine in (HH:MM): ")
                                # Set dine in booking
                                dine_in_order.set_booking_details(num_persons, date_of_visit, time_of_visit)
                                # Save Order
                                orders_list.append(dine_in_order)
                                print("\nThank you for entering the details. Your booking is confirmed.")
                                break
                            
                            # CANCEL DINE-IN CHECKOUT
                            elif proceed_to_checkout.upper() == 'N':
                                print("Order has been cancelled.")
                                break
                            else:
                                print("Invalid input. Please enter Y to proceed to checkout or N to cancel")
                        # -- END OF 1 - DINE IN ---
                        
                        # 2 - ORDER ONLINE
                        elif order_input == 2:
                            online_input = 0
                            # Loop until user chooses option 3
                            while online_input != 3:
                                online_input= show_online_screen()
                                
                                # 1 - SELF PICKUP
                                if online_input == 1:
                                    # Set ordered items placeholders
                                    ordered_items = []
                                    
                                    # Run the food menu
                                    prompts = get_food_menu()
                                    chosen_order = run_select_order(prompts)
                                    # Save ordered items
                                    ordered_items.extend(chosen_order)
                                    
                                    # Run the drinks menu
                                    prompts = get_drinks_menu()
                                    chosen_order = run_select_order(prompts)
                                    # Save ordered items
                                    ordered_items.extend(chosen_order)
                                    
                                    # Checks if no orders were made
                                    if len(ordered_items) == 0:
                                        print("You did not order any item.")
                                        break
                                    
                                    # Create instance of order
                                    pickup_object = PickUp(signed_user, ordered_items)
                                    # Display order
                                    pickup_object.show_orders()
                                    
                                    # Ask user if proceed with checkout
                                    checkout = input("Proceed with checkout [Y/N]?:")
                                    
                                    # Save the order
                                    if checkout.upper() == 'Y':
                                        pickup_date = input("Date of Pickup [dd/mm/yyyy]: ")
                                        pickup_time = input("Time of Pickup [HH:MM]: ")
                                        picker_name = input("Name of Person Picking up: ")
                                        pickup_object.set_pickup_details(picker_name, pickup_date, pickup_time)
                                        orders_list.append(pickup_object)
                                        print("Thank you for entering your details, your booking is confirmed.")
                                    else:
                                        print('Your order has been cancelled.')
                                        break
                                # -- END OF 1 - SELF PICKUP --
                                
                                # 2 - HOME DELIVERY
                                elif online_input == 2:
                                    # Check if user has entered an address
                                    if signed_user.address == '':
                                        
                                        enter_address = input("You have not mentioned your address, while signing up. \n" +
                                             "Please enter Y if you would like to enter your address. \n" +
                                             "Enter N if you would like to select other mode of order.")
                                    
                                        if enter_address.upper() == 'N':
                                            print("Going back to previous menu.")
                                            break
                                        elif enter_address.upper() == 'Y':
                                            address = input("Please enter your address: ")
                                            # Update users address
                                            signed_user.address = address
                                            print("Address has been saved.")
                                            pass
                                        else:
                                            print("Please enter a valid response Y or N:")
                                        
                                    # Set ordered items placeholders
                                    ordered_items = []
                                    
                                    # Run the food menu
                                    prompts = get_food_menu()
                                    chosen_order = run_select_order(prompts)
                                    # Save ordered items
                                    ordered_items.extend(chosen_order)
                                    
                                    # Run the drinks menu
                                    prompts = get_drinks_menu()
                                    chosen_order = run_select_order(prompts)
                                    # Save ordered items
                                    ordered_items.extend(chosen_order)
                                    
                                    # Checks if no orders were made
                                    if len(ordered_items) == 0:
                                        print("You did not order any item.")
                                        break
                                    
                                    # Create instance of order
                                    delivery_object = Deliveries(signed_user, ordered_items)
                                    # Display order
                                    delivery_object.show_orders()
                                    
                                    # Ask user if proceed with checkout
                                    checkout = input("\nProceed with checkout [Y/N]?:")
                                    
                                    # Start checkout
                                    if checkout.upper() == 'Y':
                                        delivery_date = input("Please enter the Date of Delivery [dd/mm/yyyy]:")
                                        delivery_time = input("Please enter the Time of Delivery [HH:MM]:")
                                        distance = float(input("Please enter the distance from the Restaurant [in km.]:"))
                                        
                                        # Save the delivery details
                                        delivery_object.set_delivery_details(distance, delivery_date, delivery_time)
                                        additional_charge = delivery_object.calc_additional_charge()
                                        
                                        # Checks if the additional charge is not applicable
                                        if additional_charge == False:
                                            print("The distance of your house does not support delivery. Please use Pickup instead.")
                                            break
                                        
                                        # Save the order
                                        orders_list.append(delivery_object)
                                        print("Thank you for entering your details, your order has been confirmed.")
                                    else:
                                        print('Your order has been cancelled.')
                                        break
                                # -- END OF 2 - HOME DELIVERY --
                                else:
                                    print("Please choose between 1-3.")
                                    break;
                            else:
                                print("Going back...")
                        # -- END OF 2 - ORDER ONLINE --
                        
                        # 3- GO BACK
                        elif order_input == 3:
                            print("Going back...")
                            break;
                    else:
                        print("Please choose between 1-3")
                    
                # 2.2 - SUMMARY OF TRANSACTIONS
                elif signin_input == 2.2:
                    
                    transaction_input = 0 
                    
                    # Loop until user selects 6
                    while transaction_input != 6:
                        transaction_input = show_transaction_screen()
                        
                        # All Dine in Orders
                        if transaction_input == 1:
                            show_orders('Dine-in')
                        # All Pickup Orders
                        elif transaction_input == 2:
                            show_orders('Pick-up')
                        # All Delivery Orders
                        elif transaction_input == 3:
                            show_orders('Delivery')
                        # All Orders
                        elif transaction_input == 4:
                            show_orders()
                        # Total Amount Spent
                        elif transaction_input == 5:
                            show_total_amount_spent()
                        else:
                            print("Please choose between 1-6 only.")
                        
                        # show_orders()
                
                # 2.3 - LOG OUT 
                elif signin_input == 2.3:
                    print("You have signed out.")
                
                # 2.4 - RESET PASSWORD OPTION (from assessment 2)
                elif signin_input == 2.4:
                    
                    # Loop until user successfully resets password
                    while True:
                        print("\n" + " Reset Password ".center(title_padding, "*"))
                        
                        username = input("Please enter Username (mobile number): ")
                        old_password = input("Please enter your current password: ")
                        new_password = input("Please enter new password: ")
                        
                        reset_result = is_valid_reset_password(signed_user, username, old_password, new_password)
                        
                        # Checks if the reset password if it's valid
                        if reset_result == True:
                            # Lookup user index
                            found_user_index = get_user_index(signed_user)
                            #  Update users password
                            users_list[found_user_index].password = new_password
                            print("Password has been reset.")
                            break
                        else:
                            # Prints the error message(s)
                            print(reset_result)
                else:
                    print("Please choose between 2.1-2.4")
            
    # 3 - QUIT APPLICATION
    elif user_input == 3:
        print("\n" + " Quit Application ".center(title_padding, "*") + 
              "\nThank you for using our app. Goodbye!")
        break;
    
    # 4 - LIST USERS
    elif user_input == 4:
        print('\n[Users List]\n')
        for user in users_list:
            print(user.fullname)
            print(user.mobile_no)
            print(user.date_of_birth)
            print(user.password)
            print('\n***\n')
    else:
        print("Please choose between 1-3.")

