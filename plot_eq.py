import sys
import tkinter
from PIL import Image, ImageTk


def _combine_images(path_list, row=2, col=1):
    im_list = [Image.open(each) for each in path_list]
    w = im_list[0].width
    h = im_list[0].height
    output = Image.new('RGB', (w*col, h*row))
    idx = 0
    for i in range(row):
        for j in range(col):
            im = im_list[idx]
            output.paste(im, (w*j, h*i))
            idx += 1
    return output


def show_pil_image_fullscreen(pil):
    root = tkinter.Tk()
    root.attributes('-fullscreen', True)
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry('%dx%d' % (w, h))
    root.bind('<Escape>', lambda e: root.destroy())
    root.bind("q", lambda e: sys.exit())
    root.bind("<1>", lambda e: root.focus_set())
    root.focus_set()

    image = ImageTk.PhotoImage(pil)
    canvas = tkinter.Canvas(root, width=w, height=h)
    canvas.create_image(w / 2, h / 2, image=image)
    canvas.pack()

    root.mainloop()


if __name__ == '__main__':
    img = _combine_images([sys.argv[1], sys.argv[2]])
    show_pil_image_fullscreen(img)
