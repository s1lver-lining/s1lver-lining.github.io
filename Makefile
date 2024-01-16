dev: prebuild
	hugo server --noHTTPCache

build: prebuild
	rm -rf public
	hugo

dependencies:
	pip install nbconvert
	
generate:
	git submodule update --init --recursive

update-content:
	git submodule update --remote content/sl
	git submodule update --remote content/wu

submodules:
	git submodule update --recursive --remote

prebuild: update-content
	scripts/prebuild.py content/sl
	scripts/prebuild.py content/wu