install i:
	virtualenv -p python3.9 env
	. env/bin/activate
	pip install -r requirements.txt
	. env/bin/deactivate

build b:
	docker build . -t brianwolf94/jaime:1.1.1

compile c:
	python -m compile -b -f -o dist/ .
	cp -rf variables.yaml dist/

package p:
	rm -fr build dist *.spec
	pyinstaller --add-binary logic:logic -n jaime --onefile app.py 
	mv dist/jaime jaime
	rm -fr build dist *.spec
	
