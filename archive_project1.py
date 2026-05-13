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
    """

    file_name = os.path.basename(file_path)

    with open(file_path, "rb") as f:
        data = f.read()

    name_bytes = file_name.encode("utf-8")

    # длина имени
    archive.write(struct.pack("I", len(name_bytes)))

    # имя файла
    archive.write(name_bytes)

    # размер файла
    archive.write(struct.pack("Q", len(data)))

    # данные файла
    archive.write(data)


def create_archive(archive_name, folder_path):
    """
    Создание архива из файлов папки.
    Подпапки пока не поддерживаются.
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
            name_length_bytes = archive.read(4)

            if not name_length_bytes:
                break

            name_length = struct.unpack("I", name_length_bytes)[0]
            name = archive.read(name_length).decode("utf-8")

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

    # режим append (добавление в конец)
    with open(archive_name, "ab") as archive:
        write_file_to_archive(archive, file_path)

    print("File added successfully")


def main():
    if len(sys.argv) < 4:
        print("Usage:")
        print("python archiver.py create <archive_name> <folder_path>")
        print("python archiver.py unpack <archive_name> <folder_path>")
        print("python archiver.py add <archive_name> <file_path>")
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

    else:
        print("Unknown command")


if __name__ == "__main__":
    main()