drama-downloader
=============

Download drama everyday


## Usage

- Copy config.ini.example to config.ini, and modify it

- Run `drama_download.exe` or `taskbar.exe` to execute in tray

## Config

    [baidupan]
    username=
    password=
    dest_dir=/Movies/Drama

    [drama]
    suits=http://kanmeiju.net/detail/1829.html

- `baidupan` section
  - username, password: username and password of your baidupan
  - dest_dir: destination directory to save drama in your baidupan

- Each line of `drama` section is one drama task with format `drama_name=drama_url`
  - `drama_name`: drama file will be saved in `dest_dir/drama_name`
  - `drama_url`: url used to find drama, which should be in supporteds sites list below
  - disable task with beginning of ';'

## Supported sites

- <http://cn163.net>
- <http://kanmeiju.net>
