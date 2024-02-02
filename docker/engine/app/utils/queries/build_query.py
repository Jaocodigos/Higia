from engine.app.config.logs import prepare_logs

log = prepare_logs(__name__)


def build_query(model, **kwargs):
    log.debug(f"Query parameters: {kwargs}")
    query = model.query
    if kwargs.get('filters'):
        filters = kwargs.get('filters')
        if isinstance(filters, list):
            for f in filters:
                query = query.filter(f)
        else:
            query = query.filter(filters)
    if kwargs.get('with_entities'):
        fields = model().safe_fields
        query = query.with_entities(*[getattr(model, f) for f in fields])
    if kwargs.get('limit') or kwargs.get('offset'):
        query = query.offset(kwargs.get('offset')).limit(kwargs.get('limit'))
    return query


def dict_query(query):
    return [x._asdict() for x in query]
