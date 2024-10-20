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

from tkinter import*

global_choice = None
mode = None
alphabet_label = None  # Переменная для хранения метки алфавита

# Функция для сохранения введённого текста в файл
def save_input_text():
    text = input_text_area.get("1.0", "end-1c")  # Получаем текст из текстового поля
    with open('input.txt', 'w') as f:
        f.write(text)
    print("Текст сохранён в файл input.txt")

def read_data(alphabet_file, probability_file):
    """Чтение алфавита и вероятностей из файлов с отладкой"""
    print(f"Чтение файла алфавита: {alphabet_file}")
    print(f"Чтение файла вероятностей: {probability_file}")

    try:
        with open(alphabet_file, 'r') as f_alphabet:
            alphabet = [line.strip() for line in f_alphabet.readlines()]
        print(f"Алфавит успешно прочитан: {alphabet}")

        # Обновляем метку с алфавитом
        if alphabet_label:  # Проверяем, инициализирована ли метка
            alphabet_label.config(text=f"Алфавит: {', '.join(alphabet)}")

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

    return codes, l

def decode_symbols(codes):
    """Создание обратного словаря для декодирования"""
    return {code: symbol for symbol, code in codes.items()}

def write_codes_to_file(codes, output_file):
    """Запись кодов в файл и возвращение их как строку для отображения."""
    codes_str = ""
    with open(output_file, 'w') as f_output:
        for symbol, code in codes.items():
            f_output.write(f"{symbol}: {code}\n")
            codes_str += f"{symbol}: {code}\n"  # Составляем строку для отображения
    return codes_str

def choose_probability_file():
    if global_choice == 1:
        return 'probability1.txt', 'code_words_p1.txt'
    elif global_choice == 2:
        return 'probability2.txt', 'code_words_p2.txt'
    elif global_choice == 3:
        return 'uniform_distribution.txt', 'code_words_ud.txt'

def set_choice(value):
    global global_choice
    global_choice = value
    print(f"Выбрана вероятность: {global_choice}")

    if global_choice is not None:
        process_mode(mode)  # Здесь mode должен быть глобальным или передаваться как параметр

def show_probability_buttons():
    btn_probability1.grid(column=0, row=3)
    btn_probability2.grid(column=1, row=3)
    btn_probability3.grid(column=2, row=3)

def read_input_file(input_file):
    """Чтение текста для кодирования из файла"""
    try:
        with open(input_file, 'r') as f_input:
            text = f_input.read().strip()
        return text
    except Exception as e:
        print(f"Ошибка при чтении файла ввода: {e}")
        raise

def encode_text(text, codes, alphabet):
    """Кодирование текста на основе словаря кодов"""
    if not validate_input_text(text, alphabet):
        raise ValueError("Ошибка: Введены недопустимые символы для кодирования.")
    encoded_text = ''.join(codes[char] for char in text if char in codes)
    return encoded_text

def decode_text(encoded_text, decode_codes):
    """Декодирование текста на основе словаря кодов"""
    if not validate_binary_input(encoded_text):
        raise ValueError("Ошибка: Ввод должен содержать только двоичные символы (0 и 1) для декодирования.")

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

def calculate_average_length(l, probabilities):
    """Вычисление средней длины кодового слова"""
    average_length = sum(l[i] * probabilities[i] for i in range(len(probabilities)))
    return average_length

def calculate_entropy(probabilities):
    """Вычисление энтропии H"""
    entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
    return entropy

def calculate_redundancy(average_length, entropy):
    """Вычисление избыточности"""
    return average_length - entropy

def calculate_kraft_inequality(l):
    """Вычисление неравенства Крафта"""
    kraft_sum = sum(2 ** (-li) for li in l)
    return kraft_sum

def process_mode(mode):
    alphabet_file = 'alphabet.txt'
    global global_choice
    probability_file, code_words_file = choose_probability_file()

    # Получение алфавита и вероятностей
    alphabet, probabilities = read_data(alphabet_file, probability_file)
    # Получение кодировки символов и значений l
    codes, l = encode_symbols(alphabet, probabilities)
    codes_str = write_codes_to_file(codes, code_words_file)
    codes_label.config(text=f"Кодовые слова:\n{codes_str}")  # Обновляем метку с кодовыми словами

    # Вычисление средней длины, энтропии и избыточности
    average_length = calculate_average_length(l, probabilities)
    entropy = calculate_entropy(probabilities)
    redundancy = calculate_redundancy(average_length, entropy)

    # Вывод результатов расчетов
    average_length_label.config(text=f"Средняя длина кодового слова: {average_length}")
    entropy_label.config(text=f"Энтропия: {entropy}")
    redundancy_label.config(text=f"Избыточность: {redundancy}")

    # Вычисление и проверка неравенства Крафта
    kraft_sum = calculate_kraft_inequality(l)
    kraft_label.config(text=f"Неравенство Крафта: {kraft_sum}")
    if kraft_sum == 1:
        kraft_optimality_label.config(text="Код является оптимальным.")
    elif kraft_sum < 1:
        kraft_optimality_label.config(text="Код не является оптимальным.")
    else:
        kraft_optimality_label.config(text="Ошибка: Сумма неравенства Крафта больше 1.")

    if mode == 1:  # Кодирование
        input_file = 'input.txt'
        text = read_input_file(input_file)
        try:
            encoded_text = encode_text(text, codes, alphabet)  # Передача алфавита
            write_output_file('output.txt', encoded_text)
            encoded_text_label.config(text=f"Закодированный текст: {encoded_text}")
        except ValueError as e:
            encoded_text_label.config(text=str(e))
            print(str(e))

    elif mode == 2:  # Декодирование
        input_file = 'input.txt'
        encoded_text = read_input_file(input_file)
        try:
            decode_codes = decode_symbols(codes)
            decoded_text = decode_text(encoded_text, decode_codes)
            write_output_file('output.txt', decoded_text)
            decoded_text_label.config(text=f"Декодированный текст: {decoded_text}")
        except ValueError as e:
            decoded_text_label.config(text=str(e))
            print(str(e))

def validate_input_text(text, alphabet):
    """Проверка, что все символы в тексте соответствуют алфавиту."""
    return all(char in alphabet for char in text)

def validate_binary_input(text):
    """Проверка, что ввод состоит только из двоичных символов (0 и 1)."""
    return all(bit in '01' for bit in text)

def clickedC():
    global global_choice
    global mode
    mode = 1
    global_choice = None  # Сброс выбора
    show_probability_buttons()  # Показать кнопки выбора вероятности

def clickedDC():
    global global_choice
    global mode
    mode = 2
    global_choice = None  # Сброс выбора
    show_probability_buttons()  # Показать кнопки выбора вероятности

# Основной код программы
if __name__ == "__main__":
    window = Tk()
    window.title('Кодирование/декодирование')
    window.geometry('1000x760')

    # Текстовое поле для ввода текста
    input_text_area = Text(window, height=10, width=80)
    input_text_area.grid(column=0, row=0, columnspan=3)

    # Кнопка для сохранения текста в input.txt
    btn_save_input = Button(window, text="Сохранить текст", command=save_input_text)
    btn_save_input.grid(column=4, row=0, columnspan=3)

    lbl = Label(window, text="Выбор режима работы:")
    lbl.grid(column=0, row=1)

    btn_encode = Button(window, text="Кодировать", command=clickedC)
    btn_encode.grid(column=0, row=2)

    btn_decode = Button(window, text="Декодировать", command=clickedDC)
    btn_decode.grid(column=2, row=2)

    # Кнопки выбора вероятности
    btn_probability1 = Button(window, text="Первая вероятность", command=lambda: set_choice(1))
    btn_probability2 = Button(window, text="Вторая вероятность", command=lambda: set_choice(2))
    btn_probability3 = Button(window, text="Равномерное распределение", command=lambda: set_choice(3))

    # Изначально скрываем кнопки
    btn_probability1.grid_forget()
    btn_probability2.grid_forget()
    btn_probability3.grid_forget()

    # Метка для отображения алфавита
    alphabet_label = Label(window, text="Алфавит: ")
    alphabet_label.grid(column=0, row=4, columnspan=3)  # Размещаем метку ниже кнопок

    # Метки для отображения результатов
    kraft_label = Label(window, text="Неравенство Крафта: ")
    kraft_label.grid(column=0, row=6, columnspan=3)

    kraft_optimality_label = Label(window, text="")
    kraft_optimality_label.grid(column=0, row=7, columnspan=3)

    entropy_label = Label(window, text="Энтропия: ")
    entropy_label.grid(column=0, row=8, columnspan=3)

    redundancy_label = Label(window, text="Избыточность: ")
    redundancy_label.grid(column=0, row=9, columnspan=3)

    average_length_label = Label(window, text="Средняя длина кодового слова: ")
    average_length_label.grid(column=0, row=10, columnspan=3)

    # Метка для отображения кодовых слов
    codes_label = Label(window, text="")
    codes_label.grid(column=0, row=11, columnspan=3)

    # Метка для отображения закодированного текста
    encoded_text_label = Label(window, text="", wraplength=600)  # Задаем ширину для переноса строк
    encoded_text_label.grid(column=0, row=12, columnspan=3)

    # Метка для отображения декодированного текста
    decoded_text_label = Label(window, text="", wraplength=600)  # Задаем ширину для переноса строк
    decoded_text_label.grid(column=0, row=13, columnspan=3)


    window.mainloop()