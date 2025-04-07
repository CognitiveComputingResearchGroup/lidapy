from yaml import load, dump

module_locations = {
    "GodotEnvironment" :
        r"C:\Users\brian\Documents\Fall 2024\SWENG 480\lidapy"
        r"\source\Environment\GodotEnvironment.py",
    "FrozenLakeEnvironment" :
        r"C:\Users\brian\Documents\Fall 2024\SWENG 480\lidapy"
        r"\source\Environment\FrozenLakeEnvironment.py",
    "Sensors" :
        r'C:\Users\brian\Documents\Fall 2024\SWENG 480\lidapy'
        r'\Configs\Sensors.py'
}
DEFAULT_PROCESSORS = {"text": "text_processing",
                    "image": "image_processing",
                    "audio": "audio_processing",
                    "video": "video_processing",
                    "internal_state": "internal_state_processing",
                    }

DEFAULT_SENSORS = [{"name": "text", "modality": "text", "processor":
                                                            "text_processing"},
                    {"name": "image", "modality": "image", "processor":
                                                            "image_processing"},
                    {"name": "audio", "modality": "audio", "processor":
                                                            "audio_processing"},
                    {"name": "video", "modality": "video", "processor":
                                                            "video_processing"},
                    {"name": "internal_state", "modality": "internal_state",
                                      "processor": "internal_state_processing"},
                   ]

with open("module_locations.yaml", "w", encoding="utf8") as yaml_file:
    dump(module_locations, yaml_file)

with open("DEFAULT_PROCESSORS.yaml", "w", encoding="utf8") as yaml_file:
    dump(DEFAULT_PROCESSORS, yaml_file)

with open("DEFAULT_SENSORS.yaml", "w", encoding="utf8") as yaml_file:
    dump(DEFAULT_SENSORS, yaml_file)