#TODO Google how to build a docker image where the docker rule includes the json binaries as arguments and includes them.
load("@aspect_rules_py//py:defs.bzl", "py_binary", "py_library", "py_test")
load("@pip//:requirements.bzl", "requirement")
load("@rules_oci//oci:defs.bzl", "oci_load", "oci_push")
load("//:py_layer.bzl", "py_oci_image")

py_binary(
    name = "poke_servicer",
    srcs = ["poke_servicer.py"],
    deps = ["//server:model", "//server:poke_resources", "//proto:poke_py_pb2_grpc", "//proto:poke_py_pb2"],
    visibility = ["//:__pkg__"]
)

py_library(
    name = "model",
    srcs = ["model.py"],
    deps = ["//proto:poke_py_pb2"],
    visibility = ["//:__pkg__"]
)

py_test(
    name = "server_tests",
    srcs = ["server_tests.py"],
    deps = ["//server:poke_servicer"],
)

py_test(
    name = "load_balancing",
    srcs = ["load_balancing.py"],
    deps = ["//server:poke_servicer", requirement("locust")],
)

py_test(
    name = "model_tests",
    srcs = ["model_tests.py"],
    deps = ["//server:model"],
)

filegroup(
    name = "config",
    srcs = ["//server:moves_and_templates.textproto"]
)

py_binary(
    name = "poke_resources",
    srcs = ["poke_resources.py"],
    deps = ["//proto:config_py_pb2", "//server:model", "//proto:resources_py_pb2"],
    visibility = ["//:__pkg__"],
    data = [":config"]
)

py_oci_image(
    name = "server_image",
    base = "@ubuntu",
    binary = "poke_servicer",
    exposed_ports = ["[::]:50052"],
    entrypoint = ["server/poke_servicer"]
)

oci_load(
    name = "server_tarball",
    image = ":server_image",
    repo_tags = ["ngoguened/poke_server:v0.0.1"],
)

oci_push(
    name = "server_push",
    image = ":server_image",
    remote_tags = ["v0.0.1"],
    repository = "ngoguened/poke_server",
)
