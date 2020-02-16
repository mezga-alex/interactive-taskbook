# Skyeng Grammar Filter
The project allows you to form tasks in English grammar.

## Table of Contents

- ### [Application in action](#intro)
- ### [Installation](#env)
- ### [Usage](#usage)
  * [Run the server](#server)
  * [Load the extension](#extension_load)
- ### [Documentation](#doc)
 
## Application in action <a name="intro"></a>
![](images/skyeng_gf.gif)

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
### Run the server <a name="server"><a>
To run the server:
```
bash utils/run_server.sh
```

### Load the extension  <a name="extension_load"><a>
To load up the Chrome extension follow this rules:
1. Open the Extension Management page by navigating to chrome://extensions

   * The Extension Management page can also be opened by clicking on the Chrome menu, hovering over More Tools then selecting Extensions.

2. Enable Developer Mode by clicking the toggle switch next to Developer mode.
3. Click the LOAD UNPACKED button and select the extension directory named 'Web'.

## Documentation <a name="doc"></a>
The documentation can be [found here](docs/build/html/index.html).
https://htmlpreview.github.io/?https://github.com/mezga-alex/skyeng-grammar-filter/docs/build/html/index.html"
