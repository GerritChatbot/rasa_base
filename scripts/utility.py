import pathlib
import yaml
import pandas as pd
from clumper import Clumper
from parse import compile as parse_compile


def nlu_path_to_dataframe(path):
    """
    Converts a single nlu file with intents into a dataframe.
    Usage:
    ```python
    from taipo.common import nlu_path_to_dataframe
    df = nlu_path_to_dataframe("path/to/nlu/nlu.yml")
    ```
    """
    res = (
        Clumper.read_yaml(path)
        .explode("nlu")
        .keep(lambda d: "intent" in d["nlu"].keys())
        .mutate(
            examples=lambda d: d["nlu"]["examples"].split("\n"),
            intent=lambda d: d["nlu"]["intent"],
        )
        .drop("nlu", "version")
        .explode(text="examples")
        .mutate(text=lambda d: d["text"][2:])
        .keep(lambda d: d["text"] != "")
        .collect()
    )
    return pd.DataFrame(res)


nlu_path_to_dataframe("data/nlu.yml").to_csv("new", index=False)
