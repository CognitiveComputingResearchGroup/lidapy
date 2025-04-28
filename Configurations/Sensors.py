import random

from source.Framework.Shared.LinkImpl import LinkImpl
from source.Framework.Shared.NodeImpl import NodeImpl
from source.Framework.Shared.NodeStructureImpl import NodeStructureImpl

"""def text_processing(text):
    link_buffer = NodeStructureImpl()
    for key, value in text.items():
        link = LinkImpl()
        link.setCategory(key, value)
        link_buffer.addDefaultLink__(link)
    return link_buffer"""

def text_processing(text):
    buffer = NodeStructureImpl()
    node = NodeImpl()
    node.setActivation(1.0)
    node.setId(text['id'])
    node.extended_id.setLinkCategory("link")
    node.extended_id.setSinkLinkCategory({"position": text['position']})
    node.setLabel(text['content'])
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