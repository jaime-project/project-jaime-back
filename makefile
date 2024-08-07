VERSION := 0.4.0

install i:
	virtualenv -p python3.11 env
	. env/bin/activate
	pip install -r requirements.txt
	. env/bin/deactivate

build b:
	docker build . -t ghcr.io/jaime-project/jaime-back:$(VERSION)

push p:
	docker push ghcr.io/jaime-project/jaime-back:$(VERSION)

run r:
	docker run -it --rm -p 5000:5000 ghcr.io/jaime-project/jaime-back:$(VERSION)

compile c:
	python -m compile -b -f -o dist/ .
	# cp -rf variables.yaml dist/

package:
	rm -fr build dist *.spec
	pyinstaller --add-data logic:logic -n jaime --onefile app.py 
	mv dist/jaime jaime
	rm -fr build dist *.spec
	
sonar:
	docker run -it --rm -v $(shell pwd):/usr/src sonarsource/sonar-scanner-cli sonar-scanner
