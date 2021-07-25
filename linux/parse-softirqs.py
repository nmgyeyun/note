#!/usr/bin/env python
# -*-coding:utf-8-*-
# import os
import sys
# import json
import time

softirq_path = "/proc/softirqs"

g_softirq_types = []
g_cpus = []
g_last_irqs = {}
g_inc_irqs = {}
g_interval = 3
g_output_total = 1

g_count = 0


def usage():
    print 'Usage:'
    print '    python %s <interval>\n' % sys.argv[0]
    print '      interval: seconds, default 3 seconds\n'


"""
cat /proc/softirqs 
                    CPU0       CPU1       
          HI:          0          7
       TIMER:    1783040    2620321
      NET_TX:      37699          3
      NET_RX:     281629     835955
       BLOCK:      46047          0
BLOCK_IOPOLL:          0          0
     TASKLET:          1        162
       SCHED:    1522756    1489384
     HRTIMER:          0          0
         RCU:     407251     890017
"""


def output_irq_title():
    line = ""
    for i in g_softirq_types:
        line += "%13.13s" % i
    print "%s" % line


def get_cpus():
    global g_cpus
    g_cpus = ['TOTAL']
    with open(softirq_path) as fp:
        line = fp.readline()
    header = line.strip().split(' ')
    for cpu in header:
        if cpu != '':
            g_cpus.append(cpu)


def get_softirq_types():
    global g_softirq_types
    g_softirq_types =  []
    with open(softirq_path) as fp:
        lines = fp.readlines()
    for line in lines:

        header = line.strip().split(':')
        if len(header) == 2:
            g_softirq_types.append(header[0])
    #g_softirq_types = list(set(g_softirq_types))


def output():
    global g_inc_irqs
    global g_count

    if g_count % 30 == 0:
        output_irq_title()
    g_count = g_count + 1

    if g_output_total:
        line = ""
        for irq in g_softirq_types:
            v = g_inc_irqs.get(irq, None)
            if v:
                total = v[0]
            else:
                total = 0
            # outstr = '%13.3f' % (total / 1000)
            outstr = '%13.2f' % (total)
            line += outstr
        print "%s" % line


def output_list(ident, l):
    line = "%10s " % ident
    for i in l:
        line += "%7d " % i
    print line

def main():
    if (len(sys.argv) < 2):
        pass
        # usage()
        # return

    get_softirq_types()

    global g_last_irqs
    global g_inc_irqs
    while (1):

        with open(softirq_path) as fp:
            lines = fp.readlines()

        for i, line in enumerate(lines):
            if i == 0:
                continue
            data = line.strip().split()
            data = [x.strip() for x in data if x != '']

            irq = data[0][0:-1]
            new_value = [int(x) for x in data[1:]]
            new_value.insert(0, sum(new_value))

            last_value = g_last_irqs.get(irq, None)
            if last_value:
                g_inc_irqs[irq] = [(x - y) * 1.0 / g_interval for x, y in zip(new_value, last_value)]

                # for debug
                # output_list(irq + " l", last_value)
                # output_list(irq + " n", new_value)

            g_last_irqs[irq] = new_value
        output()
        time.sleep(g_interval)


if __name__ == "__main__":
    main()
