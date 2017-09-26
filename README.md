![Version](https://img.shields.io/badge/python-v2.7.13-blue.svg?style=flat-square)
![License](https://img.shields.io/badge/license-AGPL-green.svg?style=flat-square)

# Latch'sApp

Latch’sApp is a tool for Data Exfiltration through a covert channel using Latch technology. Sensitive messages and files may be sent by codifying their contents into bits at position N of the Latch locks. The recipient can read the position of the Latch locks and interpret which bit/byte is being sent. Steganography is used in this tool, as it conceals files and messages in the Latch lock positions. Furthermore, for data protection purposes, the transformation of the bits at the Latch lock positions is encrypted by AES through a derivation function of APPID, which will recognize both the client and the server.

![LatchsApp](https://raw.githubusercontent.com/toolsprods/LatchsApp/master/img/Screenshot.png)

Install
=======
Before you begin, you need access to the creation of various operations in your latch account.
To get an application ID, secret and operations it’s necessary to register a developer account in Latch's website. On the upper right side, click on "Developer area".
To get the account ID use the "pair.sh" script.
Add this information to the beginning of the script "controller.py".

Install the dependencies and run:
```
pip install -r requirements.txt
python main.py
```

License
=======
This project is licensed under the AGPL Affero General Public License - see the LICENSE file for details
