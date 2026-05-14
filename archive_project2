import sys
import os
import struct


# Поддерживаются команды:
# create
# unpack
# add
# TODO: добавить rm (удаление файла из архива)
# TODO: возможно добавить список файлов


def write_file_to_archive(archive, file_path):
    """
    Записывает один файл в архив.
    Формат блока: [4 байта: длина имени] [имя] [8 байт: размер данных] [данные]
    """
    file_name = os.path.basename(file_path)

    with open(file_path, "rb") as f:
        data = f.read()

    name_bytes = file_name.encode("utf-8")

    # Упаковываем длину имени в 4 байта
    archive.write(struct.pack("I", len(name_bytes)))
    # Пишем имя
    archive.write(name_bytes)
    # Упаковываем размер данных в 8 байт
    archive.write(struct.pack("Q", len(data)))
    # Пишем сами данные
    archive.write(data)


def create_archive(archive_name, folder_path):
    """
    Создание архива из файлов папки.
    """
    if not os.path.exists(folder_path):
        print("Folder does not exist")
        return

    with open(archive_name, "wb") as archive:
        for file_name in os.listdir(folder_path):
            full_path = os.path.join(folder_path, file_name)
            if os.path.isfile(full_path):
                write_file_to_archive(archive, full_path)

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
            # Читаем 4 байта -> длина имени
            name_length_bytes = archive.read(4)
            if not name_length_bytes:
                break  # Конец архива

            name_length = struct.unpack("I", name_length_bytes)[0]
            name = archive.read(name_length).decode("utf-8")

            # Читаем 8 байт -> размер файла
            size = struct.unpack("Q", archive.read(8))[0]
            data = archive.read(size)

            output_path = os.path.join(output_folder, name)
            with open(output_path, "wb") as f:
                f.write(data)

    print("Archive unpacked successfully")


def add_file_to_archive(archive_name, file_path):
    """
    Добавление одного файла в уже существующий архив.
    """
    if not os.path.exists(archive_name):
        print("Archive does not exist")
        return

    if not os.path.isfile(file_path):
        print("File to add does not exist")
        return

    # Режим 'ab' (append binary) позволяет дописывать данные в конец файла
    with open(archive_name, "ab") as archive:
        write_file_to_archive(archive, file_path)

    print("File added successfully")


def remove_file_from_archive(archive_name, file_path):
    """
    Удаление файла из архива.
    Так как архив последовательный, удаляем файл путём перезаписи архива без него.
    """
    if not os.path.exists(archive_name):
        print("Archive does not exist")
        return

    target_name = os.path.basename(file_path)
    temp_name = archive_name + ".tmp"
    found = False

    # Читаем старый архив, копируем во временный всё, кроме удаляемого файла
    with open(archive_name, "rb") as src, open(temp_name, "wb") as dst:
        while True:
            name_length_bytes = src.read(4)
            if not name_length_bytes:
                break

            name_length = struct.unpack("I", name_length_bytes)[0]
            name_bytes = src.read(name_length)
            name = name_bytes.decode("utf-8")

            size = struct.unpack("Q", src.read(8))[0]
            data = src.read(size)

            if name == target_name:
                found = True  # Нашли файл, пропускаем запись
            else:
                # Копируем блок в новый архив
                dst.write(struct.pack("I", len(name_bytes)))
                dst.write(name_bytes)
                dst.write(struct.pack("Q", size))
                dst.write(data)

    if found:
        os.replace(temp_name, archive_name)  # Безопасно заменяем оригинал
        print("File removed successfully")
    else:
        os.remove(temp_name)  # Файла не было, удаляем временный архив
        print("File not found in archive")


def main():
    if len(sys.argv) < 4:
        print("Usage:")
        print("python archiver.py create <archive_name> <folder_path>")
        print("python archiver.py unpack <archive_name> <folder_path>")
        print("python archiver.py add <archive_name> <file_path>")
        print("python archiver.py rm <archive_name> <file_path>")
        return

    command = sys.argv[1]
    archive_name = sys.argv[2]
    path = sys.argv[3]

    if command == "create":
        create_archive(archive_name, path)
    elif command == "unpack":
        unpack_archive(archive_name, path)
    elif command == "add":
        add_file_to_archive(archive_name, path)
    elif command == "rm":
        remove_file_from_archive(archive_name, path)
    else:
        print("Unknown command")


if __name__ == "__main__":
    main()
