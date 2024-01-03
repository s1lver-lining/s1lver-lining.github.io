dev: prebuild
	hugo server --noHTTPCache

build: prebuild
	rm -rf public
	hugo

submodules:
	git submodule update --recursive --remote

prebuild:
	scripts/prebuild.sh content/sl
	scripts/prebuild.sh content/wu