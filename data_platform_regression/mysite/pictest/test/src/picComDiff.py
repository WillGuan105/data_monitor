#!/usr/bin/python

import Image 
from difflib import *
from PIL.ImageChops import *

def make_regalur_image(img, size = (256, 256)): 
    return img.resize(size).convert('RGB') 

def hist_similar(lh, rh): 
    assert len(lh) == len(rh) 
    return sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zip(lh, rh))/len(lh) 

def findDiff(img1, img2):
    point_table = ([0] + ([255] * 255))
    diff = difference(img1, img2)
    diff = diff.convert('L')
    diff = diff.point(point_table)
    new = diff.convert('RGB')
    new.paste(img2, mask=diff)
    return new

# same return 1, diff return 0
def comPic(img1,img2,saveimg):
	img1=Image.open(img1)
 	img2=Image.open(img2)
	img1=make_regalur_image(img1)
	img2=make_regalur_image(img2)

	sim=hist_similar(img1.histogram(), img2.histogram())
	if(sim == 1):
		return 1
	else:
		diffimg = findDiff(img1, img2)
		diffimg.save(saveimg)
		return 0

'''
image1='/home/data/xiaoyao/testPNG/test/standPNG/test_761_2015-07-20_2015-07-20.png'
image2='/home/data/xiaoyao/testPNG/test/savePNG/test_499_2015-07-20_2015-07-20.png'
saveimg='/home/data/xiaoyao/testPNG/test/diffPNG/test_761_2015-07-20_2015-07-20.png'
comPic(image1,image2,saveimg)
'''
