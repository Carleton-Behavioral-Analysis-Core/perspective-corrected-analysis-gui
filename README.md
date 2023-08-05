# Perspective Corrected Analysis Gui

## Setup 

![](https://youtu.be/_wLCJuvpfKM)

![](https://youtu.be/ucw7jR_qfww)

### Install Anaconda
https://www.anaconda.com

This allows us to install python and the main application

### Create a new Python environment
If the conda installation was successful, you should be able to open up a new terminal/command prompt (or Anaconda prompt if this fails) and create a new python environment
```
conda create -n abizaidlab-analysis python=3.10
conda install -n abizaidlab-analysis pytables
conda run -n abizaidlab-analysis pip install git+https://github.com/Carleton-Behavioral-Analysis-Core/perspective-corrected-analysis-gui
```

## Running the Application
If the install was successful, to run the application you can open terminal/command prompt and paste the following 
```
conda run -n abizaidlab-analysis python -m behavior_analysis_tool
```
