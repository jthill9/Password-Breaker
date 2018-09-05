test:
	@$(MAKE) -sk test-all

test-all:	test-scripts test-hulk

test-scripts:
	curl -sLO https://gitlab.com/nd-cse-20289-sp18/cse-20289-sp18-assignments/raw/master/homework05/test_hulk.sh
	curl -sLO https://gitlab.com/nd-cse-20289-sp18/cse-20289-sp18-assignments/raw/master/homework05/hashes.txt
	chmod +x test_hulk.sh

test-hulk:
	./test_hulk.sh
