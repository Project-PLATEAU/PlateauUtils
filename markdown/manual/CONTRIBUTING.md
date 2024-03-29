# 開発者向け情報

## CityGMLのパーサーを拡充する

CityGMLのパーサーを拡充する(パースする属性を増やす)には、ライブラリ内の[parser/city_gml_parser.py](https://github.com/eukarya-inc/plateauutils/blob/main/plateauutils/parser/city_gml_parser.py)の`_parse`メソッドを修正します。

具体的には `for city_object_member in city_object_members:` のループ内で、以下のように属性を追加します。[PR#62](https://github.com/eukarya-inc/plateauutils/pull/62)

```python
            try:
                # bldg:usageを取得
                usage = city_object_member.find(".//bldg:usage", ns)
                # bldg:usageのdescriptionを取得
                usage_xml_path = os.path.normpath(
                    os.path.join(target, "..", "../../codelists/Building_usage.xml")
                )
                usage_xml_root = ET.fromstring(zip_file.read(usage_xml_path))
                usage_text = None
                for usage_xml_root_child in usage_xml_root.findall(
                    ".//gml:dictionaryEntry", ns
                ):
                    gml_name = usage_xml_root_child.find(".//gml:name", ns)
                    if str(gml_name.text) == str(usage.text):
                        usage_text = str(
                            usage_xml_root_child.find(".//gml:description", ns).text
                        )
                        break
            except AttributeError:
                print("bldg:usage is NoneType in", gid, "in", target)
                usage_text = None
```

上記の例では`try`ブロック内で`bldg:usage`を取得し、その`description`を`codelists/Building_usage.xml`から取得しています。

`try`ブロックを使うことで、`bldg:usage`が存在しない場合にエラーが発生することを防ぎます。

Plateauではファイルによって存在しない属性があるため、`try`ブロックを使うことでエラーを回避しています。

次に、`usage_text`を`return_value`に追加します。

```python
            return_value = {
                "gid": gid,
                "center": None,
                "min_height": 10000,
                "measured_height": measured_height,
                "building_structure_type": building_structure_type_text,
                "usage": usage_text,
            }
```

最後に`parse`メソッド及び`download_and_parse`メソッドのAPIドキュメント部分を修正します。[PR#65](https://github.com/eukarya-inc/plateauutils/pull/65)

Plateauでは様々な属性が定義されているため、属性に応じて`_parse`メソッドを拡充していき、`return_value`に属性を増やしていきます。

その際に気をつけるべきことは、属性値の属性の型及び多重度です。属性値の属性の型及び多重度は、[Plateauのドキュメント](https://www.mlit.go.jp/plateau/file/libraries/doc/plateau_doc_0001_ver03.pdf)に記載されています。

例えば、`uro:realEstateIDOfBuilding`は`xs:string`型であり、`1`の多重度を持ちます。

このケースでは、`return_value`にはString型の値を追加しますが、Plateauのバージョンによっては属性が無いため、`try`ブロックを使ってエラーを回避します。

また、`uro:realEstateIDOfBuildingUnitOwnership`は`xs:string`型であり、`0..*`の多重度を持ちます。

このケースでは、`return_value`にはString型の*配列*を追加しますが、属性が存在しない場合でも必ず空の配列を返すようにします。

このように、属性値の属性の型及び多重度に応じて`_parse`メソッドを拡充していきます。

`bldg:usage`のように、`gml:CodeType`を参照する場合は`codelists`ディレクトリ内のXMLファイルを参照してください。

## コード整形について

コード整形には、[black](https://pypi.org/project/black/)を利用しています。

Visual Studio Codeの場合はすでに設定されているため、特に追加設定は不要ですが、拡張機能 [Black Formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter) をインストールしておく必要があります。

なお、現状の設定では保存時に自動的にコード整形が行われます。

## テストについて

テストには、[pytest](https://docs.pytest.org/en/6.2.x/)を利用しています。

テストに使うデータは、ネットワーク通信を含めたテストの場合はインターネット上にデータを置きます。

その際、テストデータが肥大化しないように注意をしてください。

ローカルのテストデータの場合はテストコードと同じ`tests`ディレクトリ内に配置してください。

なお、Pull Requestを送る際は、テストが通ることを確認してください。Github workflowでテストが実行されます。

## APIドキュメントについて

APIドキュメントは、[Sphinx](https://www.sphinx-doc.org/ja/master/)を利用しています。

以下のコマンドでビルドできます。

```bash
cd doc
make html
```

ビルド後、`doc/_build/html/index.html`をブラウザで開くと、APIドキュメントが閲覧できます。

## リリースについて

リリースを行うにはまず、[pyproject.toml](https://github.com/eukarya-inc/plateauutils/blob/main/pyproject.toml)の`version`を更新します。

次に、Release Tagを作成します。

```bash
git tag v0.0.15
git push --tags
```

次に、[GitHub Tags](https://github.com/eukarya-inc/plateauutils/tags)からTagを選択し、`Release`を作成します。

`Release`を作成する際には、`Generate release note`を選択して、`Release`を作成します。

最後に、[PyPI](https://pypi.org/project/plateauutils/)にリリースをアップロードします。PyPIのアカウント及びアクセストークンが必要です。

```bash
python -m build
python -m twine upload --repository plateauutils-test dist/*
python -m twine upload --repository plateauutils dist/*
```

PyPIにリリースをアップロードする際には、`--repository`オプションで`plateauutils-test`を指定することで、テストリリースをアップロードできます。