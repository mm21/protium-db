from abc import abstractmethod
from pathlib import Path
from typing import Self, Any, cast

import pydantic
import yaml


MODEL_FILENAME = ".model.yaml"


class BaseModel(pydantic.BaseModel):

    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def from_path(cls, path: Path, *args, **kwargs) -> Self:
        """
        Load model from provided path, which can be a directory or file.
        """
        path_: Path = _normalize_path(path)

        fields: dict[str, Any] = cls.get_fields(path_)

        return cls.from_fields(fields, path_, *args, **kwargs)

    # TODO: return dict, rename abstract method as adapt_fields
    @classmethod
    def from_fields(
        cls, fields: dict[str, Any], container: Path, *args, **kwargs
    ) -> Self:
        """
        Can be overridden to implement any special processing on raw fields
        before creating model.

        :param fields: Dictionary of primitive fields
        :param container: Folder from which to get additional fields
        """
        return cls(**fields)

    @staticmethod
    def get_fields(path: Path) -> dict[str, Any]:
        """
        Get primitive fields from yaml.
        """

        path_yaml: Path
        path_yaml = path if path.is_file() else path / MODEL_FILENAME

        assert path_yaml.is_file(), f"Model file does not exist {path_yaml}"

        fields: dict[str, Any] = {}
        fields_raw: dict

        with path_yaml.open() as fh:
            fields_load: dict | None = yaml.full_load(fh)
            if fields_load is None:
                fields_raw = {}
            else:
                fields_raw = cast(dict, fields_load)
            assert isinstance(
                fields_raw, dict
            ), f"Model file <{path_yaml}> does not parse to a dict: {fields_raw}"

        for key, value in fields_raw.items():
            assert isinstance(key, str)
            fields[key] = value

        return fields


class BaseFolderModel(BaseModel):
    pass


class BaseFileModel(BaseModel):
    pass


def _normalize_path(path: Path | str) -> Path:
    path_ = Path(path) if isinstance(path, str) else path
    assert isinstance(path_, Path)

    return path_
