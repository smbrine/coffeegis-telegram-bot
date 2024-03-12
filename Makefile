build-grpc:
	 python -m grpc_tools.protoc -I=./ --python_out=./ --grpc_python_out=./  ./proto/main_service.proto

run:
	python -m app.main

black:
	black -l50 .

watchdog:
	find . ! -path './.git/*' ! -path './.idea/*' | entr -r python -m bot.main
