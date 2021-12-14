#!/bin/sh
docker tag web dspatharakis/controller_druidnet:web
docker push dspatharakis/controller_druidnet:web
docker tag app1 dspatharakis/controller_druidnet:app1
docker push dspatharakis/controller_druidnet:app1
docker tag app2 dspatharakis/controller_druidnet:app2
docker push dspatharakis/controller_druidnet:app2
# TODO choose one!!
docker tag db dspatharakis/controller_druidnet:db
docker tag postgres:13-alpine dspatharakis/controller_druidnet:db
docker push dspatharakis/controller_druidnet:db
docker tag redis:6-alpine dspatharakis/controller_druidnet:redis
docker push dspatharakis/controller_druidnet:redis
docker tag druidnet_beat_worker dspatharakis/controller_druidnet:beat_worker
docker push dspatharakis/controller_druidnet:beat_worker
docker tag druidnet_celery_beat dspatharakis/controller_druidnet:celery_beat
docker push dspatharakis/controller_druidnet:celery_beat
docker tag druidnet_dashboard dspatharakis/controller_druidnet:dashboard
docker push dspatharakis/controller_druidnet:dashboard
docker tag druidnet_green_worker dspatharakis/controller_druidnet:green_worker
docker push dspatharakis/controller_druidnet:green_worker
docker tag druidnet_red_worker dspatharakis/controller_druidnet:red_worker
docker push dspatharakis/controller_druidnet:red_worker
docker tag druidnet_red_worker dspatharakis/controller_druidnet:queue_worker
docker push dspatharakis/controller_druidnet:queue_worker