# Build docker image which has the client files and runs them.

load("@aspect_bazel_lib//lib:transitions.bzl", "platform_transition_filegroup")
load("@aspect_rules_py//py:defs.bzl", "py_binary", "py_library")
load("@container_structure_test//:defs.bzl", "container_structure_test")
load("@pip//:requirements.bzl", "requirement")
load("@rules_oci//oci:defs.bzl", "oci_load", "oci_push")
load("//:py_layer.bzl", "py_oci_image")

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

py_oci_image(
    name = "client_image",
    base = "@ubuntu",
    binary = "client",
    entrypoint = ["client/client"],
)

oci_load(
    name = "client_tarball",
    image = ":client_image",
    repo_tags = ["ngoguened/poke:v0.0.1"],
)

oci_push(
    name = "client_push",
    image = ":client_image",
    remote_tags = ["v0.0.1"],
    repository = "ngoguened/poke",
)
