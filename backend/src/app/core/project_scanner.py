import os
from pathlib import Path


def check_permissions(folder: Path) -> tuple[bool, str]:
    # Basic OS-level permission check
    readable = os.access(folder, os.R_OK)
    writable = os.access(folder, os.W_OK)

    if not readable:
        return False, "Folder is not readable"

    if not writable:
        return False, "Folder is not writable"

    # Real write test (create + delete a dummy file)
    try:
        test_file = folder / ".testgen_permission_test"
        with Path.open(test_file, "w") as f:
            f.write("test")
        test_file.unlink()
    except PermissionError:
        return False, "Folder is readable but not writable"

    return True, "OK"
