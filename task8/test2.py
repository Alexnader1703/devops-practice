#!/usr/bin/env python3
import json
import logging

import grpc
import yandexcloud
from yandex.cloud.compute.v1.image_service_pb2 import GetImageLatestByFamilyRequest
from yandex.cloud.compute.v1.image_service_pb2_grpc import ImageServiceStub
from yandex.cloud.compute.v1.instance_pb2 import IPV4, Instance
from yandex.cloud.compute.v1.instance_service_pb2 import (
    AttachedDiskSpec,
    CreateInstanceMetadata,
    CreateInstanceRequest,
    NetworkInterfaceSpec,
    OneToOneNatSpec,
    PrimaryAddressSpec,
    ResourcesSpec,
)
from yandex.cloud.compute.v1.instance_service_pb2_grpc import InstanceServiceStub

# Конфигурация
SERVICE_ACCOUNT_KEY_FILE = r'C:\Users\Alexander\Documents\GitHub\devops-practice\task8\key.json'
FOLDER_ID = "b1gdpoivp1poeknjahoq"
ZONE = "ru-central1-a"
NAME = "created-python-instance"
SUBNET_ID = "e9b4lfpg6agdsvkl5s1f"
IMAGE_FAMILY = "ubuntu-2404-lts-oslogin"
SSH_PUBLIC_KEY = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIL3akDT7ekJPzIeQC2p1hlbQTQlbkG7eSfL3mVxLxG+w danac@DESKTOP-5SPESM9"
HOSTNAME = "trainee-8"



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

    # Получаем последний образ по семейству
    image_service = sdk.client(ImageServiceStub)
    source_image = image_service.GetLatestByFamily(
        GetImageLatestByFamilyRequest(
            folder_id="standard-images",  # Обычно стандартные образы находятся в папке standard-images
            family=IMAGE_FAMILY
        )
    )

    # Создаём инстанс
    instance_service = sdk.client(InstanceServiceStub)
    logging.info("Запускается создание виртуальной машины...")
    operation = instance_service.Create(
        CreateInstanceRequest(
            folder_id=FOLDER_ID,
            name=NAME,
            resources_spec=ResourcesSpec(
                memory=2 * 2**30,  # 2 ГБ памяти
                cores=2,
                core_fraction=0,  # Если 0, то используется полная производительность ядер (обычно можно указать 100)
            ),
            zone_id=ZONE,
            platform_id="standard-v1",
            boot_disk_spec=AttachedDiskSpec(
                auto_delete=True,
                disk_spec=AttachedDiskSpec.DiskSpec(
                    type_id="network-hdd",
                    size=20 * 2**30,  # 20 ГБ диска
                    image_id=source_image.id,
                ),
            ),
            network_interface_specs=[
                NetworkInterfaceSpec(
                    subnet_id=SUBNET_ID,
                    primary_v4_address_spec=PrimaryAddressSpec(
                        one_to_one_nat_spec=OneToOneNatSpec(
                            ip_version=IPV4,
                        )
                    ),
                ),
            ],
            metadata={
                'ssh-keys': f'alex:{SSH_PUBLIC_KEY}',
                "hostname": HOSTNAME
            },
        )
    )

    # Ожидаем завершения операции создания инстанса
    logging.info("Ожидание завершения операции...")
    operation_result = sdk.wait_operation_and_get_result(
        operation,
        response_type=Instance,
        meta_type=CreateInstanceMetadata,
    )

    # Здесь важно: структура ответа может отличаться. Например, чтобы получить ID инстанса, 
    # возможно, нужно обращаться к operation_result.response.instance_id или operation_result.response.id.
    # Выведем структуру результата:
    logging.info("Результат операции: %s", operation_result)

    try:
        instance_id = operation_result.response.id
    except AttributeError:
        # Если атрибута id нет, можно вывести весь response, чтобы посмотреть, что доступно.
        logging.error("Атрибут 'id' не найден в ответе операции. Доступные поля: %s", dir(operation_result.response))
        return

    logging.info("Виртуальная машина создана с ID: %s", instance_id)

if __name__ == "__main__":
    main()
