
import yaml
class NoAliasDumper(yaml.SafeDumper):
    """Prevents yaml from using id to save space (would potentially mess up certain functions)"""
    def ignore_aliases(self, data):
        return True

info= {"folderPath": "","DLCfolderPath": "","videoPaths":[],"DLCvideoPaths":[], "zone":[],"BoxHeight":"","BoxWidth":"","Name":"","Path":"","numFeatures":"2",
                "data":
                {' Videos':[],
                    'Feature 1': [],
                    'Feature 2': []},
                    "uncertainty":0.6}
with open('config.yaml', 'w') as file:
    yaml.dump(info,file,default_flow_style=False) 


helper= {"ValidationVideoSettings":{"PlayBackSpeed":1,"Frame":0,"FPS":30,"TotalFrames":1},"PartsOfInterest":[]}
print(len(helper))
with open('helper.yaml', 'w') as file:
    yaml.dump(helper,file,default_flow_style=False, Dumper=NoAliasDumper) 