# Python Interface for the 4Chan JSON API

## Usage

    import py4chan
    posts = py4chan.get_thread('b',9001)
    for p in posts:
        print p["filename"]
        print p.get_file_url()

