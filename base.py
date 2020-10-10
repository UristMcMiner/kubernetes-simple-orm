class ORMBase:

    mapped_attributes = {}
    api_group = ""
    kind = ""
    version = ""
    plural = ""

    @staticmethod
    def deserialize(class_obj, name, client):
        version = class_obj.version
        namespace = client.namespace
        group = class_obj.api_group
        plural = class_obj.plural
        try:
            raw_data = client.get_live_object(group, version, namespace, plural, name)
        except Exception as ex:
            raise Exception(str(ex))
        class_to_create = class_obj
        attributes_to_map = class_to_create.mapped_attributes
        parameter_list = [raw_data['metadata']['name']]
        for attribute in attributes_to_map:
            attribute_name = attribute['name']
            if attribute['type'] == "list":
                if attribute['mapped_field_name'] in raw_data['spec']:
                    mapped_class = attribute['mapped_type']
                    mapped_list = list()
                    for item in raw_data['spec'][attribute_name]:
                        mapped_list.append(mapped_class.deserialize(mapped_class, item, client))
                    parameter_list.append(mapped_list)
                else:
                    parameter_list.append(list())

            elif attribute['type'] == "str":
                if attribute_name in raw_data['spec']:
                    parameter_list.append(raw_data['spec'][attribute_name])
                else:
                    parameter_list.append(None)
            elif attribute['type'] == "array":
                if attribute_name in raw_data['spec']:
                    append_list = list()
                    for item in raw_data['spec'][attribute_name]:
                        append_list.append(item)
                    parameter_list.append(append_list)
                else:
                    parameter_list.append(list())
        return class_to_create(*parameter_list)


    def serialize(self, client, create=False, patch=False):
        class_to_create = self.__class__
        attributes_to_map = class_to_create.mapped_attributes
        attributes_map = dict()
        attributes_map['body'] = dict()
        attributes_map['api_group'] = class_to_create.api_group
        attributes_map['version'] = class_to_create.version
        attributes_map['kind'] = class_to_create.kind
        attributes_map['plural'] = class_to_create.plural
        for at in attributes_to_map:
            name = at['name']
            type = at['type']
            if type == "str":
                value = getattr(self, name)
                attributes_map['body'][name] = value
            elif type == "list":
                items = getattr(self, name)
                mapped_field_name = at['mapped_field_name']
                mapped_class = at['mapped_type']
                mapped_api_group = mapped_class.api_group
                mapped_version = mapped_class.version
                mapped_kind = mapped_class.kind
                mapped_plural = mapped_class.plural
                if items.__len__() > 0:
                    attributes_map['body'][mapped_field_name] = list()
                    for i in items:
                        try:
                            client.get_live_object(mapped_api_group, mapped_version, client.namespace, mapped_plural, i.name)
                            if patch:
                                print("Referenced object exists, patching %s/%s" % (class_to_create.kind, i.name))
                                client.patch_object(i)
                        except Exception as ex:
                            if create:
                                print("Referenced object does not exist, creating %s/%s" % (class_to_create.kind, i.name))
                                client.add_object(i)
                            else:
                                raise Exception("Referenced object %s/%s does not exist" % (class_to_create.kind, i.name))
                        i.serialize(client)
                        attributes_map['body'][mapped_field_name].append(i.name)
            elif type == "array":
                items = getattr(self, name)
                if items.__len__() > 0:
                    attributes_map['body'][name] = list()
                    for i in items:
                        attributes_map['body'][name].append(i)
        return attributes_map
