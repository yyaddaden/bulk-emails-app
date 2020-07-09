# bulk-emails-app

***A Python based command line tool allowing to send custom bulk emails.***

---

## Table of Contents

- [Requirements](#requirements)
- [Basic Usage](#basic-usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Requirements

This project is developed using these technologies:

- Programming Language: **Python 3.7.6 x64**
- Libraries: 
  - **smtplib** (SMTP protocol client): https://docs.python.org/3/library/smtplib.html
- Integrated Development Environment: **Microsoft Visual Studio code x64**

## Basic Usage

For now, two actions (commands) might executed :

- Sending test email
- Sending cutom bulk emails

> **Important** : *for both commands, you have to set the **`config.json`** file (see below).*

```yaml
{
    "server": "SERVER",
    "port": "SERVER_PORT",  
    "username": "USERNAME",
    "from": "EMAIL_ADDRESS",
    "password": "PASSWORD" 
}
```

At any time, you may execute the command `python ./run.py -h` to display the help & instructions:

```
usage: run.py [-h] [-t] [-e] [-b] [-s] [-m] [-d] [-l]

Send Custom Bulk Emails by Yacine YADDADEN [ https://github.com/yyaddaden ]

optional arguments:
  -h, --help       show this help message and exit

send test email:
  -t, --test       send test email
  -e , --email     email address for testing

send bulk emails:
  -b, --bulk       send bulk emails
  -s , --subject   subject in bulk emails
  -m , --mail      text file for the mail template
  -d , --data      csv file for the data to include
  -l , --limit     max emails per connection
```

### 1. Sending test email

> **Description** : *this command aims to verify and ensure that the **`config.json`** file is set correctly by sending a test email.*

This command requires two parameters :

1. **`-t`** *to choose the testing operation*,
2. **`-e EMAIL_ADDRESS`** *to indicate the email address to whom the test email will be sent*.

### 2. Sending custom bulk emails

> **Description** : *this command aims to send customized bulk emails.*

This command requires four parameters :

1. **`-b`** *to choose the bulk email operation*,
2. **`-s "SUBJECT"`** *to specify the subject of the emails*,
3. **`-m FILE_NAME.TXT`** *to specify the mail template file (.txt file) with **variables** that will be used*,
4. **`-d FILE_NAME.CSV`** *to specify the data file (.csv file with commas as separator) with **values** that repalce the **variables***.

**Example of data file (.csv file):**

```
ending_date,title,name,email
10 july 2020,Mr,Alex,alex.doe@hotmail.com
30 August 2020,Mme,Sofia,sofia.doe@gmail.com 
```

> **Important** : *in the data file (.csv file with commas as separator), a variable is required which is **`email`***.

**Example of mail template file (.txt file):**

```
Hi %title% %name%,

We inform you that your subscription ends in %ending_date%.

Thank you.
```

Which gives after replacing the variable for the first row of the data file (.csv file):

```
Hi Mr Alex,

We inform you that your subscription ends in 10 july 2020.

Thank you.
```

> **Managing limitation** : *sometimes, the used server has a limitation in terms of number of emails to send per connection. In order to overcome this limitation, you can specify an optional parameter **`-l NUMBER_EMAILS_PER_CONNECTION`**. There will be **60 seconds** between two connections.*

## Features

For now, there are three main features which consist in :

1. Sending a test email in order to verfiy the configuration,
2. Sending bulk custom emails which is the main feature,
3. Saving the logs for every performed operation in **`logs.txt`**. 

## Contributing

> In order to contribue to this project, there are two options :

- **Option 1** : 🍴 Fork this repo!
- **Option 2** : 👯 Clone this repo to your local machine using `https://github.com/yyaddaden/bulk-emails-app.git`

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://opensource.org/licenses/mit-license.php)
