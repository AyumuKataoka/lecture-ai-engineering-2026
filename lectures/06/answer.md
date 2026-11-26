# 第6回 解答

## 演習

<!-- [tool call] の行は、表示された行をそのまま貼り付けてください。終わらなかった STEP は、空欄のままでかまいません。 -->

- STEP 1 のツールの名前：glossary_search_glossary
- STEP 2 の [tool call]：glossary_search_glossary({'query': '3レベル'})
- STEP 3 の [tool call]：fetch_fetch({'url': 'https://modelcontextprotocol.io/'})
- STEP 4 の [tool call]：
  - aws_aws___search_documentation({'search_phrase': 'Amazon S3 バージョニング'})
  - aws_aws___search_documentation({'search_phrase': 'Using versioning in S3 buckets'})
- 気づき・疑問：

## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル：実装
- やったこと：
  - 第3回で作った `make_quiz` を、`app/mcp_server.py` で MCP のツールとして公開した（`server.tool()(tools.make_quiz)`）。`app/mcp_servers.json` は変えていない（サーバーの起動方法は同じで、ツールは接続時にサーバーへ問い合わせて見つかるため）
  - 範囲外の回では、用語がある回の一覧を含むメッセージを `return` で返す（第3回で実装済み）
  - 比較のため、一時的に同じメッセージを `raise ValueError` で出す版も試した
- 結果：「第99回のクイズを作って」を各4回実行（`homework/implementation/trace_return.txt`・`trace_raise.txt`）
  - `return` 版：`[tool return] glossary_make_quiz -> 第99回の用語は用語集にありません。用語がある回: 1, 2, 3, 4, 6`。モデルは3回とも「第1〜4回、第6回」を挙げて別の回を勧めた
  - `raise` 版：`[tool error] glossary_make_quiz -> Error executing tool make_quiz`。メッセージ本文はモデルに渡らず、回答は「第1回〜第N回など」とぼかした
  - どちらも4回中1回はツールを呼ばず、モデルが自分で「第99回はない」と答えた
- 気づき・疑問：
