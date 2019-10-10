class AP:
    def __init__(self, name, label_func):
        self.name = name
        self.label_func = label_func

    def __call__(self, graph, st, *args, **kwargs):
        return self.label_func(graph, st, args, kwargs)