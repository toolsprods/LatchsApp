# -*- coding: utf-8 -*-

try:
    import tkinter as tk  # for python 3
except:
    import Tkinter as tk  # for python 2

import time
import base64
import threading
from tkFileDialog import askopenfilename

from view.view import View
import latch.latch as latch

from Crypto.Cipher import AES
from Crypto import Random

APP_ID = "APP_ID_HERE"
SECRET_KEY = "SECRET_KEY_HERE"

# Get this from pair.sh
ACCOUNT_ID = "ACCOUNT_ID_HERE"

OP_0 = "OP_0_HERE"
OP_1 = "OP_1_HERE"
OP_2 = "OP_2_HERE"
OP_3 = "OP_3_HERE"
OP_4 = "OP_4_HERE"
OP_5 = "OP_5_HERE"
OP_6 = "OP_6_HERE"
OP_7 = "OP_7_HERE"
OP_R = "OP_R_HERE"
OP_F = "OP_F_HERE"
OP_E = "OP_E_HERE"

api = latch.Latch(APP_ID, SECRET_KEY)

locks = {}
locks[0] = OP_0
locks[1] = OP_1
locks[2] = OP_2
locks[3] = OP_3
locks[4] = OP_4
locks[5] = OP_5
locks[6] = OP_6
locks[7] = OP_7
locks[8] = OP_R
locks[9] = OP_F
locks[10] = OP_E


class Controller:
    def __init__(self, master):
        self.msg_index = 0

        self.get_view = View(master)
        self.get_view.mainwindow.master.protocol("WM_DELETE_WINDOW", self.quit)
        self.get_view.mainwindow.master.bind('<Return>', self.send)
        self.get_view.builder.connect_callbacks(self)

        # Set logo on canvas
        banner = tk.PhotoImage(file=r'view/imgs/banner.gif')
        self.latch_on = tk.PhotoImage(file=r'view/imgs/on.gif')
        self.latch_off = tk.PhotoImage(file=r'view/imgs/off.gif')

        # image = Image.open('view/imgs/LatchsApp.png')
        # banner = ImageTk.PhotoImage(image)
        # banner = ImageTk.PhotoImage(file=r'view/imgs/LatchsApp.png')
        # print(banner.format, banner.size, banner.mode)

        self.canvas_banner = self.get_view.builder.get_object('canvas_logo')
        self.canvas_banner.create_image(20, 5, image=banner, anchor='nw')
        self.canvas_banner.image = banner

        self.canvas_latch = self.get_view.builder.get_object('canvas_latch')
        self.set_latch_view(0, 0, 0, 0, 0, 0, 0, 0)

        self.check_encrypt = self.get_view.builder.get_variable('check_encrypt')
        self.check_encrypt.set(1)

        self.read_evt = True
        self.tread = threading.Thread(target=self.read_latch)
        self.tread.start()

    def send(self, event=None):
        api.unlock(ACCOUNT_ID, locks[9])
        text = self.get_view.builder.get_variable('text_input')
        if (text.get() != ''):
            message = text.get()
            self.set_msg(self.msg_index, message)
            text.set('')
            t = threading.Thread(target=self.send_latch, args=(message,))
            t.start()

    def file(self):
        api.lock(ACCOUNT_ID, locks[9])
        filename = askopenfilename()
        bin_file = open(filename, "rb")
        self.set_msg(self.msg_index, ("Send file -> %s" % filename))
        t = threading.Thread(target=self.send_latch, args=(bin_file.read(),))
        t.start()

    def set_msg(self, i, msg):
        listbox = self.get_view.builder.get_object('Listbox_1')
        listbox.insert(i, msg)
        self.msg_index += 1

    def set_msg_display(self, msg):
        self.textbox = self.get_view.builder.get_object('Text_Display')
        self.textbox.insert(tk.END, msg)

    def set_latch_view(self, op_0, op_1, op_2, op_3, op_4, op_5, op_6, op_7):
        if op_0 == "1":
            img_op0 = self.latch_on
        else:
            img_op0 = self.latch_off

        if op_1 == "1":
            img_op1 = self.latch_on
        else:
            img_op1 = self.latch_off

        if op_2 == "1":
            img_op2 = self.latch_on
        else:
            img_op2 = self.latch_off

        if op_3 == "1":
            img_op3 = self.latch_on
        else:
            img_op3 = self.latch_off

        if op_4 == "1":
            img_op4 = self.latch_on
        else:
            img_op4 = self.latch_off

        if op_5 == "1":
            img_op5 = self.latch_on
        else:
            img_op5 = self.latch_off

        if op_6 == "1":
            img_op6 = self.latch_on
        else:
            img_op6 = self.latch_off

        if op_7 == "1":
            img_op7 = self.latch_on
        else:
            img_op7 = self.latch_off

        self.canvas_latch.create_image(75, 30, image=img_op0)
        self.canvas_latch.create_image(75, 80, image=img_op1)
        self.canvas_latch.create_image(75, 130, image=img_op2)
        self.canvas_latch.create_image(75, 180, image=img_op3)
        self.canvas_latch.create_image(75, 230, image=img_op4)
        self.canvas_latch.create_image(75, 280, image=img_op5)
        self.canvas_latch.create_image(75, 330, image=img_op6)
        self.canvas_latch.create_image(75, 380, image=img_op7)
        self.canvas_latch.image = self.latch_on

    def can_write(self):
        response = api.operationStatus(ACCOUNT_ID, locks[8], silent=True)
        responseData = response.get_data()['operations'][locks[8]]['status']
        if responseData == "off":
            return False
        elif responseData == "on":
            return True

    def msg_to_bin(self, msg):
        data = list(msg)
        data_bin = []
        for i in range(len(data)):
            data_bin.append('{0:08b}'.format(ord(data[i])))
        return data_bin

    def bin_to_bit(self, data_bin):
        binary = list(data_bin)
        binary_list = []
        for i in range(8):
            binary_list.append(binary[i])
        return binary_list

    def bit_to_bin(self, data_bit):
        bits_list = ''
        for i in range(8):
            bits_list = bits_list + str(data_bit[i])
        return bits_list

    def send_latch(self, data):
        self.read_evt = False
        if self.check_encrypt.get() == '1':
            response = api.lock(ACCOUNT_ID, locks[10])
            data = self.encrypt(data, APP_ID[:16])
            data = "%s" % self.b64encode(data)
        else:
            response = api.unlock(ACCOUNT_ID, locks[10])
        msg = self.msg_to_bin(data)

        bit_list = []
        for i in range(len(msg)):
            while not self.can_write():
                self.can_write()
                time.sleep(1)

            bit_list = self.bin_to_bit(msg[i])
            self.set_latch_view(bit_list[0], bit_list[1], bit_list[2],
                                bit_list[3], bit_list[4], bit_list[5],
                                bit_list[6], bit_list[7])
            self.set_msg_display(list(data)[i])
            for i in range(8):
                if bit_list[i] == str(1):
                    response = api.lock(ACCOUNT_ID, locks[i])
                else:
                    response = api.unlock(ACCOUNT_ID, locks[i])

            response = api.lock(ACCOUNT_ID, locks[8])
        while not self.can_write():
            self.can_write()

        self.set_latch_view(0, 0, 0, 0, 0, 0, 0, 0)
        self.textbox.delete("1.0", tk.END)
        for i in range(8):
            response = api.unlock(ACCOUNT_ID, locks[i])
        response = api.lock(ACCOUNT_ID, locks[8])

        # Inicio lectura de nuevo...
        self.read_evt = True
        response = api.operationStatus(ACCOUNT_ID, locks[8], silent=True)
        responseData = response.get_data()
        while responseData['operations'][locks[8]]['status'] == "off":
            response = api.operationStatus(ACCOUNT_ID, locks[8], silent=True)
            responseData = response.get_data()
            print('wait to close...')

        self.tread = threading.Thread(target=self.read_latch)
        self.tread.start()

    def read_latch(self):
        print('reading...')
        msg = ''
        while True:
            if not self.read_evt:
                print("Exit reading...")
                break
            if not self.can_write():
                bits = []
                for i in range(8):
                    response = api.operationStatus(ACCOUNT_ID, locks[i],
                                                   silent=True)
                    responseData = response.get_data()
                    if responseData['operations'][locks[i]]['status'] == "on":
                        bits.append(0)
                    else:
                        bits.append(1)
                bit_list = self.bit_to_bin(bits)
                self.set_latch_view(bit_list[0], bit_list[1], bit_list[2],
                                    bit_list[3], bit_list[4], bit_list[5],
                                    bit_list[6], bit_list[7])
                bin_int = int(bit_list, 2)
                print(chr(bin_int))
                self.set_msg_display(chr(bin_int))
                response = api.unlock(ACCOUNT_ID, locks[8])
                if not bin_int == 0:
                    msg += chr(bin_int)
                if bin_int == 0:
                    response = api.operationStatus(ACCOUNT_ID, locks[10],
                                                   silent=True)
                    responseData = response.get_data()
                    if responseData['operations'][locks[10]]['status'] == "off":
                        msg = self.b64decode(msg)
                        msg = "%s" % self.decrypt(msg, APP_ID[:16])

                    response = api.operationStatus(ACCOUNT_ID, locks[9],
                                                   silent=True)
                    responseData = response.get_data()
                    if responseData['operations'][locks[9]]['status'] == "off":
                        self.set_msg(self.msg_index, "File received")
                        newFile = open("file", "wb")
                        newFile.write(msg)
                        newFile.close()
                    else:
                        self.set_msg(self.msg_index, msg)
                    self.textbox.delete("1.0", tk.END)
                    self.read_latch()

    # Cypher functions
    def pad(self, s):
        return s + b'\0' * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b'\0')

    def b64encode(self, message):
        return base64.b64encode(message)

    def b64decode(self, message):
        return base64.b64decode(message)

    def quit(self, event=None):
        self.read_evt = False
        self.get_view.mainwindow.master.destroy()
