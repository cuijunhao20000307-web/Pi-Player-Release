# Pi Player 安装说明

请将完整安装包解压到 SD 卡根目录。主要文件位置：

| 文件 | 用途 |
| --- | --- |
| `switch/piplayer/piplayer.nro` | Pi Player 主应用 |
| `switch/.overlays/piplayer-overlay.ovl` | Tesla 菜单里的 Piplayer 插件 |
| `atmosphere/contents/4200000000000000/` | 后台播放模块 |
| `switch/piplayer/music/` | 自己的本地音乐 |
| `licenses/` | 许可证和对应源码 |

安装后台模块后请重启 Switch。Tesla 插件需要主机已具备可用的 Tesla 菜单环境。

本地音乐支持 MP3、FLAC、WAV。同名 LRC 可以与歌曲放在一起。更新应用时保留已有音乐、收藏、歌词和缓存，无需删除这些数据。

当前主应用版本为 0.1.0；Tesla 菜单应显示 **Piplayer 0.1.0**。
