
def merge(from_obj, to_obj):
    for related in from_obj._meta.get_all_related_objects():
        accessor_name = related.get_accessor_name()
        varname = related.field.name
        field = getattr(from_obj, accessor_name)
        if related.multiple:
            field.all().update(**{varname: to_obj})
        elif related.one_to_one:
            try:
                getattr(to_obj, accessor_name)
            except Exception as e:
                # doesn't exist, safe to overwrite
                setattr(field, varname, to_obj)
                field.save()
        else:
            import pdb; pdb.set_trace()
            raise Exception('unknown code path')

    for related_m2m in from_obj._meta.get_all_related_many_to_many_objects():
        accessor_name = related.get_accessor_name()
        varname = related.field.name

        #for obj in getattr(from_obj, varname)

