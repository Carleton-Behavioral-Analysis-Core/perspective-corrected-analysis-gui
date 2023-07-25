
import yaml
class NoAliasDumper(yaml.SafeDumper):
    """Prevents yaml from using id to save space (would potentially mess up certain functions)"""
    def ignore_aliases(self, data):
        return True
# centroid = transformed_df.groupby(level="coords", axis=1).mean()
info = {
                "folderPath": "",
                "DLCfolderPath": "",
                "videoPaths": [],
                "DLCvideoPaths": [],
                "analysis_zones": {"center": []},
                "BoxHeight": 500,
                "BoxWidth": 500,
                "Name": "",
                "Path": "",
                "data": {" Videos": [], "Feature 1": [], "Feature 2": []},
                "dlc_pcutoff": 0.6,
                "treatment_groups": [],
                "threshold": 20
            }
with open('config.yaml', 'w') as file:
    yaml.dump(info,file,default_flow_style=False) 


helper = {
                "ValidationVideoSettings": {
                    "PlayBackSpeed": 1,
                    "Frame": 0,
                    "FPS": 30,
                    "TotalFrames": 1,
                },
                "PartsOfInterest": [],
                "registration_points": [],
                "Zones":{}
            }
with open('helper.yaml', 'w') as file:
    yaml.dump(helper,file,default_flow_style=False, Dumper=NoAliasDumper) 