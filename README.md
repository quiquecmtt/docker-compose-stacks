# Docker Compose Stacks
This repo tries make it easy to deploy multiple stacks in simple steps.

## Full deploy instructions
1. Configure environment variables to generate `.env` files.
```console
$ mv pyconfig.d/envvars.yaml.tpl pyconfig.d/envvars.yaml
$ vim pyconfig.d/envvars.yaml
$ vim pyconfig.d/pyconfig.yaml
```
2. Run Python script `create_env_files.py`.
```console
$ python3 create_env_files.py
```
3. Run Shell script to deploy stacks using `docker-compose`.
```console
$ sh dc-up-all.sh
```
4. If you want to remove all the deployment (except volumes).
```console
$ sh dc-down-all.sh
```

## Host ports
1. 53 -> pihole-dns
1. 67 -> pihole-dhcp
1. 80 -> traefik-reverse-proxy
1. 3000 -> filezilla
1. 8043 -> filebrowser-gui-secure
1. 8080 -> traefik-gui
1. 8081 -> pihole-gui
1. 8082 -> filebrowser-gui
1. 8084 -> mongo-express-gui
1. 9000 -> portainer-gui
1. 27017 -> mongo-db
1. 51820 -> wg-vpn
1. 51821 -> wg-gui