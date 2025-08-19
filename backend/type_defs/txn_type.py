import enum

class TxnType(str, enum.Enum):
    po_created      = "po_created"       # incoming +q
    po_canceled     = "po_canceled"      # incoming -q
    po_received     = "po_received"      # incoming -q, on_hand +q

    so_allocated    = "so_allocated"     # allocated +q
    so_unallocated  = "so_unallocated"   # allocated -q
    pick_ship       = "pick_ship"        # allocated -q, on_hand -q

    adjustment_in   = "adjustment_in"    # on_hand +q
    adjustment_out  = "adjustment_out"   # on_hand -q

    return_customer = "return_customer"  # on_hand +q
    return_supplier = "return_supplier"  # on_hand -q

    transfer_in     = "transfer_in"      # on_hand +q
    transfer_out    = "transfer_out"     # on_hand -q