from tkinter import *
from tkinter import ttk, messagebox
import requests
import speedtest
from threading import Thread
from PIL import ImageTk, Image
from io import BytesIO
#import cProfile
#import asyncio


def start():
    progressbar.start(10) # запускаем progressbar
    thread = Thread(target=measure_internet_speed)
    thread.start()


def stop(): progressbar.stop()      # останавливаем progressbar


def measure_internet_speed():
    # Создаем объект Speedtest
    st = speedtest.Speedtest()
    clients = st.results.client
    text = f"IP: {clients['ip']}, {clients['isp']}; lat_lon: ({clients['lat']}, {clients['lon']})"
    st_text.configure(text=text)
    root.update()

    # Выбираем сервер для тестирования скорости http://speedtest.dataline.ua:8080/speedtest/upload.php
    best = st.get_best_server()
    text2 = text +"\n" + f"Сервер: {best['host']}; {best['country']}, {best['name']}; lat_lon: ({best['lat']}, {best['lon']})"
    st_text.configure(text=text2)
    root.update()
    # Запускаем тест скорости загрузки выгрузки
    download_speed = st.download() / 10 ** 6
    upload_speed = st.upload() / 10 ** 6

    st_ping = st.results.ping
    st_send = st.results.bytes_sent / 10 ** 6
    st_reseived = st.results.bytes_received / 10 ** 6
    st_share = st.results.share()
    img = WebImage(st_share).get()
    imagelab['image'] = img
    imagelab.image = img
    stop()

    result = (f"Скорость загрузки: {round(download_speed, 2)} Мбит/с\n"
              f"Скорость отдачи: {round(upload_speed, 2)} Мбит/с\n"
              f"Пинг: {st_ping} миллисекунд\n"
              f"Отдано: {round(st_send, 2)} Мб\n"
              f"Загружено: {round(st_reseived, 2)} Мб\n")
    messagebox.showinfo(title='Результат тестирования', message=result)


class WebImage:
    def __init__(self, url):
        u = requests.get(url)
        self.image = ImageTk.PhotoImage(Image.open(BytesIO(u.content)))

    def get(self):
        return self.image


root = Tk()
root.title("Speed test by Okla")
root.geometry('765x535+0+0')
root.iconbitmap('speedtest.ico')

st_button = Button(root, text='Начать тестирование', font=('Arial', 10, 'bold'), command=start)
st_button.grid(row=0, column=0, padx=5, pady=5, sticky='we')
st_text = Label(root, foreground='blue', font=('Arial', 12))
st_text.grid(row=1, column=0, padx=5, pady=5, sticky='we')

progressbar = ttk.Progressbar(root, orient="horizontal", mode="indeterminate")
progressbar.grid(row=2, column=0, padx=5, pady=5, sticky='we')

img_st = PhotoImage(file="photo1.png")
imagelab = Label(root, image=img_st)
imagelab.grid(row=3, column=0, padx=5, pady=5)

root.update()
mw = root.geometry()
mw = mw.split('+')
mw = mw[0].split('x')
w_win = int(mw[0])
h_win = int(mw[1])
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
ws = ws // 2 - w_win // 2
hs = hs // 2 - h_win // 2
root.geometry(f'+{ws}+{hs}')
#cProfile.run(measure_internet_speed())

root.mainloop()


# import requests
# url = '<https://example.com/image.jpg>'
# response = requests.get(url)
# with open('image.jpg', 'wb') as f:
#     f.write(response.content)