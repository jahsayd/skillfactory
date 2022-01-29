from django import template

register = template.Library()

@register.filter(name='Censor')

def Censor(value: str):
    variants = []  # непристойные выражения
    with open('censor_list.txt') as f:
        variants = f.read().split(", ")
    ln = len(variants)
    filtred_value = ''
    string = ''
    pattern = '*'  # чем заменять непристойные выражения
    for i in value:
        string += i
        string2 = string.lower()

        flag = 0
        for j in variants:
            if not string2 in j:
                flag += 1
            if string2 == j:
                filtred_value += pattern * len(string)
                flag -= 1
                string = ''

        if flag == ln:
            filtred_value += string
            string = ''

    if string2 != '' and string2 not in variants:
        filtred_value += string
    elif string2 != '':
        filtred_value += pattern * len(string)

    return filtred_value