# facerec

##### Dependencies:
 - dlib `https://pypi.org/project/dlib/`
 - face_recognition `https://github.com/ageitgey/face_recognition`
 - flask `https://pypi.org/project/Flask/`
 - numpy `https://pypi.org/project/numpy/`
 - pytorch-DEX `https://github.com/siriusdemon/pytorch-DEX`
 
##### Install pytorch-DEX (Deep EXpectation):
 - install dependences using `pip`
```
pip3 install numpy opencv-python
pip3 install https://download.pytorch.org/whl/cpu/torch-1.0.1.post2-cp36-cp36m-linux_x86_64.whl
pip3 install torchvision (optional)
```
 - or install using `conda`
```
conda install opencv numpy
conda install pytorch-cpu torchvision-cpu -c pytorch
```

##### Rules:
 - `POST`: 0.0.0.0:5001/facerec => Recognize (name, gender, age) by image
    - body => `form-data:`
        - key: `file`
        - value: `[image].jpg/jpeg`
    - response:
        ```text
        {
          "predict": {
              "data": {
                  "age": "23", 
                  "gender": "Male", 
                  "name": "Purwo"
              }, 
              "status": {
                  "code": 200, 
                  "sucess": true, 
                  "timestamp": "2020-04-02T00:01:34Z"
              }
          }
        }
        ```
    
 - `GET`: 0.0.0.0:5001/crop => Crop image to create datasets / push to `facerec`
    - `required implementation!` => Check the code!
 
 - `POST`: 0.0.0.0:5001/facematch => Matching 2 image / picture (optional function)
 
##### Run App:
```
python3.6 app.py
```

##### Models: Gender & Age
 - Download files and place into a folder`modules/gender_age/dex/pth`
```
https://www.dropbox.com/s/y2d7o51dvzmn0rm/age_sd.pth?dl=0
https://www.dropbox.com/s/soahy3t3hm3n7mh/gender_sd.pth?dl=0
```
