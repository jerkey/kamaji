from subprocess import PIPE, Popen, TimeoutExpired

def get_hydro_stats():
    p = Popen("timeout --preserve-status 1 sox -q -t alsa hw:1,0 -c 1 -n stat", shell=True, stdout=PIPE, stderr=PIPE)
    stderr = p.communicate()[1].decode()
    #print("stderr: '%s'" % stderr)

    hydro_stats = {}
    for i in stderr.splitlines():
        #print(i)
        j = i.split()
        if len(j) > 1:
            #print             ({" ".join(j[0:-1]), j[-1]})
            hydro_stats.update([(" ".join(j[0:-1]), j[-1])])
    return hydro_stats

def print_date():
    print(Popen("date +%Y%m%d_%H%M%S", shell=True, stdout=PIPE, stderr=PIPE).communicate()[0].decode(), end='')

def reset_water_heater():
    try:
        process = Popen('gpioset -c gpiochip0 27=1', shell=True) # activate hydrogenerator disconnect relay
        process.communicate(timeout=1)
    except TimeoutExpired:
        process.kill()

    try:
        process = Popen('gpioset -c gpiochip0 27=0', shell=True) # de-activate hydrogenerator disconnect relay
        process.communicate(timeout=1)
    except TimeoutExpired:
        process.kill()

    print('reset_water_heater ', end='')
    print_date()

water_heater_misbehaving = 0 # counter of how bad the situation is

if __name__ == "__main__":
    while True:
        stats = get_hydro_stats()
        MIDLINE = float(stats['Midline amplitude:'])
        #MEAN = float(stats['Mean amplitude:'])
        FREQUENCY = float(stats['Rough frequency:'])
        ADJUSTMENT = float(stats['Volume adjustment:'])
        print("{:.4f}".format(MIDLINE), end='	')
        print("{:.0f}".format(FREQUENCY), end='	')
        print("{:2.3f}".format(ADJUSTMENT), end='	')
        print(water_heater_misbehaving, end='	')
        print_date()

        if (MIDLINE > 0.01) and (MIDLINE < 0.07) and (FREQUENCY > 1200) and (ADJUSTMENT < 10):
            print('+', end='')
            water_heater_misbehaving += 1
        else:
            water_heater_misbehaving = 0

        if (water_heater_misbehaving > 2):
            reset_water_heater()
            water_heater_misbehaving = 0

# 0.3900  1325    1.086   0       20261121_015542
# 0.0174  1209    5.516   0       20261121_015543
# 0.4237  1280    1.005   0       20261121_015544
# 0.0172  1256    5.721   0       20261121_015546
# 0.0166  1340    6.049   0       20261121_015547
# 0.0156  1473    6.660   0       20261121_015548
# 0.0179  2126    7.498   0       20261121_015549
# 0.0193  2522    7.194   0       20261121_015551
# 0.0255  3563    6.203   0       20261121_015552
# 0.0249  3546    6.151   1       20261121_015553
# 0.0242  2663    5.867   2       20261121_015554
# Traceback (most recent call last):
#   File "/home/pi/kamaji/kamaji.py", line 45, in <module>
#     reset_water_heater()
#     ~~~~~~~~~~~~~~~~~~^^
#   File "/home/pi/kamaji/kamaji.py", line 18, in reset_water_heater
#     Popen('timeout 1 gpioset -c gpiochip0 27=1') # activate hydrogenerator disconnect relay
#     ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/usr/lib/python3.13/subprocess.py", line 1039, in __init__
#     self._execute_child(args, executable, preexec_fn, close_fds,
#     ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#                         pass_fds, cwd, env,
#                         ^^^^^^^^^^^^^^^^^^^
#     ...<5 lines>...
#                         gid, gids, uid, umask,
#                         ^^^^^^^^^^^^^^^^^^^^^^
#                         start_new_session, process_group)
#                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/usr/lib/python3.13/subprocess.py", line 1972, in _execute_child
#     raise child_exception_type(errno_num, err_msg, err_filename)
# FileNotFoundError: [Errno 2] No such file or directory: 'timeout 1 gpioset -c gpiochip0 27=1'

#0.005859        0.006973        1638    64.000
#0.006180        0.007204        1697    57.690
#0.006607        0.006812        1789    57.087

#0.017746        0.007985        1085    5.274
#0.017487        0.007763        1090    5.295

#{'Samples read:': '40960',
# 'Length (seconds):': '0.853333',
# 'Scaled by:': '2147483647.0',
# 'Maximum amplitude:': '0.018036',
# 'Minimum amplitude:': '-0.003448',
# 'Midline amplitude:': '0.007294',
# 'Mean norm:': '0.007286',
# 'Mean amplitude:': '0.007286',
# 'RMS amplitude:': '0.007500',
# 'Maximum delta:': '0.009186',
# 'Minimum delta:': '0.000000',
# 'Mean delta:': '0.000906',
# 'RMS delta:': '0.001568',
# 'Rough frequency:': '1596',
# 'Volume adjustment:': '55.445'}

