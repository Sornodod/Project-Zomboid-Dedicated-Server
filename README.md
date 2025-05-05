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
При первом запуске сервера скрипт попросит нас ввести пароль от админа. Придумываем пароль.
![image](https://github.com/user-attachments/assets/850fe429-025d-4ffb-ad1f-0cbe4b5b8a11)


Пример того что сервер запустился:
![image](https://github.com/user-attachments/assets/007d7a70-29cb-49ee-9e03-ad07abc31ba5)

Далее идём в Project Zomboid, в вкладку "Сетевая". И заполяняем поля:
 * Имя сервера: любое. Абсолютно не имеет значения;
 * IP: ip нашего VPS сервера;
 * Локальный IP: не заполняем;
 * Порт: если мы его не меняли, то по дефолту будет 16261;
 * Пароль сервера: по дефолту его нет;
 * Описание: любое. Не имееет значения;
 * Имя: это имя нашего персонажа;
 * Пароль: это пароль от персонажа;
 * Использовать Steam Relay: галочку можно не ставить.

Нажимаем "Сохранить".
## Как войти из под админа?
Помните мы ранее пароль задавали от админа? \
Так вот, в поле "Имя" вводим "admin", в поле "Пароль" вводим ранее заданный в консоли пароль. Таким образом можем войти из под админа.
#Шаг №4. Автозапуск
Как только мы убедились что сервер запустился то можно его пустить в автозапуск путём создания службы.
```shell
sudo nano /etc/systemd/system/pzserver.service
```
Далее вписываем туда вот такое содержимое:
```ini
[Unit]
Description=Project Zomboid Server
After=network.target

[Service]
Type=simple
User=pzuser
WorkingDirectory=/home/pzuser/pzserver
ExecStart=/home/pzuser/pzserver/start-server.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
Перезапускаем systemd-демона:
```shell
sudo systemctl daemon-reload
```
Включаем в автозапуск всё это дело:
```shell
systemctl enable pzserver.service
```
Запускаем службу:
```shell
systemctl start pzserver.service
```
Логи можно посмотреть так в реальном времени:
```shell
journalctl -u pzserver.service -f
```
# Как ставить моды
На самом деле всё просто. \
Допустим мы хотим добавить мод на Автобус - Autotsar Tuning Atelier - Bus [TUNING 2.0] [  ](https://steamcommunity.com/sharedfiles/filedetails/?id=2592358528) \
Спускаемся в самый низ странички мода пока не увидим заветные строки:
* Workshop ID: 2592358528
* Mod ID: ATA_Bus

Запомнили эти IDшники и полезли менять конфиг сервера:
```shell
nano ~/Zomboid/Server/servertest.ini
```
Ищем строки `Mods=` и `WorkshopItems=` и добавляем туда ID скопированные выше. Должно получится так:
```ini
Mods=ATA_Bus
WorkshopItems=2592358528
```
Всё. Перезапускаем сервер и готово. Сервер сам скачает и установит моды. Перезапустить сервер можно так:
```shell
systemctl restart pzserver.service
```
# Бот для управления сервером Project Zomboid.
Предположим мы не хотим что бы в наше отсуствие шло время на сервере. А то вдруг, мы вернёмся в игру спустя неделю реального времени, а тут зима. \
Ну или мы хотим перезапустить сервер, а по SSH прыгать не очень хочется. \
В таком случае можно кинуть на сервер бота что приложен в данном репозитории. \
Только не забудьте поменять `API_TOKEN` и `ADMIN_CHAT_ID`.

