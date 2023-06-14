
import yaml


info= {"folderPath": "","DLCfolderPath": "","videoPaths":[],"DLCvideoPaths":[], "points":[],"BoxHeight":"","BoxWidth":"","Name":"","Path":"","numFeatures":"2",
                "data":
                {' Videos':[],
                    'Feature 1': [],
                    'Feature 2': []}}
with open('config.yaml', 'w') as file:
    yaml.dump(info,file,default_flow_style=False) 