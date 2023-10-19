import markdown


def wiki_parse(wiki, text):
    # Chuyển đổi văn bản Creole sang HTML
    html_content = markdown.markdown(text)
    return html_content.emit()
