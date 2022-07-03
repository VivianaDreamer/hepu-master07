from django import template

register = template.Library()

@register.filter(name='custom_aprox')
def custom_aprox(value):
    """Corta un numero decimal en dos digitos"""
    return "{0:.2f}".format(value)

def _recursive_process(value:list)->str:
    if len(value)<1:
        return "No apply"
    elif len(value)==1:
        return str(value[0])
    else:
        if len(value) == 2:
            return "{} and {}".format(value[0],value[1])
        else:
            result = value[0]
            value.pop(0)
            return result + ', ' + _recursive_process(value)

@register.filter(name="list_formater")
def list_formater(value) -> str:
    """Retorna una frase ordenada dependiendo de la lista entregada"""
    value = eval(value)
    value = [str(x) for x in value]
    return _recursive_process(value)        

def _process(value:str) -> str:
    aux, count = [], 0
    value = list(value)
    while len(value) > 0:
        aux.insert(0,value[-1])
        count += 1
        if count == 3 and len(value)>1:
            aux.insert(0," ")
            count = 0
        value.pop()
    return "".join(aux)

@register.filter(name="number_format")
def number_format(value):
    value = str(value)
    if "." in value:
        parts = value.split(".")
        return _process(parts[0]) +"."+ parts[1][0:2]
    return _process(value)

@register.filter(name="lcoh_display")
def lcoh_display(value:str,key:str) -> str:
    data:dict = eval(value)
    if not key in data.keys():
        return "No apply"
    return number_format(data[key])