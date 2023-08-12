def get_data_instance(dataclass_type: object, instance: object) -> object:
    data = {}
    for field in dataclass_type.__dataclass_fields__.keys():
        data[field] = getattr(instance, field)
    return dataclass_type(**data)


def update_model_instance(mymodel: object, data: dict) -> None:
    for key, value in data.items():
        setattr(mymodel, key, value)
    mymodel.save()
