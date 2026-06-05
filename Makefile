# Local working copies of the content repositories, mounted live in development
# (see config/development/module.yaml). Override if your clones live elsewhere,
# e.g. `make dev SL_DEV=/path/to/Starlight`.
SL_DEV ?= ../Starlight
WU_DEV ?= ../ctf-writeups

# Live development: generate + watch content from the sibling working repos above
# and serve with `hugo server`. The "development" environment mounts those repos
# over the submodules, so edits there are reflected immediately. The generated
# files (_index.md, *-ext.md) are gitignored inside those repos.
dev:
	scripts/prebuild.py $(SL_DEV)
	scripts/prebuild.py $(WU_DEV)
	scripts/prebuild.py --watch $(SL_DEV) &
	scripts/prebuild.py --watch $(WU_DEV) &
	npx postcss --watch --config postcss.config.js assets/css/styles.css -o assets/css/compiled/main.css &
	hugo server --noHTTPCache

build: prebuild
	rm -rf public
	hugo

build-css:
	npx postcss --config postcss.config.js assets/css/styles.css -o assets/css/compiled/main.css

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