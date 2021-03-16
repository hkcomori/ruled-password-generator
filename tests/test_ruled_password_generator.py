# -*-coding: utf-8 -*-

import string

from ruled_password_generator import PasswordGenerator


def test_generate():
    default_all_letters = ''.join([
        string.ascii_lowercase,
        string.ascii_uppercase,
        string.digits,
        string.punctuation,
    ])
    for i in range(4, 128):
        for j in range(i+1, 128):
            # Test for length (one parameter)
            pwg = PasswordGenerator(i)
            password = pwg.generate()
            assert len(password) == i

            # Test for default rules
            assert any(c in string.ascii_lowercase for c in password)
            assert any(c in string.ascii_uppercase for c in password)
            assert any(c in string.digits for c in password)
            assert any(c in string.punctuation for c in password)
            assert all(c in default_all_letters for c in password)

            # Test for length (two parameter)
            pwg = PasswordGenerator(i, j)
            password = pwg.generate()
            assert i <= len(password) <= j

    # Test for password randomness
    pwg = PasswordGenerator(4, 128)
    passwords = {pwg.generate() for i in range(1024)}
    assert len(passwords) > 1
    password_lengths = {len(p) for p in passwords}
    assert len(password_lengths) > 1

    # Test for letters uniqueness
    for i in range(4, 32):
        pwg = PasswordGenerator(i, uniques=-1)
        password = pwg.generate()
        chars = set(password)
        assert len(chars) == i

    for i in [4, 10, 16, 32, 64, 128]:
        for j in range(min(32, i)):
            pwg = PasswordGenerator(i, uniques=j)
            password = pwg.generate()
            chars = set(password)
            assert len(chars) >= j


def test_bulk_generate():
    pwg = PasswordGenerator(10)
    for i in [1, 128, 256, 512, 1024]:
        passwords = pwg.bulk_generate(i)
        assert len(passwords) == i

        passwords = pwg.bulk_generate(i, unique=True)
        assert len(passwords) == i
        assert len(set(passwords)) == i
