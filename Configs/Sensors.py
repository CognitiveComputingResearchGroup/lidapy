from source.Framework.Shared.NodeImpl import NodeImpl
from source.ModuleInitialization.DefaultLogger import getLogger

logger = getLogger(__name__).logger

def _process_text(text):
    logger.debug(f"Processing text: {text}")
    pass

def _process_image(image):
    logger.debug(f"Processing image")
    return NodeImpl(label=image, activation=1)

def _process_audio(audio):
    logger.debug(f"Processing audio")
    pass

def _process_touch(touch):
    logger.debug(f"Processing touch")
    pass

def _process_internal_state(state):
    logger.debug(f"Processing internal state")
    pass