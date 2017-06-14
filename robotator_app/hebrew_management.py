#!/usr/bin/python
# -*- coding: utf-8 -*-

class HebrewManagement():

    @staticmethod
    def multiline(text, num_char, start_to_end=False):
        text0 = text
        if start_to_end:
            text0 = text0[::-1]
        new_lines = []
        i = 0
        while i < len(text0):
            j = 0
            txt = ""
            while j < num_char or not text0[i].isspace():
                if text0[i] == "*":
                    i = i+1
                    break
                txt += text0[i]
                j = j+1
                i = i+1
                if not i < len(text0):
                    break

            new_lines.append(txt.strip())

        return new_lines

    text_input_var = {}

    @staticmethod
    def text_change(instance, value):
        print('========', value, len(value))
        if len(value) > 0:
            if instance not in HebrewManagement.text_input_var:
                HebrewManagement.text_input_var[instance] = {
                    "internal_text_change": False,
                    "prev_text": "",
                    "last_value": "",
                    "weird": False
                }
            # check if wierd unicode
            if len(HebrewManagement.text_input_var[instance]["prev_text"]) == 0 and len(value) == 2:
                HebrewManagement.text_input_var[instance]["weird"] = True
                print('=======  WEIRD !!!! =======')

            print('-----', value, HebrewManagement.text_input_var[instance])
            first_character = (HebrewManagement.text_input_var[instance]["weird"] and len(value) == 2) or \
                              (not HebrewManagement.text_input_var[instance]["weird"] and len(value) == 1)

            if first_character or value != HebrewManagement.text_input_var[instance]["last_value"]:
                if not HebrewManagement.text_input_var[instance]["internal_text_change"]:
                    HebrewManagement.text_input_var[instance]["last_value"] = value
                print(1)
                if not HebrewManagement.text_input_var[instance]["internal_text_change"]:
                    print(2)
                    HebrewManagement.text_input_var[instance]["internal_text_change"] = True
                    if len(HebrewManagement.text_input_var[instance]["prev_text"]) <= len(value):
                        print(3)
                        if HebrewManagement.text_input_var[instance]["weird"]:
                            if value[-1] == ' ':
                                instance.text = value[-1] + value[:-1]
                            else:
                                instance.text = value[-2:] + value[:-2]
                        else:
                            instance.text = value[-1] + value[:-1]
                        HebrewManagement.text_input_var[instance]["prev_text"] = instance.text
                    else:
                        print(4)
                        if HebrewManagement.text_input_var[instance]["weird"]:
                            if HebrewManagement.text_input_var[instance]["prev_text"][0] == ' ':
                                instance.text = HebrewManagement.text_input_var[instance]["prev_text"][1:]
                            else:
                                instance.text = HebrewManagement.text_input_var[instance]["prev_text"][2:]
                        else:
                            instance.text = HebrewManagement.text_input_var[instance]["prev_text"][1:]
                        HebrewManagement.text_input_var[instance]["prev_text"] = instance.text
                    print(5)
                    if HebrewManagement.text_input_var[instance]["internal_text_change"]:
                        print(6)
                        HebrewManagement.text_change(instance, value)
                else:
                    print(7)
                    HebrewManagement.text_input_var[instance]["internal_text_change"] = False

                print(value, HebrewManagement.text_input_var[instance]["prev_text"])

                max_size = max(instance._lines_rects, key=lambda r: r.size[0]).size
                px = [10, -5]
                px[0] = instance.width - max_size[0] - 10
                instance.padding_x = px
