test-pub:
	python3 -m unittest phemexboy/tests/public_tests.py

test-auth:
	python3 -m unittest phemexboy/tests/auth_tests.py

test-help:
	python3 -m unittest phemexboy/tests/helper_tests.py

test-order:
	python3 -m unittest phemexboy/tests/order_tests.py

test-position:
	python3 -m unittest phemexboy/tests/position_tests.py

test-proxy:
	python3 -m unittest phemexboy/tests/proxy_tests.py
