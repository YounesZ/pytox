from typing import Iterable


# ==========================================
# ============= DATA FORMATS ===============
# ==========================================
def get_host_type() -> Iterable['local', 'cloud']:

    # ----------------
    # Specific imports
    from platform import node
    # ----------------

    node_name = node()
    node_type = node_name[-6:]
    if node_type == '.local':
        return 'local'
    else:
        return 'cloud'
