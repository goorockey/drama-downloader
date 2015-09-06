drama-downloader
=============

## Installation

    pip install -r requirements.txt


## Usage

- Copy config.ini.example to config.ini, and modify it

- Run `python drama_download.py` or `taskbar.exe` to execute in tray

## Config

    [baidupan]
    username=
    password=
    dest_dir=/Movies/Drama

    [drama]
    suits=http://kanmeiju.net/detail/1829.html,5

- `baidupan` section
  - username, password: username and password of your baidupan
  - dest_dir: destination directory to save drama in your baidupan
- Fill `drama` section in format: 'drama_name=drama_url;download_day'
  - drama_name: drama file will be saved in `dest_dir/drama_name`
  - drama_url: url used to find drama, which should be in supporteds sites list below.
  - download_day: download in specific day every week

## Supported sites

<<<<<<< HEAD
    optional arguments:
      -h, --help  show this help message and exit
      -d          Daemon mode.
      -c CONFIG   Config file. Default is config.ini
<<<<<<< HEAD
<<<<<<< HEAD
=======
=======
>>>>>>> 814b061... Save resource url in history
<<<<<<< HEAD
>>>>>>> e4bacc9d9a9ee680b2ee4f5dfdace2ef791ef9d9
=======
>>>>>>> 388a46e... Ask to enter captcha if failed to recognize
<<<<<<< HEAD
>>>>>>> c05a785... Ask to enter captcha if failed to recognize
=======
=======
      -l LOG      Log file. Default is history.log
>>>>>>> 9f35ada... Save resource url in history
<<<<<<< HEAD
>>>>>>> 814b061... Save resource url in history
=======
=======
- <http://cn163.net>
- <http://kanmeiju.net>
>>>>>>> 9df9d9b... Limit drama url in supported sites only
>>>>>>> 31522bd... Limit drama url in supported sites only
