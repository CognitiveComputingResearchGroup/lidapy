import random


from Framework.Shared.NodeImpl import NodeImpl
from Framework.Shared.NodeStructureImpl import NodeStructureImpl

def text_processing(text):
    buffer = NodeStructureImpl()
    node = NodeImpl()
    node.label = text["content"]
    node.setActivation(1.0)
    node.id = text['id']
    node.extended_id.setLinkCategory("link")
    node.extended_id.setSinkLinkCategory({"position": text['position']})
    node.extended_id.setSinkNode1Id(random.randint(1, 101))
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