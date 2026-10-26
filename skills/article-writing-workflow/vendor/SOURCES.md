# vendor 来源

本目录是第三方 Skill 的副本，让本项目可以独立使用。不要在这里直接修改；上游更新后在仓库根目录运行 `scripts/sync-vendor.sh`（默认从 GitHub 拉取） 重新复制，并更新下表。

| 目录 | 上游位置 | 复制内容 | 版本 | 复制日期 | 授权 |
|---|---|---|---|---|---|
| `diagram-design/` | https://github.com/cathrynlavery/diagram-design 的 `skills/diagram-design/` | 整个 skill 目录（SKILL.md、references、assets、scripts） | 取自本地副本，未记录 commit（下次同步时补上） | 2026-10-22 | 见 `diagram-design/LICENSE` |
| `yomiyasu/` | https://github.com/nanaism/yomiyasu | `SKILL.md`、`references/`、`scripts/`、`LICENSE` | git `8f77b7a`（2026-10-07） | 2026-10-22 | 见 `yomiyasu/LICENSE` |

`article-figures` 是自有 Skill，不在 vendor：正本在本仓库 `skills/article-figures/`。
