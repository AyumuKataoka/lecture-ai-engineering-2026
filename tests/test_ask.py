from types import SimpleNamespace

import app.ask as ask_module


def test_ask_returns_text_and_token_counts(monkeypatch):
    response = SimpleNamespace(
        text="回答",
        usage_metadata=SimpleNamespace(prompt_token_count=12, candidates_token_count=7),
    )
    client = SimpleNamespace(models=SimpleNamespace(generate_content=lambda **_: response))
    monkeypatch.setattr(ask_module.genai, "Client", lambda **_: client)
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")

    assert ask_module.ask("質問") == ("回答", 12, 7)


def test_main_displays_input_and_output_token_counts(monkeypatch, capsys):
    monkeypatch.setattr(ask_module, "ask", lambda _: ("回答", 12, 7))
    monkeypatch.setattr("sys.argv", ["app.ask", "質問"])

    ask_module.main()

    output = capsys.readouterr().out
    assert "入力: 12" in output
    assert "出力: 7" in output