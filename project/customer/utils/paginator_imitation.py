def paginator_imitation(collection, page, per_page):
    try:
        iter(collection)
        page = int(page)
        per_page = int(per_page)
    except TypeError or ValueError as err:
        print(err)
        return collection
    else:
        return collection[per_page * (page - 1):per_page * page]
