from yaml import load, dump

module_locations = {
    "GodotEnvironment" : r"\Source\Environment\GodotEnvironment.py",
    "FrozenLakeEnvironment" : r"\Source\Environment\FrozenLakeEnvironment.py",
    "AtariEnvironment" : r"\Source\Environment\AtariEnvironment.py",
    "Sensors" : r"\Source\SensoryMemory\Sensors.py"
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