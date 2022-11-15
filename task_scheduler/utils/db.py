def update_instance(instance, validated_data):
    for data in validated_data:
        setattr(instance, data, validated_data[data])
    instance.save()
    instance.refresh_from_db()
    return instance
