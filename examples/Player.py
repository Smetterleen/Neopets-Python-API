import secrets

try:
    raise Exception('Test')
    import Trainer
    import time
    import Banker
    from neopapi.core import Time
    from datetime import timedelta
    from neopapi.main import User
    import Investor
    
    tasks = []
    
    plugins = [Investor, Trainer, Banker]
    
    for plugin in plugins:
            time.sleep(1)
            tasks.append((Time.NST_time(), plugin))
    
    while True:
        if not User.is_logged_in(secrets.username):
            print("User is not logged in. Logging in")
            User.login(secrets.username, secrets.password)
            
        ordered_tasks = sorted(tasks, key=lambda x: x[0], reverse=True)
        first_task = ordered_tasks.pop()
        print('Plugin ' + first_task[1].__name__ + ' is first on the list')
        if first_task[0] > Time.NST_time():
            print('Waiting until %s NST (localtime: %s) to start %s' % (first_task[0].strftime('%x %X'), (first_task[0] + timedelta(hours=9)).strftime('%X'), first_task[1].__name__))
            time.sleep((first_task[0] - Time.NST_time()).total_seconds())
        print('Running ' + first_task[1].__name__)
        next_task_time = first_task[1].run()
        ordered_tasks.append((next_task_time, first_task[1]))
        tasks = ordered_tasks
except Exception as e:
    # Import smtplib for the actual sending function
    import smtplib
    
    # Import the email modules we'll need
    from email.mime.text import MIMEText
    
    # Create a text/plain message
    msg = MIMEText(str(e))
    
    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = 'Error'
    msg['From'] = secrets.email
    msg['To'] = secrets.email
    
    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP(secrets.smtp_server, secrets.smtp_port)
    s.login(secrets.email, secrets.email_pw)
    s.sendmail(secrets.email, [secrets.email], msg.as_string())
    s.quit()