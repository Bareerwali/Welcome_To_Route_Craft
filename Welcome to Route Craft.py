import tkinter
from tkinter import ttk
from tkinter import messagebox  # Import the messagebox for feedback messages
from PIL import Image, ImageTk, ImageFilter  # Import from Pillow
from datetime import datetime
import pytz
import heapq

# Sample graph with towns and distances
graph = {
    'Lahore': {'Islamabad': 270, 'Karachi': 1400, 'Murree': 60, 'Naran': 240, 'Skardu': 640, 'Hunza': 550},
    'Islamabad': {'Lahore': 270, 'Karachi': 1400, 'Murree': 60, 'Naran': 240, 'Skardu': 640, 'Hunza': 550},
    'Karachi': {'Lahore': 1400, 'Islamabad': 1400, 'Murree': 1420, 'Naran': 1530, 'Skardu': 1870, 'Hunza': 1760},
    'Murree': {'Lahore': 60, 'Islamabad': 60, 'Karachi': 1420, 'Naran': 130, 'Skardu': 530, 'Hunza': 670},
    'Naran': {'Lahore': 240, 'Islamabad': 240, 'Karachi': 1530, 'Murree': 130, 'Skardu': 680, 'Hunza': 820},
    'Skardu': {'Lahore': 640, 'Islamabad': 640, 'Karachi': 1870, 'Murree': 530, 'Naran': 680, 'Hunza': 230},
    'Hunza': {'Lahore': 550, 'Islamabad': 550, 'Karachi': 1760, 'Murree': 670, 'Naran': 820, 'Skardu': 230},
}

# Dijkstra's algorithm to find the shortest path
def dijkstra(graph, start, end):
    distances = {city: float('inf') for city in graph}
    previous = {city: None for city in graph}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_city = heapq.heappop(priority_queue)

        if current_city == end:
            path = []
            while current_city is not None:
                path.append(current_city)
                current_city = previous[current_city]
            return path[::-1], distances[end]

        for neighbor, weight in graph[current_city].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_city
                heapq.heappush(priority_queue, (distance, neighbor))

    return None, float('inf')

def open_hotels_window():
    # Create a new top-level window for hotel selection
    hotels_window = tkinter.Toplevel()
    hotels_window.title("Hotels in Cities")
    hotels_window.geometry("500x1000")
    hotels_window.configure(bg="white")  # Set background color

    # Hotel data for each city
    hotels = {
        'Lahore': ["Pearl Continental Hotel", "Nishat Hotel", "Heritage Luxury Suites"],
        'Islamabad': ["Serena Hotel Islamabad", "Marriott Hotel Islamabad", "Ramada Islamabad"],
        'Karachi': ["Pearl Continental Hotel Karachi", "Marriott Hotel Karachi", "Avari Towers Karachi"],
        'Murree': ["Shangrila Resort Hotel", "Hotel One Mall Road", "Lockwood Hotel Murree"],
        'Naran': ["Arcadian Riverside", "Pine Top Hotel", "Fairyland Hotel Naran"],
        'Skardu': ["Serena Shigar Fort", "Shangrila Resort Skardu", "Hotel Reego"],
        'Hunza': ["Hunza Serena Inn", "Eagle's Nest Hotel", "Luxus Hunza"]
    }

    # Add a label for the title
    title_label = tkinter.Label(hotels_window, text="Select Your Favorite Hotels", font=("Georgia", 24, "normal"), bg="white", fg="#7e4a35")
    title_label.pack(pady=10)

    # Dictionary to store selected hotel for each city
    selected_hotels = {city: tkinter.StringVar() for city in hotels}

    # Hotel info for each hotel (including price and meal options)
    hotel_info = {
        "Pearl Continental Hotel": ("One-night stay included, Breakfast buffet available.", "$150"),
        "Nishat Hotel": ("One-night stay included, Dinner included in the package.", "$130"),
        "Heritage Luxury Suites": ("One-night stay included, Full meal plan.", "$200"),
        "Serena Hotel Islamabad": ("One-night stay included, Breakfast and dinner available.", "$180"),
        "Marriott Hotel Islamabad": ("One-night stay included, Buffet meals included.", "$170"),
        "Ramada Islamabad": ("One-night stay included, Only breakfast included.", "$140"),
        "Pearl Continental Hotel Karachi": ("One-night stay included, Dinner and breakfast included.", "$160"),
        "Marriott Hotel Karachi": ("One-night stay included, Breakfast available.", "$150"),
        "Avari Towers Karachi": ("One-night stay included, Full meal plan.", "$210"),
        "Shangrila Resort Hotel": ("One-night stay included, Breakfast included.", "$120"),
        "Hotel One Mall Road": ("One-night stay included, Dinner available.", "$110"),
        "Lockwood Hotel Murree": ("One-night stay included, Full meal plan available.", "$140"),
        "Arcadian Riverside": ("One-night stay included, Breakfast included.", "$130"),
        "Pine Top Hotel": ("One-night stay included, Dinner included.", "$120"),
        "Fairyland Hotel Naran": ("One-night stay included, Full meal plan.", "$160"),
        "Serena Shigar Fort": ("One-night stay included, Dinner and breakfast available.", "$220"),
        "Shangrila Resort Skardu": ("One-night stay included, Full meal plan available.", "$190"),
        "Hotel Reego": ("One-night stay included, Only breakfast available.", "$100"),
        "Hunza Serena Inn": ("One-night stay included, Dinner and breakfast included.", "$180"),
        "Eagle's Nest Hotel": ("One-night stay included, Full meal plan.", "$200"),
        "Luxus Hunza": ("One-night stay included, Breakfast available.", "$170")
    }

    # Function to show hotel details in a message box
    def show_hotel_info(hotel_name):
        info, price = hotel_info.get(hotel_name, ("No information available for this hotel.", "N/A"))
        messagebox.showinfo(f"{hotel_name} Details", f"{info}\nPrice for One Night: {price}")

    # Add hotel options for each city
    for city, hotel_list in hotels.items():
        # Section title for each city
        city_label = tkinter.Label(hotels_window, text=f"{city} Hotels", font=("Georgia", 14, "bold"), bg="white", fg="#7e4a35")
        city_label.pack(pady=5)

        # Create a Frame to hold the radio buttons horizontally
        hotel_frame = tkinter.Frame(hotels_window, bg="white")
        hotel_frame.pack(pady=5)

        # Add radio buttons for each hotel inside the frame
        for index, hotel in enumerate(hotel_list):
            hotel_button = tkinter.Radiobutton(
                hotel_frame,
                text=hotel,
                variable=selected_hotels[city],
                value=hotel,
                font=("Georgia", 12),
                bg="white",
                fg="#7e4a35",
                anchor="w",
                command=lambda h=hotel: show_hotel_info(h)  # Show info when hotel is selected
            )
            hotel_button.grid(row=0, column=index, padx=10)
    # Initialize `StringVar` for each city without a default value
    selected_hotels = {city: tkinter.StringVar(value="") for city in hotels}

   # Function to handle selection of a hotel
    def select_hotel():
    # Check if the user has selected a hotel for each city
        unselected_cities = [city for city, var in selected_hotels.items() if not var.get()]
        if unselected_cities:
            # Show a warning dialog box if any city has no hotel selected
            messagebox.showwarning(
                "Selection Required",
                f"Please select a hotel for the following cities: {', '.join(unselected_cities)}"
            )
        else:
        # Close the current window if all cities have a selected hotel
            hotels_window.destroy()
            print("Hotels selected:")
            for city, var in selected_hotels.items():
                print(f"{city}: {var.get()}")  # Print selected hotel for each city
    # Add a close button at the bottom
    close_button = tkinter.Button(hotels_window, text="Select it", font=("Georgia", 14, "bold"), bg="#8b6f47", fg="white", relief="flat", width=25, command=select_hotel)
    close_button.pack(pady=20)

def open_result_window():
    # Create a new top-level window
    result_window = tkinter.Toplevel()
    result_window.title("Result Window")
    result_window.geometry("400x300")

    # Set background color for the result window
    result_window.configure(bg="white")

    # Get the starting and ending cities from the entry fields
    start_city = start_town_var.get()
    end_city = destination_town_var.get()

    # Calculate the shortest path using Dijkstra's algorithm
    path, distance = dijkstra(graph, start_city, end_city)

    # Prepare the result to be displayed
    if path:
        result_text = f"Shortest path from {start_city} to {end_city}:\n{' -> '.join(path)}\nDistance: {distance} km"
    else:
        result_text = f"No path found from {start_city} to {end_city}"

    vehicle_type = vehicle_type_var.get()
    # Get the speed based on the vehicle type
    if vehicle_type == "Car":
        speed = 80  # Average speed for a car (km/h)
    else:
        speed = 60  # Average speed for a train (km/h)

    # Calculate the time taken based on speed
    if path:
        time_taken = distance / speed  # Time in hours
        hours = int(time_taken)  # Whole hours
        minutes = int((time_taken - hours) * 60)  # Remaining minutes

        # Generate result text
        result_text = (
            f"Shortest path from {start_city} to {end_city}:\n{' -> '.join(path)}\n\n"
            f"Distance: {distance} km\n"
            f"Time taken by {vehicle_type.lower()}: {hours} hour(s) and {minutes} minute(s)"
        )
    else:
        result_text = f"No path found from {start_city} to {end_city}"
    
   
    # Save the result to a file
    save_result_to_file(result_text)

    # Display the result in a label
    result_label = tkinter.Label(result_window, text=result_text, font=("Georgia", 14, "normal"), bg="white", fg="#7e4a35")
    result_label.pack(pady=50)

    # Add a button to close the result window
    close_button = tkinter.Button(result_window, text="Close", font=("Georgia", 14, "normal"), bg="#8b6f47", fg="white", width=25, relief="flat", command=result_window.destroy)
    close_button.pack(pady=10)

# Function to save the result in a text file
def save_result_to_file(result_text):
    # Open or create a file to save the result
    with open("result_output.txt", "w") as file:
        file.write("Result Summary:\n")
        file.write(result_text + "\n\n")
        


    

def open_trip_planner_window():
    # Create a new top-level window
    trip_window = tkinter.Toplevel()  
    trip_window.title("Plan Your Trip")
    trip_window.geometry("1000x600")  # Set the size of the window

    # Set the background color and window layout
    trip_window.configure(bg="#3C2A69")  # Set background color of the window

    # Left section: Color section (can add more content here later)
    left_frame = tkinter.Frame(trip_window, bg="#7e4a35", width=500, height=600)
    left_frame.pack(side="left", fill="y")

    # Right section: Trip Planner form
    right_frame = tkinter.Frame(trip_window, bg="white", width=500, height=600)
    right_frame.pack(side="right", fill="both", expand=True)

    # Add a label to the left section for example
    left_label = tkinter.Label(left_frame, text="Trip Planning", font=("Georgia", 24, "normal"), bg="#7e4a35", fg="white")
    left_label.place(relx=0.5, rely=0.5, anchor="center")  # Center the label in the left section

    # Add some content to the right section (Trip Planner)
    trip_label = tkinter.Label(right_frame, text="Plan Your Dream Trip!", font=("Georgia", 24, "normal"), bg="white", fg="#7e4a35")
    trip_label.pack(pady=20)

    # Starting Town Label and Dropdown (for selecting the start town)
    start_town_label = tkinter.Label(right_frame, text="Select Starting Town:", font=("Georgia", 14, "normal"), bg="white", fg="#7e4a35")
    start_town_label.pack(pady=5)

    # Dropdown list for starting town options (from the graph keys)
    towns = list(graph.keys())  # List of towns available in the graph
    global start_town_var  # Declare globally
    start_town_var = tkinter.StringVar()  # Variable to hold the selected starting town

    # Set the default value (first town in the list)
    start_town_var.set(towns[0])

    # Create the OptionMenu widget for the starting town dropdown
    start_town_dropdown = tkinter.OptionMenu(right_frame, start_town_var, *towns)
    start_town_dropdown.config(font=("Georgia", 14), width=25, relief="solid", bg="white", fg="#7e4a35")
    start_town_dropdown.pack(pady=10)

    # Destination Town Label and Dropdown (for selecting the destination town)
    destination_town_label = tkinter.Label(right_frame, text="Select Destination Town:", font=("Georgia", 14, "normal"), bg="white", fg="#7e4a35")
    destination_town_label.pack(pady=5)

    # Dropdown list for destination town options (from the graph keys)
    global destination_town_var  # Declare globally
    destination_town_var = tkinter.StringVar()  # Variable to hold the selected destination town

    # Set the default value (first town in the list)
    destination_town_var.set(towns[0])

    # Create the OptionMenu widget for the destination town dropdown
    destination_town_dropdown = tkinter.OptionMenu(right_frame, destination_town_var, *towns)
    destination_town_dropdown.config(font=("Georgia", 14), width=25, relief="solid", bg="white", fg="#7e4a35")
    destination_town_dropdown.pack(pady=10)

    # Vehicle Type Selection
    vehicle_type_label = tkinter.Label(right_frame, text="Select Vehicle Type:", font=("Georgia", 14, "normal"), bg="white", fg="#7e4a35")
    vehicle_type_label.pack(pady=5)

    global vehicle_type_var
    vehicle_type_var = tkinter.StringVar()
    vehicle_type_var.set("Car")  # Default selection

    # Radio buttons for vehicle type
    car_radio = tkinter.Radiobutton(right_frame, text="Car", variable=vehicle_type_var, value="Car", font=("Georgia", 14), bg="white", fg="#7e4a35")
    car_radio.pack(anchor="w", padx=100)
    train_radio = tkinter.Radiobutton(right_frame, text="Train", variable=vehicle_type_var, value="Train", font=("Georgia", 14), bg="white", fg="#7e4a35")
    train_radio.pack(anchor="w", padx=100)


    # result Button (for showing the shortest path)
    result_button = tkinter.Button(right_frame, text="Show Result", font=("Georgia", 14, "normal"), bg="#7e4a35",fg="white", relief="flat", width=25, command=open_result_window)
    result_button.pack(pady=10)

    # hotel Button (for showing the shortest path)
    hotel_button = tkinter.Button(right_frame, text="hotel names", font=("Georgia", 14, "normal"), bg="#8b6f47",fg="white", relief="flat", width=25, command=open_hotels_window)
    hotel_button.pack(pady=10)


# Function to handle login (account creation)
def login():
    username = username_entry.get()
    password = password_entry.get()
    user_id = user_id_entry.get()
    contact_info = contact_entry.get()

    # Check if any fields are empty
    if username == "" or password == "" or user_id == "" or contact_info == "":
        messagebox.showerror("Login Error", "Please fill in all fields.")
        return

    # Validate the username and password (for demo purposes)
    if len(username) < 4:
        messagebox.showerror("Login Error", "Username must be at least 4 characters.")
        return
    if len(password) < 6:
        messagebox.showerror("Login Error", "Password must be at least 6 characters.")
        return
    with open("user_login_info.txt", "w") as file:  # "w" mode will overwrite the file
        file.write(f"Username: {username}\n")
        file.write(f"Password: {password}\n")  # Save password to the file
        file.write(f"User ID: {user_id}\n")
        file.write(f"Contact: {contact_info}\n")
    
    # Display account creation success message
    messagebox.showinfo("Account Created", f"Your account for {username} has been created successfully!\n\nWelcome to the system!")

    # Display the success message in the answer box
    success_message.set(f"Welcome, {username}!\nID: {user_id}\nContact: {contact_info}")

# Function to reset all fields
def reset_fields():
    username_entry.delete(0, tkinter.END)
    password_entry.delete(0, tkinter.END)
    user_id_entry.delete(0, tkinter.END)
    contact_entry.delete(0, tkinter.END)
    success_message.set("")  # Clear the success message

# Function to handle existing user login
def already_have_account():
    def check_existing_user():
        entered_username = username_existing_entry.get()
        entered_password = password_existing_entry.get()
        

        # Check if all fields are filled
        if entered_username == "" or entered_password == "" :
            messagebox.showerror("Login Error", "Please fill in all fields.")
            return

        # Check if the user exists in the file and if the entered password matches
        try:
            with open("user_login_info.txt", "r") as file:
                lines = file.readlines()

            saved_username = ""
            saved_password = ""
            
            for line in lines:
                if line.startswith("Username:"):
                    saved_username = line.split(":")[1].strip()
                if line.startswith("Password:"):
                    saved_password = line.split(":")[1].strip()
                
            # Check if the entered username and password match the saved details
            if entered_username != saved_username or entered_password != saved_password:
                messagebox.showerror("Login Error", "Your username or password is incorrect. Please try again.")
                return

            

            # If all details match, show a success message
            messagebox.showinfo("Login Successful", f"Welcome back, {entered_username}!")

        except FileNotFoundError:
            messagebox.showerror("Login Error", "No existing user data found.")
            return    # Create new window for existing user login
    existing_user_window = tkinter.Toplevel(window)
    existing_user_window.title("Existing User Login")
    existing_user_window.geometry("500x400")
    

    # Username Label and Entry
    username_existing_label = tkinter.Label(existing_user_window, text="Username:", font=("Georgia", 14, "normal"),bg="white", fg="#7e4a35")
    username_existing_label.pack(pady=5)
    username_existing_entry = tkinter.Entry(existing_user_window, font=("Georgia", 14), bd=2, relief="solid", width=25)
    username_existing_entry.pack(pady=10)

    # Password Label and Entry
    password_existing_label = tkinter.Label(existing_user_window, text="Password:", font=("Georgia", 14, "normal"),bg="white", fg="#7e4a35")
    password_existing_label.pack(pady=5)
    password_existing_entry = tkinter.Entry(existing_user_window, font=("Georgia", 14), bd=2, relief="solid", show="*", width=25)
    password_existing_entry.pack(pady=10)

    

    # Login Button
    login_button_existing = tkinter.Button(existing_user_window, text="Login", font=("Georgia", 14, "bold"),bg="#7e4a35", fg="white", relief="flat", width=25, command=check_existing_user)
    login_button_existing.pack(pady=20)

# Create login page window
def create_Sign_page():
    global username_entry, password_entry, user_id_entry, contact_entry, success_message, window

    window = tkinter.Tk()
    window.title("Sign_In Page")
    window.geometry("1000x800")

    # Set the background color and window layout
    window.configure(bg="#3C2A69")  # Set background color of the window

    # Left section: Color section (instead of an image)
    left_frame = tkinter.Frame(window, bg="#7e4a35", width=500, height=600)
    left_frame.pack(side="left", fill="y")

    # Right section: Login form
    right_frame = tkinter.Frame(window, bg="white", width=500, height=600)
    right_frame.pack(side="right", fill="both", expand=True)

    # Title label (Login header)
    title_label = tkinter.Label(right_frame, text="Sign_In", font=("Georgia", 24, "normal"), bg="white", fg="#7e4a35")
    title_label.pack(pady=30)

    # Username Label and Entry
    username_label = tkinter.Label(right_frame, text="Username:", font=("Georgia", 14, "normal"), bg="white", fg="#7e4a35")
    username_label.pack(pady=5)
    username_entry = tkinter.Entry(right_frame, font=("Georgia", 14), bd=2, relief="solid", width=25)
    username_entry.pack(pady=10)

    # Password Label and Entry
    password_label = tkinter.Label(right_frame, text="Password:", font=("Georgia", 14, "normal"), bg="white", fg="#7e4a35")
    password_label.pack(pady=5)
    password_entry = tkinter.Entry(right_frame, font=("Georgia", 14), bd=2, relief="solid", show="*", width=25)
    password_entry.pack(pady=10)

    # ID Label and Entry
    user_id_label = tkinter.Label(right_frame, text="CNIC:", font=("Georgia", 14, "normal"), bg="white", fg="#7e4a35")
    user_id_label.pack(pady=5)
    user_id_entry = tkinter.Entry(right_frame, font=("Georgia", 14), bd=2, relief="solid", width=25)
    user_id_entry.pack(pady=10)



    # Validation function for numeric input
    def validate_numeric_input(input_value):
        return input_value.isdigit() or input_value == ""


    # Contact Info Label and Entry
    contact_label = tkinter.Label(right_frame, text="Contact Information:", font=("Georgia", 14, "normal"), bg="white", fg="#7e4a35")
    contact_label.pack(pady=5)

    # Register the validation function
    validate_command = window.register(validate_numeric_input)
    contact_entry = tkinter.Entry(right_frame, font=("Georgia", 14), bd=2, relief="solid", width=25,validate="key",
    validatecommand=(validate_command, "%P"))  # %P is the new text in the entry)
    contact_entry.pack(pady=10)

    # Login Button (for creating a new account)
    Sign_button = tkinter.Button(right_frame, text="Sign_Up", font=("Georgia", 14, "bold"), bg="#d4ac6e",fg="white", relief="flat", width=25, command=login)
    Sign_button.pack(pady=10)

    # Reset Button
    reset_button = tkinter.Button(right_frame, text="Reset", font=("Georgia", 14, "bold"), bg="#8b6f47", fg="white", relief="flat", width=25, command=reset_fields)
    reset_button.pack(pady=10)

    # Already Have Account Button
    already_have_account_button = tkinter.Button(right_frame, text="Already Have an Account?", font=("Georgia", 14, "bold"), bg="#7e4a35",
                                                 fg="white", relief="flat", width=25, command=already_have_account)
    already_have_account_button.pack(pady=10)

    # Label for success or error message (answer box)
    success_message = tkinter.StringVar()
    success_label = tkinter.Label(right_frame, textvariable=success_message, font=("Georgia", 14), bg="white", fg="#3C2A69", wraplength=250, justify="center")
    success_label.pack(pady=10)

    # Add some space at the bottom for aesthetics
    bottom_label = tkinter.Label(right_frame, text="Please enter your details to Sign_In", font=("Georgia", 14), bg="white", fg="#7e4a35")
    bottom_label.pack(pady=10)



def open_start_window():
    start_window = tkinter.Toplevel(root)
    start_window.title("Start Your Journey")
    start_window.geometry("800x600")  # Set the size of the window
    
    # Load and blur the background image
    image_path = r"C:\Users\fatima\Desktop\areeba uni\2nd semester\DATA STRUCTURE\data labs\background1.jpg"
    image = Image.open(image_path)
    blurred_image = image.filter(ImageFilter.GaussianBlur(5))  # Apply a blur with a radius of 5
    bg_image = ImageTk.PhotoImage(blurred_image)
    
    # Store the image reference to prevent garbage collection
    start_window.bg_image = bg_image
    
    # Set the background image to a label
    bg_label = tkinter.Label(start_window, image=bg_image)
    bg_label.place(relheight=1, relwidth=1)  # Stretch the background image to fill the window
    
    # Add a main heading
    heading_label = tkinter.Label(
        start_window, 
        text="“Take only memories, leave only footprints.”", 
        font=("Georgia", 24, "normal"), 
        bg="#4f3222",  # Solid background color for the text
        fg="white"
    )
    heading_label.pack(pady=20)

    
    # Add a plan your trip button
    trip_button = tkinter.Button(
        start_window,
        text="Plan Your Trip With Us",
        font=('Georgia', 16),
        bg="#7e4a35",  # Background color
        fg="white",
        width=25, relief="flat",
        command=open_trip_planner_window
    )
    trip_button.place(relx=0.5, rely=0.5, anchor='center')  # Centered below the Login button
    
    
    
     # Add a toggle button to remove or restore the background
    is_background_shown = [True]  # Use a mutable list to track the toggle state

    def toggle_button_action():
        if is_background_shown[0]:  # If the background is currently shown
            bg_label.place_forget()  # Hide the background image
            start_window.configure(bg="white")  # Set plain white background
            heading_label.configure(bg="white", fg="black")  # Adjust heading label colors
            toggle_button.config(text="Show Background", bg="#dac292")  # Update the toggle button text
        else:  # If the background is currently hidden
            bg_label.place(relheight=1, relwidth=1)  # Show the background image
            start_window.configure(bg="#dac292")  # Reset window background
            heading_label.configure(bg="#dac292", fg="white")  # Reset heading label colors
            toggle_button.config(text="Remove Background", bg="#dac292")  # Update the toggle button text
        
        is_background_shown[0] = not is_background_shown[0]  # Toggle the state

    toggle_button = tkinter.Button(
        start_window,
        text="Remove Background",  # Initial state
        font=('Georgia', 16),
        bg="#8b6f47",  # Background color
        fg="white",
        width=25, relief="flat",
        command=toggle_button_action  # Link to toggle function
    )
    toggle_button.place(relx=0.5, rely=0.6, anchor='center')


def save_feedback(feedback):

    local_tz = pytz.timezone("Asia/Karachi")
    # Get the current date and time
    current_time = datetime.now().strftime("%I:%M%p")
    
    # Open the feedback file and append the feedback with date and time
    with open("feedback.txt", "a") as file:  # Change to 'a' to append instead of overwriting
        file.write(f"Time: {current_time}\n")
        file.write(f"Feedback: {feedback}\n")
        file.write("-" * 40 + "\n")
        
# Function to open a feedback window with a blurred background
def open_feedback_window():
    feedback_window = tkinter.Toplevel(root)
    feedback_window.title("Feedback")
    feedback_window.geometry("400x300")  # Set the size of the feedback window
    
    # Load and blur the background image
    image_path = r"C:\Users\fatima\Desktop\areeba uni\2nd semester\DATA STRUCTURE\data labs\background1.jpg"
    image = Image.open(image_path)
    blurred_image = image.filter(ImageFilter.GaussianBlur(5))  # Apply a blur with a radius of 5
    bg_image = ImageTk.PhotoImage(blurred_image)
    
    # Store the image reference to prevent garbage collection
    feedback_window.bg_image = bg_image
    
    # Set the background image to a label
    bg_label = tkinter.Label(feedback_window, image=bg_image)
    bg_label.place(relheight=1, relwidth=1)
    
    # Add a label for feedback
    feedback_label = tkinter.Label(feedback_window, text="“Great things are never done alone.”", font=('Georgia', 19, 'normal'), bg="#4f3222",  
    fg="white")
    feedback_label.pack(pady=10)
    
    # Create a Text widget for feedback
    feedback_text = tkinter.Text(feedback_window, height=6, width=40, font=('Georgia', 12))
    
    # Set the background color of the area where the user will type
    feedback_text.config(bg="#e6e2d3", fg="black")  # Set background to #4CAF50 (green) and text to white
    
    feedback_text.pack(pady=10, padx=20, fill="both", expand=True)
        
    # Function to handle feedback submission
    def submit_feedback():
        # Get the feedback text from the Text widget
        feedback = feedback_text.get("1.0", "end-1c").strip()  # Strip to remove trailing newline
        if feedback:
            save_feedback(feedback)  # Save the feedback to the file
            messagebox.showinfo("Success", "Feedback submitted successfully!")
            feedback_window.destroy()  # Close the feedback window
        else:
            messagebox.showwarning("Input Error", "Please provide some feedback.")
    

    # Add a submit button
    submit_button = tkinter.Button(
        feedback_window, 
        text="Submit Feedback", 
        font=('Georgia', 16),
        bg="#8b6f47",  # Background color
        fg="white",
        width=25, relief="flat",
        command=submit_feedback  # Use submit_feedback to handle the button click
    )
    submit_button.pack(pady=10)

    # Add a back button to close the feedback window
    back_button = tkinter.Button(
        feedback_window, 
        text="  Back  ", 
        font=('Georgia', 16),
        bg="#7e4a35",  # Background color
        fg="white",
        width=25, relief="flat",
        command=feedback_window.destroy  # Close the feedback window when clicked
    )
    back_button.pack(pady=10)

# Create the main window
root = tkinter.Tk()
root.title("Welcome To Route Craft")
root.geometry("500x600")


# Load the image using Pillow
image_path = r"C:\Users\fatima\Desktop\areeba uni\2nd semester\DATA STRUCTURE\data labs\background1.jpg"
image = Image.open(image_path)
bg_image = ImageTk.PhotoImage(image)

# Store the image reference to prevent garbage collection
root.bg_image = bg_image

# Set the background image
bg_label = tkinter.Label(root, image=bg_image)
bg_label.place(relheight=1, relwidth=1)

# Add a text label on top of the image
text_label = tkinter.Label(
    root,
    text="Welcome to Route Craft",
    font=('Georgia', 24, 'normal'),
    bg="#4f3222",  # Solid background color for the text
    fg="white"
)
text_label.place(relx=0.5, rely=0.1, anchor='center')  # Centered at the top

# Add a "Feedback" button
feedback_button = tkinter.Button(
    root,
    text="Feedback",
    font=('Georgia', 16),
    bg="#d4ac6e",  # Background color
    fg="white",
    width=25, relief="flat",
    command=open_feedback_window  # When clicked, it opens the feedback window
)
feedback_button.place(relx=0.5, rely=0.3, anchor='center')  # Centered below the Login button


# Add a "Login Account" button
login_account = tkinter.Button(
    root,
    text="Sign_In",
    font=('Georgia', 16),
    bg="#8b6f47",  # Background color
    fg="white",
    width=25, relief="flat",
    command= create_Sign_page# When clicked, it opens the blank window
)
login_account.place(relx=0.5, rely=0.4, anchor='center')  # Centered below the text label


# Add a "start_journey" button
start_journey = tkinter.Button(
    root,
    text="Let's Start Your Journey",
    font=('Georgia', 16),
    bg="#7e4a35",  # Background color
    fg="white",
    width=25, relief="flat",
    command=open_start_window  # When clicked, it opens the blank window
)
start_journey.place(relx=0.5, rely=0.5, anchor='center')  # Centered below the text label

# Run the main loop
root.mainloop()
