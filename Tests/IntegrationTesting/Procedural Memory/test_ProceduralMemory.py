from source.Framework.Shared.NodeStructureImpl import NodeStructureImpl
from source.PAM.PAM_Impl import PAMImpl
from source.Framework.Shared.NodeImpl import NodeImpl
from source.Framework.Shared.LinkImpl import LinkImpl

"""IN WORKING PROCESSES & ADD NOTIFY WITH GW"""
def test_notify_with_PAM(procedural_memory):
    #Mocking the PAM
    module = PAMImpl()
    module.current_cell = NodeImpl()
    module.associations = NodeStructureImpl()
    assert isinstance(module.current_cell, NodeImpl) is True

    module.add_association(module.current_cell)
    default_link = LinkImpl()
    default_link.setSource(module.current_cell.getId())
    links = [default_link]
    module.associations.addLinks(links, "default")

    procedural_memory.scheme = ["avoid hole", "seek goal"]
    module.add_observer(procedural_memory)
    module.notify_observers()

    assert procedural_memory.get_state() == module.current_cell
    assert default_link in module.retrieve_association(module.current_cell)