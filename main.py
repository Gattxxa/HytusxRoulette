import io
from PIL import Image, ImageTk
import random
import requests
import tkinter as tk
import webbrowser

# Share message (https://tools.ikunaga.net/tweet-link/)
HTTPS = "https://twitter.com/intent/tweet?text="
SUCCEED_MESSAGE = "%E5%9B%9E%E3%81%A7%E3%81%8B%E3%81%97%E3%82%8F%E3%81%AE%E5%BE%A9%E6%B4%BB%E3%81%AB%E6%88%90%E5%8A%9F%E3%81%97%E3%81%BE%E3%81%97%E3%81%9F%EF%BC%81%EF%BC%81"
FAILED_MESSAGE = "%E3%81%8B%E3%81%97%E3%82%8F%E3%81%AE%E5%BE%A9%E6%B4%BB%E3%81%AB%E5%A4%B1%E6%95%97%E3%81%97%E3%81%BE%E3%81%97%E3%81%9F%E2%80%A6%E2%80%A6"
SHARE = "%20%23%E3%81%8B%E3%81%97%E3%82%8F%E3%83%AB%E3%83%BC%E3%83%AC%E3%83%83%E3%83%88%0Ahttps%3A%2F%2Fgithub.com%2FGattxxa%2FHytusxRoulette"

# Images
IMG_BACKGROUND = "https://raw.githubusercontent.com/Gattxxa/HytusxRoulette/master/img/background/background.png"
HYTUSX_NW = "https://raw.githubusercontent.com/Gattxxa/HytusxRoulette/master/img/hytusx/hytusx_nw.png"
HYTUSX_NE = "https://raw.githubusercontent.com/Gattxxa/HytusxRoulette/master/img/hytusx/hytusx_ne.png"
HYTUSX_SW = "https://raw.githubusercontent.com/Gattxxa/HytusxRoulette/master/img/hytusx/hytusx_sw.png"
HYTUSX_SE = "https://raw.githubusercontent.com/Gattxxa/HytusxRoulette/master/img/hytusx/hytusx_se.png"

# Global
cnt = 0
success = False

# Share result
def tweet():
    if success:
        link = HTTPS + str(cnt) + SUCCEED_MESSAGE + SHARE
    else:
        link = HTTPS + FAILED_MESSAGE + SHARE
    return webbrowser.open(link, new=0, autoraise=True)

# Webから画像持ってくる君
def get_image(url, angle):
    image = Image.open(io.BytesIO(requests.get(url).content))
    return ImageTk.PhotoImage(image.rotate(angle))

# HytusxRoulette
root = tk.Tk()
root.title('HytusxRoulette')
root.geometry('854x480')
root.resizable(width=0, height=0)

# hyretsux（hytusxではない）
hytusx_parts = [get_image(HYTUSX_NW, 0), get_image(HYTUSX_NE, 0), 
                get_image(HYTUSX_SW, 0), get_image(HYTUSX_SE, 0)]
for angle in range(90, 360, 90):
    hytusx_parts.append(get_image(HYTUSX_NW, angle))
    hytusx_parts.append(get_image(HYTUSX_NE, angle))
    hytusx_parts.append(get_image(HYTUSX_SW, angle))
    hytusx_parts.append(get_image(HYTUSX_SE, angle))

# background
background = get_image(IMG_BACKGROUND, 0)
canvas_background = tk.Canvas(width=854, height=480)
canvas_background.create_image(0, 0, image=background, anchor='nw')
canvas_background.pack()

# hytusx_nw
hytusx_nw = tk.Canvas(width=100, height=100, bd=-2) # bd=-2 でデフォのボーダー消せるみたい
hytusx_nw.create_image(0, 0, image=hytusx_parts[11], anchor='nw')
hytusx_nw.place(x=625, y=25)

# hytusx_ne
hytusx_ne = tk.Canvas(width=100, height=100, bd=-2)
hytusx_ne.create_image(0, 0, image=hytusx_parts[10], anchor='nw')
hytusx_ne.place(x=725, y=25)

# hytusx_sw
hytusx_sw = tk.Canvas(width=100, height=100, bd=-2)
hytusx_sw.create_image(0, 0, image=hytusx_parts[9], anchor='nw')
hytusx_sw.place(x=625, y=125)

# hytusx_se
hytusx_se = tk.Canvas(width=100, height=100, bd=-2)
hytusx_se.create_image(0, 0, image=hytusx_parts[8], anchor='nw')
hytusx_se.place(x=725, y=125)

# Game over
def game_over():
    btn_shuffle.configure(state='disable')
    btn_share = tk.Button(width=30, height=4, bg='#00ACEE', relief='groove', bd='3', 
        text='結果をシェアする', font=('Helvetica', 16),command=tweet)
    btn_share.place(x=250, y=350)

# Shuffle
def shuffle():
    global cnt, success
    cnt += 1
    nw = random.randrange(0, 15, 4)
    ne = random.randrange(1, 15, 4)
    sw = random.randrange(2, 15, 4)
    se = random.randrange(3, 15, 4)
    hytusx_nw.create_image(0, 0, image=hytusx_parts[nw], anchor='nw')
    hytusx_ne.create_image(0, 0, image=hytusx_parts[ne], anchor='nw')
    hytusx_sw.create_image(0, 0, image=hytusx_parts[sw], anchor='nw')
    hytusx_se.create_image(0, 0, image=hytusx_parts[se], anchor='nw')
    label_count['text'] = cnt
    # Success
    if nw == 0 and ne == 1 and sw == 2 and se == 3:
        success = True
        game_over()
    # Fail
    elif cnt == 100:
        game_over()
        
# Shuffle button
btn_shuffle = tk.Button(width=15, height=2, text='シャッフル', command=shuffle)
btn_shuffle.place(x=670, y=425)

# Shuffle counter
label_count = tk.Label(width=3, bg='#fafafa', relief='sunken', bd='3', font=('Helvetica', 48), anchor='e')
label_count['text'] = cnt
label_count.place(x=665, y=325)

root.mainloop()

