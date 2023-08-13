from django.db import models


def get_data_instance(dataclass_type: object, instance: models.Model) -> object:
    data = {}
    for field in dataclass_type.__dataclass_fields__.keys():
        if hasattr(instance, field):
            field_value = getattr(instance, field)
            if isinstance(field_value, models.Model):  # For foreign keys
                _dataclass_type = dataclass_type.__annotations__[field]

                field_value = get_data_instance(_dataclass_type, field_value)
            data[field] = field_value
    return dataclass_type(**data)


def update_model_instance(mymodel: models.Model, data: dict) -> None:
    for key, value in data.items():
        setattr(mymodel, key, value)
    mymodel.save()
