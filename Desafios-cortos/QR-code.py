import qrcode

data = 'Don\'t forget to subscribe'

qr = qrcode.QRCode(version = 1, box_size=10, border=5)
qr.add_data(data)

qr.make(fit=True)
img = qr.make_image(fill_color = 'blue', back_color = 'white')

img = qrcode.make(data)

img.save('C:/Users/javie/OneDrive/Escritorio/Python/New/myqrcode.png')




