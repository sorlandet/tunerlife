import multiprocessing

bind = "127.0.0.1:9000"
# bind = "unix:/home/proft/projects/blog/run/blog.socket"
workers = multiprocessing.cpu_count() * 2 + 1
user = "wwwpub"
group = "wwwpub"
loglevel = "info"
proc_name = 'wheel-size'
graceful_timeout = 60