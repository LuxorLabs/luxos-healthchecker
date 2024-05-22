import pytest

from luxos import ips


def test_splitip():
    assert ips.splitip("123.1.2.3") == ("123.1.2.3", None)
    assert ips.splitip("123.1.2.3:123") == ("123.1.2.3", 123)
    pytest.raises(RuntimeError, ips.splitip, "123.1.2222.3:123")


def test_iter_ip_ranges():
    assert set(ips.iter_ip_ranges("127.0.0.1")) == {("127.0.0.1", None)}
    assert set(ips.iter_ip_ranges("127.0.0.1:8080")) == {("127.0.0.1", 8080)}

    assert set(ips.iter_ip_ranges("127.0.0.1-127.0.0.3")) == {
        ("127.0.0.1", None),
        ("127.0.0.2", None),
        ("127.0.0.3", None),
    }

    assert set(ips.iter_ip_ranges("127.0.0.1:8080-127.0.0.3")) == {
        ("127.0.0.1", 8080),
        ("127.0.0.2", 8080),
        ("127.0.0.3", 8080),
    }

    assert set(ips.iter_ip_ranges("127.0.0.1-127.0.0.3:9090")) == {
        ("127.0.0.1", 9090),
        ("127.0.0.2", 9090),
        ("127.0.0.3", 9090),
    }

    pytest.raises(
        RuntimeError, set, ips.iter_ip_ranges("127.0.0.1:8080-127.0.0.3:9090")
    )

    assert set(ips.iter_ip_ranges("127.0.0.1:1234 - 127.0.0.3, 127.0.0.15:999")) == {
        ("127.0.0.1", 1234),
        ("127.0.0.2", 1234),
        ("127.0.0.3", 1234),
        ("127.0.0.15", 999),
    }
