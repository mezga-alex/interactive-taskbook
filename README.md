# Skyeng Grammar Filter
The project allows you to form tasks in English grammar.

## Application in action <a name="intro"></a>
![](images/skyeng_gf.gif)


## Table of Contents

- ### [Application in action](#intro)
  * [Installation](#env)
  * [Usage](#usage)
- ### [skyeng Grammar Filter](#fedlearn)
  * [Documentation](#exp)
  * [Usage](#results)
   


## Installation <a name="env"></a>
To create virtual environment and download dependencies of project run from terminal:
```
bash utils/install.sh
```

For running model with GPU you will required to have: 
* CUDA >= 10.0
* nvidia-drivers >= 418

To update your drivers, follow this user-friendly [medium article](https://medium.com/@aspiring1/installing-cuda-toolkit-10-0-and-cudnn-for-deep-learning-with-tensorflow-gpu-on-ubuntu-18-04-lts-f7e968b24c98) with instructions

To install spacy GPU version and check the capability to use it run:
```
bash utils/install_GPU.sh
```

Dependencies of project can be also installed with requirements.txt:
```
pip install -r utils/requirements.txt
```

## Usage <a name="usage"><a>
To run the server:
```
bash utils/run_server.sh
```

To install chrome-extension follow this rules:
