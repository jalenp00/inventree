from sqlalchemy import text

class InventoryQ:
    get_available_to_build = text("""
    WITH RECURSIVE bom_expanded AS (
            SELECT b.parent_id, b.child_id, b.qty::NUMERIC AS effective_qty
            FROM bom b
            WHERE b.parent_id = :item_id
            UNION ALL
            SELECT be.parent_id, b.child_id, be.effective_qty * b.qty
            FROM bom_expanded be
            JOIN bom b ON be.child_id = b.parent_id
        )
        SELECT MIN(i.on_hand / be.effective_qty) AS available
        FROM bom_expanded be
        LEFT JOIN bom b2 ON be.child_id = b2.parent_id
        JOIN inventory i ON be.child_id = i.item_id
        WHERE b2.parent_id IS NULL;
    """)