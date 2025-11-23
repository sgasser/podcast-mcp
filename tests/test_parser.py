import pytest
from podcast_mcp.parser.script_parser import parse_script

def test_parse_simple_dialogue():
    script = """
    <voice1>Hello, this is voice one.
    <voice2>And this is voice two.
    """
    
    result = parse_script(script)
    
    assert result["language"] == "en"
    assert len(result["dialogue"]) == 2
    assert result["dialogue"][0]["speaker"] == "1"
    assert result["dialogue"][0]["text"] == "Hello, this is voice one."
    assert result["dialogue"][1]["speaker"] == "2"
    assert result["dialogue"][1]["text"] == "And this is voice two."

def test_parse_with_language():
    script = """
    language: de
    
    <voice1>Hallo
    <voice2>Guten Tag
    """
    
    result = parse_script(script)
    
    assert result["language"] == "de"
    assert len(result["dialogue"]) == 2

def test_parse_empty_script():
    script = "No voice tags here"
    
    with pytest.raises(ValueError, match="No dialogue found"):
        parse_script(script)

def test_parse_multiline_dialogue():
    script = """
    <voice1>This is a longer
    piece of dialogue that
    spans multiple lines.
    <voice2>And this is another one.
    """
    
    result = parse_script(script)
    
    assert len(result["dialogue"]) == 2
    assert "multiple lines" in result["dialogue"][0]["text"]

def test_parse_with_closing_tags():
    """Test that closing tags are properly stripped and don't cause TTS gibberish"""
    script = """
    <voice1>Hello, welcome to our show!</voice1>
    <voice2>Thanks for having me here.</voice2>
    <voice1>Let's get started.</voice1>
    """
    
    result = parse_script(script)
    
    assert len(result["dialogue"]) == 3
    assert result["dialogue"][0]["text"] == "Hello, welcome to our show!"
    assert result["dialogue"][1]["text"] == "Thanks for having me here."
    assert result["dialogue"][2]["text"] == "Let's get started."
    # Ensure no closing tags in the text
    for segment in result["dialogue"]:
        assert "</voice" not in segment["text"]

