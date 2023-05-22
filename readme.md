timeline micro service

```shell
git clone --recursive https://github.com/bangumi/service-timeline
cd service-timeline
```

## install deps

Use [python-poetry](https://github.com/python-poetry/poetry)

```shell
poetry install --sync
```


## generate stub

use [go-task](https://github.com/go-task/task)

```shell
task gen
```


## API

[./proto/api/v1/timeline.proto](https://github.com/bangumi/proto/blob/master/api/v1/timeline.proto)

## 性能

chii_timeline 表目前非常大，查询条件的 where 条件 **必需** 命中索引。
