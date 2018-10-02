## 1 способ: запуск с Docker образа
```
docker build -t "alpha_zero_general" --build-arg CACHEBUST=$(date +%s) https://raw.githubusercontent.com/0x384c0/alpha-zero-general/master/Dockerfile
docker create -it -p 5000:5000 --name "alpha_zero_general_5000" "alpha_zero_general"
docker start -ai "alpha_zero_general_5000"
```
Открыть в браузере Chrome [http://0.0.0.0:5000](http://0.0.0.0:5000) и играть против ИИ.


## 2 способ: запуск на основной системе
требованя
* python 3
* pip
* более 8 gb оперативной памаяти

установка зависимостей
```
make setup
```

установка зависимостей c CUDA
```
make setup-gpu
# then set GPU_MODE to \"True\" in MakeFile
```

тренировка
```
make train
```

игра c RandomPlayer
```
make play
```

игра c HumanTKPlayer
```
make play_with_himan
```

запуск сервера на [http://0.0.0.0:5000](http://0.0.0.0:5000)
```
make start_server_rest
```