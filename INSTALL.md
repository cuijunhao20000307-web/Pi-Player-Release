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

## 0.1.1 搜索与批量收藏

搜索结果向下浏览可自动加载下一页；也可点击右上角“加载更多”或按左摇杆。

点击“批量收藏”或按右摇杆进入多选：A 勾选、X 全选当前已加载歌曲、Y 保存、B 返回；支持触摸。重复收藏自动跳过。Tesla 在线搜索页也可继续加载并批量收藏已加载结果。

收藏实时写入 `switch/piplayer/favorites.tsv`，上一份完整记录保存在同目录 `.bak` 文件中。请保留这些文件；已经没有保存成功且没有备份的历史收藏不能自动找回。
