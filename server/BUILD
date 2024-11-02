#TODO Google how to build a docker image where the docker rule includes the json binaries as arguments and includes them.
load("@aspect_rules_py//py:defs.bzl", "py_binary", "py_library")
load("@pip//:requirements.bzl", "requirement")

py_binary(
    name = "poke_servicer",
    srcs = ["poke_servicer.py"],
    deps = ["//server:model", "//server:poke_resources", "//proto:poke_py_pb2_grpc", "//proto:poke_py_pb2"],
    visibility = ["//:__pkg__"]
)

py_library(
    name = "model",
    srcs = ["model.py"],
    visibility = ["//:__pkg__"]
)

py_binary(
    name = "poke_resources",
    srcs = ["poke_resources.py", "moves_and_templates.textproto"],
    # "//proto:resources_py_pb2",
    deps = ["//proto:config_py_pb2", "//server:model"],
    visibility = ["//:__pkg__"]
)