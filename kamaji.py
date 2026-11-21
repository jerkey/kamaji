from subprocess import PIPE, Popen

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

def reset_water_heater():
    Popen('timeout 1 gpioset -c gpiochip0 27=1') # activate hydrogenerator disconnect relay
    Popen('timeout 1 gpioset -c gpiochip0 27=0') # de-activate hydrogenerator disconnect relay

print(get_hydro_stats())

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

