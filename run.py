# -*- coding: UTF-8 -*-

from BulkEmails import *

from argparse import ArgumentParser


def test():
    print("test")


if __name__ == '__main__':
    #####

    # parameters management
    args_parser = ArgumentParser(
        description="Send Custom Bulk Emails by Yacine YADDADEN [ https://github.com/yyaddaden ]")
    args_parser.version = "1.0"

    group = args_parser.add_argument_group("send test email")
    group.add_argument(
        "-t", "--test", help="send test email", action="store_true")
    group.add_argument("-e", "--email", metavar="",
                       help="email address for testing", action="store")

    group = args_parser.add_argument_group("send bulk emails")
    group.add_argument(
        "-b", "--bulk", help="send bulk emails", action="store_true")
    group.add_argument("-s", "--subject", metavar="",
                       help="subject in bulk emails", action="store")
    group.add_argument("-m", "--mail", metavar="",
                       help="text file for the mail template", action="store")
    group.add_argument("-d", "--data", metavar="",
                       help="csv file for the data to include", action="store")
    group.add_argument("-l", "--limit", metavar="",
                       help="max emails per connection", action="store", type=int, default=None)

    args = args_parser.parse_args()

    # parameters validation & execution
    if(args.test):
        if(args.email):
            bulkEmails = BulkEmails()
            bulkEmails.send_test(args.email)
            bulkEmails.write_logs()
        else:
            args_parser.print_help()
            exit(1)

    elif(args.bulk):
        if(args.subject and args.mail and args.data):
            bulkEmails = BulkEmails()
            bulkEmails.send_emails(args.mail, args.data,
                                   args.subject, args.limit)
            bulkEmails.write_logs()
        else:
            args_parser.print_help()
            exit(1)

    else:
        args_parser.print_help()
