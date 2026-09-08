import qrcode
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
lang='EN'
def languageTuggle():
    global lang
    if lang == 'EN':
        lang = 'AR'
    else:
        lang = 'EN'

def generate_qr():
    # Get the link from the input field
    link = link_entry.get()
    
    if not link:
        if lang == 'EN':
            messagebox.showwarning("Warning", "Please enter the link first!")
        else:
            messagebox.showwarning("تنبيه", "يرجى إدخال الرابط أولاً!")
        return

    try:
        # Create the QR code
        qr_img = qrcode.make(link)
        
        # Save the image as PNG
        file_name = "example.png"
        qr_img.save(file_name)
        
        # Display the image inside the interface
        # Resize the image to fit the interface
        qr_img = qr_img.resize((200, 200)) 
        tk_img = ImageTk.PhotoImage(qr_img)
        
        # Update the image display area
        qr_label.config(image=tk_img)
        qr_label.image = tk_img # Keep the image in memory so it does not disappear
        
        if lang == 'EN':
            messagebox.showinfo("Success", "QR Code created and saved successfully!")
        else:
            messagebox.showinfo("نجاح", "تم إنشاء وحفظ الـ QR Code بنجاح!")
        
    except Exception as e:
        if lang == 'EN':
            messagebox.showerror("Error", f"An error occurred while creating the QR Code: {e}")
        else:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء الإنشاء: {e}")

# Set up the main window
root = tk.Tk()
root.title("QR Code Generator")
root.geometry("350x450")
root.eval('tk::PlaceWindow . center') # Center the window

# Add a simple title
title_label = tk.Label(root, text="Enter the link here:", font=("Arial", 14))
title_label.pack(pady=10)

# Link input field (Textfield)
link_entry = tk.Entry(root, width=40, font=("Arial", 12))
link_entry.pack(pady=10)

# Generate button (Generator Button)
generate_btn = tk.Button(root, text="Generate QR Code", command=generate_qr, font=("Arial", 12), bg="#4CAF50", fg="white")
generate_btn.pack(pady=15)

# Space for displaying the QR code below the button
qr_label = tk.Label(root)
qr_label.pack(pady=10)

# Run the interface
if __name__ == "__main__":
    root.mainloop()