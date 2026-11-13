"""講座全体で共通の設定。

APIキーやモデル名はコードに書かず、環境変数から読み込む。
"""

import os

# 既定モデル。環境変数 AIE_MODEL を設定すると切り替えられる。
#   例: export AIE_MODEL=gemini-3.5-flash
DEFAULT_MODEL = "gemini-3.5-flash-lite"
MODEL = os.getenv("AIE_MODEL", DEFAULT_MODEL)


def api_error_message(status: int, detail: str = "") -> str:
    """HTTPステータスコードを、受講生向けの日本語の説明にする（ask.py と agent.py で共用）。"""
    if status == 429:
        return "レート制限に達しました。1分ほど待ってから再実行してください。"
    if status == 503:
        return "モデルが混み合っています（503）。少し待ってから再実行してください。"
    if status in (400, 401, 403, 404):
        return f"APIキーかモデル名に問題があります（{status}）: {detail}"
    return f"APIエラー（{status}）: {detail}"


def get_api_key() -> str:
    """環境変数 GEMINI_API_KEY を返す。未設定なら手順を表示して終了する。"""
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise SystemExit(
            "環境変数 GEMINI_API_KEY が見つかりません。\n"
            "1. GitHub の Settings → Codespaces → Secrets に GEMINI_API_KEY を登録し、\n"
            "   使う repository に自分の fork を選んでください。\n"
            "2. Codespaces を起動したあとに登録した場合は、Codespaces を再起動してください。\n"
            "   （左下の「Codespaces」→「Stop Current Codespace」→ 再度開く）"
        )
    return key


def get_google_provider():
    """Gemini を呼ぶプロバイダを返す（agent.py と judge.py で共用）。

    既定は Gemini API（GEMINI_API_KEY）。環境変数 AIE_PROVIDER=vertex のときだけ Vertex AI を使う。
    Vertex AI のときは Application Default Credentials（gcloud auth application-default login）で認証し、
    プロジェクトは AIE_GCP_PROJECT、リージョンは AIE_GCP_LOCATION（既定 global）で渡す。
    プロジェクト ID はコードに書かない（公開リポジトリに出さないため）。
    GOOGLE_CLOUD_PROJECT / GOOGLE_CLOUD_LOCATION は読まない（ほかのツール用に別の値が入っていることがあるため）。
    """
    if os.getenv("AIE_PROVIDER", "").lower() == "vertex":
        from pydantic_ai.providers.google_cloud import GoogleCloudProvider

        project = os.getenv("AIE_GCP_PROJECT")
        if not project:
            raise SystemExit("AIE_PROVIDER=vertex のときは、環境変数 AIE_GCP_PROJECT に GCP のプロジェクト ID を設定してください")
        # project と location を明示して渡す（渡さないと GEMINI_API_KEY が拾われ、Vertex AI に向かないため）
        return GoogleCloudProvider(project=project, location=os.getenv("AIE_GCP_LOCATION", "global"))

    from pydantic_ai.providers.google import GoogleProvider

    return GoogleProvider(api_key=get_api_key())
