import ollama

def list_models():
    return list(ollama.list().models)


def get_model_names(models_list):
    return [x.model.split(':')[0] for x in models_list]
