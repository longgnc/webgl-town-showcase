# 云溪古镇 · WebGL 三维漫游

在浏览器中漫步于白墙灰瓦、木楼临水的滇西风格古镇。本仓库保存云溪古镇、清明上河图场景、单文件交付、制作说明和可复用的制作技能。

## 公网体验

- **[进入云溪古镇](https://longgnc.github.io/webgl-town-showcase/)**
- [直接打开云溪古镇单文件](https://longgnc.github.io/webgl-town-showcase/云溪古镇_离线漫游.html)
- [清明上河图完整漫游](https://longgnc.github.io/webgl-town-showcase/清明上河图_完整漫游.html)
- [GitHub 项目仓库](https://github.com/longgnc/webgl-town-showcase)

网站通过 GitHub Pages 公开发布，无需登录或安装客户端。首页自动进入 `云溪古镇_离线漫游.html`；该文件已内嵌场景脚本、引擎和样式，运行不依赖外部 CDN。首次打开需要等待场景生成和着色器编译。

建议在支持 WebGL 2 的桌面浏览器中开启硬件加速。帧率受显卡、分辨率和视角影响，可在菜单中选择「均衡」或「流畅」。手机、触屏和手柄尚未完成实机验收。

## 游览操作

点击「入镇漫游」开始，或选择「先随镜头游览」。进入漫游时浏览器可能锁定鼠标，按 Esc 可退出锁定并暂停。

| 操作 | 按键 / 入口 |
| --- | --- |
| 行走 / 环顾 | W A S D / 鼠标 |
| 奔跑 / 跳跃 / 蹲下 | Shift / 空格 / C |
| 暂停与设置 | Esc / 右上角「游览菜单」 |
| 地图与地标传送 | M / 右下角「地图」 |
| 显示或隐藏人物 | N / 右下角「行人」；每次打开默认关闭 |
| 隐藏界面 | H |
| 光景与画质 | 菜单内切换暮色、清晨、夜景及三档画质 |
| 环境声音 | 右下角「声景」；菜单中调整音量 |

## 项目内容

| 路径 | 内容 |
| --- | --- |
| `云溪古镇_离线漫游.html` | 云溪古镇单文件，也是当前公网主页面 |
| `云溪古镇/` | 可编辑的 HTML、CSS、场景脚本、引擎及历史验收材料 |
| `清明上河图_完整漫游.html` | 清明上河图单文件 |
| `清明上河图/` | 对应源码、纹理资源、制作工具、版本留档及验收材料 |
| `cinematic-webgl-town/` | 可复用制作技能、参考说明、起始项目和打包脚本 |
| `技术拆解与制作说明.md` | 项目技术分析与制作说明 |
| `几猫国产3A大作_V1.html` | 原有参考文件 |
| `云溪古镇_项目与Skill.zip` | 原有项目与技能打包归档；不会随源码自动更新 |
| `index.html` / `.nojekyll` | Pages 首页入口 / 禁用 Jekyll 处理 |

云溪古镇包含约 640 × 640 米镇区、484 栋建筑、六座桥、地图地标，以及可切换的人群、光景和画质。它是原创风格化场景，不是实测古城重建；建筑以外观为主，人物为简化程序角色。

## 本地运行

下载 `云溪古镇_离线漫游.html` 后，可尝试直接用桌面浏览器打开。已记录的浏览器验收使用 HTTP，未将所有浏览器的 `file://` 双击运行视为已验证。

更稳定的本地方式：安装 Python 3，在仓库根目录运行：

```sh
python -m http.server 8000 --bind 127.0.0.1
```

随后访问 [本地首页](http://127.0.0.1:8000/)，或者 [可编辑版云溪古镇](http://127.0.0.1:8000/云溪古镇/)。Ctrl+C 停止服务。

## 修改与重新发布

1. 修改 `云溪古镇/` 下的 `town.js`、`realism.js`、`style.css` 或 `index.html`。
2. 在仓库根目录重新生成公网使用的单文件：

   ```sh
   python cinematic-webgl-town/scripts/build_standalone.py --project 云溪古镇 --output 云溪古镇_离线漫游.html
   ```

3. 本地打开页面，检查场景、菜单、地图及漫游操作。
4. 提交并推送到 `main` 分支：

   ```sh
   git add .
   git commit -m "Update Yunxi town"
   git push origin main
   ```

GitHub 仓库 **Settings → Pages** 使用 **Deploy from a branch → main → / (root)**。推送后 GitHub Pages 自动构建发布，通常需要几分钟；进度可在仓库 Actions 中查看。若只修改可编辑版而没有重新打包，公网主页面仍是旧的单文件内容。

发布方式参考 [GitHub Pages 官方文档](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)。

## 验收与范围

历史完整功能与画面记录见 [云溪古镇最新写实优化验收](云溪古镇/evidence/写实优化验收.md)，包含 30 项自检及截图。历史记录反映当时设备和版本，不代表所有浏览器、设备或网络环境均已通过测试。

本仓库保留原有参考文件和第三方资源的说明与标记；公开可见不等于对所有素材授予统一开源许可。复用引擎、参考文件或纹理时，请检查相应来源和许可。
