import random


from source.Framework.Shared.NodeImpl import NodeImpl
from source.Framework.Shared.NodeStructureImpl import NodeStructureImpl

def text_processing(text):
    buffer = NodeStructureImpl()
    node = NodeImpl()
    node.label = {"content" : text["content"],
                  "observation_space" : text["observation_space"],
                  "action_space" : text["action_space"],
                  "Reward" : text["Reward"],
                  "position": text["position"]}
    node.setActivation(1.0)
    node.id = text['id']
    buffer.addNode_(node)
    return buffer


def image_processing(image):
    pass

def audio_processing(audio):
    pass

def video_processing(video):
    pass

def internal_state_processing(internal_state):
    pass