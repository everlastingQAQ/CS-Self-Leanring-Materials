# CS 自学材料

[docs.everlasting.xin](https://docs.everlasting.xin/) 的网站源码。项目使用固定版本的 Material for MkDocs 构建多个静态文档站，再聚合为一个 GitHub Pages 发布产物。

当前收录：

- CS61B Spring 2021 中文教程
- 22 篇课程教材
- 11 篇 Lab、3 篇 Homework（不发布 HW1）、6 篇 Project
- 4 篇考试资料
- Spring 2021 原课程主页的中文归档版

## 维护入口

本机仓库：

```text
/home/everlasting/docs.everlasting.xin
```

线上网站：<https://docs.everlasting.xin/>

GitHub 仓库：<https://github.com/everlastingQAQ/docs.everlasting.xin>

进入项目：

```bash
cd /home/everlasting/docs.everlasting.xin
```

## 公开地址

| 内容 | 地址 |
| --- | --- |
| 教程总目录 | `/` |
| CS61B 首页 | `/CS61B/2021Spring/` |
| 中文课程主页 | `/CS61B/2021Spring/course/` |
| 课程教材 | `/CS61B/2021Spring/chapters/.../` |
| 实验 | `/CS61B/2021Spring/labs/.../` |
| 作业 | `/CS61B/2021Spring/homeworks/.../` |
| 项目 | `/CS61B/2021Spring/projects/.../` |
| 考试 | `/CS61B/2021Spring/exams/.../` |
| 来源与许可 | `/CS61B/2021Spring/about/` |

旧的 `/chapters/.../` 和 `/about/` 地址由构建脚本生成静态跳转页，兼容以前的链接。GitHub Pages 不支持服务端 301，因此这些页面通过 HTML 和 JavaScript 跳转。

## 项目结构

```text
.
├── portal/                              # docs.everlasting.xin 根门户
│   ├── docs/
│   └── mkdocs.yml
├── courses/
│   └── CS61B/2021Spring/
│       ├── data/calendars/              # 归档的 2021 课程日历
│       ├── docs/
│       │   ├── chapters/                # 导入生成的 22 篇教材
│       │   ├── labs/                    # 导入生成的实验
│       │   ├── homeworks/               # 导入生成的作业
│       │   ├── projects/                # 导入生成的项目
│       │   ├── exams/                   # 考试资料
│       │   ├── course/                  # 原课程主页中文版
│       │   └── assets/                  # 本地图片、CSS、JS、MathJax
│       ├── hooks.py
│       ├── mkdocs.yml                   # 课程导航和主题配置
│       └── search-dict.txt              # 中文搜索自定义词典
├── shared/overrides/                    # 门户和课程共用的模板覆盖
├── scripts/                             # 导入、构建、检查和兼容跳转脚本
├── server/                              # 已停用的旧服务器配置，仅作历史冷备份
├── .github/workflows/                   # GitHub Pages 构建与部署
├── Dockerfile
├── requirements.txt                     # 固定 Python 依赖版本
└── dist/                                # 本地构建产物，不提交 Git
```

## 哪些文件可以直接修改

可以直接维护：

- `portal/docs/`：根门户内容与样式。
- `portal/mkdocs.yml`：根门户配置。
- `courses/CS61B/2021Spring/docs/index.md`：CS61B Material 首页。
- `courses/CS61B/2021Spring/docs/about.md`：来源与许可页。
- `courses/CS61B/2021Spring/docs/exams/`：当前考试资料。
- `courses/CS61B/2021Spring/mkdocs.yml`：课程导航、主题和插件配置。
- `courses/CS61B/2021Spring/search-dict.txt`：中文搜索分词。
- `courses/CS61B/2021Spring/docs/assets/stylesheets/`：课程样式。
- `shared/overrides/`：共用模板与缓存刷新逻辑。

以下内容由脚本生成，手工修改可能在下次导入时丢失：

- `courses/CS61B/2021Spring/docs/chapters/`
- `courses/CS61B/2021Spring/docs/labs/`
- `courses/CS61B/2021Spring/docs/homeworks/`
- `courses/CS61B/2021Spring/docs/projects/`
- `courses/CS61B/2021Spring/docs/course/index.md`
- `courses/CS61B/2021Spring/docs/import-manifest.json`
- `courses/CS61B/2021Spring/docs/coursework-import-manifest.json`

需要改变这些页面的生成规则时，应修改相应导入脚本，再重新导入。

## 环境要求

日常构建只需要：

- Docker
- Python 3
- Git

MkDocs 及其 Python 依赖在 Docker 镜像内安装，本机不需要单独安装。当前固定版本见 `requirements.txt`：

```text
mkdocs-material==9.7.7
jieba==0.42.1
beautifulsoup4==4.13.4
```

不要在没有完整测试的情况下自动升级这些依赖。

## 本地构建与预览

严格构建：

```bash
./scripts/build.sh
```

该脚本会依次：

1. 构建固定依赖版本的 Docker 镜像。
2. 严格构建根门户到 `dist/`。
3. 严格构建 CS61B 到 `dist/CS61B/2021Spring/`。
4. 移除 Sitemap 中无法准确维护的统一 `lastmod`。
5. 生成旧地址的静态跳转页。
6. 为页面、CSS、JavaScript 和搜索索引写入内容版本。
7. 检查页面数量、链接、锚点、搜索、图片、SEO 元数据、备案信息、导航和 Pages 产物。

构建成功时会看到类似：

```text
Validated 80 HTML pages, 22 chapters, 24 legacy redirects, ...
```

本地预览：

```bash
./scripts/serve.sh
```

然后访问 <http://127.0.0.1:8000/>。`serve.sh` 会先完整构建，再启动静态文件服务器；按 `Ctrl+C` 结束。

`dist/` 是一次性构建产物，已被 `.gitignore` 忽略，不要提交。

## 更新课程教材

教材的默认只读来源：

```text
/home/everlasting/下载/Hug61B_分章Markdown
```

重新导入 22 篇教材：

```bash
python3 scripts/import_content.py
```

使用其他来源目录：

```bash
HUG61B_SOURCE=/绝对路径/到/Markdown目录 \
  python3 scripts/import_content.py
```

导入脚本会：

- 检查预期的 22 个源文件。
- 规范标题层级和年份文字。
- 根据 `scripts/import_content.py` 中的 `CHAPTER_DESCRIPTIONS` 写入每章独立的 SEO 描述。
- 本地化远程图片。
- 写入教材来源与许可信息。
- 准备仓库内的 MathJax 运行时。
- 更新 `import-manifest.json`。

如果只需更新现有教材的 SEO 描述，并把来源与许可信息重新移动到每篇底部，不重新下载资源：

```bash
python3 scripts/import_content.py --attribution-only
```

完成后必须执行：

```bash
./scripts/build.sh
git diff --check
```

## 更新 Lab、Homework 和 Project

当前逐字对应翻译的默认只读来源：

```text
/home/everlasting/下载/CS61B_SP21_逐字对应中文翻译
```

重新导入：

```bash
python3 scripts/import_sp21_coursework.py
```

指定其他来源目录：

```bash
python3 scripts/import_sp21_coursework.py --source /绝对路径/到/翻译目录
```

导入约定：

- 导入 11 篇 Lab、3 篇 Homework 和 6 篇 Project，共 20 篇。
- HW1 明确不发布。
- 每个 Lab、Homework 或 Project 都是一个可连续向下阅读的页面。
- 页面顶部不保留翻译说明。
- 每篇页面最下方仅保留对应的“原始页面”链接。
- 图片下载到 `docs/assets/coursework/`，并记录大小和 SHA-256。
- 默认复用已经校验过的本地图片，避免每次导入联网。
- 导入会重写三个分类的内容页和目录页。

仅在确实需要重新下载所有课程作业图片时使用：

```bash
python3 scripts/import_sp21_coursework.py --refresh-images
```

此选项需要网络，任意图片下载或校验失败都会终止导入。

## 更新中文课程主页

`/CS61B/2021Spring/course/` 是 Spring 2021 原课程主页的中文归档版。普通作业导入只会更新其中指向本站资料的链接，不会联网重抓整个首页。

仅在明确需要重新获取原主页和两份公开日历时运行：

```bash
python3 scripts/import_sp21_coursework.py --refresh-course-home
```

同时重抓课程作业图片：

```bash
python3 scripts/import_sp21_coursework.py \
  --refresh-course-home \
  --refresh-images
```

刷新课程主页属于高影响操作。提交前应重点比较：

- `courses/CS61B/2021Spring/docs/course/index.md`
- `courses/CS61B/2021Spring/data/calendars/`
- `courses/CS61B/2021Spring/docs/coursework-import-manifest.json`

## 修改导航和样式

CS61B 左侧导航在以下文件中维护：

```text
courses/CS61B/2021Spring/mkdocs.yml
```

增加、删除或改名页面时，必须同步更新 `nav`。课程教材页的左侧页内目录只显示到 H2，因为当前配置为 `toc_depth: 2`。

主要样式文件：

```text
portal/docs/assets/stylesheets/extra.css
courses/CS61B/2021Spring/docs/assets/stylesheets/extra.css
courses/CS61B/2021Spring/docs/assets/stylesheets/course-home-v2.css
```

独立课程主页模板：

```text
shared/overrides/course-home.html
```

Material 页面共用模板：

```text
shared/overrides/main.html
shared/overrides/partials/cache-refresh.html
```

修改 CSS 或 JavaScript 后仍应运行完整构建。构建阶段会自动添加 `sitev` 内容版本参数，不需要手工改查询参数来清缓存。

## 缓存更新机制

每次构建会根据全部静态产物生成 `dist/site-version.json`，并执行以下处理：

- CSS 和 JavaScript URL 自动附加 `?sitev=<内容指纹>`。
- 中文搜索索引使用同一内容指纹。
- 页面每 30 秒检查一次新版本。
- 浏览器标签重新获得焦点或恢复可见时再次检查。
- 检测到新版本后，当前页面自动刷新一次。

如果线上页面没有更新，按以下顺序检查：

1. GitHub Actions 是否构建和部署成功。
2. `https://docs.everlasting.xin/site-version.json` 是否已经变化。
3. 当前页面是否仍指向正确地址。
4. 浏览器扩展或代理是否拦截了版本请求。

不要通过修改 `scripts/stamp_release.py`、删除版本检查或反复手工改 CSS 查询参数来掩盖部署问题。

## 备案与搜索收录

备案号在根门户和课程配置的 `copyright` 中维护，独立课程主页在 `shared/overrides/course-home.html` 中维护。当前统一使用：

```text
鄂ICP备2026035887号
https://beian.miit.gov.cn/
```

修改备案信息时必须同步三处，并运行完整构建；严格检查会验证所有正常页面都包含备案号和链接。

根站的 `WebSite` JSON-LD 位于 `shared/overrides/main.html`，只允许在 `https://docs.everlasting.xin/` 输出。教材页的描述由导入脚本维护，不要只修改生成后的 Markdown。

发布后在 Google Search Console 和 Bing Webmaster Tools 提交：

```text
https://docs.everlasting.xin/sitemap.xml
https://docs.everlasting.xin/CS61B/2021Spring/sitemap.xml
```

本项目不配置百度站长验证或提交。Sitemap 不写入无法准确反映内容变更时间的 `lastmod`；如未来需要恢复，必须使用每一页真实的更新时间。

## 发布到 GitHub Pages

发布由 `.github/workflows/` 中的工作流完成：

- Pull Request：只构建和验证，不发布。
- 推送到 `main`：构建、验证并发布到 GitHub Pages。
- `workflow_dispatch`：允许在 GitHub Actions 页面手动重新发布。

标准发布流程：

```bash
git status
git diff --check
./scripts/build.sh
git add <本次需要提交的文件>
git commit -m "说明本次修改"
git push origin main
```

不要直接执行 `git add .`。仓库可能同时存在尚未提交的个人修改，应只暂存本次确认过的文件。

推送后在以下页面确认构建和部署均成功：

<https://github.com/everlastingQAQ/docs.everlasting.xin/actions>

旧服务器发布脚本 `scripts/deploy.sh` 已故意禁用。当前网站只由 GitHub Pages 提供，不要重新把 `dist/` 上传到服务器。

## 添加一门新课程

建议每门课程使用独立构建配置：

```text
courses/<课程名>/<学期>/
├── docs/
├── mkdocs.yml
└── 该课程需要的脚本或数据
```

添加课程时至少需要完成：

1. 创建课程目录、首页和 `mkdocs.yml`。
2. 将 `site_url` 设置为最终子路径。
3. 在根门户 `portal/docs/index.md` 添加课程入口。
4. 在 `scripts/build.sh` 中把课程构建到对应的 `dist/<课程名>/<学期>/`。
5. 扩展 `scripts/check_site.py`，验证新课程入口、资源、链接和页面数量。
6. 检查根 `robots.txt` 与各课程 Sitemap。
7. 本地严格构建并测试桌面端、移动端、搜索和 404。

不要让一门课程依赖另一门课程的生成目录；共享模板应放在 `shared/`，课程专用资源应留在自己的目录中。

## 提交前检查清单

```bash
git status --short
git diff --check
./scripts/build.sh
git status --short
```

同时人工确认：

- 首页、课程首页和本次修改的页面能打开。
- 内部链接与标题锚点正确。
- 图片、公式、代码块和中文搜索正常。
- 移动端没有整页横向溢出。
- HW1 没有出现在导航、搜索或构建产物中。
- Lab、Homework 和 Project 页面底部只有一个正确的原始页面链接。
- `dist/`、密钥、证书和本地下载目录没有进入 Git 暂存区。

## 常见问题

### 导入脚本提示源文件缺失

确认下载目录名称、文件名和层级没有改变。实践资料也可以通过 `--source` 指向其他目录；教材通过 `HUG61B_SOURCE` 指定目录。

### 图片下载失败

普通重复导入应复用仓库中的本地图片。只有需要更新图片时才使用 `--refresh-images`；网络异常时不要提交不完整的导入结果。

### 构建提示 Material 或 MkDocs 的未来版本警告

项目依赖已固定。只要严格构建最终成功，该上游提示本身不代表当前构建失败。升级依赖必须单独测试导航、模板、搜索、MathJax 和缓存机制。

### `scripts/deploy.sh` 返回错误

这是预期行为。服务器部署已停用，发布方式是推送 `main` 并由 GitHub Pages 工作流部署。

### 想撤销一次线上更新

优先使用 Git 创建一个反向提交，再推送 `main`，让 GitHub Pages 重新构建。不要修改 GitHub Pages 的生成环境或恢复旧服务器入口。

## 许可与来源

中文整理内容采用 [CC BY-NC-SA 4.0](LICENSE.md)。原作及课程资料版权归 Josh Hug、UC Berkeley 和相应作者所有；每篇导入页面保留自己的原始页面链接。
