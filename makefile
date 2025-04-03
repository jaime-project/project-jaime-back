VERSION := 0.5.0

build b:
	docker build . -t ghcr.io/jaime-project/jaime-back:$(VERSION) --build-arg ARG_VERSION=$(VERSION)

push p:
	docker push ghcr.io/jaime-project/jaime-back:$(VERSION)

run r:
	docker run -it --rm -p 5000:5000 ghcr.io/jaime-project/jaime-back:$(VERSION)

compile c:
	python -m compile -b -f -o dist/ .

binary bin:
	rm -fr build dist *.spec
	pyinstaller --add-data logic:logic --onefile app.py -n jaime
	mv dist/jaime jaime
	rm -fr build dist *.spec
	
