import qrcode
data = 'Código QR usando la función make()'

img = qrcode.make(data)
img.save('gr1.png')