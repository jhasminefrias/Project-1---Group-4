def paginate(items, page_size):
    index = 0
    while index < len(items):
        yield items[index:index + page_size]
        index += page_size