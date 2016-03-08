"""
Mail interface for gmail
"""
import gmail
import logging
import datetime
logger = logging.getLogger(__name__)
import os

class Mail:

    username = None
    password = None
    g = None
    before = datetime.datetime.now()
    after = datetime.datetime.now() - datetime.timedelta(minutes=1)
    message_file = 'status_message.txt'

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.login()

    def login(self):
        try:
            gl = gmail.login(self.username, self.password)
            self.g = gl
        except:
            raise

    def search_mail(self, after=None, before=None):
        # if after is not None: self.after = after
        # if before is not None: self.before = before
        try:

            mails = self.g.inbox().mail(after=self.after, before=self.before)
            if mails is not None:
                mails[0].fetch()
                print mails[0].subject
        except:
            raise

    def generate_status(self, to='rsingh@loggly.com'):
        if os.path.isfile(os.path.dirname(os.path.abspath(__file__))+'/'+self.message_file):
            body_message = ''
            f = open(self.message_file, 'r')
            for line in f:
                body_message+=line
            if body_message!='':
                confirm = raw_input('Status Confirmed?. [yes, no]: ')
                if confirm == 'yes':
                    print 'sent'
                else:
                    print 'You can modify your message from file.'


class Task:

    task_list = []
    greetings = 'Greetings!!'
    message_file = 'status_message.txt'
    def create_status(self):
        """
        Create a status
        :return:
        """
        self.greetings = raw_input('Enter greetings message: ')
        cont = True
        while cont:
            task = raw_input('New Task?. [yes, no]: ')
            if task == 'yes':
                task_obj = {}
                title = raw_input('Title: ')
                status = raw_input('Status: ')
                blocker = raw_input('Blocker: ')
                task_obj['title'] = title
                task_obj['status'] = status
                task_obj['blocker'] = blocker
                self.task_list.append(task_obj)
            elif task == 'no':
                cont = False
        print self.task_list

    def generate_message(self):
        if self.task_list.__len__() > 0:
            f = open(self.message_file, 'w')
            f.write(self.greetings)
            f.write('\n\n\n')
            for t in self.task_list:
                f.write('-- {}\n'.format(t['title']))
                f.write('\t\bStatus\b: {}\n'.format(t['status']))

                if t['blocker']!='':
                    f.write('\t\bBlocker\b: {}\n'.format(t['blocker']))
                f.write('\n')
            f.close()
        else:
            print 'No status for write'





if __name__ == '__main__':
    g = Mail('rsingh@loggly.com', 'rsingh@loggly')
    t = Task()
    t.create_status()
    t.generate_message()
    g.generate_status()




