from django import template
register = template.Library()

@register.filter(name = 'pathcheck')
def path(value,args):
    return value.find(args) > -1

@register.filter(name = 'get')
def get(value,args):
    if hasattr(value,args):
        return getattr(value,args,None)
    return None
@register.filter(name = 'dictget')
def get(value,args):
    return value.__dict__.get(args)