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


def dict_query(query, with_entities=False):
    if with_entities:
        return [{k: ("" if v is None else v) for k, v in x._asdict().items()} for x in query]
    return [x.serialized(x.protected_fields) for x in query]
