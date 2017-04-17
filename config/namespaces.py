
namespaces = dict(
    textnet =dict(secrets=['local']),
    makiwara=dict(secrets=['local']),
)

def get(name):
    return namespaces[name]
