"""
Имеющиеся в программе файлы хранят следующие данные:
 probability1.txt -- распределение появления символов алфавита P1
 probability2.txt -- распределение появления символов алфавита P2
 uniform_distribution.txt -- равномерное распределение появления символов алфавита
 alphabet.txt -- алфавит источника А
 input.txt -- последовательность символов для кодирования/декодирования
 output.txt -- закодированная/декодированная последовательность
 code_words_p1.txt -- полученные кодовые слова для P1
 code_words_p2.txt -- полученные кодовые слова для P2
 code_words_ud.txt -- полученные кодовые слова для равномерного распределения

"""

import math

def read_data(alphabet_file, probability_file):
    """Чтение алфавита и вероятностей из файлов с отладкой"""
    print(f"Чтение файла алфавита: {alphabet_file}")
    print(f"Чтение файла вероятностей: {probability_file}")

    try:
        with open(alphabet_file, 'r') as f_alphabet:
            alphabet = [line.strip() for line in f_alphabet.readlines()]
        print(f"Алфавит успешно прочитан: {alphabet}")
    except Exception as e:
        print(f"Ошибка при чтении файла алфавита: {e}")
        raise

    try:
        with open(probability_file, 'r') as f_prob:
            probabilities = [float(line.strip()) for line in f_prob.readlines()]
        print(f"Вероятности успешно прочитаны: {probabilities}")
    except ValueError as ve:
        print(f"Ошибка преобразования в число в файле вероятностей: {ve}")
        raise
    except Exception as e:
        print(f"Ошибка при чтении файла вероятностей: {e}")
        raise

    return alphabet, probabilities

def calculate_q(probabilities):
    """Вычисляем кумулятивную вероятность q для каждого символа"""
    q = [0]  # q(1) = 0
    for i in range(1, len(probabilities)):
        q.append(q[i - 1] + probabilities[i - 1])
    return q

def calculate_sigma(q, probabilities):
    """Вычисляем значение sigma(i)"""
    sigma = []
    for i in range(len(probabilities)):
        sigma_value = q[i] + probabilities[i] / 2
        sigma.append(sigma_value)
    return sigma

def calculate_l(probabilities):
    """Вычисляем значение l(i), округленное в большую сторону"""
    l = []
    for prob in probabilities:
        l_value = math.ceil(-math.log2(prob / 2))
        l.append(l_value)
    return l

def float_to_binary(fraction, bits):
    """Переводим дробную часть числа в двоичную систему, оставляя первые bits символов"""
    binary = ""
    while len(binary) < bits:
        fraction *= 2
        if fraction >= 1:
            binary += '1'
            fraction -= 1
        else:
            binary += '0'
    return binary

def encode_symbols(alphabet, probabilities):
    """Основная функция кодирования символов"""
    q = calculate_q(probabilities)
    sigma = calculate_sigma(q, probabilities)
    l = calculate_l(probabilities)

    codes = {}
    for i in range(len(alphabet)):
        fractional_part = sigma[i] - int(sigma[i])  # Извлекаем дробную часть
        binary_code = float_to_binary(fractional_part, l[i])
        codes[alphabet[i]] = binary_code

    return codes

def decode_symbols(codes):
    """Создание обратного словаря для декодирования"""
    return {code: symbol for symbol, code in codes.items()}

def write_codes_to_file(codes, output_file):
    """Запись кодов в файл"""
    with open(output_file, 'w') as f_output:
        for symbol, code in codes.items():
            f_output.write(f"{symbol}: {code}\n")

def choose_probability_file():
    """Функция для выбора файла с вероятностями"""
    print("Выберите файл с вероятностями:")
    print("1. probability1.txt")
    print("2. probability2.txt")
    print("3. uniform_distribution.txt")

    choice = input("Ваш выбор (1/2/3): ")

    if choice == '1':
        return 'probability1.txt', 'code_words_p1.txt'
    elif choice == '2':
        return 'probability2.txt', 'code_words_p2.txt'
    elif choice == '3':
        return 'uniform_distribution.txt', 'code_words_ud.txt'
    else:
        print("Неправильный выбор, попробуйте снова.")
        return choose_probability_file()

def read_input_file(input_file):
    """Чтение текста для кодирования из файла"""
    try:
        with open(input_file, 'r') as f_input:
            text = f_input.read().strip()
        return text
    except Exception as e:
        print(f"Ошибка при чтении файла ввода: {e}")
        raise

def encode_text(text, codes):
    """Кодирование текста на основе словаря кодов"""
    encoded_text = ''.join(codes[char] for char in text if char in codes)
    return encoded_text

def decode_text(encoded_text, decode_codes):
    """Декодирование текста на основе словаря кодов"""
    decoded_text = ''
    current_code = ''
    for bit in encoded_text:
        current_code += bit
        if current_code in decode_codes:
            decoded_text += decode_codes[current_code]
            current_code = ''
    return decoded_text

def write_output_file(output_file, text):
    """Запись текста в файл"""
    with open(output_file, 'w') as f_output:
        f_output.write(text)

# Основной код программы
if __name__ == "__main__":
    # Выбор режима работы
    mode = input("Выберите режим работы (1 - кодировать, 2 - декодировать): ")

    alphabet_file = 'alphabet.txt'
    probability_file, code_words_file = choose_probability_file()

    alphabet, probabilities = read_data(alphabet_file, probability_file)

    # Получение кодировки символов
    codes = encode_symbols(alphabet, probabilities)

    # Запись кодов в файл
    write_codes_to_file(codes, code_words_file)

    if mode == '1':  # Кодирование
        # Чтение текста для кодирования
        input_file = 'input.txt'
        text = read_input_file(input_file)

        # Кодирование текста
        encoded_text = encode_text(text, codes)

        # Запись закодированного текста в файл
        write_output_file('output.txt', encoded_text)

        print(f"Кодировка символов записана в файл {code_words_file}")
        print(f"Закодированный текст записан в файл output.txt")

    elif mode == '2':  # Декодирование
        # Чтение закодированного текста из файла
        input_file = 'input.txt'
        encoded_text = read_input_file(input_file)

        # Создание обратного словаря для декодирования
        decode_codes = decode_symbols(codes)

        # Декодирование текста
        decoded_text = decode_text(encoded_text, decode_codes)

        # Запись декодированного текста в файл
        write_output_file('output.txt', decoded_text)

        print(f"Кодировка символов записана в файл {code_words_file}")
        print(f"Декодированный текст записан в файл output.txt")

    else:
        print("Неправильный выбор режима работы. Программа завершена.")
