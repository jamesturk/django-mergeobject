from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class MergeException(Exception):
    pass


class OneToOneConflict(MergeException):
    pass


ERROR = 0
KEEP = 1
DELETE = 2


def merge(from_obj, to_obj, one_to_one_conflict=ERROR):
    if not isinstance(from_obj, type(to_obj)):
        raise ValueError("both objects must be of the same type")

    if from_obj.pk == to_obj.pk:
        raise ValueError("cannot merge object with itself")

    for related in from_obj._meta.get_all_related_objects():
        accessor_name = related.get_accessor_name()
        varname = related.field.name

        # in Django 1.8 can test for related.one_to_one
        if isinstance(related.field, models.OneToOneField):
            try:
                field = getattr(from_obj, accessor_name)
                try:
                    to_field = getattr(to_obj, accessor_name)
                    if one_to_one_conflict == KEEP:
                        pass    # do nothing
                    elif one_to_one_conflict == DELETE:
                        to_field.delete()
                        setattr(field, varname, to_obj)
                        field.save()
                    else:
                        raise OneToOneConflict(
                            "both fields have an attribute set for {}".format(accessor_name))
                except ObjectDoesNotExist:
                    # doesn't exist, safe to overwrite
                    setattr(field, varname, to_obj)
                    field.save()
            except ObjectDoesNotExist:
                # from_obj one to one isn't set, skip
                pass
        # in Django 1.8 can test for related.multiple
        elif isinstance(related.field, models.ForeignKey):
            field = getattr(from_obj, accessor_name)
            field.all().update(**{varname: to_obj})
        else:
            raise NotImplementedError('unexpected relation type, please file a bug')

    for related in from_obj._meta.get_all_related_many_to_many_objects():
        accessor_name = related.get_accessor_name()
        varname = related.field.name

        if not accessor_name:
            # not set in M2M to self, but varname will match
            accessor_name = varname

        field = getattr(from_obj, accessor_name)
        for f in field.all():
            getattr(f, varname).remove(from_obj)
            getattr(f, varname).add(to_obj)
