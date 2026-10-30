# 定稿后日文翻译

仅在 G3 后且用户要求日文时加载，路径以 `<skill>` 根目录为基准；独立审核的输入与复审规则见 [独立审核协议](review-protocol.md)。

### 定稿后日文翻译（可选）

仅在 G3 批准定稿后、且用户要求翻译成日文时执行；未要求时不翻译，也不预建文件。翻译不是第十阶段，不改变九阶段与三个决策点。

1. **确认来源版本**：以 G3 批准的 article.md 版本为唯一来源，在 working.md 记录版本。定稿尚未批准时，先说明需要 G3，不翻译未定稿内容。
2. **翻译**：译成自然的日文，保存为 `article.ja.draft.md`。事实、数字、单位、条件、限定、否定、案例结果及人称立场与中文定稿一致；不增删主张。专有名词、产品名、Skill 名、命令和路径保持原样。默认使用である常体；文章明显面向读者说明时可用です・ます体，全文统一。标题、图说和 alt 文字一起翻译。
3. **yomiyasu 润色**：读取 `<skill>/vendor/yomiyasu/SKILL.md` 的当前版本，以及其中引用的 `references/gemini-syntax.md`、`references/slop-catalog.md` 和对应领域文件（`references/domains/tech.md`／`business.md`／`essay.md`）。按其 Step 1–4 判断领域，修正不自然的比喩、主述关系、过度装饰和单调文末，保存为 `article.ja.md`。
4. **yomiyasu 检查**：对 `article.ja.md` 运行 `python3 -I <skill>/vendor/yomiyasu/scripts/yomiyasu_lint.py article.ja.md`；再运行 `python3 -I <skill>/vendor/yomiyasu/scripts/yomiyasu_diff.py article.ja.draft.md article.ja.md --stance=<勧め|決まり|説明>`，无法判断立场时省略 `--stance`。逐条判断候选，按 yomiyasu 规则只修正一次，不为消除警告反复改写。
5. **对照中文定稿**：yomiyasu 只比较日文前后差异，看不到中文原文。润色后逐段对照 article.md，确认没有漏译、错译、新增或删除事实，数字与条件一致。
6. **配图文字**：图片内文字默认保持原语言，不自动重做。用户要求日文配图时，用 article-figures 以 `article.ja.md` 为依据另行渲染到 `visuals/ja/`，并附日文校对清单。
7. **记录与交付**：在 working.md 记录来源版本、领域判断、lint 分数、diff 中采纳和未采纳的候选、对照中发现的问题。交付 `article.ja.md`，并说明 yomiyasu 主要修改和需要作者确认的日文表达。

翻译中发现中文定稿本身有事实或逻辑问题时，不在日文版单独修正；先报告，按审核边界退回对应阶段，修订后重新 G3，再翻译。只调整日文措辞时，不需要重新 G3。yomiyasu 不存在或脚本无法运行时明确报告；仍可按其 SKILL.md 规则人工检查，但不得写成已完成脚本检查。

