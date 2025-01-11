#!/usr/bin/env python3
import json
import logging

import grpc
import yandexcloud
from yandex.cloud.compute.v1.instance_service_pb2 import GetInstanceRequest
from yandex.cloud.compute.v1.instance_service_pb2_grpc import InstanceServiceStub

# Конфигурация
SERVICE_ACCOUNT_KEY_FILE = r'C:\Users\Alexander\Documents\GitHub\devops-practice\task8\key.json'
INSTANCE_ID = "fhm84ff9rhcbicg2h6kv"  # Замените на актуальный ID инстанса

def main():
    logging.basicConfig(level=logging.INFO)
    
    # Загружаем ключ сервисного аккаунта
    with open(SERVICE_ACCOUNT_KEY_FILE, "r") as f:
        service_account_key = json.load(f)
        
    interceptor = yandexcloud.RetryInterceptor(
        max_retry_count=5,
        retriable_codes=[grpc.StatusCode.UNAVAILABLE]
    )
    sdk = yandexcloud.SDK(interceptor=interceptor, service_account_key=service_account_key)
    
    # Создаем клиент для работы с инстансами
    instance_service = sdk.client(InstanceServiceStub)
    
    # Формируем запрос на получение информации об инстансе
    request = GetInstanceRequest(instance_id=INSTANCE_ID)
    
    try:
        # Получаем объект инстанса
        instance = instance_service.Get(request)
    except Exception as e:
        logging.error("Ошибка при получении информации об инстансе: %s", e)
        return
    
    # Выводим базовую информацию об инстансе
    logging.info("Информация об инстансе:")
    
    # ID инстанса и имя
    logging.info("ID: %s", instance.id)
    logging.info("Имя: %s", instance.name)
    
    # Зона, платформа, статус
    logging.info("Зона: %s", instance.zone_id)
    logging.info("Платформа: %s", instance.platform_id)
    logging.info("Статус: %s", instance.status)
    
    # Ресурсы инстанса (память, CPU)
    if instance.HasField("resources"):
        resources = instance.resources
        logging.info("CPU: %s, Memory: %s ГБ", resources.cores, resources.memory / (2**30))
    else:
        logging.info("Информация о ресурсах не найдена.")
    
    # Информация о загрузочном диске
    if instance.HasField("boot_disk"):
        boot_disk = instance.boot_disk
        logging.info("Boot Disk ID: %s", boot_disk.disk_id)
        logging.info("Boot Disk Mode: %s", boot_disk.mode)
    else:
        logging.info("Информация о загрузочном диске не найдена.")
    
    # Сетевая информация: IP-адреса
    if instance.network_interfaces:
        for idx, iface in enumerate(instance.network_interfaces):
            logging.info("Интерфейс #%s:", idx)
            # Первичный внутренний адрес
            if iface.primary_v4_address.address:
                logging.info("  Внутренний IP: %s", iface.primary_v4_address.address)
            # Если назначен NAT, выводим публичный IP
            if iface.primary_v4_address.one_to_one_nat:
                nat = iface.primary_v4_address.one_to_one_nat
                logging.info("  Публичный IP: %s", nat.address)
    else:
        logging.info("Сетевая информация не найдена.")
    
    # Информация об образе (ОС)
    # Обычно информация об образе хранится в boot_disk либо в metadata инстанса
    #if instance.boot_disk and instance.boot_disk.HasField("disk_id"):
        # Если имеется привязка к образу, можно попробовать вывести часть информации об образе
        # Иногда содержимое образа может не приходить напрямую в этом запросе.
        # Поэтому можно проверить metadata инстанса или вызвать отдельный метод получения информации об образе.
        #logging.info("Проверьте, какая ОС установлена (обычно задается образ при создании).")
   # else:
       # logging.info("Информация об образе не доступна в ответе.")
    
    # Дополнительную информацию можно посмотреть через печать всего объекта:
    # print(instance)
    
if __name__ == "__main__":
    main()
