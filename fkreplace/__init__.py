from django.core.exceptions import ObjectDoesNotExist


class MergeException(Exception):
    pass


class OneToOneConflict(MergeException):
    pass


ERROR = 0
KEEP = 1
UPDATE = 2


def merge(from_obj, to_obj, one_to_one_conflict=ERROR):
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
                    to_obj_field = getattr(to_obj, accessor_name)
                    raise OneToOneConflict("both fields have an attribute set for {}".format(accessor_name))
                except ObjectDoesNotExist:
                    # doesn't exist, safe to overwrite
                    setattr(field, varname, to_obj)
                    field.save()
            except ObjectDoesNotExist:
                # from_obj one to one isn't set, skip
                pass
        else:
            raise NotImplementedError('unexpected relation type, please file a bug')

    for related in from_obj._meta.get_all_related_many_to_many_objects():
        accessor_name = related.get_accessor_name()
        varname = related.field.name

        if not accessor_name:
            # not set in M2M to self, but varname will match
            accessor_name = varname

        field = getattr(from_obj, accessor_name)
        if related.many_to_many:
            for f in field.all():
                getattr(f, varname).remove(from_obj)
                getattr(f, varname).add(to_obj)
