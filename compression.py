import numpy
from numpy.core.fromnumeric import shape
from numpy.core.numeric import binary_repr
import cv2
import matplotlib.pyplot as plt
import sys
import os
import math
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import re
import numpy as numpy
from PIL import Image, ImageTk



def get_size(fname):
    stat = os.stat(fname)
    size=stat.st_size
    return size

# FUNCTION THAT RETURNS THE SIZE OF A FILE IN HUMAN READABLE FORM
def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

# IMAGE COMPRESSOR CLASS
class ImageCompressor(Tk):
    def __init__(self, winTitle, xSize, ySize, *args):
        super(ImageCompressor, self).__init__()
        if args:
            self.configure(bg=args)
        self.geometry(f'{xSize}x{ySize}')
        self.title(winTitle)
        self.resizable(False, False)

        self.uncompressedLabel = Label(self, text = "Uncompressed")
        self.uncompressedLabel.config(font =("Courier", 14))
        self.uncompressedLabel.place(x=200, y=15)

        self.uncompressedLabel = Label(self, text = "Compressed")
        self.uncompressedLabel.config(font =("Courier", 14))
        self.uncompressedLabel.place(x=400, y=15)

        self.uncompressedLabel = Label(self, text = "Decompressed")
        self.uncompressedLabel.config(font =("Courier", 14))
        self.uncompressedLabel.place(x=600, y=15)

        self.compressFile = Button(text="Choose Image", command=self.GetImageFile)
        self.compressFile.place(x=25, y=15)

        self.compressImageBtn = Button(text="Huffman Compress", command=self.CompressImageHuffman, bd=5)
        self.compressImageBtn.place(x=25, y=45)
        self.compressImageBtn = Button(text="Huffman Decompress", command=self.DecompressImageHuffman, bd=5)
        self.compressImageBtn.place(x=25, y=75)

        self.SVDcompressImageBtn = Button(text="SVD Compress", command=self.SVDCompress, bd=5)
        self.SVDcompressImageBtn.place(x=25, y=105)
        
        self.mainloop()

    #  FUNCTION TO COLLECT CHOSEN IMAGE
    def GetImageFile(self):
        self.compressLocation = filedialog.askopenfilename()
        if self.compressLocation:
            print(self.compressLocation)
            self.imagePic = Image. open(self.compressLocation)
            self.imagePic = self.imagePic.resize((150,150))
            self.image2 =  ImageTk. PhotoImage(self.imagePic)
            self.image_label = ttk. Label(self , image = self.image2)
            self.image_label.place(x=200, y=50)

            self.imageSize = (convert_size(get_size(self.compressLocation)))
            self.uncompressedLabelSize = Label(self, text = self.imageSize)
            self.uncompressedLabelSize.config(font =("Courier", 14))
            self.uncompressedLabelSize.place(x=200, y=210)
            messagebox.showinfo("File", self.compressLocation)

        else:
            messagebox.showwarning("Error", "No image selected")

    # FUNCTION TO CALCULATE MSE
    def mse(self, imageA, imageB):
        img1 = cv2.imread(imageA, 0) 
        img2 = cv2.imread(imageB, 0) 
        err = numpy.sum((img1.astype("float") - img2.astype("float")) ** 2)
        err /= float(img1.shape[0] * img1.shape[1])
        return err

    # FUNCTION TO COMPRESS IMAGE USING HUFFMAN
    def CompressImageHuffman(self):
        try:
            file = self.compressLocation
            my_string = numpy.asarray(Image.open(file),numpy.uint8)
            global shape
            shape = my_string.shape
            a = my_string
            print ("Enetered string is:",my_string)
            my_string = str(my_string.tolist())

            letters = []
            only_letters = []
            for letter in my_string:
                if letter not in letters:
                    frequency = my_string.count(letter)             #frequency of each letter repetition
                    letters.append(frequency)
                    letters.append(letter)
                    only_letters.append(letter)

            nodes = []
            while len(letters) > 0:
                nodes.append(letters[0:2])
                letters = letters[2:]                               # sorting according to frequency
            nodes.sort()
            huffman_tree = []
            huffman_tree.append(nodes)                             #Make each unique character as a leaf node

            def combine_nodes(nodes):
                pos = 0
                newnode = []
                if len(nodes) > 1:
                    nodes.sort()
                    nodes[pos].append("1")                       # assigning values 1 and 0
                    nodes[pos+1].append("0")
                    combined_node1 = (nodes[pos] [0] + nodes[pos+1] [0])
                    combined_node2 = (nodes[pos] [1] + nodes[pos+1] [1])  # combining the nodes to generate pathways
                    newnode.append(combined_node1)
                    newnode.append(combined_node2)
                    newnodes=[]
                    newnodes.append(newnode)
                    newnodes = newnodes + nodes[2:]
                    nodes = newnodes
                    huffman_tree.append(nodes)
                    combine_nodes(nodes)
                return huffman_tree                                     # huffman tree generation

            newnodes = combine_nodes(nodes)

            huffman_tree.sort(reverse = True)
            print("Huffman tree with merged pathways:")

            checklist = []
            for level in huffman_tree:
                for node in level:
                    if node not in checklist:
                        checklist.append(node)
                    else:
                        level.remove(node)
            count = 0
            for level in huffman_tree:
                print("Level", count,":",level)             #print huffman tree
                count+=1
            print()

            global letter_binary
            letter_binary = []
            if len(only_letters) == 1:
                lettercode = [only_letters[0], "0"]
                letter_binary.append(letter_code*len(my_string))
            else:
                for letter in only_letters:
                    code =""
                    for node in checklist:
                        if len (node)>2 and letter in node[1]:           #genrating binary code
                            code = code + node[2]
                    lettercode =[letter,code]
                    letter_binary.append(lettercode)
            print(letter_binary)
            print("Binary code generated:")
            for letter in letter_binary:
                print(letter[0], letter[1])

            bitstring =""
            for character in my_string:
                for item in letter_binary:
                    if character in item:
                        bitstring = bitstring + item[1]
            global binary
            binary ="0b"+bitstring
            
            uncompressed_file_size = len(my_string)
            compressed_file_size = len(binary)

            print("Your original file size was", uncompressed_file_size,"bits. The compressed size is:",compressed_file_size)
            print("This is a saving of ",uncompressed_file_size-compressed_file_size,"bits")
            output = open("compressed.txt","w+")
            print("Compressed file generated as compressed.txt")
            output = open("compressed.txt","w+")
            output.write(bitstring)

            self.imagePicCompressed = Image. open(self.compressLocation)
            self.imagePicCompressed = self.imagePicCompressed.resize((150,150))
            self.imageCompressed2 =  ImageTk. PhotoImage(self.imagePicCompressed)
            self.image_label2 = ttk. Label(self , image = self.imageCompressed2)
            self.image_label2.place(x=400, y=50)

            self.imageSizeCompressed = convert_size(compressed_file_size)
            self.compressedLabelSize = Label(self, text = self.imageSizeCompressed)
            self.compressedLabelSize.config(font =("Courier", 14))
            self.compressedLabelSize.place(x=400, y=210)

        except:
            messagebox.showwarning("Error", "Something went wrong")

    # FUNCTION TO DECOMPRESS IMAGE FROM .TXT BINARY BACK TO IMAGE
    def DecompressImageHuffman(self):

        print("Decoding.......")

        bitstring = str(binary[2:])
        uncompressed_string =""
        code =""
        for digit in bitstring:
            code = code+digit
            pos=0                                        #iterating and decoding
            for letter in letter_binary:
                if code ==letter[1]:
                    uncompressed_string=uncompressed_string+letter_binary[pos] [0]
                    code=""
                pos+=1

        print("Your UNCOMPRESSED data is:")
        
        temp = re.findall(r'\d+', uncompressed_string)
        res = list(map(int, temp))
        res = numpy.array(res)
        res = res.astype(numpy.uint8)
        res = numpy.reshape(res, shape)
        print(res)
        print("Observe the shapes and inumpyut and output arrays are matching or not")
        print("Inumpyut image dimensions:",shape)
        print("Output image dimensions:",res.shape)
        data = Image.fromarray(res)
        data.save('decompressed.bmp')

        
        self.imagePicDecompressed = Image. open("decompressed.bmp")
        self.imagePicDecompressed = self.imagePicDecompressed.resize((150,150))
        self.imageDecompressed2 =  ImageTk. PhotoImage(self.imagePicDecompressed)
        self.imageDecom_label2 = ttk. Label(self , image = self.imageDecompressed2)
        self.imageDecom_label2.place(x=600, y=50)

        self.imageSizeDecompressed = (convert_size(get_size("decompressed.bmp")))
        self.decompressedLabelSize = Label(self, text = self.imageSizeDecompressed)
        self.decompressedLabelSize.config(font =("Courier", 14))
        self.decompressedLabelSize.place(x=600, y=210)
        
    
        if a.all() == res.all():
            print("Success")

        # FUNCTION DEFINTIONS:

    # OPEN IMAGE AND RETURN 3 MATRICES
    def openImage(self, imagePath):
        imOrig = Image.open(imagePath)
        im = numpy.array(imOrig)

        aRed = im[:, :, 0]
        aGreen = im[:, :, 1]
        aBlue = im[:, :, 2]

        return [aRed, aGreen, aBlue, imOrig]


    #  COMPRESS THE IMAGE TO A SINGLE CHANNEL
    def compressSingleChannel(self,channelDataMatrix, singularValuesLimit):
        uChannel, sChannel, vhChannel = numpy.linalg.svd(channelDataMatrix)
        aChannelCompressed = numpy.zeros((channelDataMatrix.shape[0], channelDataMatrix.shape[1]))
        k = singularValuesLimit

        leftSide = numpy.matmul(uChannel[:, 0:k], numpy.diag(sChannel)[0:k, 0:k])
        aChannelCompressedInner = numpy.matmul(leftSide, vhChannel[0:k, :])
        aChannelCompressed = aChannelCompressedInner.astype('uint8')
        return aChannelCompressed
    

    # FUNCTION TO COMPRESS IMAGE USING SVG COMPRESSION ALGO
    def SVDCompress(self):
        aRed, aGreen, aBlue, originalImage = self.openImage(self.compressLocation)
        im = cv2.imread(self.compressLocation)

        h, w, c = im.shape


        # image width and height:
        imageWidth = w
        imageHeight = h

        # number of singular values to use for reconstructing the compressed image
        singularValuesLimit = 160

        aRedCompressed = self.compressSingleChannel(aRed, singularValuesLimit)
        aGreenCompressed = self.compressSingleChannel(aGreen, singularValuesLimit)
        aBlueCompressed = self.compressSingleChannel(aBlue, singularValuesLimit)

        imr = Image.fromarray(aRedCompressed, mode=None)
        img = Image.fromarray(aGreenCompressed, mode=None)
        imb = Image.fromarray(aBlueCompressed, mode=None)

        newImage = Image.merge("RGB", (imr, img, imb))

        data = newImage
        data.save('SVDCompressed.bmp')
        newImage.show()

        # CALCULATE AND DISPLAY THE COMPRESSION RATIO
        mr = imageHeight
        mc = imageWidth

        originalSize = mr * mc * 3
        compressedSize = singularValuesLimit * (1 + mr + mc) * 3

        self.SVGCompressed = Image. open("SVDCompressed.bmp")
        self.SVGCompressed = self.SVGCompressed.resize((150,150))
        self.SVGCompressedAlt =  ImageTk. PhotoImage(self.SVGCompressed)
        self.SVGCompressedLabel = ttk. Label(self , image = self.SVGCompressedAlt)
        self.SVGCompressedLabel.place(x=400, y=50)

        self.compressedLabelSize = Label(self, text = convert_size(compressedSize))
        self.compressedLabelSize.config(font =("Courier", 14))
        self.compressedLabelSize.place(x=400, y=210)

        ratio = compressedSize * 1.0 / originalSize
        percentage = str(round(ratio * 100, 2))
        meanSquareError = self.mse(self.compressLocation, "SVDCompressed.bmp")
        ratioString = "Compression Ratio is 1 to " + str(ratio)
        percentageString = "Compressed image is " + percentage + "%" + " of original image"
        MSEString = "MSE (Mean Square Error) : " + str(meanSquareError)

        self.compressedLabelRatio = Label(self, text = ratioString)
        self.compressedLabelRatio.config(font =("Courier", 14))
        self.compressedLabelRatio.place(x=200, y=250)

        self.compressedLabelPercentage = Label(self, text = percentageString)
        self.compressedLabelPercentage.config(font =("Courier", 14))
        self.compressedLabelPercentage.place(x=200, y=270)

        self.compressedLabelMSE = Label(self, text = MSEString)
        self.compressedLabelMSE.config(font =("Courier", 14))
        self.compressedLabelMSE.place(x=200, y=290)



MyNewGUI = ImageCompressor("Image Compressor", 800, 350)




