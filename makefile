install i:
	virtualenv -p python3.9 env
	. env/bin/activate
	pip install -r requirements.txt
	. env/bin/deactivate

build b:
	docker build . -t brianwolf94/jaime:1.0.0

compile c:
	python -m compile -b -f -o dist/ .
	rm -fr dist/repo_modules_default dist/env/
	cp -rf repo_modules_default dist/
	cp -rf variables.env dist/

package p:
	rm -fr build dist *.spec
	pyinstaller --add-binary logic:logic --onefile app.py
	mv dist/app app
	rm -fr build dist *.spec