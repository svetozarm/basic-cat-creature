#!/usr/bin/python

import Tkinter
import os, sys, datetime
from PIL import ImageTk, Image

class ImageSelector(Tkinter.Tk):

    img_list = []
    sel_list = None
    idx = 0
    photoView = None
    checkView = None
    img = None
    prevImg = None
    nextImg = None

    def __init__(self, parent, dirname):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.bind("<Control-w>", self.quit)
        self.bind("<Right>", self.nextImage)
        self.bind("<Left>", self.prevImage)
        self.bind("<space>", self.toggleCurrent)
        for f in os.listdir(dirname):
            filename = "%s/%s" % (dirname,f)
            if self.isImage(filename):
                self.img_list += [filename]
        self.img_list.sort()

        if len(self.img_list) == 0:
            print "No images found at " + dirname
            exit()

        self.sel_list = [ False ] * len(self.img_list)
        self.checkView = Tkinter.Checkbutton(self)
        self.checkView.pack()

        self.showImage()

    def isImage(self, filename):
        if (filename.lower().endswith(".jpg")):
            return True
        return False

    def getSize(self, imgsize):
        self.update()
        ww = self.winfo_width()
        wh = self.winfo_height() - self.checkView.winfo_height()
        iw = imgsize[0]
        ih = imgsize[1]

        ratio = float(ww) / float(iw)
        w = ratio * iw
        h = ratio * ih

        if h > wh:
            ratio = float(ww) / float(iw)
            w = ratio * iw
            h = ratio * ih


        return (int(w), int(h))

    def nextImage(self, event):
        self.idx += 1
        if self.idx >= len(self.img_list):
            self.idx = 0
        self.showImage()
        self.updateCheck()

    def prevImage(self, event):
        if self.idx == 0:
            self.idx = len(self.img_list) - 1
        else:
            self.idx -= 1
        self.showImage()
        self.updateCheck()
    
    def toggleCurrent(self, event):
        self.sel_list[self.idx] = not self.sel_list[self.idx]
        self.updateCheck()

    def updateCheck(self):
        if self.sel_list[self.idx]:
            self.checkView.select()
        else:
            self.checkView.deselect()

    def showImage(self):
        if self.photoView:
            self.photoView.destroy()
        im_temp = Image.open(self.img_list[self.idx])
        size = self.getSize(im_temp.size)
        im_temp = im_temp.resize(size)

        self.img = ImageTk.PhotoImage(im_temp);
        self.photoView = Tkinter.Label(self, image = self.img)
        self.photoView.pack()#fill="both", expand="yes")
        #self.pack()

    def dumpToFile(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        with open("selection_%s.txt" % timestamp, "w") as f:
            for i in xrange(len(self.sel_list)):
                if self.sel_list[i]:
                    f.write(self.img_list[i])
                    f.write("\n")


    def quit(self, event):
        self.dumpToFile()
        self.destroy()

if len(sys.argv) < 2:
    print "Please provide a directory name"
    exit()
dirname = os.path.abspath(sys.argv[1])

if __name__ == "__main__":
    app = ImageSelector(None, dirname)
    app.title("ImageSelector")
    app.mainloop()


