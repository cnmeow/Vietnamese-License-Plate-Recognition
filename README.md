# 🇻🇳 Vietnamese License Plate Recognition

## Introduction

This project aims to build a web application for recognizing Vietnamese license plates, using efficient deep-learning algorithms for accurate and rapid recognition. This system can work on 2 types of license plate in Vietnam, 1 line plates and 2 lines plates.

<img width="700" alt="shortlp" src="https://github.com/cnmeow/Vietnamese-License-Plate-Recognition/assets/73975520/ced357e1-e967-4982-ab53-ad70929729f6">

## Features

- Detect license plates in images
- Recognize characters on Vietnamese license plates
- User-friendly web interface
- High accuracy and performance

## Algorithm
<img width="685" alt="image" src="https://github.com/cnmeow/Vietnamese-License-Plate-Recognition/assets/73975520/6fd72e6c-8650-4c78-8ec0-c0f96046954d">

## Installation

- Clone the repository:

    ```bash
    git clone https://github.com/cnmeow/Vietnamese-License-Plate-Recognition.git
    cd Vietnamese-License-Plate-Recognition
    ```
    
- Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```
- Pretrained model provided in `model` folder
- Download yolov5 from this link:** [yolov5 - Google Drive](https://drive.google.com/file/d/1g1u7M4NmWDsMGOppHocgBKjbwtDA-uIu/view?usp=sharing)
- Copy `yolov5` folder to `project` folder

## Inference

### Web application
- Run the web server:
```bash
python main.py
```
- Open your web browser and go to `localhost:4000`.
  
  <img width="700" alt="index" src="https://github.com/cnmeow/Vietnamese-License-Plate-Recognition/assets/73975520/85e28ce8-180e-4211-a362-9058aa9d0f31">

- Click `Choose File` button, select the image of the license plate you want to recognize
- Click the `Upload and Recognize` button to process the recognition.

### On image
```bash
python lp_image.py -i test_image/3.jpg
```

### On webcam
```bash
python webcam.py
```

## Training

**Training code for Yolov5:**

Use code in `training folder`
```bash
  training/Plate_detection.ipynb     #for LP_Detection
  training/Letter_detection.ipynb    #for Letter_detection
```
## References
- [trungdinh22](https://github.com/trungdinh22/License-Plate-Recognition)
- [License Plate Detection Dataset](https://drive.google.com/file/d/1xchPXf7a1r466ngow_W_9bittRqQEf_T/view?usp=sharing)
- [Character Detection Dataset](https://drive.google.com/file/d/1bPux9J0e1mz-_Jssx4XX1-wPGamaS8mI/view?usp=sharing)
- [Mì Ai](https://www.miai.vn/thu-vien-mi-ai/)
- [winter2897](https://github.com/winter2897/Real-time-Auto-License-Plate-Recognition-with-Jetson-Nano/blob/main/doc/dataset.md)
