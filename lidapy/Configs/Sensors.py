from Framework.Shared.LinkImpl import LinkImpl
from Framework.Shared.NodeStructureImpl import NodeStructureImpl


def text_processing(text):
    link_buffer = NodeStructureImpl()
    for key, value in text.items():
        link = LinkImpl()
        link.setCategory(key, value)
        link_buffer.addDefaultLink__(link)
    return link_buffer

def image_processing(image):
    pass

def audio_processing(audio):
    pass

def video_processing(video):
    pass

def internal_state_processing(internal_state):
    pass