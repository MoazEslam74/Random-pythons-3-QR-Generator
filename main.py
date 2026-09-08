import qrcode
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw

lang = 'EN'
selected_icon_path = None  # Variable to store the selected image path

def toggle_language():
    """Function to switch languages and update the interface"""
    global lang
    if lang == 'EN':
        lang = 'AR'
    else:
        lang = 'EN'
    update_ui_texts()
    
def paste_arabic(event):
    """Function to support paste shortcut when the keyboard is in Arabic mode"""
    event.widget.event_generate("<<Paste>>")
    return "break"

def selectAll_arabic(event):
    """Function to support selectAll shortcut when the keyboard is in Arabic mode"""
    event.widget.event_generate("<<SelectAll>>")
    return "break"

def copy_arabic(event):
    """Function to support copy shortcut when the keyboard is in Arabic mode"""
    event.widget.event_generate("<<Copy>>")
    return "break"

def cut_arabic(event):
    """Function to support cut shortcut when the keyboard is in Arabic mode"""
    event.widget.event_generate("<<Cut>>")
    return "break"

def update_ui_texts():
    """Function to change the interface text based on the current language"""
    if lang == 'EN':
        root.title("Advanced QR Code Generator")
        lang_btn.config(text="عربي")
        title_label.config(text="Enter the link here:")
        icon_label_title.config(text="Add an Icon (Optional):")
        icon_btn.config(text="Browse Icon...")
        
        if selected_icon_path:
            icon_label.config(text="Icon Selected ✅")
        else:
            icon_label.config(text="No icon selected")
            
        rb_square.config(text="Square")
        rb_rounded.config(text="Rounded")
        rb_circle.config(text="Circle")
        generate_btn.config(text="Generate QR Code")
    else:
        root.title("صانع الـ QR Code المتقدم")
        lang_btn.config(text="English")
        title_label.config(text="أدخل الرابط هنا:")
        icon_label_title.config(text="إضافة أيقونة (اختياري):")
        icon_btn.config(text="تصفح الأيقونة...")
        
        if selected_icon_path:
            icon_label.config(text="تم اختيار الأيقونة ✅")
        else:
            icon_label.config(text="لم يتم اختيار أيقونة")
            
        rb_square.config(text="مربع")
        rb_rounded.config(text="حواف دائرية")
        rb_circle.config(text="دائري")
        generate_btn.config(text="إنشاء رمز QR")

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
    """Crop the image according to the selected shape"""
    img = img.convert("RGBA")
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    
    width, height = img.size
    
    if shape == "circle":
        draw.ellipse((0, 0, width, height), fill=255)
    elif shape == "rounded":
        radius = width // 5 
        draw.rounded_rectangle((0, 0, width, height), radius=radius, fill=255)
    else:  
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
        qr = qrcode.QRCode(
            version=4, 
            error_correction=qrcode.constants.ERROR_CORRECT_H, 
            box_size=10,
            border=4,
        )
        qr.add_data(link)
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
        
        if selected_icon_path:
            icon = Image.open(selected_icon_path)
            
            factor = 4
            icon_size = (qr_img.size[0] // factor, qr_img.size[1] // factor)
            icon = icon.resize(icon_size, Image.Resampling.LANCZOS)
            
            shape = shape_var.get()
            icon = apply_mask(icon, shape)
            
            pos_x = (qr_img.size[0] - icon_size[0]) // 2
            pos_y = (qr_img.size[1] - icon_size[1]) // 2
            
            qr_img.paste(icon, (pos_x, pos_y), icon) 
        
        file_name = "Exported.png"
        qr_img.save(file_name)
        
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
root.geometry("400x680") # Slight increase in height to fit the new button
root.eval('tk::PlaceWindow . center')

# Language toggle button (placed at the top-right)
lang_btn = tk.Button(root, text="عربي", command=toggle_language, font=("Arial", 10, "bold"), bg="#2196F3", fg="white", cursor="hand2")
lang_btn.pack(anchor="ne", padx=10, pady=5)

# Link title
title_label = tk.Label(root, text="Enter the link here:", font=("Arial", 12, "bold"))
title_label.pack(pady=(5, 5))

link_entry = tk.Entry(root, width=40, font=("Arial", 12))
link_entry.pack(pady=5)

#Arabic shortcuts
link_entry.bind("<Control-ر>", paste_arabic)
link_entry.bind("<Control-ش>", selectAll_arabic) # Ctrl + a
link_entry.bind("<Control-ؤ>", copy_arabic)      # Ctrl + c
link_entry.bind("<Control-ء>", cut_arabic)       # Ctrl + x
# Decorative separator line
tk.Frame(root, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=20, pady=10)

# Icon selection section
icon_label_title = tk.Label(root, text="Add an Icon (Optional):", font=("Arial", 10, "bold"))
icon_label_title.pack(pady=5)

icon_btn = tk.Button(root, text="Browse Icon...", command=choose_icon, font=("Arial", 10), cursor="hand2")
icon_btn.pack(pady=5)

icon_label = tk.Label(root, text="No icon selected", fg="gray")
icon_label.pack(pady=2)

# Icon shape selection section
shape_var = tk.StringVar(value="square") # Default shape

shape_frame = tk.Frame(root)
shape_frame.pack(pady=10)

rb_square = tk.Radiobutton(shape_frame, text="Square", variable=shape_var, value="square", cursor="hand2")
rb_square.pack(side=tk.LEFT, padx=5)

rb_rounded = tk.Radiobutton(shape_frame, text="Rounded", variable=shape_var, value="rounded", cursor="hand2")
rb_rounded.pack(side=tk.LEFT, padx=5)

rb_circle = tk.Radiobutton(shape_frame, text="Circle", variable=shape_var, value="circle", cursor="hand2")
rb_circle.pack(side=tk.LEFT, padx=5)

# Decorative separator line
tk.Frame(root, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=20, pady=10)

# QR Code generation button
generate_btn = tk.Button(root, text="Generate QR Code", command=generate_qr, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", padx=10, cursor="hand2")
generate_btn.pack(pady=10)

# Image display area
qr_label = tk.Label(root)
qr_label.pack(pady=10)

if __name__ == "__main__":
    root.mainloop()