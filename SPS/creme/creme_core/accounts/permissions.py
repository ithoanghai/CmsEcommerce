# permissions.py

def is_staff_or_self(request, view):
    """
    Fail if non-staff user specifies object by any PK except "self".

    Requires view to provide a `pk` attribute.
    """
    if request.user.is_staff:
        return (True, 200, "")

    if view.pk != request.user.pk:
        return (False, 403, "ID must be \"{}\"".format(request.user.pk))