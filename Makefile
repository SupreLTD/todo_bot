run:
	docker build -t do . && docker run -d --name do do


restart:
	docker rm -f do && docker rmi do && docker build -t do . && docker run -d --name do do

down:
	docker rm -f do && docker rmi do