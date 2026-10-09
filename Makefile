.PHONY: test build deploy check-update snapshot-update extract-references clean

test:
	python3 -m unittest discover -s tests -v
	node --test tests/test_spanish_translation.cjs

build: test
	./tools/build.sh

deploy: build
	python3 tools/deploy.py

check-update:
	python3 tools/compatibility.py check

snapshot-update:
	python3 tools/compatibility.py snapshot

extract-references:
	python3 tools/extract_references.py

clean:
	python3 tools/clean.py

