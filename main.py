import qrcode

def main(): 

    link=input("Enter the link :")


    qr=qrcode.make(link)
    qr.save("example.png")

    print("QR code created successfully")

if __name__ == "__main__":
    main()