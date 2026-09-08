import qrcode
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw

lang = 'EN'
selected_icon_path = None  # Variable to store the selected image path

def languageTuggle():
    global lang
    if lang == 'EN':
        lang = 'AR'
    else:
        lang = 'EN'
    # You can later connect this function to a button to update the UI text

def choose_icon():
    global selected_icon_path
    file_path = filedialog.askopenfilename(
        title="Select Icon" if lang == 'EN' else "اختر أيقونة",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )
    if file_path:
        selected_icon_path = file_path
        icon_label.config(text="Icon Selected ✅" if lang == 'EN' else "تم اختيار الأيقونة ✅")

def apply_mask(img, shape):
    """Function to crop the image according to the selected shape"""
    img = img.convert("RGBA")
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    
    width, height = img.size
    
    if shape == "circle":
        draw.ellipse((0, 0, width, height), fill=255)
    elif shape == "rounded":
        radius = width // 5  # Set the corner rounding ratio
        draw.rounded_rectangle((0, 0, width, height), radius=radius, fill=255)
    else:  # square
        draw.rectangle((0, 0, width, height), fill=255)
        
    result = Image.new("RGBA", img.size)
    result.paste(img, (0, 0), mask)
    return result

def generate_qr():
    link = link_entry.get()
    
    if not link:
        if lang == 'EN':
            messagebox.showwarning("Warning", "Please enter the link first!")
        else:
            messagebox.showwarning("تنبيه", "يرجى إدخال الرابط أولاً!")
        return

    try:
        # Use advanced QR settings to keep it readable after adding the logo
        qr = qrcode.QRCode(
            version=4, # Base square size
            error_correction=qrcode.constants.ERROR_CORRECT_H, # Very high error correction (important when adding a logo)
            box_size=10,
            border=4,
        )
        qr.add_data(link)
        qr.make(fit=True)
        
        # Create the QR image
        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
        
        # If an icon was selected
        if selected_icon_path:
            icon = Image.open(selected_icon_path)
            
            # Set the icon size to about a quarter of the QR code size
            factor = 4
            icon_size = (qr_img.size[0] // factor, qr_img.size[1] // factor)
            icon = icon.resize(icon_size, Image.Resampling.LANCZOS)
            
            # Crop the icon to the selected shape
            shape = shape_var.get()
            icon = apply_mask(icon, shape)
            
            # Calculate the coordinates to place the icon in the center
            pos_x = (qr_img.size[0] - icon_size[0]) // 2
            pos_y = (qr_img.size[1] - icon_size[1]) // 2
            
            # Merge the icon with the QR code
            qr_img.paste(icon, (pos_x, pos_y), icon) # Pass icon as the mask for transparency
        
        # Save the final image
        file_name = "Exported.png"
        qr_img.save(file_name)
        
        # Display the image inside the interface
        qr_img_resized = qr_img.resize((200, 200)) 
        tk_img = ImageTk.PhotoImage(qr_img_resized)
        
        qr_label.config(image=tk_img)
        qr_label.image = tk_img
        
        if lang == 'EN':
            messagebox.showinfo("Success", "QR Code created and saved successfully!")
        else:
            messagebox.showinfo("نجاح", "تم إنشاء وحفظ الـ QR Code بنجاح!")
            
    except Exception as e:
        if lang == 'EN':
            messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("خطأ", f"حدث خطأ: {e}")

# Set up the window
root = tk.Tk()
root.title("Advanced QR Code Generator")
root.geometry("400x650") # Slightly enlarge the window to fit the new elements
root.eval('tk::PlaceWindow . center')

# Link title
title_label = tk.Label(root, text="Enter the link here:", font=("Arial", 12, "bold"))
title_label.pack(pady=(15, 5))

link_entry = tk.Entry(root, width=40, font=("Arial", 12))
link_entry.pack(pady=5)

# Decorative separator line
tk.Frame(root, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=20, pady=10)

# Icon selection section
icon_label_title = tk.Label(root, text="Add an Icon (Optional):", font=("Arial", 10, "bold"))
icon_label_title.pack(pady=5)

icon_btn = tk.Button(root, text="Browse Icon...", command=choose_icon, font=("Arial", 10))
icon_btn.pack(pady=5)

icon_label = tk.Label(root, text="No icon selected", fg="gray")
icon_label.pack(pady=2)

# Icon shape selection section
shape_var = tk.StringVar(value="square") # Default shape

shape_frame = tk.Frame(root)
shape_frame.pack(pady=10)

tk.Radiobutton(shape_frame, text="Square", variable=shape_var, value="square").pack(side=tk.LEFT, padx=5)
tk.Radiobutton(shape_frame, text="Rounded", variable=shape_var, value="rounded").pack(side=tk.LEFT, padx=5)
tk.Radiobutton(shape_frame, text="Circle", variable=shape_var, value="circle").pack(side=tk.LEFT, padx=5)

# Decorative separator line
tk.Frame(root, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=20, pady=10)

# QR Code generation button
generate_btn = tk.Button(root, text="Generate QR Code", command=generate_qr, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", padx=10)
generate_btn.pack(pady=10)

# Image display area
qr_label = tk.Label(root)
qr_label.pack(pady=10)

if __name__ == "__main__":
    root.mainloop()