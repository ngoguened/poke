load("@com_google_protobuf//:protobuf.bzl", "py_proto_library")
load("@rules_proto_grpc_python//:defs.bzl", "python_proto_library", "python_grpc_library")
load("@rules_proto//proto:defs.bzl", "proto_library")

proto_library(
    name = "poke",
    srcs = ["poke.proto"],
    visibility = ["//visibility:public"],
)

python_proto_library(
    name = "poke_py_pb2",
    protos = [":poke"],
    visibility = ["//visibility:public"]
)

python_grpc_library(
    name = "poke_py_pb2_grpc",
    protos = [":poke"],
    visibility = ["//visibility:public"]
)

proto_library(
    name = "resources",
    srcs = ["resources.proto"],
    visibility = ["//visibility:public"],
    deps = ["//proto:config"]
)

python_proto_library(
    name = "resources_py_pb2",
    protos = [":resources"],
    visibility = ["//visibility:public"]
)

proto_library(
    name = "config",
    srcs = ["config.proto"],
    visibility = ["//visibility:public"]
)

python_proto_library(
    name = "config_py_pb2",
    protos = [":config"],
    visibility = ["//visibility:public"]
)