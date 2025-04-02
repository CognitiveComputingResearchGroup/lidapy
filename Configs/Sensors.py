from source.Framework.Shared.LinkImpl import LinkImpl
from source.Framework.Shared.NodeStructureImpl import NodeStructureImpl


def text_processing(text):
    data = ""
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