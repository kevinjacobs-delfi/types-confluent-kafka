"""
types-confluent-kafka: A package providing type hints for the confluent-kafka Python package.
This package is licensed under the Apache 2.0 License.
"""
from __future__ import annotations

# standard library
from logging import Logger
from threading import Lock
from typing import DefaultDict, Literal

# pypi/conda library
from requests import Session

from .error import SchemaRegistryError as SchemaRegistryError

log: Logger
VALID_AUTH_PROVIDERS: Literal["URL", "USER_INFO"]

class _RestClient:
    session: Session
    base_url: str

    def __init__(self, conf: dict) -> None: ...
    def get(self, url: str, query: dict | None = ...): ...
    def post(self, url: str, body, **kwargs): ...
    def delete(self, url: str): ...
    def put(self, url: str, body: str | None = None): ...
    def send_request(
        self,
        url: str,
        method: Literal["GET", "POST", "DELETE", "PUT"],
        body: str | None = None,
        query: dict | None = None,
    ): ...

class _SchemaCache:
    lock: Lock
    schema_id_index: dict
    schema_index: dict
    subject_schemas: DefaultDict[str, set]

    def __init__(self) -> None: ...
    def set(self, schema_id: int, schema: Schema, subject_name: str | None = None) -> None: ...
    def get_schema(self, schema_id: int) -> Schema | None: ...
    def get_schema_id_by_subject(self, subject, schema: Schema) -> Schema | None: ...

class SchemaRegistryClient:
    def __init__(self, conf: dict) -> None: ...
    def __enter__(self) -> SchemaRegistryClient: ...
    def __exit__(self, *args) -> None: ...
    def register_schema(self, subject_name: str, schema: Schema, normalize_schemas: bool = False) -> int: ...
    def get_schema(self, schema_id) -> Schema: ...
    def lookup_schema(self, subject_name: str, schema: Schema, normalize_schemas: bool = False) -> RegisteredSchema: ...
    def get_subjects(self) -> list[str]: ...
    def delete_subject(self, subject_name: str, permanent: bool = ...) -> list[int]: ...
    def get_latest_version(self, subject_name: str) -> RegisteredSchema: ...
    def get_version(self, subject_name: str, version: int) -> RegisteredSchema: ...
    def get_versions(self, subject_name: str) -> list[int]: ...
    def delete_version(self, subject_name: str, version: int) -> int: ...
    def set_compatibility(self, subject_name: str | None = None, level: str | None = None) -> str: ...
    def get_compatibility(self, subject_name: str | None = None) -> str: ...
    def test_compatibility(
        self,
        subject_name: str,
        schema: Schema,
        version: int | Literal["latest"] = "latest",
    ) -> bool: ...

class Schema:
    schema_str: str
    schema_type: str
    references: list[SchemaReference]

    def __init__(self, schema_str: str, schema_type: str, references: list[SchemaReference] = []) -> None: ...
    def __eq__(self, other) -> bool: ...
    def __hash__(self) -> int: ...

class RegisteredSchema:
    schema_id: int
    schema: Schema
    subject: str
    version: int

    def __init__(self, schema_id: int, schema: Schema, subject: str, version: int) -> None: ...

class SchemaReference:
    name: str
    subject: str
    version: str

    def __init__(self, name: str, subject: str, version: str) -> None: ...
