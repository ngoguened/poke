load("@pip//:requirements.bzl", "requirement")
load("@aspect_rules_py//py:defs.bzl", "py_binary", "py_library")

py_library(
    name = "poke_pb2",
    srcs = ["poke_pb2.py"],
    visibility = ["//visibility:public"],
    deps = [requirement("protobuf")]
)

py_library(
    name = "poke_pb2_grpc",
    srcs = ["poke_pb2_grpc.py"],
    visibility = ["//visibility:public"],
    deps = [requirement("protobuf")]
)