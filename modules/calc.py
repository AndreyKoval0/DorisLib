from .base import Module

class Calc(Module):
    def exec(self, question):
        question = question.lower().replace("сколько ", "").replace("будет ", "").replace("на ", "") + " "
        numbers = {"один":1, "два":2, "три":3,"четыре":4,"пять":5,"шесть":6,"семь":7,"восемь":8,"девять":9,"десять":10,
                    "одинадцать":11,"двенадцать":12,"тринадцать":13,"четырнадцать":14,"пятнадцать":15,
                    "шестнадцать":16,"семнадцать":17,"восемнадцать":18,"девятнадцать":19,"двадцать":20,
                    "тридцать":30,"сорок":40,"пятьдесят":50,"шестьдесят":60,"семьдесят":70,"восемьдесят":80,
                    "девяносто":90, "сто":100, "двести":200, "триста":300, "четыреста":400, "пятьсот":500, "шестьсот":600,
                    "семьсот":700, "восемьсот":800, "девятьсот":900}
        signs = ["плюс", "минус", "умножить", "разделить"]
        sign_ = ''
        
        for sign in signs:
            if sign in question:
                question = question.split(" " + sign + " ")
                sign_ = sign
                break
        for number in list(numbers):
            if number in question[0]:
                question[0] = question[0].replace(number, str(numbers[number]))
            if number in question[1]:
                question[1] = question[1].replace(number, str(numbers[number]))
        
        number_a = sum(list(map(int, question[0].split())))
        number_b = sum(list(map(int, question[1].split())))
        if sign_ == "плюс":
            return number_a + number_b
        elif sign_ == "минус":
            return number_a - number_b
        elif sign_ == "умножить":
            return number_a * number_b
        elif sign_ == "разделить":
            return number_a / number_b
        return "Вы неправильно произнели команду"