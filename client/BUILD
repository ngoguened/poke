# Build docker image which has the client files and runs them.

load("@aspect_bazel_lib//lib:transitions.bzl", "platform_transition_filegroup")
load("@aspect_rules_py//py:defs.bzl", "py_binary", "py_library")
load("@pip//:requirements.bzl", "requirement")

py_library(
    name = "client_model",
    srcs = ["client_model.py"],
    visibility = ["//:__pkg__"]
)

py_library(
    name = "view",
    srcs = ["view.py"],
    visibility = ["//:__pkg__"]
)

py_library(
    name = "controller",
    srcs = ["controller.py"],
    visibility = ["//:__pkg__"]
)

py_binary(
    name = "client",
    srcs = ["client.py"],
    deps = [
        "//client:client_model", "//client:controller", "//client:view", "//proto:poke_py_pb2_grpc", "//proto:poke_py_pb2"],
    visibility = ["//:__pkg__"],
    main = "client.py"
)

filegroup(
    name = "image_load.tar",
    srcs = [":image_load"],
    output_group = "tarball",
)
