#TODO Google how to build a docker image where the docker rule includes the json binaries as arguments and includes them.

py_binary(
    name = "poke_servicer",
    srcs = ["poke_servicer.py"],
    deps = ["//server:model", "//server:poke_resources"],
    visibility = ["//:__pkg__"]
)

py_library(
    name = "model",
    srcs = ["model.py"],
    visibility = ["//:__pkg__"]
)

py_library(
    name = "poke_resources",
    srcs = ["poke_resources.py"],
    visibility = ["//:__pkg__"]
)