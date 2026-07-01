from PIL import Image, ImageDraw, ImageFont

img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

draw.rounded_rectangle((2, 2, 62, 62), radius=8, fill="#1a1a1a")
draw.ellipse((16, 8, 48, 40), fill="#00ff88")
draw.rectangle((12, 40, 52, 56), fill="#00ff88")
draw.text((22, 18), "AI", fill="#1a1a1a", font=None)

img.save("app_icon.png")
img.save("app_icon.ico", format="ICO", sizes=[(64, 64)])
