# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 23:17:13 2020

@author: anmol
"""

import glob
import cv2
import pydicom as dicom
import numpy as np
import csv
import os
from shutil import copy

base_folder = "TrainingSet"
out_folder = "ProcessedData"
os.makedirs(out_folder + "\\input")
os.makedirs(out_folder + "\\gt_icontour")
os.makedirs(out_folder + "\\gt_ocontour")
os.makedirs(out_folder + "\\no_gt_input")

patient_folders = sorted(glob.glob(base_folder+"/*"))

for patient_folder in patient_folders:
    patient_num = str(patient_folder).split('\\')[-1][7:]
    print(patient_num)
    list_contours = sorted(glob.glob(str(patient_folder) + "\\P" + patient_num + "contours-manual\\*.txt"))
    for contour in list_contours:
        idx = str(contour).split('\\')[-1].split('contour')[0][:-2]
        contour_type = str(contour).split('\\')[-1].split('-')[2]
        dcm_file = str(patient_folder) + "\\P" + patient_num + "dicom\\" + idx + ".dcm"
        reader = csv.reader(open(contour, "r"), delimiter=" ")
        points = []
        for row in reader:
            #points.append([float(row[0])/ds.PixelSpacing[0], float(row[1])/ds.PixelSpacing[1]])
            points.append([float(row[0]), float(row[1])])
        points = np.array(points, dtype=np.int32)
        ds = dicom.dcmread(dcm_file)
        pixel_array = ds.pixel_array
        scaled_array = np.array(pixel_array/np.max(pixel_array))
        blank_im = np.zeros(scaled_array.shape, np.uint8)
        contour_filled = cv2.fillPoly(blank_im, pts=[points], color=(255, 255, 255))
        contour_filename = out_folder + "\\gt_" + contour_type + "\\" + idx + ".png"
        out_dcm_filename = out_folder + "\\input\\" + idx + ".dcm"
        cv2.imwrite(contour_filename, contour_filled)
        copy(dcm_file, out_dcm_filename)

#for patient_folder in patient_folders:
#    patient_num = str(patient_folder).split('\\')[-1][7:]
#    print(patient_num)
#    list_dcms = sorted(glob.glob(str(patient_folder) + "\\P" + patient_num + "dicom\\*.dcm"))
#    for dcm_file in list_dcms:
#        toss = np.random.uniform()
#        if toss > 0.5:
#            out_dcm_filename = out_folder + "\\no_gt_input\\" + dcm_file.split("\\")[-1]
#            copy(dcm_file, out_dcm_filename)
        