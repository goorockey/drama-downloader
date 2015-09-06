# coding: utf8

_CONF_FILE = 'config.ini'
_LOG_FILE = 'history.log'
_CODE_FILE = 'code.jpg'

_SUPPORT_SITES = {
    'http://cn163.net': "//div[@id='entry']//strong[2]/preceding-sibling::a[1]/@href",
    'http://kanmeiju.net': "//div[@class='vpl'][1]//a[contains(@href, 'ed2k://')][last()]/@href",
}
