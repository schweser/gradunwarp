### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the gradunwarp package for the
#   copyright and license terms.
#
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
from collections import namedtuple
import numpy as np
import re
import globals
from globals import siemens_cas, ge_cas


log = globals.get_logger()


Coeffs = namedtuple('Coeffs', 'alpha_x, alpha_y, alpha_z, \
                        beta_x, beta_y, beta_z, R0_m')


def get_coefficients(vendor, cfile):
    ''' depending on the vendor and the coefficient file,
    return the spherical harmonics coefficients as a named tuple.
    '''
    if vendor == 'siemens' and cfile.endswith('.coef'):
        return get_siemens_coef(cfile)


def coef_file_parse(cfile, txt_var_map):
    ''' a separate function because GE and Siemens .coef files
    have similar structure

    modifies txt_var_map in place
    '''
    # parse .coef file. Strip unneeded characters. a valid line in that file is
    # broken into validline_list
    coef_re = re.compile('^[^\#]')  # regex for first character not a '#'
    coef_file = open(cfile, 'r')
    for line in coef_file.readlines():
        if coef_re.match(line):
            validline_list = line.lstrip(' \t').rstrip(';\n').split()
            if validline_list:
                log.info('Parsed : %s' % validline_list)
                l = validline_list
                x = int(l[1])
                y = int(l[2])
                txt_var_map[l[0]][x, y] = float(l[3])


def get_siemens_coef(cfile):
    ''' Parse the Siemens .coef file.
    Note that R0_m is not explicitly contained in the file
    '''
    R0m_map = {'sonata': 0.25,
               'avanto': 0.25,
               'quantum': 0.25,
               'allegra': 0.14,
               'as39s': 0.25,
               'as39st': 0.25,
               'as39t': 0.25}
    for rad in R0m_map.keys():
        if cfile.startswith(rad):
            R0_m = R0m_map[rad]

    coef_array_sz = siemens_cas
    # allegra is slightly different
    if cfile.startswith('allegra'):
        coef_array_sz = 15
    ax = ay = az = bx = by = bz = np.zeros((coef_array_sz, coef_array_sz))
    txt_var_map = {'Alpha_x': ax,
                   'Alpha_y': ay,
                   'Alpha_z': az,
                   'Beta_x': bx,
                   'Beta_y': by,
                   'Beta_z': bz}

    coef_file_parse(cfile, txt_var_map)

    return Coeffs(ax, ay, az, bx, by, bz, R0_m)


def get_ge_coef(cfile):
    ''' Parse the GE .coef file.
    '''
    ax = ay = az = bx = by = bz = np.zeros((ge_cas, ge_cas))
    txt_var_map = {'Alpha_x': ax,
                   'Alpha_y': ay,
                   'Alpha_z': az,
                   'Beta_x': bx,
                   'Beta_y': by,
                   'Beta_z': bz}

    coef_file_parse(cfile, txt_var_map)

    return Coeffs(ax, ay, az, bx, by, bz, R0_m)