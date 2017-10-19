test:
	cd tests && rm -f *.log
	cd tests && python -m unittest test_commands
#	cd tests && python -m unittest test_structure

install:
	python setup.py install --user --record installed_files.txt

uninstall:
	cat installed_files.txt | xargs rm -rf
	rm -f installed_files.txt

init:
	pip install --user -r requirements.txt

clean:
	$(MAKE) -C docs clean
	rm -rf .cache build dist closeup.egg-info closeup.log
