# Locker initial system data (global data)
current_time = 0  # Simulated elapsed time in hours

pending_discount = {} # Stores pending rewards, mobile is set to "WAIT" when a saved 10% reward is awaiting use
phone_usage = {} # Tracks the numbers of times each mobile has been used
discount_codes = {} # Stores generated discount codes and thier associated rewards 
used_phones = set() # Keeps track of mobiles that have already redeemed a reward
logs = [] # Stores system activity and transaction logs

# List of lockers and their current occupancy, user, and rental details
lockers = [
    {"id": "L01", "occupied": False, "mobile": "", "passcode": "", "start_time": 0, "paid_hours": 0},
    {"id": "L02", "occupied": False, "mobile": "", "passcode": "", "start_time": 0, "paid_hours": 0},
    {"id": "L03", "occupied": False, "mobile": "", "passcode": "", "start_time": 0, "paid_hours": 0},
    {"id": "L04", "occupied": False, "mobile": "", "passcode": "", "start_time": 0, "paid_hours": 0},
    {"id": "L05", "occupied": False, "mobile": "", "passcode": "", "start_time": 0, "paid_hours": 0},
]

# Main menu options displayed to the user
menu = (
    ("1", "View lockers"),
    ("2", "Store luggage"),
    ("3", "Retrieve luggage"),
    ("4", "My usage info"),
    ("5", "Exit")
)

# Predefined timestamps used for storage and retrieval receipts
timestamps = {
    "L01": (2026, 5, 29, 11, 1, 12),
    "L02": (2026, 5, 29, 11, 2, 45),
    "L03": (2026, 5, 29, 11, 3, 59),
    "L04": (2026, 5, 29, 11, 11, 28),
    "L05": (2026, 5, 29, 11, 25, 51)
}

# Global constants 
BASE_RATE = 2.5 
MID_RATE = 5
LATE_RATE = 10 # Penalty
VERIFICATION_CODE = "12345" # Simulated code 

# Functions 
# Finds and returns a locker by its ID
def find_locker(locker_list, locker_id):
    for locker in locker_list:
        if locker["id"] == locker_id:
            return locker
    return None

# Resets a locker to its default empty state
def reset_locker(locker):
    locker["occupied"] = False
    locker["mobile"] = ""
    locker["passcode"] = ""
    locker["start_time"] = 0
    locker["paid_hours"] = 0

# Formats date and time values into a readable timestamp string
def format_timestamp(year, month, day, hour, minute, second):
    return f"{year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}"

# Returns a predefined storage timestamp for a locker, used in receipt in option 2, faking storing timestamp
def get_time(locker_id): 
    year, month, day, hour, minute, second = timestamps.get(locker_id, (2026, 5, 29, 0, 0, 0))
    return format_timestamp(year, month, day, hour, minute, second)

# Returns a simulated retrieval timestamp based on storage duration, used in receipt in option 3, faking retrieval timestamp
def get_retrieval_time(locker_id, used_hours): 
    year, month, day, hour, minute, second = timestamps.get(locker_id, (2026, 5, 29, 0, 0, 0))
    hour += used_hours
    # handle hours beyond midnight
    day += hour // 24
    hour = hour % 24
    return format_timestamp(year, month, day, hour, minute, second)

# Displays a payment receipt for a storage transaction
def get_receipt(amount, locker_id, mobile, status, time_stamp=None):
    if time_stamp is None:
        time_stamp = get_time(locker_id)
    print("\n=========== RECEIPT ===========")
    print(f"{'Locker:':<12}{locker_id}")
    print(f"{'Mobile:':<12}{mobile}")
    print(f"{'Status:':<12}{status}")
    print("--------------------------------")
    print(f"{'Paid:':<12}£{amount:.2f}")
    print(f"{'Date:':<12}{time_stamp[:10]}")
    print(f"{'Time:':<12}{time_stamp[-8:]}")
    print("================================")
    print("Thank you for using our service!")

# Validates and returns an 11-digit mobile number
def get_valid_mobile(): 
    while True:
        mobile = input("Enter mobile number: ").strip()
        if mobile.isdigit() and len(mobile) == 11:
            return mobile
        print("Invalid mobile number. Must be 11 digits.")

# Validates and returns a 4-digit passcode
def get_valid_passcode():
    while True:
        passcode = input("Enter 4-digit passcode: ").strip()
        if passcode.isdigit() and len(passcode) == 4:
            return passcode
        print("Invalid passcode. Must be 4 digits.")

# Validates and returns a locker ID from the available options
def get_valid_id(valid_ids):
    while True:
            locker_id = input("\nEnter locker ID: ").strip().upper()
            if locker_id in valid_ids:
                return locker_id
            print("Invalid locker ID. Choose from:", ", ".join(valid_ids))

# Validates and returns the storage duration in hours
def get_duration():
    while True:
        try:
            duration = int(input("\nEnter number of hours: "))
            if 1 <= duration <= 15:
                return duration
            print("Invalid duration. Maximum storage time is 15 hours.")
        except ValueError:
            print("Handled error: Invalid input. Please enter a number.")
        except EOFError:
            print("Handled error: No input provided.")

# Calculates the storage charge based on rental duration
def calculate_charge(hours):
    if hours <= 5:
        return hours * BASE_RATE
    elif hours <= 15:
        return (5 * BASE_RATE) + ((hours - 5) * MID_RATE)
    else:
        return (5 * BASE_RATE) + (10 * MID_RATE) + ((hours - 15) * LATE_RATE)

# Calculates additional charges for exceeding the paid duration
def calculate_extra_charge(used_hours, paid_hours):
    if used_hours <= paid_hours:
        return 0, 0  # extra_charge, extra_hours
    total_cost = calculate_charge(used_hours)
    paid_cost = calculate_charge(paid_hours)
    extra_charge = total_cost - paid_cost
    extra_hours = used_hours - paid_hours
    return extra_charge, extra_hours

# Simulates processing a selected payment method
def process_payment_method(method):
    print(f"\nInsert {method}...")
    print("Processing...")
    print(f"{method.title()} accepted.")

# Handles cash and card payment transactions
def process_payment(amount):
    print("\nPlease pay to proceed.")
    print("1. Cash\n2. Card")
    while True:
        choice = input("\nEnter option: ").strip()
        #CASH PAYMENT
        if choice == "1":
            total_cash = 0.0
            while True:
                try:
                    cash = float(input("Enter cash amount inserted: £").strip())
                    total_cash +=cash
                    remaining = round(amount - total_cash, 2)
                    if remaining > 0:    
                        print(f"Insufficient cash. You still owe £{remaining:.2f}.")
                        while True:
                            option = input("Press C to continue with cash or S to switch to card: ").strip().upper()
                            if option == "C":
                                break
                            elif option == "S":
                                print(f"\nYou still owe £{remaining:.2f}.")
                                process_payment_method("card")
                                print(f"Remaining amount £{remaining:.2f} paid.")
                                print(f"Total amount paid: £{amount:.2f}")
                                return
                            else:
                                print("Invalid option. Please enter C or S.")

                    else:
                        change = round(total_cash - amount, 2)
                        process_payment_method("cash")
                        if change > 0:
                            print(f"Please take your change: £{change:.2f}")
                        else:
                            print("Exact amount received. No change.")
                        print(f"Payment of £{amount:.2f} received.")
                        return    
                except ValueError:
                    print("Handled error: Invalid amount. Please enter a number.")

        #CARD PAYMENT
        elif choice == "2":
            process_payment_method("card")
            print(f"Payment of £{amount:.2f} received.")
            return
        else:
            print("Invalid option. Enter 1 for Cash or 2 for Card.")

# Validates and returns a Yes/No user response
def get_yes_no(prompt):
    while True:
        choice = input(prompt).strip().upper()
        if choice in ("Y", "N"):
            return choice
        print("Invalid input. Please enter Y or N.")

# Sends a digital receipt to the user's mobile number
def get_sms(mobile):
    send_sms = get_yes_no("\nWould you like a digital receipt sent to your mobile? (Y/N): ")
    if send_sms == "Y":
        print("\nProcessing request...")
        print("Sending SMS...")
        masked = "********" + mobile[-3:]
        print(f"Receipt sent to {masked}")
    else:
        print("\nNo SMS will be sent.")

# Displays occupancy warnings when locker demand is high
def high_demand_warning(locker_list):
    occupied = 0
    for locker in locker_list:
        if locker["occupied"]:
            occupied+=1
    if occupied == len(locker_list):
        print("⚠ All lockers are occupied!")
    elif occupied >= len(locker_list) * 0.6:
        print("⚠ High demand: Most lockers are occupied!")

# Records a user activity in the system log
def log_activity(log_list, mobile, locker_id, action):
    log_list.append({
        "mobile": mobile,
        "locker": locker_id,
        "action": action,
        "time": current_time,
    })

# Generates a unique discount code based on usage count
def generate_code(mobile, uses):
    last_digits = mobile[-3:]
    return f"DISC{uses}-{last_digits}"

# Advances the simulated system time
def advance_time(hours):
    global current_time
    current_time += hours

# Main program loop
option = ""

while option != "5":

    # Display main menu
    print("\n=== SMART LOCKER SYSTEM ===") 
    for number, text in menu:
        print(f"{number}. {text}")

    # Validate menu option
    while True:
        option = input("\nEnter option: ").strip()
        if option in ("1", "2", "3", "4", "5"):
            break
        print("Invalid option. Please enter 1-5.")

    match option:
    
        case "1": # Option 1: View lockers

            print("\n=== LOCKER STATUS ===")
            
            for locker in lockers:
                if locker["occupied"]:
                    print(f"{locker['id']:<5} | {'Occupied':>9}")   
                else:
                    print(f"{locker['id']:<5} | {'Available':>10}")

            high_demand_warning(lockers)
            print(f"\nCurrently active users: {len(used_phones)}")
            
        case "2": # Option 2: Store luggage

            # Check if all lockers are full
            if all(locker["occupied"] for locker in lockers):
                    print("All lockers are currently occupied.")
            else:
                available_lockers = [] # Build list of available lockers
                for locker in lockers:
                    if not locker["occupied"]:
                        available_lockers.append(locker["id"])
                print("\nAvailable lockers:", ", ".join(available_lockers))
                locker_id = get_valid_id(available_lockers)
                # Find locker
                selected_locker = find_locker(lockers, locker_id)
                # Check if locker exist
                if selected_locker is None:
                    print("Invalid locker ID.")

                # Check if occupied
                elif selected_locker["occupied"]:
                    print("This locker is occupied, choose another one.")
                else: 
                    # Mobile validation
                    mobile = get_valid_mobile()
                    # Passcode validation
                    passcode = get_valid_passcode()
                    # Duration input validation
                    hours = get_duration()
                    # Calculate storage cost based on selected duration
                    charge = calculate_charge(hours)
                    print(f"Estimated cost: £{charge:.2f}")                         
                    # Rate message
                    if hours <= 5:
                        print("Rate 1 charge applied.")
                        print("Note: After 5 hours higher rate will apply.")
                    elif hours <= 15:
                        print("Rate 1 and Rate 2 charges applied.")
                        print("Note: After 15 hours penalty rate will be applied.")
                        print("Late collection (after 24 hours) may result in ")
                        print(" additional charges or luggage confiscation.")
                                
                    # Confirm before storing
                    confirm = get_yes_no("\nConfirm storing luggage? (Y/N): ")
                    if confirm == "N":
                        print("Operation cancelled.")
                        continue

                    # Ask for discount code
                    entered_code = input("Enter discount code (if you have one, otherwise press Enter): ").strip()
                    # Apply discount only after confirmation
                    current_uses = phone_usage.get(mobile, 0)
                    uses = current_uses + 1
                    final_charge = charge

                    # Apply loyalty rewards or discount codes
                    if entered_code:
                        # Handle manual code only  
                        if mobile in discount_codes and entered_code == discount_codes[mobile]["code"]:
                            print("Discount code accepted!")
                            # Apply discount    
                            discount = discount_codes[mobile]["discount"]
                            final_charge = charge * (1- discount)
                            # Remove code after use    
                            del discount_codes[mobile]   
                        else:
                            print("Invalid discount code.")
                                
                    else:
                        # Loyalty logic only runs if no code entered
                        status = pending_discount.get(mobile)

                        # Priority 1: apply saved 20% reward
                        if status == "WAIT": 
                            if uses % 5 == 0:
                                final_charge = charge * 0.8
                                print("\nLoyalty reward: 20% discount applied!")
                                pending_discount.pop(mobile)
                            else:
                                print("\nSaved discount pending. Keep going to reach 20%!")

                        # Priority 2: normal 20% reward (no saved discount)
                        elif uses % 5 == 0:
                            final_charge = charge * 0.8
                            print("\nLoyalty reward: 20% discount applied!")
                                
                        # Priority 3: 10% reward (only if no saved discount)
                        elif uses >= 3 and (uses - 3) % 5 == 0:
                            discounted_price = charge * 0.9
                            print("\nLoyalty reward: 10% discount available!")
                            print(f"Discounted price: £{discounted_price:.2f}")
                            choice = get_yes_no("Use 10% now (Y) or save for 20% later (N)? ")
                            if choice == "Y":
                                final_charge = discounted_price
                                print("10% discount applied!")
                            else:
                                pending_discount[mobile] = "WAIT"
                                print("Discount saved.")
                                print("\nKeep going! 20% discount unlocks at 5 uses.")
                                print("You can redeem your discount at any time using Option 4.")
                        else:
                            print("\nNo discount applied.")
                    # Show final price
                    print(f"Final price to pay: £{final_charge:.2f}")
                    # Payment 1
                    process_payment(final_charge)
                    # Save locker booking information
                    selected_locker["occupied"] = True
                    selected_locker["mobile"] = mobile
                    selected_locker["passcode"] = passcode
                    selected_locker["paid_hours"] = hours
                    selected_locker["start_time"] = current_time
                    # Update usage statistics and activity log
                    used_phones.add(mobile)
                    phone_usage[mobile] = phone_usage.get(mobile, 0) + 1
                    log_activity(logs, mobile, selected_locker["id"], "stored")
                    print("\nDoor opened. Please store your luggage.")
                    get_receipt(final_charge, locker_id, mobile, "Stored")
                    get_sms(mobile)
                    # Confirmation
                    print("\nLocker", locker_id, "is now occupied.")
                    print("Please keep your passcode safe.")
                    print("\nThank you for using the SMART LOCKER SYSTEM.")
                    # Note
                    print("\nNote:")
                    print("-Maximum storage time: 15 hours")
                    print("-Fee:")
                    print("Rate 1: £2.5/hour (first 5 hours)")
                    print("Rate 2: £5/hour (next 10 hours)")
                    print("Rate 3: £10/hour (after 15 hours - penalty rate)")
                    print("-Late collection: Items not collected after 24 hours may incur")
                    print(" in additional charges or be confiscated.")
                
        case "3": # Option 3: Retrieve luggage
            mobile = get_valid_mobile()
            
            # Locate all active lockers linked to the mobile number
            customer_lockers = []
            for locker in lockers:
                if locker["mobile"] == mobile and locker["occupied"]:
                    customer_lockers.append(locker)   
            # No lockers found
            if not customer_lockers:
                print("No lockers found for this mobile number.")
                continue
            
            # Allow customer to select a locker if multiple are rented
            if len(customer_lockers) > 1:
                locker_ids = []
                for locker in customer_lockers:
                    locker_ids.append(locker["id"])
                print("\nThis mobile has rented multiple lockers:")
                for locker in customer_lockers:
                    print(f"- {locker['id']}")
                locker_id = get_valid_id(locker_ids)

                # Find selected locker
                selected_locker = find_locker(customer_lockers, locker_id)
                if selected_locker is None:
                    print("Invalid locker ID.")
                    continue

            # Only one locker
            else:
                selected_locker = customer_lockers[0]
                print(f"\nThis mobile has rented locker {selected_locker['id']}")

            # Total attempts(1 initial + 2 extra)
            attempts = 3
            success = False
            # Authenticate user with passcode
            while attempts > 0:
                passcode = get_valid_passcode()
                if selected_locker["passcode"] == passcode:
                    success = True
                    break
                attempts -= 1
                print("Incorrect passcode. You have", attempts, "attempt(s) remaining.")
                if attempts > 0:
                    choice = get_yes_no("Forgot passcode? (Y/N): ")
                    # Passcode recovery process
                    if choice == "Y":
                        masked = "********" + mobile[-3:]
                        print(f"A verification code has been sent to {masked}.")
                        entered_code = input("Enter verification code: ")

                        if entered_code == VERIFICATION_CODE:    
                            new_passcode = get_valid_passcode()
                            selected_locker["passcode"] = new_passcode
                            print("Passcode reset successful.")
                            print("Please log in again using your new passcode.")
                            # Reset attempts and restart login loop
                            attempts = 3
                            continue
                        else:
                            print("Invalid verification code. Access denied.")
                            continue
            if not success:
                print("Incorrect passcode. Too many attempts. Access denied. Try later.")
                continue

            # Calculate actual storage duration
            used_hours = current_time - selected_locker["start_time"]
            paid_hours = selected_locker.get("paid_hours", 0)
            print(f"\nTime used: {used_hours}h")
            print(f"Time paid: {paid_hours}h")
            
            # Check if luggage exceeded maximum storage limit and should be confiscated
            if used_hours > 24:
                print("\n⚠ Storage limit exceeded.")
                print("⚠ Item confiscated.")
                print("\nThis item was not collected within 24 hours.")
                print("Please contact customer service.")
                log_activity(logs, mobile, selected_locker["id"], "confiscated")
                reset_locker(selected_locker)
                if not any(
                    locker["occupied"] and locker["mobile"] == mobile
                    for locker in lockers
                ):
                    used_phones.discard(mobile)
                continue

            # Extra charge calculation
            extra_charge, extra_hours = calculate_extra_charge(used_hours, paid_hours)
            if extra_charge == 0:
                print("No extra charge. Thank you!")
            else:
                print(f"⚠ Extra time: {extra_hours}h")
                if paid_hours <= 15 and used_hours > 15:
                    print("⚠ Penalty rate applied (£10/hour after 15h)")
                print(f"Extra charge: £{extra_charge:.2f}")

            # Payment only if needed 
            retrieval_time = get_retrieval_time(selected_locker["id"], used_hours)
            if extra_charge > 0:
                print(f"\nPlease pay £{extra_charge:.2f} to unlock the locker.")
                process_payment(extra_charge)
                get_receipt(extra_charge, selected_locker["id"], mobile, "Retrieved", retrieval_time)
                get_sms(mobile) 
            else:
                print("\nNo payment required. Unlocking...")

            log_activity(logs, mobile, selected_locker["id"], "retrieved")
            # Release locker after successful retrieval
            reset_locker(selected_locker)
            if not any(locker["occupied"] and locker["mobile"] == mobile 
                    for locker in lockers):
                used_phones.discard(mobile)
            
            print(f"\nLocker {selected_locker['id']} opened successfully.")
            print("Thank you for using the SMART LOCKER SYSTEM.")
            continue
        
        case "4": # Option 4: My usage info
            mobile = get_valid_mobile()
            uses = phone_usage.get(mobile, 0)
            print(f"\nTotal uses: {uses}")
            print("\n=== YOUR ACTIVITY LOG ===")
            found = False
            # Display customer's activity history
            for log in logs:
                if log["mobile"] == mobile:
                    print(f"{log['locker']} | {log['action']} by {log['mobile']}")
                    found = True
            if not found:
                print("No activity found")

            # Check if customer qualifies for a discount reward
            discount_available = False
            # 20% reward every 5 uses
            if uses > 0 and (uses + 1) % 5 == 0:
                if mobile not in discount_codes:
                    code = generate_code(mobile, uses)
                    discount_codes[mobile] = {"code": code, "discount": 0.2}    
                print("\nAlmost there!")
                print("Your NEXT booking will have a 20% discount.")
                print(f"Your discount code: {discount_codes[mobile]['code']}")
                print("You can use it at this terminal automatically or redeem it at another station.")
                discount_available = True

            # 10% reward every 3 uses
            elif uses >= 2 and (uses - 2) % 5 == 0:
                if mobile not in discount_codes:
                    code = generate_code(mobile, uses)
                    discount_codes[mobile] = {"code": code, "discount": 0.1}
                print("\nNext booking will have a 10% discount.")
                print(f"Your discount code: {discount_codes[mobile]['code']}")
                print("You can use it at this terminal automatically or redeem it at another station.")
                discount_available = True

            # Otherwise show progress
            # Next 10% reward
            if uses < 3:
                next_10 = 3 - uses
            else:
                next_10 = 5 - ((uses - 3) % 5)

            # Next 20% reward
            next_20 = 5 - (uses % 5)
            if next_20 == 0:
                next_20 = 5
            if not discount_available:
                print("\nNo discount available right now.")
                print(f"{next_10} more use(s) to next 10% reward.")
                print(f"{next_20} more use(s) to next 20% reward.") 

        case "5": # Option 5: Exit
            print("Program ended. See you next time.")
            break

    advance_time(1) # Simulate one hour passing after each completed transaction
    
    




