from hurry.filesize import size


def humanize_size(bytes_count):
    """Convert bytes to human-readable format."""
    return size(bytes_count)
