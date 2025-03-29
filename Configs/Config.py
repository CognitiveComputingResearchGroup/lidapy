from yaml import load, dump

module_locations = {
    "godot_client" :
        r"C:\Users\brian\Documents\Fall 2024\SWENG 480\lidapy"
        r"\source\Godot_command_line\Godot_client.py",
    "godot_subscriber" :
        r"C:\Users\brian\Documents\Fall 2024\SWENG 480\lidapy"
        r"\source\Godot_command_line\Godot_subscriber.py",
    "Sensors" :
        r'C:\Users\brian\Documents\Fall 2024\SWENG 480\lidapy'
        r'\Configs\Sensors.py'
}
DEFAULT_PROCESSORS = {"text": "_process_text",
                    "image": "_process_image",
                    "audio": "_process_audio",
                    "touch": "_process_touch",
                    "internal_state": "_process_internal_state",
                    }

DEFAULT_SENSORS = [{"name": "text", "modality": "text", "processor":
                                                            "_process_text"},
                    {"name": "image", "modality": "image", "processor":
                                                            "_process_image"},
                    {"name": "audio", "modality": "audio", "processor":
                                                            "_process_audio"},
                    {"name": "touch", "modality": "touch", "processor":
                                                            "_process_touch"},
                    {"name": "visual2", "modality": "image", "processor":
                                                            "_process_image"},
                    {"name": "internal_state", "modality": "internal_state",
                                      "processor": "_process_internal_state"},
                   ]

with open("module_locations.yaml", "w", encoding="utf8") as yaml_file:
    dump(module_locations, yaml_file)

with open("DEFAULT_PROCESSORS.yaml", "w", encoding="utf8") as yaml_file:
    dump(DEFAULT_PROCESSORS, yaml_file)

with open("DEFAULT_SENSORS.yaml", "w", encoding="utf8") as yaml_file:
    dump(DEFAULT_SENSORS, yaml_file)