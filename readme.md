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

`SubjectProgress` 和 `EpisodeCollect` 还没有真正的实现，可以引入 break change。
