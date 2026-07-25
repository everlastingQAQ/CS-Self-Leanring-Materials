# docs.everlasting.xin

CS自学材料网站源码，使用 Material for MkDocs 构建并发布到 <https://docs.everlasting.xin/>。

## 站点结构

- `/`：教程总目录
- `/CS61B/2021Spring/`：CS61B Spring 2021 中文教程
- `/CS61B/2021Spring/course/`：原课程主页的中文版
- `/CS61B/2021Spring/labs/`、`homeworks/`、`projects/`、`exams/`：中文实践资料

每门教程拥有独立配置、导航、搜索和资源，统一聚合到 `dist/` 后由 GitHub Pages 发布。

## 更新 CS61B 内容

```bash
python3 scripts/import_content.py
```

默认从 `/home/everlasting/下载/Hug61B_分章Markdown` 读取原始 Markdown，也可以通过 `HUG61B_SOURCE` 指定其他目录。导入只改写仓库中的生成内容，不修改原始目录。

Lab、作业、项目、考试及原课程主页使用独立导入脚本：

```bash
python3 scripts/import_sp21_coursework.py
```

脚本校验源 manifest 和文件数量，以原站 HTML 为页面基准，只翻译页面文字、替换本站已有中文资料链接，并将两份 2021 年公开日历静态化。默认只读源目录为 `/home/everlasting/下载/CS61B_SP21_Labs_Assignments_Exams_CN`。

## 构建、预览与发布

```bash
./scripts/build.sh
./scripts/serve.sh
```

构建使用固定依赖版本，并严格检查章节、链接、锚点、中文搜索、年份文案和本地运行时资源。
`main` 分支的构建通过后由 GitHub Actions 自动发布至 GitHub Pages；Pull Request 只执行验证，不发布。
`scripts/deploy.sh` 已禁用，避免再次把产物上传到旧服务器。

## 许可

课程中文整理内容使用 [CC BY-NC-SA 4.0](LICENSE.md)，原作归 Josh Hug 及相应作者所有，中文整理：everlasting。
