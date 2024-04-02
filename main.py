import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

def show_error(message):
    messagebox.showerror("Ошибка", message)

def show_confirmation(message):
    messagebox.showinfo("Сохранено", message)

def process_image():
    if file_path == "":
        show_error("Выберите изображение перед запуском.")
        return

    scale_percentage = entry_scale.get()
    if scale_percentage == '':
        show_error('Введите процент масштабирования.')
        return

    try:
        scale_percentage = float(scale_percentage)
    except ValueError:
        show_error('Неверный формат процента масштабирования.')
        return

    if scale_percentage < 0.01 or scale_percentage > 99999999:
        show_error('Процент масштабирования должен быть в диапазоне от 0.01 до 99999999.')
        return
    
    if scale_percentage >= 100:
    
      width = max(1, int(image.width * scale_percentage / 100))
      height = max(1, int(image.height * scale_percentage / 100))
    else:
      width = max(1, int(image.width * scale_percentage / 100))
      height = max(1, int(image.height * scale_percentage / 100))

    width = max(1, int(image.width * scale_percentage / 100))
    height = max(1, int(image.height * scale_percentage / 100))

    ascii_chars = '@%# '

    ascii_image = ''
    img_width, img_height = image.size
    for y in range(0, img_height, max(1, img_height // height)):
        for x in range(0, img_width, max(1, img_width // width)):
            avg_pixel_value = 0
            count = 0
            for i in range(max(1, img_width // width)):
                for j in range(max(1, img_height // height)):
                    try:
                        pixel_value = image.getpixel((x + i, y + j))
                        avg_pixel_value += pixel_value[0]  # Используйте [0] для выбора компоненты цвета
                        count += 1
                    except IndexError:
                        pass
            avg_pixel_value //= count
            ascii_image += ascii_chars[avg_pixel_value // 85]
        ascii_image += '\n'

    file_name = file_path.split('/')[-1].split('.')[0]

    imports_dir = 'imports'
    outputs_dir = 'outputs'

    if not os.path.exists(imports_dir):
        os.makedirs(imports_dir)
    
    import_path = os.path.join(imports_dir, file_path.split('/')[-1])
    image.save(import_path)

    if not os.path.exists(outputs_dir):
        os.makedirs(outputs_dir)

    output_path = os.path.join(outputs_dir, f'{file_name}.txt')
    with open(output_path, 'w') as file:
        file.write(ascii_image)

    show_confirmation(f'ASCII-арт изображения сохранен в файл {output_path}')

def select_image():
    global file_path, image
    file_path = filedialog.askopenfilename()
    image = Image.open(file_path)
    image.thumbnail((100, 100))
    img_photo = ImageTk.PhotoImage(image)
    label_image.config(image=img_photo)
    label_image.image = img_photo

root = tk.Tk()
root.title('ASCII Art Generator')
root.resizable(False, False)

file_path = ""
image = None

label_scale = tk.Label(root, text='Введите масштабирование ASCII-арта в процентах относительно оригинала:')
label_scale.pack()
entry_scale = tk.Entry(root)
entry_scale.pack()

button_browse = tk.Button(root, text='Выбрать файл изображения', command=select_image)
button_browse.pack()

button_start = tk.Button(root, text='Начать', command=process_image)
button_start.pack()

frame = tk.Frame(root)
frame.pack(side='right')

label_image = tk.Label(frame)
label_image.pack()

root.mainloop()