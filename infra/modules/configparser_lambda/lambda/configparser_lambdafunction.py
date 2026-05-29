from __future__ import print_function

import gzip
import json
import os
import urllib.parse

import boto3
import requests

CLUSTER_ENDPOINT = os.environ["CLUSTER_ENDPOINT"]
CLUSTER_PORT = os.environ["CLUSTER_PORT"]

# Reuse the Neptune traversal across invocations but initialize lazily.
g = None
T = None


def get_traversal():
    global g, T
    if g is None:
        from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
        from gremlin_python.process.traversal import T as TraversalTokens
        from gremlin_python.structure.graph import Graph

        remote_conn = DriverRemoteConnection(
            f"wss://{CLUSTER_ENDPOINT}:{CLUSTER_PORT}/gremlin",
            "g",
        )
        graph = Graph()
        g = graph.traversal().withRemote(remote_conn)
        T = TraversalTokens
    return g


def run_sample_gremlin_websocket():
    traversal = get_traversal()
    return traversal.V().hasLabel("Instance").toList()


def run_sample_gremlin_http():
    url = f"https://{CLUSTER_ENDPOINT}:{CLUSTER_PORT}/gremlin"
    payload = {
        "gremlin": "g.V().hasLabel('Instance').valueMap().with_('~tinkerpop.valueMap.tokens').toList()"
    }
    return requests.post(
        url,
        data=json.dumps(payload),
    )


def insert_vertex_graph(vertex_id, vertex_label):
    traversal = get_traversal()
    node_exists_id = traversal.V(str(vertex_id)).toList()
    if node_exists_id:
        return
    traversal.addV(str(vertex_label)).property(T.id, str(vertex_id)).next()


def insert_edge_graph(edge_id, edge_from, edge_to, to_vertex_label, edge_label):
    traversal = get_traversal()
    insert_vertex_graph(edge_to, to_vertex_label)

    edge_exists_id = traversal.E(str(edge_id)).toList()
    if edge_exists_id:
        return

    traversal.V(str(edge_from)).addE(str(edge_label)).to(traversal.V(str(edge_to))).property(T.id, str(edge_id)).next()


def parse_vertex_info(vertex_input):
    traversal = get_traversal()
    vertex_id = vertex_input["resourceId"]
    label = vertex_input["resourceType"]
    item_status = vertex_input["configurationItemStatus"]

    if item_status == "ResourceDeleted":
        node_exists_id = traversal.V(str(vertex_id)).toList()
        if not node_exists_id:
            insert_vertex_graph(vertex_id, label)
        traversal.addV(str(item_status)).property(T.id, str(vertex_id)).next()
        return

    insert_vertex_graph(vertex_id, label)


def parse_edge_info(edge_input):
    item_status = edge_input["configurationItemStatus"]
    if item_status == "ResourceDeleted":
        return

    for item in edge_input.get("relationships", []):
        from_vertex = edge_input["resourceId"]
        to_vertex = item.get("resourceId") or item.get("resourceName")
        if not to_vertex:
            continue

        to_vertex_label = item["resourceType"]
        edge_id = f"{from_vertex}:{to_vertex}"
        label = item["name"]
        insert_edge_graph(edge_id, from_vertex, to_vertex, to_vertex_label, label)


def lambda_handler(event, context):
    bucket = None
    obj_key = None

    if "Records" in event and event["Records"][0].get("eventSource") == "aws:s3":
        s3_data = event["Records"][0].get("s3", {})
        bucket = s3_data.get("bucket", {}).get("name")
        obj_key = s3_data.get("object", {}).get("key")
    elif "tasks" in event and event["tasks"][0].get("s3BucketArn"):
        bucket = event["tasks"][0]["s3BucketArn"].split(":::")[1]
        obj_key = event["tasks"][0].get("s3Key")

    if not bucket or not obj_key:
        return {"statusCode": 400, "body": json.dumps("Missing S3 object metadata in event")}

    s3 = boto3.resource("s3")
    decoded_key = urllib.parse.unquote(obj_key)

    if decoded_key.endswith(".gz"):
        s3_object = s3.Object(bucket, decoded_key)
        with gzip.GzipFile(fileobj=s3_object.get()["Body"]) as gzipfile:
            content = json.loads(gzipfile.read())

        for item in content.get("configurationItems", []):
            parse_vertex_info(item)
            parse_edge_info(item)

    return {"statusCode": 200, "body": json.dumps("Processed config file")}
