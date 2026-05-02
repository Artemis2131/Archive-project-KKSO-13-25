import sys
import os
import struct


# Пока поддерживаются только create и unpack
# TODO: добавить add и rm
# TODO: добавить более аккуратную обработку ошибок


def create_archive(archive_name, folder_path):
    """
    Создание архива из файлов в папке.
    Подпапки пока не поддерживаются.
    """

    # Проверка существования папки
    if not os.path.exists(folder_path):
        print("Folder does not exist")
        return

    with open(archive_name, "wb") as archive:

        for file_name in os.listdir(folder_path):
            full_path = os.path.join(folder_path, file_name)

            if os.path.isfile(full_path):

                with open(full_path, "rb") as f:
                    data = f.read()

                name_bytes = file_name.encode("utf-8")

                # Записываем длину имени (4 байта)
                archive.write(struct.pack("I", len(name_bytes)))

                # Записываем имя файла
                archive.write(name_bytes)

                # Записываем размер файла (8 байт)
                archive.write(struct.pack("Q", len(data)))

                # Записываем содержимое файла
                archive.write(data)

    print("Archive created successfully")


def unpack_archive(archive_name, output_folder):
    """
    Распаковка архива.
    """

    if not os.path.exists(archive_name):
        print("Archive not found")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(archive_name, "rb") as archive:

        while True:
            # Читаем длину имени
            name_length_bytes = archive.read(4)

            # Если данных больше нет — конец архива
            if not name_length_bytes:
                break

            name_length = struct.unpack("I", name_length_bytes)[0]

            # Читаем имя файла
            name = archive.read(name_length).decode("utf-8")

            # Читаем размер файла
            size = struct.unpack("Q", archive.read(8))[0]

            # Читаем данные файла
            data = archive.read(size)

            # Записываем файл
            output_path = os.path.join(output_folder, name)

            with open(output_path, "wb") as f:
                f.write(data)

    print("Archive unpacked successfully")
