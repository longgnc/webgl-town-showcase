# 云溪古镇与清明上河图 · WebGL 三维漫游

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


## 清明上河图新版

[公网体验：清明上河图完整漫游](https://longgnc.github.io/webgl-town-showcase/清明上河图_完整漫游.html) · [项目说明](清明上河图/README.md) · [画质与验收记录](清明上河图/画质优化与验收说明.md)

当前完整漫游文件已更新为写实优化版，内嵌纹理，约 43 MB，首次加载请稍候。支持鸟瞰（B）、自由漫游、地图（M）、人物开关（N）和隐藏界面（H）。人物默认关闭。旧版保存在 `清明上河图/versions/初版留档/`。

重新打包清明上河图并更新公网文件：

```sh
python cinematic-webgl-town/scripts/build_standalone.py --project 清明上河图 --output 清明上河图_完整漫游.html
```

## 参考项目、感谢与声明

本项目参照用户提供的 `几猫国产3A大作_V1.html` 开发，并实际提取、复用和适配了其中的 Three.js、输入、天空、材质、阴影及后处理相关代码；并非全部底层技术从零独立编写。在此基础上另行制作了云溪古镇和清明上河图的场景、建筑布局、漫游交互及相关展示功能。

**向《Saltline》的创作者 Felix Rieseberg 以及相关技术贡献者致谢。** 感谢其展示单文件浏览器三维场景、程序化内容与实时光影的可能性；同时感谢 Three.js 社区、Poly Haven 和故宫博物院提供的技术与文化资料。

溯源截至 2026-11-12：本地参考 HTML 中保留 `SALTLINE_SKY`、`SALTLINE_SHADOW`、`SALTLINE_POST` 标识。公开报道将其上游指向 Felix Rieseberg 发布的《Saltline》。中文改名/传播版本的具体制作者未确认，不能把文件名“几猫”或某个转载仓库的维护者直接当作上游原作者。原发布帖及 Artifact 在本次自动读取中不可访问，因此这里明确保留溯源证据的限制，不宣称完成逐字源码对比或取得作者授权。

- [Felix Rieseberg 个人网站](https://felixrieseberg.com/)
- [《Saltline》原发布帖线索](https://x.com/felixrieseberg/status/2119925633564463609)
- [《Saltline》原始试玩线索](https://claude.ai/artifact/BGY1SztrAYcJQHSsnHHGmp)
- [公开溯源报道（含上述原始链接）](https://aitest123.com/news/tng5cf)
- [中文传播版本仓库（仅作传播线索，不认定其为原作者）](https://github.com/odin1024/jimao)

本仓库为参照开发的学习、研究与展示项目，与上游作者及其所属机构不存在官方合作、背书或隶属关系。原项目名称、第三方代码、图像和纹理的权利归各自权利人所有；致谢不替代许可，不将未核实授权的第三方内容重新声明为本仓库原创或统一开源许可。“国产3A大作”仅保留为所收参考文件的原文件名，不作为本项目的质量或原创性宣传。若权利人提出署名或使用范围问题，将据实核查并调整。
