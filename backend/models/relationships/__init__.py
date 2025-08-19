# models/relationships/__init__.py

def attach_relationships() -> None:
    """
    Import relationship modules so their side-effects attach
    relationship() attributes onto mapped classes.
    """
    from . import item_relationship          
    from . import bom_relationship           
    from . import inventory_txn_relationship
