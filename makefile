VERSION := 1.7.1

install i:
	virtualenv -p python3.9 env
	. env/bin/activate
	pip install -r requirements.txt
	. env/bin/deactivate

build b:
	podman build . -t ghcr.io/jaime-project/jaime:$(VERSION)

push p:
	podman push ghcr.io/jaime-project/jaime:$(VERSION)

compile c:
	python -m compile -b -f -o dist/ .
	cp -rf variables.yaml dist/

package:
	rm -fr build dist *.spec
	pyinstaller --add-binary logic:logic -n jaime --onefile app.py 
	mv dist/jaime jaime
	rm -fr build dist *.spec
	
