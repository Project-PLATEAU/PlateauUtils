import pytest
import httpretty


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_public_query():
    from plateauutils.citygmlfinder.from_reearth_cms import public_query

    f = open("./plateauutils/citygmlfinder/tests/data3.json")
    data = f.read()
    httpretty.register_uri(
        httpretty.GET,
        "http://localhost:8081/api?page=1",
        body=data,
        content_type="application/json",
    )
    result = public_query(
        endpoint="http://localhost:8081/api",
        prefecture="東京都",
        city_name="西東京市",
    )
    assert (
        result
        == "https://localhost:8081/assets/1e/b01fc6-2ce9-4277-983f-09f8069034f7/13229_nishitokyo-shi_2020_citygml_1.zip"
    )


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_public_query_fail_less_args():
    from plateauutils.citygmlfinder.from_reearth_cms import public_query
    from plateauutils.citygmlfinder.from_reearth_cms import NoArgsException

    asserted = False
    with pytest.raises(NoArgsException) as e:
        result = public_query(
            prefecture="東京都",
            city_name="西東京市",
        )


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_public_query_not_found():
    from plateauutils.citygmlfinder.from_reearth_cms import public_query
    from plateauutils.citygmlfinder.from_reearth_cms import NotFoundException

    f = open("./plateauutils/citygmlfinder/tests/data4.json")
    data4 = f.read()
    httpretty.register_uri(
        httpretty.GET, "http://localhost:8081/api?page=1", status=404
    )
    asserted = False
    with pytest.raises(NotFoundException) as e:
        result = public_query(
            endpoint="http://localhost:8081/api",
            prefecture="東京都",
            city_name="西東京市",
        )


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_public_query_many_jsons():
    from plateauutils.citygmlfinder.from_reearth_cms import public_query
    from plateauutils.citygmlfinder.from_reearth_cms import NoArgsException

    f1 = open("./plateauutils/citygmlfinder/tests/data3.json")
    data3 = f1.read()
    f2 = open("./plateauutils/citygmlfinder/tests/data4.json")
    data4 = f2.read()

    # NOTE: order of calling register_url matters
    # data4 contains hasMore
    httpretty.register_uri(
        httpretty.GET,
        "http://localhost:8081/api?page=2",
        body=data3,
        content_type="application/json",
    )
    httpretty.register_uri(
        httpretty.GET,
        "http://localhost:8081/api?page=1",
        body=data4,
        content_type="application/json",
    )
    result = public_query(
        endpoint="http://localhost:8081/api",
        prefecture="東京都",
        city_name="西東京市",
    )
    assert (
        result
        == "https://localhost:8081/assets/1e/b01fc6-2ce9-4277-983f-09f8069034f7/13229_nishitokyo-shi_2020_citygml_1.zip"
    )


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_private_query():
    from plateauutils.citygmlfinder.from_reearth_cms import private_query

    f = open("./plateauutils/citygmlfinder/tests/data2.json")
    data = f.read()

    # NOTE: order of calling register_url matters
    httpretty.register_uri(
        httpretty.GET,
        "http://localhost:8081/api/projects/testprj/models/test/items?sort=createdAt&dir=desc&page=1&perPage=50&ref=latest",
        body=data,
        content_type="application/json",
    )

    result = private_query(
        endpoint="http://localhost:8081/api",
        access_token="dummy",
        project="testprj",
        model="test",
        prefecture="東京都",
        city_name="西東京市",
    )
    assert result is not None


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_private_query_with_many():
    from plateauutils.citygmlfinder.from_reearth_cms import private_query

    f1 = open("./plateauutils/citygmlfinder/tests/data1.json")
    data1 = f1.read()
    f2 = open("./plateauutils/citygmlfinder/tests/data2.json")
    data2 = f2.read()

    # NOTE: order of calling register_url matters
    httpretty.register_uri(
        httpretty.GET,
        "http://localhost:8081/api/projects/testprj/models/test/items?sort=createdAt&dir=desc&page=2&perPage=50&ref=latest",
        body=data2,
        content_type="application/json",
    )
    httpretty.register_uri(
        httpretty.GET,
        "http://localhost:8081/api/projects/testprj/models/test/items?sort=createdAt&dir=desc&page=1&perPage=50&ref=latest",
        body=data1,
        content_type="application/json",
    )

    result = private_query(
        endpoint="http://localhost:8081/api",
        access_token="dummy",
        project="testprj",
        model="test",
        prefecture="東京都",
        city_name="西東京市",
    )
    assert result is not None


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_private_query_fail():
    from plateauutils.citygmlfinder.from_reearth_cms import private_query

    httpretty.register_uri(
        httpretty.GET,
        "http://localhost:8081/api/projects/testprj/models/test/items?sort=createdAt&dir=desc&page=1&perPage=50&ref=latest",
        status=404,
    )
    result = private_query(
        endpoint="http://localhost:8081/api",
        access_token="dummy",
        project="testprj",
        model="test",
        prefecture="東京都",
        city_name="西東京市",
    )
    assert result is None


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_private_query_fail_on_second():
    from plateauutils.citygmlfinder.from_reearth_cms import private_query

    f = open("./plateauutils/citygmlfinder/tests/data1.json")
    data = f.read()
    httpretty.register_uri(
        httpretty.GET,
        "http://localhost:8081/api/projects/testprj/models/test/items?sort=createdAt&dir=desc&page=2&perPage=50&ref=latest",
        status=404,
    )
    httpretty.register_uri(
        httpretty.GET,
        "http://localhost:8081/api/projects/testprj/models/test/items?sort=createdAt&dir=desc&page=1&perPage=50&ref=latest",
        body=data,
        content_type="application/json",
    )
    result = private_query(
        endpoint="http://localhost:8081/api",
        access_token="dummy",
        project="testprj",
        model="test",
        prefecture="東京都",
        city_name="西東京市",
    )
    assert result is None

@httpretty.activate(verbose=True, allow_net_connect=False)
def test_asset_upload():
    from plateauutils.citygmlfinder.from_reearth_cms import upload_to_reearth

    data = """{
  "archiveExtractionStatus": "done",
  "contentType": "text/plain; charset=utf-8",
  "createdAt": "2023-09-29T08:58:10.712Z",
  "file": {
    "contentType": "text/plain; charset=utf-8",
    "name": "sample.txt",
    "path": "/sample.txt",
    "size": 13
  },
  "id": "01hbg2hrwr1qvx6prdxsf44x1z",
  "name": "sample.txt",
  "previewType": "unknown",
  "projectId": "01h2f43g1w67as5meqvbh4xas6",
  "totalSize": 13,
  "updatedAt": "0001-01-01T00:00:00Z",
  "url": "http://localhost:8080/assets/assets/6b/665c61-9168-4a30-b9c4-5ee88be7f71a/sample.txt"
}"""
    httpretty.register_uri(
        httpretty.POST,
        "http://localhost:8081/api/projects/dummy/assets",
        body=data,
        content_type="application/json",
    )
    result = upload_to_reearth(
        endpoint="http://localhost:8081/api",
        access_token="dummy",
        project="dummy",
        filepath="./plateauutils/citygmlfinder/tests/data1.json"
    )
    assert (
        result
        == True
    )

@httpretty.activate(verbose=True, allow_net_connect=False)
def test_asset_upload_fail():
    from plateauutils.citygmlfinder.from_reearth_cms import upload_to_reearth

    data = """{
  "error": "operation denied"
}"""
    httpretty.register_uri(
        httpretty.POST,
        "http://localhost:8081/api/projects/dummy/assets",
        status=400,
        body=data,
        content_type="application/json",
    )
    result = upload_to_reearth(
        endpoint="http://localhost:8081/api",
        access_token="dummy",
        project="dummy",
        filepath="./plateauutils/citygmlfinder/tests/data1.json"
    )
    assert (
        result
        == False
    )