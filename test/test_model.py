from protium import BaseModel


class Model1(BaseModel):
    field1: str
    field2: str | None = None


def test_model1():

    model = Model1.from_path("test/db-test/model1")

    assert model.field1 == "abc"
    assert model.field2 is None
