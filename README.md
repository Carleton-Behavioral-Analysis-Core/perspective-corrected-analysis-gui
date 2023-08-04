# Perspective Corrected Analysis Gui

## Setup 

### Install Anaconda
https://www.anaconda.com

This allows us to install python and the main application

### Create a new Python environment
If the conda installation was successful, you should be able to open up a new terminal/command prompt (or Anaconda prompt if this fails) and create a new python environment
```
conda env create -n abizaidlab-analysis python=3.10 pytables
conda run -n abizaidlab-analysis pip install git+https://github.com/Carleton-Behavioral-Analysis-Core/perspective-corrected-analysis-gui/tree/main
```

## Running the Application
If the install was successful, from now on you just have to run 
```
conda run -n abizaidlab-analysis python -m behavior_analysis_tool
```
