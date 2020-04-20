from tkinter import *
from PIL import Image, ImageTk

# To be honest, I realised that playing gifs with tkinter is a bad idea,
# but it was too late to choose another implementation.
# So I found class, that does what I want and make it work for my case.


class Animation(Label):
    def __init__(self, master, fps):
        seq = []
        # Save all the images that are in 'frames' folder
        i = 1
        try:
            while 1:
                filename = 'frames/_img{:04d}.png'.format(i)
                img = Image.open(filename)
                seq.append(img.copy())
                i += 1
        except FileNotFoundError:
            # images ended
            pass

        self.delay = 1000 // fps
        first = seq[0].convert('RGBA')

        self.frames = [ImageTk.PhotoImage(first)]

        Label.__init__(self, master, image=self.frames[0])

        temp = seq[0]
        for image in seq[1:]:
            temp.paste(image)
            frame = temp.convert('RGB')
            self.frames.append(ImageTk.PhotoImage(frame))

        self.idx = 0

        self.cancel = self.after(self.delay, self.play)

    def play(self):
        self.config(image=self.frames[self.idx])
        self.idx += 1
        if self.idx == len(self.frames):
            self.idx = 0
        self.cancel = self.after(self.delay, self.play)

