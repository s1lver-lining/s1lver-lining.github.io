dev: prebuild
	scripts/prebuild.py --watch content/sl &
	scripts/prebuild.py --watch content/wu &
	npx postcss --watch  --config postcss.config.js --env production themes/hextra/assets/css/styles.css -o assets/css/compiled/main.css &
	hugo server --noHTTPCache

build: prebuild
	rm -rf public
	hugo

build-css:
	npx postcss --config postcss.config.js --env production themes/hextra/assets/css/styles.css -o assets/css/compiled/main.css

dependencies:
	pip install nbconvert
	npm install
	
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