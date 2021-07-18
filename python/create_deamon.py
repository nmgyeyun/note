def create_deamon():
    try:
        if os.fork() > 0:
            os._exit(0)
    except OSError as error:
        MyLog.info('fork myself failed:#1 %d(%s)' % (error.errno, error.strerror))
        os._exit(1)

    # child process
    os.chdir('/')
    os.setsid()
    os.umask(0)

    try:
        pid = os.fork()
        if pid > 0:
            MyLog.info('create deamon: %d' % pid)
            os._exit(0)
    except OSError as error:
        MyLog.info('fork myself failed:#2 %d (%s)' % (error.errno, error.strerror))
        os._exit(1)

    sys.stdout.flush()
    sys.stderr.flush()

    si = file("/dev/null", 'r')
    so = file("/dev/null", 'a+')
    se = file("/dev/null", 'a+', 0)

    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

