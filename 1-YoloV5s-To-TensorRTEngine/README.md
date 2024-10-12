# YOLOv5 Object Detection on Jetson Nano with TensorRT

This guide provides step-by-step instructions on how to set up and run YOLOv5 object detection on a Jetson Nano using TensorRT for optimized performance.

## Table of Contents
* [Prerequisites](#prerequisites)
* [Installation](#installation)
   * [Update and Install Libraries](#update-and-install-libraries)
   * [Upgrade Pip](#upgrade-pip)
   * [Install Necessary Python Packages](#install-necessary-python-packages)
   * [Install PyCUDA](#install-pycuda)
   * [Install Seaborn](#install-seaborn)
   * [Install PyTorch and Torchvision](#install-pytorch-and-torchvision)
   * [Optional: Install jetson-stats](#optional-install-jetson-stats)
* [Generate WTS File](#generate-wts-file)
* [Build the Project](#build-the-project)
   * [CMake and Make](#cmake-and-make)
   * [Build the TensorRT Engine](#build-the-tensorrt-engine)



## Installation

### Update and Install Libraries
First, update the package lists and install the necessary system libraries:

```bash
sudo apt-get update
sudo apt-get install -y liblapack-dev libblas-dev gfortran libfreetype6-dev libopenblas-base libopenmpi-dev libjpeg-dev zlib1g-dev
sudo apt-get install -y python3-pip
```

### Upgrade Pip
Upgrade `pip` to the latest version:

```bash
python3 -m pip install --upgrade pip
```

### Install Necessary Python Packages
Uninstall the existing version of `numpy` and install the required versions of the necessary Python packages:

```bash
python3 -m pip uninstall -y numpy
python3 -m pip install numpy==1.19.0 pandas==0.22.0 Pillow==8.4.0 PyYAML==3.12 scipy==1.5.4 psutil tqdm==4.64.1 imutils
```

### Install PyCUDA
Set the CUDA paths and install `pycuda`:

```bash
export PATH=/usr/local/cuda-10.2/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda-10.2/lib64:$LD_LIBRARY_PATH
python3 -m pip install pycuda --user
```

### Install Seaborn
Install `seaborn` for data visualization:

```bash
sudo apt-get install -y python3-seaborn
```

### Install PyTorch and Torchvision
Download and install the PyTorch wheel compatible with Jetson Nano:

```bash
wget https://nvidia.box.com/shared/static/fjtbno0vpo676a25cgvuqc1wty0fkkg6.whl -O torch-1.10.0-cp36-cp36m-linux_aarch64.whl
python3 -m pip install torch-1.10.0-cp36-cp36m-linux_aarch64.whl
```

Clone the `torchvision` repository and install it:

```bash
git clone --branch v0.11.1 https://github.com/pytorch/vision torchvision
cd torchvision
sudo python3 setup.py install
cd ..
```

### Optional: Install jetson-stats
Install `jetson-stats` for monitoring system resources (optional but recommended):

```bash
sudo python3 -m pip install jetson-stats==3.1.4
```

## Generate WTS File
Generate the `.wts` file from your YOLOv5 model:

```bash
python3 gen_wts.py -w yolov5s.pt -o yolov5s.wts
```

* `-w`: Path to your YOLOv5 PyTorch model (`.pt` file)
* `-o`: Output path for the generated `.wts` file

## Build the Project

### CMake and Make
If you're using a custom model, make sure to update `kNumClass` in `yolov5/src/config.h` to match the number of classes in your dataset.

Build the project using CMake and Make:

```bash
cd yolov5/
mkdir build
cd build
cp ../../yolov5s.wts .
cmake ..
make
```

### Build the TensorRT Engine
Generate the TensorRT engine from the `.wts` file:

```bash
./yolov5_det -s yolov5s.wts yolov5s.engine s
```

* `-s`: Indicates that you want to serialize the model and build the engine
* `yolov5s.wts`: Input `.wts` file
* `yolov5s.engine`: Output TensorRT engine file
* `s`: Model size (s, m, l, x)

## Testing
Run the object detection on sample images:

```bash
./yolov5_det -d yolov5s.engine ../images
```

* `-d`: Indicates that you want to run the detection
* `yolov5s.engine`: Path to the TensorRT engine file


## Notes
* Ensure that all environment variables are correctly set, especially the CUDA paths.
* If you encounter issues with package versions, double-check the compatibility with your JetPack SDK version.
* For custom models, adjust the configuration files accordingly.


