dev: prebuild
	hugo server --noHTTPCache

build: prebuild
	rm -rf public
	hugo

generate:
	git submodule update --init --recursive

submodules:
	git submodule update --recursive --remote

prebuild:
	scripts/prebuild.py content/sl
	scripts/prebuild.py content/wu