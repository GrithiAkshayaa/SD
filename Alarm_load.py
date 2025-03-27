from confd import maapi, maagic

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
maapi.connect(sock, "127.0.0.1", 4565)
maapi.start_user_session(sock, "admin", "system", [], "127.0.0.1", maapi.AUTH_LOCAL)
th = maapi.start_trans(sock, maapi.RUNNING, maapi.READ_WRITE)

root = maagic.get_root(th)
root.alarms.alarm.create("1")  # Creates an alarm entry with id 1

maapi.apply_trans(th)
maapi.finish_trans(th)
maapi.end_user_session(sock)
maapi.disconnect(sock)
