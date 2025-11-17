import argparse
import os
from pdf2docx import Converter
from docx2pdf import convert
from PIL import Image


def parse_args():
    parser = argparse.ArgumentParser(description="Office Tweaks — работа с файлами")

    parser.add_argument("--pdf2docx", help="Преобразовать PDF в DOCX. Укажите файл или 'all'")
    parser.add_argument("--docx2pdf", help="Преобразовать DOCX в PDF. Укажите файл или 'all'")

    parser.add_argument("--compress", help="Сжать изображение. Укажите файл или 'all'")
    parser.add_argument("--quality", type=int, default=75, help="Качество сжатия (1–100)")

    parser.add_argument("--delete", action="store_true", help="Удалить группу файлов")
    parser.add_argument("--mode", choices=["startswith", "endswith", "contains", "extension"])
    parser.add_argument("--pattern", help="Строка/маска для удаления")
    parser.add_argument("--directory", help="Каталог для удаления файлов")

    return parser.parse_args()


def delete_group_files_cli(path, mode, pattern):
    if not pattern or not mode:
        print("Ошибка: --delete требует --mode и --pattern")
        return

    for file in os.listdir(path):
        full = os.path.join(path, file)

        if mode == "startswith" and file.startswith(pattern):
            os.remove(full)
            print(f'Удалён файл: {file}')

        elif mode == "endswith" and file.endswith(pattern):
            os.remove(full)
            print(f'Удалён файл: {file}')

        elif mode == "contains" and pattern in file:
            os.remove(full)
            print(f'Удалён файл: {file}')

        elif mode == "extension" and file.lower().endswith(pattern.lower()):
            os.remove(full)
            print(f'Удалён файл: {file}')


def cli_mode(args):
    current_dir = args.directory or os.getcwd()

    if args.pdf2docx:
        if args.pdf2docx == "all":
            for f in os.listdir(current_dir):
                if f.lower().endswith(".pdf"):
                    convert_pdf_to_docx(os.path.join(current_dir, f))
        else:
            convert_pdf_to_docx(os.path.join(current_dir, args.pdf2docx))

    if args.docx2pdf:
        if args.docx2pdf == "all":
            for f in os.listdir(current_dir):
                if f.lower().endswith(".docx"):
                    convert_docx_to_pdf(os.path.join(current_dir, f))
        else:
            convert_docx_to_pdf(os.path.join(current_dir, args.docx2pdf))

    if args.compress:
        if args.compress == "all":
            for f in os.listdir(current_dir):
                if f.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
                    compress_image(os.path.join(current_dir, f), args.quality)
        else:
            compress_image(os.path.join(current_dir, args.compress), args.quality)

    if args.delete:
        directory = args.directory or os.getcwd()
        delete_group_files_cli(directory, args.mode, args.pattern)


def print_header(current_path):
    print(f"\nТекущий каталог: {current_path}\n")
    print("Выберите действие:")
    print("0. Сменить рабочий каталог")
    print("1. Преобразовать PDF в Docx")
    print("2. Преобразовать Docx в PDF")
    print("3. Произвести сжатие изображения")
    print("4. Удалить группу файлов")
    print("5. Выход")


def list_files(path, extensions):
    files = [f for f in os.listdir(path) if f.lower().endswith(extensions)]
    for i, f in enumerate(files, 1):
        print(f"{i}. {f}")
    return files


def convert_pdf_to_docx(filepath):
    output = filepath.replace(".pdf", ".docx")
    cv = Converter(filepath)
    cv.convert(output)
    cv.close()
    print(f'Файл "{os.path.basename(output)}" успешно создан!')


def convert_docx_to_pdf(filepath):
    output = filepath.replace(".docx", ".pdf")
    convert(filepath, output)
    print(f'Файл "{os.path.basename(output)}" успешно создан!')


def compress_image(filepath, quality):
    img = Image.open(filepath)
    img.save(filepath, quality=quality)
    print(f'Файл "{os.path.basename(filepath)}" успешно сжат!')


def delete_group_files(path):
    print("\nВыберите действие:")
    print("1. Удалить все файлы начинающиеся на определённую подстроку")
    print("2. Удалить все файлы заканчивающиеся на определённую подстроку")
    print("3. Удалить все файлы содержащие определённую подстроку")
    print("4. Удалить все файлы по расширению")

    choice = input("Введите номер действия: ")
    substring = input("Введите подстроку: ")

    for file in os.listdir(path):
        full = os.path.join(path, file)

        if choice == "1" and file.startswith(substring):
            os.remove(full)
            print(f'Файл "{file}" успешно удалён!')

        elif choice == "2" and file.endswith(substring):
            os.remove(full)
            print(f'Файл "{file}" успешно удалён!')

        elif choice == "3" and substring in file:
            os.remove(full)
            print(f'Файл "{file}" успешно удалён!')

        elif choice == "4" and file.lower().endswith(substring.lower()):
            os.remove(full)
            print(f'Файл "{file}" успешно удалён!')


def main():
    args = parse_args()

    if any([args.pdf2docx, args.docx2pdf, args.compress, args.delete]):
        cli_mode(args)
        return

    current_path = os.getcwd()

    while True:
        print_header(current_path)
        choice = input("Ваш выбор: ")

        if choice == "0":
            new_path = input("Укажите корректный путь к рабочему каталогу: ")
            if os.path.isdir(new_path):
                current_path = new_path
            else:
                print("Указан неверный путь.")

        elif choice == "1":
            print("\nСписок файлов с расширением .pdf в данном каталоге:")

            files = list_files(current_path, (".pdf",))

            if not files:
                print("Нет файлов указанного типа в данном каталоге.")
                continue

            num = int(input("\nВведите номер файла (0 = обработать все): "))

            if num == 0:
                for f in files:
                    convert_pdf_to_docx(os.path.join(current_path, f))

            else:
                convert_pdf_to_docx(os.path.join(current_path, files[num - 1]))


        elif choice == "2":
            print("\nСписок файлов с расширением .docx в данном каталоге:")

            files = list_files(current_path, (".docx",))

            if not files:
                print("Нет файлов указанного типа в данном каталоге.")

                continue

            num = int(input("\nВведите номер файла (0 = обработать все): "))
            if num == 0:

                for f in files:
                    convert_docx_to_pdf(os.path.join(current_path, f))

            else:
                convert_docx_to_pdf(os.path.join(current_path, files[num - 1]))


        elif choice == "3":
            print("\nСписок файлов с расширением ('.jpeg', '.gif', '.png', '.jpg') в данном каталоге:")

            files = list_files(current_path, (".jpeg", ".gif", ".png", ".jpg"))

            if not files:
                print("Нет изображений указанных форматов в данном каталоге.")

                continue

            num = int(input("\nВведите номер файла (0 = обработать все): "))
            quality = int(input("Введите параметр степени сжатия (от 0 до 100): "))

            if num == 0:
                for f in files:
                    compress_image(os.path.join(current_path, f), quality)

            else:
                compress_image(os.path.join(current_path, files[num - 1]), quality)

        elif choice == "4":
            delete_group_files(current_path)

        elif choice == "5":
            print("Завершение работы.")
            break

        else:
            print("Неизвестный пункт меню.\n")


if __name__ == "__main__":
    main()
