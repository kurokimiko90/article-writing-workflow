# article-writing-workflow

把草稿、笔记、经验或访谈材料，按九阶段整理成可信、易懂、有故事主线的文章，再依完成的文章制作配图或 PPT，并保存可重用的知识。人类保留三次决定：方向（G1）、知识基准（G2）、定稿（G3）。

本仓库是工作流的正本。使用方项目通过 `install.sh` 建立 symlink 引用，不各自复制。

## 目录

| 路径 | 内容 |
|---|---|
| `skills/article-writing-workflow/SKILL.md` | 九阶段主流程、人类决策点、审核与交付规则 |
| `skills/article-writing-workflow/references/` | 默认值（defaults）、执行方法（methods）、工作模板（templates） |
| `skills/article-writing-workflow/agents/figure-reviewer.md` | 独立审图 Agent：直接读 PNG，以设计大赛得奖水准审核，只审不改 |
| `skills/article-writing-workflow/scripts/md2html.py` | article.md → 带目录的单文件 article.html，并列出过长的无图段落 |
| `skills/article-writing-workflow/scripts/warm-paper/` | warm-paper 出图脚本（`warm-paper-build.py`）、机械检查 `figure-lint.py`、profile 正本、lucide 图标 |
| `agents/claude/article-knowledge-editor.md` | Claude Code 专用执行 Agent |
| `agents/codex/article-knowledge-editor.toml` | Codex 入口：读取 Claude 版定义执行，规则只维护一份 |
| `skills/article-writing-workflow/vendor/` | 第三方 Skill 副本（diagram-design、yomiyasu）及来源记录 `SOURCES.md` |
| `skills/article-figures/` | 封面与叙事图 Skill（自有） |
| `scripts/sync-vendor.sh` | 从上游重新复制 vendor |
| `docs/index.html`、`docs/plan.pdf` | 工作流设计文档（繁体中文，v2.6，2026-10-26；旧版在 `docs/archive/`） |

## 安装到其他项目

```bash
./install.sh <对象项目路径>
```

会建立以下 symlink（已有实体文件时跳过，不覆盖）：

- `.claude/skills/article-writing-workflow`、`.claude/skills/article-figures`、`.claude/agents/article-knowledge-editor.md`、`.claude/agents/article-figure-reviewer.md`
- `.agents/skills/article-writing-workflow`、`.codex/agents/article-knowledge-editor.toml`
- `~/.diagram-design/profiles/warm-paper*`（全项目共用）

## 用到的其他 Skill（全部在本项目内）

| Skill | 位置 | 用途 | 说明 |
|---|---|---|---|
| article-figures | `skills/article-figures/` | 封面与叙事图 | 自有 Skill |
| diagram-design | `skills/article-writing-workflow/vendor/diagram-design/` | 知识图解、说明型配图 | 第三方副本，勿直接修改 |
| yomiyasu | `skills/article-writing-workflow/vendor/yomiyasu/` | 定稿后日文润色与 lint／diff | 第三方副本，勿直接修改 |

第三方副本的来源与版本记在 `vendor/SOURCES.md`；上游更新后运行 `./scripts/sync-vendor.sh`（默认从 GitHub 拉取）重新复制。

运行环境只需要 Python 3、Google Chrome（headless 截图）与 git（同步 vendor 时）。

Skill 内的路径以 `<skill>`（Skill 目录）为基准，不依赖安装位置。

## 吉祥物 Miko

`skills/article-figures/templates/warm-paper/assets/miko/` 下的 4 张贴图（`cover`、`look`、`ok`、`cheer`）是作者用 AI 生成的原创角色图，只用于 article-figures 的封面与叙事图（右下或右上角点缀，不一定每张都放）；结构图解（diagram-design）不使用。随本仓库的授权一起发布。

## 产出位置

文章产出不在本仓库内，默认写到使用方项目的 `exports/articles/<文章短名>/`。
