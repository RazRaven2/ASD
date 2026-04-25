import pytest
from string_manip import *  # Import functions from string_manip.py

def test_capitalize_words_basic_operations():
    assert capitalize_words("hello world") == "Hello World"
    assert capitalize_words("python programming") == "Python Programming"

def test_capitalize_words_empty_string():
    assert capitalize_words("") == ""

def test_capitalize_words_with_list():
    with pytest.raises(TypeError):
        capitalize_words(['hello', 'world'])  

def test_capitalize_words_with_tuple():
    with pytest.raises(TypeError):
        capitalize_words(('hello', 'world'))  

def test_capitalize_words_with_object():
    with pytest.raises(TypeError):
        capitalize_words(object())  

def test_capitalize_words_with_none():
    with pytest.raises(TypeError):
        capitalize_words(None)  

def test_capitalize_words_with_bytearray():
    with pytest.raises(TypeError):
        capitalize_words(bytearray(b"hello world"))  


def test_remove_extra_spaces_collapses_internal_spaces():
    assert remove_extra_spaces("hello    world") == "hello world"


def test_remove_extra_spaces_removes_leading_and_trailing_spaces():
    assert remove_extra_spaces("   hello world   ") == "hello world"


def test_remove_extra_spaces_empty_string():
    assert remove_extra_spaces("") == ""


def test_remove_extra_spaces_with_list():
    with pytest.raises(TypeError):
        remove_extra_spaces(['hello', 'world'])


def test_remove_extra_spaces_with_tuple():
    with pytest.raises(TypeError):
        remove_extra_spaces(('hello', 'world'))


def test_remove_extra_spaces_with_object():
    with pytest.raises(TypeError):
        remove_extra_spaces(object())


def test_remove_extra_spaces_with_none():
    with pytest.raises(TypeError):
        remove_extra_spaces(None)


def test_remove_extra_spaces_with_bytearray():
    with pytest.raises(TypeError):
        remove_extra_spaces(bytearray(b"hello world"))


def test_reverse_words_reverses_sentence_word_order():
    assert reverse_words("hello world from python") == "python from world hello"


def test_reverse_words_single_word():
    assert reverse_words("hello") == "hello"


def test_reverse_words_empty_string():
    assert reverse_words("") == ""


def test_reverse_words_with_list():
    with pytest.raises(TypeError):
        reverse_words(['hello', 'world'])


def test_reverse_words_with_tuple():
    with pytest.raises(TypeError):
        reverse_words(('hello', 'world'))


def test_reverse_words_with_object():
    with pytest.raises(TypeError):
        reverse_words(object())


def test_reverse_words_with_none():
    with pytest.raises(TypeError):
        reverse_words(None)


def test_reverse_words_with_bytearray():
    with pytest.raises(TypeError):
        reverse_words(bytearray(b"hello world"))

