#!/usr/bin/env python3
import json
import logging

import grpc
import yandexcloud

from google.protobuf import field_mask_pb2 as field_mask  # для задания update_mask

from yandex.cloud.compute.v1.instance_service_pb2 import (
    UpdateInstanceRequest,
    # Если потребуется, можно импортировать и тип метаданных UpdateInstanceMetadata,
    # но в данном примере достаточно работы с request и wait_operation_and_get_result
)
from yandex.cloud.compute.v1.instance_service_pb2_grpc import InstanceServiceStub

# Конфигурация
SERVICE_ACCOUNT_KEY_FILE = r'C:\Users\Alexander\Documents\GitHub\devops-practice\task8\key.json'
FOLDER_ID = "b1gdpoivp1poeknjahoq"

# ID инстанса, который нужно обновить (его можно получить после создания инстанса или задать вручную)
INSTANCE_ID = "fhm84ff9rhcbicg2h6kv"  # Замените на актуальный ID инстанса

# Новый SSH публичный ключ (и имя пользователя). Формат: "<username>:<ssh-public-key>"
NEW_SSH_PUBLIC_KEY ="alex:ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIITBFyZ8fWtWz1UN3EHYaXbNHjABl4FaEMLpIS5AiXSZ alexander@DESKTOP-K80QIOG" 

def main():
    logging.basicConfig(level=logging.INFO)

    # Загружаем ключ сервисного аккаунта
    with open(SERVICE_ACCOUNT_KEY_FILE, "r") as f:
        service_account_key = json.load(f)

    # Инициализируем SDK с интерцептором для повтора (retry)
    interceptor = yandexcloud.RetryInterceptor(
        max_retry_count=5,
        retriable_codes=[grpc.StatusCode.UNAVAILABLE]
    )
    sdk = yandexcloud.SDK(interceptor=interceptor, service_account_key=service_account_key)

    # Создаем клиент для работы с инстансами
    instance_service = sdk.client(InstanceServiceStub)

    # Формируем запрос на обновление: указываем, что хотим обновить метаданные (только поле ssh-keys)
    update_request = UpdateInstanceRequest(
        instance_id=INSTANCE_ID,
        update_mask=field_mask.FieldMask(paths=["metadata"]),
        metadata={
            "ssh-keys": NEW_SSH_PUBLIC_KEY
        }
    )

    logging.info("Запускается обновление SSH-ключа для инстанса с ID: %s", INSTANCE_ID)
    
    # Отправляем запрос на обновление
    operation = instance_service.Update(update_request)
    
    # Ожидаем завершения операции обновления
    operation_result = sdk.wait_operation_and_get_result(
        operation,
        # Если имеется конкретный тип метаданных для update-операции, можно его указать,
        # но часто достаточно дождаться завершения операции.
    )
    
    logging.info("SSH-ключ успешно обновлен для инстанса %s", INSTANCE_ID)
    logging.info("Результат операции: %s", operation_result)

if __name__ == "__main__":
    main()
