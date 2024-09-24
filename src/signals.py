def simply_detect_keywords(text, keywords):
    """ Returns True if the text contains any of the keywords

    Args:
        text (str): The text to search in
        keywords (set): The keywords to search for
    """
    if len(keywords) == 0:
        return False

    words = {word for word in text.split()}
    if keywords & words:
        return True
    return False
