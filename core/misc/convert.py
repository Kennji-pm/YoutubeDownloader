def convert_seconds(seconds: int):
    t_sec = seconds
    hour = int(t_sec / 3600)
    min = int((t_sec % 3600) / 60)
    sec = int((t_sec % 3600) % 60)
    length = f"{hour}hr {min}min {sec}sec" if not hour == 0 else f"{min}min {sec}sec"
    return length

def convert_filesize(size: int):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0
    return size