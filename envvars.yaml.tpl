---
all:
  dynamic:
    TIMEZONE: cat /etc/timezone
    HUID: id -u
    HGID: id -g
  static:
    FQDN: 
    ALLPASS: &allpass 

databases:
  dynamic:
  static:
    MONGOROOTUSER: 
    MONGOROOTPASS: *allpass
    MYSQLROOTUSER: 
    MYSQLROOTPASS: *allpass
  tags:
    MONGOTAG: ""
    MONGOEXPRESSTAG: ""

file-sharing:
  dynamic:
  static:
  tags:
    FILEBROWSERTAG: ""
    FILEZILLATAG: ""

management:
  dynamic:
  static:
  tags:
    PORTAINERTAG: ""
    WATCHTOWERTAG: ""

networking:
  dynamic:
    WGPUBLICIP: curl -s ifconfig.me
  static:
    PIHOLEPASS: *allpass
    WIREGUARDPASS: *allpass
    WGPORT: ""
    WGPKA: ""
    WGDEFADD: ""
    WGAIPS: ""
    PIHOLENETIP: 172.20.1.53
    TRAEFIKNETIP: 172.20.1.80
    WGNETIP: 172.20.1.51
  tags:
    PIHOLETAG: ""
    TRAEFIKTAG: ""
