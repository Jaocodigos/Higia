from engine.app.resources.frontend import view


@view.context_processor()
def list_processor():
    def length(items: list) -> int:
        return len(items)
    return dict(length=length)
