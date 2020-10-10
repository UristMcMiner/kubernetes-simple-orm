import kubernetes
from kubernetes.client.rest import ApiException
from pprint import pprint


class ORM:

    def __init__(self, kubernetes_host, token, namespace):
        self.kubernetes_host = kubernetes_host
        self.token = token
        self.lock = False
        self.namespace = namespace

        self.configuration = kubernetes.client.Configuration()
        self.configuration.api_key['authorization'] = token
        self.configuration.api_key_prefix['authorization'] = 'Bearer'
        self.configuration.host = kubernetes_host
        self.configuration.verify_ssl = False

        self.api_client = kubernetes.client.ApiClient(self.configuration)
        self.custom_object_api = kubernetes.client.CustomObjectsApi(self.api_client)

    def get_live_object(self, group, version, namespace, plural, name):
        return self.custom_object_api.get_namespaced_custom_object(group, version, namespace, plural, name)

    def add_object(self, object):
        mapped_attributes = object.serialize(self, create=True)
        version = mapped_attributes['version']
        namespace = self.namespace
        group = mapped_attributes['api_group']
        plural = mapped_attributes['plural']
        kind = mapped_attributes['kind']
        body = {
            "apiVersion": "%s/%s" % (group, version),
            "kind": kind,
            "metadata": {
                "name": object.name
            },
            "spec": mapped_attributes['body']
        }
        print(body)
        try:
            api_response = self.custom_object_api.create_namespaced_custom_object(group, version, namespace, plural, body)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling CustomObjectsApi->create_namespaced_custom_object: %s\n" % e)

    def delete_object(self, object):
        mapped_attributes = object.serialize(self)
        version = mapped_attributes['version']
        namespace = self.namespace
        group = mapped_attributes['api_group']
        plural = mapped_attributes['plural']
        kind = mapped_attributes['kind']
        try:
            api_response = self.custom_object_api.delete_namespaced_custom_object(group, version, namespace, plural, object.name)
        except ApiException as e:
            print("Exception when calling CustomObjectsApi->delete_namespaced_custom_object: %s\n" % e)


    def patch_object(self, object):
        mapped_attributes = object.serialize(self, patch=True)
        version = mapped_attributes['version']
        namespace = self.namespace
        group = mapped_attributes['api_group']
        plural = mapped_attributes['plural']
        kind = mapped_attributes['kind']
        body = {
            "apiVersion": "%s/%s" % (group, version),
            "kind": kind,
            "metadata": {
                "name": object.name
            },
            "spec": mapped_attributes['body']
        }
        try:
            api_response = self.custom_object_api.patch_namespaced_custom_object(group, version, namespace, plural, object.name, body)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling CustomObjectsApi->patch_namespaced_custom_object: %s\n" % e)

    def get_object(self, class_obj, name):
        version = class_obj.version
        namespace = self.namespace
        group = class_obj.api_group
        plural = class_obj.plural
        return class_obj.deserialize(class_obj, name, self)