from knowledge_base_app.document_pipeline import chunk_text, normalize_space


def test_normalize_space():
    text = "  hello   world\n\nnext  line  "
    result = normalize_space(text)
    assert "hello world" in result
    assert "next line" in result


def test_chunk_text_basic():
    text = "word " * 50
    chunks = chunk_text(text, chunk_size=100, overlap=20)
    assert len(chunks) >= 1
    assert all(len(chunk) <= 180 for chunk in chunks)
