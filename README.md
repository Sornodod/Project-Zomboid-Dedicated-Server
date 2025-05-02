# В ПРОЦЕССЕ НАПИСАНИЯ

# Мануал по поднятию выделенного сервера.

## Шаг №1. VPS
Нам нужен VPS сервер с Debian на борту. \
Системные требования сервера:
* 6GB RAM
* 2 CPU
* 40 GB SSD

## Шаг №2. Настройка сервера
Речь сейчас пойдёт не про настройку Project Zomboid. А про настройку самого VPS. \
\
## Обновление системы:
```shell
sudo apt-get update && apt-get upgrade
```
## Создание swap раздела.
Создание файла размером 2 ГБ:
```shell
sudo fallocate -l 2G /swapfile
```
Установка прав доступа (только root)
```shell
sudo chmod 600 /swapfile
```
Форматирование файла как swap-раздел
```shell
sudo mkswap /swapfile
```
Активация swap-файла
```shell
sudo swapon /swapfile
```
Добавление в `/etc/fstab`
Устаналвиваем текстовый рекдактор `nano`
```shell
apt install nano
```
Открываем через `nano` fstab
```shell
sudo nano /etc/fstab
```
Добавляем в конце строку
```txt
/swapfile none swap sw 0 0
```
Готово. SWAP раздел готов.

## Шаг №3. Установка STEAMCDM
```shell
dpkg --add-architecture i386
```
```shell
sudo apt install screen libsdl2-2.0-0:i386
```
```shell
sudo apt-get update && apt-get upgrade
```
```shell
sudo adduser pzuser
```
Задаём пароль для пользователя pzuser
И даём ему возможность пользоваться sudo:
```shell
usermod -aG sudo pzuser
```
Переходим в учётку pzuser:
```shell
su - pzuser
```
Создаём раздел для сервера PZ:
```shell
mkdir steamcmd pzserver
```
И переходим в него:
```shell
cd steamcmd
```
И вот теперь устанавливаем SteamCMD:
```shell
wget [https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz](https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz)
```
```shell
tar -xvzf steamcmd_linux.tar.gz
```
```shell
./steamcmd.sh
```
```shell
force_install_dir /home/pzuser/pzserver/
```
```shell
login anonymous
```
```shell
app_update 380870 validate
```
```shell
exit
```
## Шаг №3. Проверка запуска
```shell
cd
```
```shell
cd pzserver
```
```shell
./start-server.sh
```


