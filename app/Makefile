all:
	rm -rf .build/
	mkdir -p .build/
ifeq (${dev},1)
	cp Dockerfile Pipfile Pipfile.lock .build/
	tar zcf .build/build.tar --exclude build.tar  --exclude .build --exclude node_modules .
	cd .build/ && docker build . -t skep/app:dev
else
	git show HEAD:app/Dockerfile > .build/Dockerfile
	git show HEAD:app/Pipfile > .build/Pipfile
	git show HEAD:app/Pipfile.lock > .build/Pipfile.lock
	git archive --format tar -o .build/build.tar HEAD
	cd .build/ && docker build . -t skep/app
endif
