
def merge(from_obj, to_obj):
    if not isinstance(from_obj, type(to_obj)):
        raise ValueError("both objects must be of the same type")

    if from_obj.pk == to_obj.pk:
        raise ValueError("cannot merge object with itself")

    for related in from_obj._meta.get_all_related_objects():
        accessor_name = related.get_accessor_name()
        varname = related.field.name

        if related.multiple:
            field = getattr(from_obj, accessor_name)
            field.all().update(**{varname: to_obj})
        elif related.one_to_one:
            try:
                field = getattr(from_obj, accessor_name)
                try:
                    getattr(to_obj, accessor_name)
                except Exception as e:
                    # doesn't exist, safe to overwrite
                    setattr(field, varname, to_obj)
                    field.save()
            except Exception as e:
                # from_obj one to one isn't set, skip
                pass
        else:
            import pdb; pdb.set_trace()
            raise Exception('unknown code path')

    for related in from_obj._meta.get_all_related_many_to_many_objects():
        accessor_name = related.get_accessor_name()
        if accessor_name:
            varname = related.field.name
            field = getattr(from_obj, accessor_name)
            if related.many_to_many:
                for f in field.all():
                    getattr(f, varname).remove(from_obj)
                    getattr(f, varname).add(to_obj)
