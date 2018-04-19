[[ -d incubator-airflow ]] && rm -rf incubator-airflow
cp -r ../../git/incubator-airflow .
docker build -t af-dev .
