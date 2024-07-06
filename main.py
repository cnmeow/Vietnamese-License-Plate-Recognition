from flask import Flask, render_template, request, redirect
import os
from PIL import Image
import pillow_heif
import cv2
import torch
import math 
import function.utils_rotate as utils_rotate
from IPython.display import display
import os
import time
import argparse
import function.helper as helper

# Constraints
type_file = ['jpg', 'jpeg', 'png', 'heic'] # Supported file types
min_lp_acreage = 0.02 # Minimum license plate acreage as a fraction of the image acreage
max_in_plane_rotation = 25 # Maximum in-plane rotation in degrees along the x-axis

app = Flask(__name__)
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

pillow_heif.register_heif_opener()

yolo_LP_detect = torch.hub.load('yolov5', 'custom', path='model/LP_detector.pt', force_reload=True, source='local')
yolo_license_plate = torch.hub.load('yolov5', 'custom', path='model/LP_ocr.pt', force_reload=True, source='local')
yolo_license_plate.conf = 0.60

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def predict():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']

    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file:
        filename = file.filename

        # Check type file
        type = filename.split(".")[-1].lower()
        if type not in type_file:
            return render_template('index.html', error=str(type) + " file type is not supported. Supported file types are: " + ', '.join(type_file))
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'upload.jpg')

        if type in ['jpg', 'jpeg', 'png']:
            file.save(file_path)
        else: # convert to jpg
            image = Image.open(file)
            image.save(file_path, format='JPEG')

        img = cv2.imread(file_path)
        
        start_time = time.time()
        plates = yolo_LP_detect(img, size=640)
        list_plates = plates.pandas().xyxy[0].values.tolist()
        list_read_plates = set()
        if len(list_plates) == 0:
            lp = helper.read_plate(yolo_license_plate,img)
            if lp != "unknown":
                cv2.putText(img, lp, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
                list_read_plates.add(lp)
        else:
            for plate in list_plates:
                flag = 0
                x = int(plate[0]) # xmin
                y = int(plate[1]) # ymin
                w = int(plate[2] - plate[0]) # xmax - xmin
                h = int(plate[3] - plate[1]) # ymax - ymin  
                crop_img = img[y:y+h, x:x+w]                   
                cv2.rectangle(img, (int(plate[0]),int(plate[1])), (int(plate[2]),int(plate[3])), color = (0,0,225), thickness = 2)
                cv2.imwrite("crop.jpg", crop_img)
                lp = ""
                for cc in range(0,2):
                    for ct in range(0,2):
                        lp = helper.read_plate(yolo_license_plate, utils_rotate.deskew(crop_img, cc, ct))
                        if lp != "unknown":
                            list_read_plates.add(lp)
                            cv2.putText(img, lp, (int(plate[0]), int(plate[1]-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
                            flag = 1
                            break
                    if flag == 1:
                        break
        end_time = time.time()
        run_time = str(round(end_time - start_time, 2))

        cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], 'result.jpg'), img)
        return render_template('index.html', filename=filename, runtime=run_time, lp=lp, error=None)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
