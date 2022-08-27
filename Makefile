run:
	echo "Iniciando banco"
	sudo docker-compose up -d postgres_economizei
	
	sleep 4
	echo "Iniciando app"
	sudo docker-compose up -d app
	echo "aplicando migracoes"
	sudo docker-compose exec app alembic upgrade head