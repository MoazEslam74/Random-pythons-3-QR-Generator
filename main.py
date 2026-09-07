import qrcode

data = "https://www.example.com"

qr=qrcode.make(data)
qr.save("example.png")

print("QR code created successfully")