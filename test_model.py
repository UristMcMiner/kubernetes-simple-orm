from kube_orm.base import ORMBase

api_group_global = "homeautomation.stack.io"
version_global = "v1"

class GPIO(ORMBase):

    api_group = api_group_global
    version = version_global
    kind = "GPIO"
    plural = "gpios"
    mapped_attributes = [
        {"name": "node", "type": "str"},
        {"name": "pin_id", "type": "str"}]

    def __init__(self, name, node, pin_id):
        self.name = name
        self.node = node
        self.pin_id = pin_id

    def get_json(self):
        return {"node": self.node,
                "pin_id": self.pin_id}

class Metric(ORMBase):

    api_group = api_group_global
    version = version_global
    kind = "Metric"
    plural = "metrics"
    mapped_attributes = [
        {"name": "description", "type": "str"},
        {"name": "type", "type": "str"}]

    def __init__(self, name, description, type):
        self.name = name
        self.description = description
        self.type = type


class Node(ORMBase):

    api_group = api_group_global
    version = version_global
    kind = "Node"
    plural = "nodes"
    mapped_attributes = [
        {"name": "gpios", "type": "list", "mapped_field_name": "gpios", "mapped_type": GPIO},
        {"name": "metrics", "type": "list", "mapped_field_name": "metrics", "mapped_type": Metric},
        {"name": "capabilities", "type": "array"}]

    def __init__(self, name, gpios, metrics, capabilities):
        self.name = name
        self.gpios = gpios
        self.metrics = metrics
        self.capabilities = capabilities

    def get_gpios(self):
        ret_list = list()
        for i in self.gpios:
            ret_list.append(i.get_json())
        return ret_list

    def get_metrics(self):
        ret_list = list()
        for i in self.metrics:
            ret_list.append(i.get_json())
        return ret_list

    def gpio_exists(self, pin_id):
        for i in self.gpios:
            if str(i.pin_id) == str(pin_id):
                return True
        return False

    def get_json(self):
        return {"name": self.name,
                "capabilities": self.capabilities,
                "gpios": self.get_gpios(),
                "metrics": self.get_metrics()
                }

class Operation(ORMBase):

    api_group = api_group_global
    version = version_global
    kind = "Operation"
    plural = "operations"
    mapped_attributes = [
        {"name": "description", "type": "str"},
        {"name": "pin", "type": "str"},
        {"name": "node", "type": "str"},
        {"name": "toggle", "type": "str"},
        {"name": "state", "type": "str"}]

    def __init__(self, name, description, pin, node, toggle, state):
        self.name = name
        self.description = description
        self.pin = pin
        self.node = node
        self.toggle = toggle
        self.state = state


class Task(ORMBase):

    api_group = api_group_global
    version = version_global
    kind = "Task"
    plural = "tasks"
    mapped_attributes = [
        {"name": "description", "type": "str"},
        {"name": "oneshot", "type": "str"},
        {"name": "time", "type": "str"},
        {"name": "cron_expression", "type": "str"},
        {"name": "operations", "type": "list", "mapped_field_name": "operations", "mapped_type": Operation}]

    def __init__(self, name, description, oneshot, time, cron_expression, operations):
        self.name = name
        self.description = description
        self.oneshot = oneshot
        self.time = time
        self.cron_expression = cron_expression
        self.operations = operations