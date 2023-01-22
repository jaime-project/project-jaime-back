VERSION := 1.10.0

build b:
	podman build . -t ghcr.io/jaime-project/jaime-back:$(VERSION)

push p:
	podman push ghcr.io/jaime-project/jaime-back:$(VERSION)

compile c:
	python -m compile -b -f -o dist/ .
	cp -rf variables.yaml dist/

package:
	rm -fr build dist *.spec
	pyinstaller --add-binary logic:logic -n jaime --onefile app.py 
	mv dist/jaime jaime
	rm -fr build dist *.spec
	
python py:
	uvicorn app:app --port 5000 --reload