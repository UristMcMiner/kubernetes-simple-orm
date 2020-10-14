from library import orm
from kube_orm import test_model

url = "https://<address>:6443"
token = ""
client = orm.ORM("https://192.168.1.49:6443", token, "default")
gpios = [test_model.GPIO("test1", "local-sensor-node", "6"), test_model.GPIO("test2", "local-sensor-node", "8")]
metrics = [test_model.Metric("testmetric1", "test-metric", "gauge"), test_model.Metric("testmetric2", "test-metric2", "gauge")]
node_to_add = test_model.Node("test", gpios, metrics, ["test"])

client.add_object(node_to_add)
input("Waiting for check, add")
object_from_api = client.get_object(test_model.Node, "test")
input("Waiting for check, get")
node_to_add.capabilities = ["cap2"]
node_to_add.metrics[0].description = "SampleDescription"
client.patch_object(node_to_add)
input("Waiting for check, patch")
client.delete_object(node_to_add)
for i in gpios:
    client.delete_object(i)
for i in metrics:
    client.delete_object(i)