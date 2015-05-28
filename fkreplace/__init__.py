# thanks to https://djangosnippets.org/snippets/2283/ for inspiration on m2m

def migrate(from_obj, to_obj):
    for related in from_obj._meta.get_all_related_objects():
        accessor_name = related.get_accessor_name()
        varname = related.field.name
        getattr(from_obj, accessor_name).all().update(**{varname: to_obj})

    for related_m2m in from_obj._meta.get_all_related_many_to_many_objects():
        accessor_name = related.get_accessor_name()
        varname = related.field.name

        #for obj in getattr(from_obj, varname)

