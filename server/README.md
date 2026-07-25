# 服务器部署说明

- Web 根目录：`/opt/1panel/www/sites/docs.everlasting.xin/current`
- 版本目录：`/opt/1panel/www/sites/docs.everlasting.xin/releases/<UTC 时间>-<Git SHA>`
- OpenResty 配置：`/opt/1panel/www/conf.d/docs.everlasting.xin.conf`
- ACME Webroot：`/opt/1panel/www/sites/docs.everlasting.xin/acme`
- 证书部署目录：`/opt/1panel/www/sites/docs.everlasting.xin/ssl`

部署新静态版本：

```bash
./scripts/build.sh
./scripts/deploy.sh
```

聚合发布内容包括根教程门户和 `/CS61B/2021Spring/` 课程站。旧 `/chapters/` 与 `/about/` 地址由 OpenResty 永久重定向到课程路径。

回滚时，将服务器上的 `current` 软链接原子切换到上一个 `releases` 目录，然后在容器内执行 `openresty -t`。静态文件切换本身不需要重启 OpenResty。
