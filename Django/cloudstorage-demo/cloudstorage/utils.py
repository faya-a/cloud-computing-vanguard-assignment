def get_filesize_string(size_in_bytes: int) -> str:
    """Get something like `343 MB` or `1.25 GB` depending on sizes."""
    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]

    for unit in units:
        # 1024 or 1000 ?
        if size_in_bytes >= 1000.0:
            size_in_bytes /= 1000.0
        else:
            break

    return f"{size_in_bytes:.2f} {unit}"
