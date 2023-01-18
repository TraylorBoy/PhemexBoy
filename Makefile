test-pub:
	python3 -m unittest -f -v phemexboy/tests/public_tests.py

test-auth:
	python3 -m unittest -f -v phemexboy/tests/auth_tests.py

test-proxy:
	python3 -m unittest -f -v phemexboy/tests/proxy_tests.py

test-proxy-auth:
	python3 -m unittest -f -v phemexboy.tests.proxy_tests.TestProxy.test_auth

test-proxy-public:
	python3 -m unittest -f -v phemexboy.tests.proxy_tests.TestProxy.test_public

test-order-and-position:
	python3 -m unittest -f -v phemexboy.tests.proxy_tests.TestProxy.test_order_and_position

test-spot-trade:
	python3 -m unittest -f -v phemexboy.tests.spot_tests.TestSpot.test_trade

test-spot:
	python3 -m unittest -f -v phemexboy.tests.spot_tests.TestSpot.test_spot

test-future:
	python3 -m unittest -f -v phemexboy.tests.future_tests.TestFuture.test_future

test-future-trade:
	python3 -m unittest -f -v phemexboy.tests.future_tests.TestFuture.test_trade

test-order-edit-update:
	python3 -m unittest -f -v phemexboy.tests.proxy_tests.TestProxy.test_order_edit_update
