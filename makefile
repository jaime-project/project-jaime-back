install i:
	virtualenv -p python3.9 env
	. env/bin/activate
	pip install -r requirements.txt
	. env/bin/deactivate

build b:
	docker build . -t brianwolf94/jaime:0.12.0

compile c:
	python -m compile -b -f -o dist/ .
	rm -fr dist/repo_modules_default dist/env/
	cp -rf repo_modules_default dist/
	cp -rf variables.env dist/