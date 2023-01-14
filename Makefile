test-pub:
	python3 -m unittest -f -v phemexboy/tests/public_tests.py

test-auth:
	python3 -m unittest -f -v phemexboy/tests/auth_tests.py

test-proxy:
	python3 -m unittest -f -v phemexboy/tests/proxy_tests.py

test-trade:
	python3 -m unittest -f -v phemexboy.tests.order_tests.TestOrderClient.test_trade

test-order:
	python3 -m unittest -f -v phemexboy.tests.order_tests.TestOrderClient.test_order

test-position:
	python3 -m unittest -f -v phemexboy.tests.position_tests.TestPositionClient.test_position

test-swap:
	python3 -m unittest -f -v phemexboy.tests.position_tests.TestPositionClient.test_swap
