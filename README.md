# docs.everlasting.xin

Everlasting 中文教程站源码，使用 Material for MkDocs 构建并发布到 <https://docs.everlasting.xin/>。

## 站点结构

- `/`：教程总目录
- `/CS61B/2021Spring/`：CS61B Spring 2021 中文教程

每门教程拥有独立配置、导航、搜索和资源，统一聚合到 `dist/` 后部署。

## 更新 CS61B 内容

```bash
python3 scripts/import_content.py
```

默认从 `/home/everlasting/下载/Hug61B_分章Markdown` 读取原始 Markdown，也可以通过 `HUG61B_SOURCE` 指定其他目录。导入只改写仓库中的生成内容，不修改原始目录。

## 构建、预览与部署

```bash
./scripts/build.sh
./scripts/serve.sh
./scripts/deploy.sh
```

构建使用固定依赖版本，并严格检查章节、链接、锚点、中文搜索、年份文案和本地运行时资源。

## 许可

课程中文整理内容使用 [CC BY-NC-SA 4.0](LICENSE.md)，原作归 Josh Hug 及相应作者所有，中文整理：everlasting。
