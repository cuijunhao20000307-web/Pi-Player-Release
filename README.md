# Pi Player

**Pi Player for Nintendo Switch — Official Release Repository**

Pi Player（圆周率音乐播放器）官方发布仓库，作者 **LINKO**。

当前版本：**0.1.0 正式版 · R1 启动波纹修正版**。Tesla 菜单名称：**Piplayer**。

## 下载

- [最新正式版](https://github.com/cuijunhao20000307-web/Pi-Player-Release/releases/latest)
- [完整 SD 安装包](https://github.com/cuijunhao20000307-web/Pi-Player-Release/releases/download/0.1.0/PiPlayer-0.1.0-R1-Full-SD.zip)：首次安装或使用 Tesla / 后台播放时，请下载这个包。
- [单独主应用 NRO](https://github.com/cuijunhao20000307-web/Pi-Player-Release/releases/download/0.1.0/PiPlayer-0.1.0.nro)：适用于已安装完整环境、只替换主应用的情况。
- [启动动画 GIF 预览](https://github.com/cuijunhao20000307-web/Pi-Player-Release/releases/download/0.1.0/PiPlayer-0.1.0-Ripple-Preview.gif)

![启动动画预览](assets/startup.gif)

## 安装

1. 下载完整 SD 安装包。
2. 将包内全部内容解压到 SD 卡根目录，按提示覆盖同名文件；保留自己的音乐、收藏和缓存。
3. 首次安装或更换后台模块后，重启 Switch。
4. 从 Homebrew Menu 打开 `/switch/piplayer/piplayer.nro`。
5. 已配置 Tesla 菜单的用户可在菜单中打开 **Piplayer**。

请勿只复制 NRO 后就期待 Tesla 或后台模块可用。详细目录说明见 [INSTALL.md](INSTALL.md)。

## 功能

- 中文界面、在线搜索、歌曲缓存、封面和歌词。
- 本地 MP3 / FLAC / WAV 音乐、本地 LRC、收藏与播放队列。
- Tesla 播放控制、音量和可拖动进度条，以及停止并退出。
- 程序绘制的 4 秒启动动画，包含两圈向外扩散的水滴波纹。

## 发布与版本索引

正式安装包通过本仓库的 **Releases** 发布。`version.json` 保存当前正式版本，`versions.json` 保存正式版历史。下载校验值见每个 Release 的 `SHA256SUMS.txt`。

本仓库用于发行与反馈；开发仓库独立管理。完整安装包内附相关许可证及对应源码。

Pi Player 是非官方 Homebrew 项目，与 Nintendo 无隶属关系。在线曲目可用性取决于音源站点和网络，请支持正版并使用有权访问的内容。
