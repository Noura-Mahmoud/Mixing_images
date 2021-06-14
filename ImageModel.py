from PyQt5 import QtWidgets, QtCore, uic, QtGui, QtPrintSupport
from pyqtgraph import PlotWidget, plot
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import *   
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from os import path
import pyqtgraph as pg
import queue as Q
import pandas as pd
import numpy as np
import sys
import os
from PIL import Image
from PyQt5.QtGui import QPixmap
import cv2
import numpy as np
from matplotlib import pyplot as plt

class ImageModel():
    def __init__(self, imgPath: str,id):
        self.imgPath = imgPath
        self.img = cv2.imread(self.imgPath, flags=cv2.IMREAD_GRAYSCALE).T
        self.imgShape = self.img.shape
        self.fourier = np.fft.fft2(self.img)
        self.real = np.real(self.fourier)
        self.imaginary = np.imag(self.fourier)
        self.magnitude = np.abs(self.fourier)
        self.mag_spectrum = np.log10(self.magnitude)
        self.phase = np.angle(self.fourier)
        self.uniformMagnitude = np.ones(self.img.shape)
        self.uniformPhase = np.zeros(self.img.shape)
        self.component_list=[self.mag_spectrum,self.phase,self.real,self.imaginary]

    def mix(self, imageToBeMixed, magnitudeOrRealRatio, phaesOrImaginaryRatio , image1_component , image2_component):
        weight_img1 = magnitudeOrRealRatio
        weight_img2 = phaesOrImaginaryRatio
        mixInverse = None

        Magnitude1 = self.magnitude
        Magnitude2 = imageToBeMixed.magnitude

        Phase1 = self.phase
        Phase2 = imageToBeMixed.phase

        Real1 = self.real
        Real2 = imageToBeMixed.real

        Imaginary1 = self.imaginary
        Imaginary2 = imageToBeMixed.imaginary

        if image1_component == 'Real' or 'Imaginary' : 

            if image1_component == 'Real' : 
            
                realMix = weight_img1*Real1 + (1-weight_img1)*Real2
                imaginaryMix = (1-weight_img2)*Imaginary1 + weight_img2*Imaginary2
                    
            else :
                realMix = (1-weight_img2)*Real1 + weight_img2*Real2
                imaginaryMix = weight_img1*Imaginary1+(1-weight_img1)*Imaginary2

            combined = realMix + imaginaryMix * 1j

        else:
            if image1_component == 'Magnitude' : 
                magnitudeMix = weight_img1*Magnitude1 + (1-weight_img1)*Magnitude2

            elif image1_component == 'Phase' :
                phaseMix = weight_img1*Phase1  + (1-weight_img1)*Phase2

            elif image2_component == 'Phase' : 
                phaseMix = (1-weight_img2)*Phase1 + weight_img2*Phase2

            elif image2_component == 'Magnitude' :
                magnitudeMix= (1-weight_img2)*Magnitude1 + weight_img2*Magnitude2

            elif image1_component or image2_component == 'UniMagnitude' :
                Magnitude1 = self.uniformMagnitude
                magnitudeMix = Magnitude1

            elif image1_component or image2_component == 'UniPhase' :
                Phase1 = self.uniformPhase
                phaseMix = Phase1 

            combined = np.multiply(magnitudeMix, np.exp(1j * phaseMix))
            
        mixInverse = np.real(np.fft.ifft2(combined))

        return abs(mixInverse)