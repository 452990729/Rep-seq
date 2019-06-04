#!/usr/bin/env python

import re

def kwargs_to_command_line_options(reserved_arguments=set(), sep=" ", long_prefix="--", short_prefix="-",
                                   replace_chars=dict(), **kwargs):
    """
    Convert **kwargs provided by user to a string usable command line programs as arguments.

    Args:
        reserved_arguments (set or list of str): set of arguments that this function prohibited for user use
        sep (str): separator between option/value pairs ('='for --jobmode=sge).
                   WARNING: switch args (--abc), which take no value, break if sep is not ' '
        long_prefix (str): prefix for options with more than one character ("--" for --quiet, for example)
        short_prefix (str): prefix for options with one character ("-" for -q, for example)
        replace_chars (dict): map of characters to replace in specified variable names
                            (if --align-reads is command-line option, specify align_reads with replace chars -> {'_':'-'}
        **kwargs (dict): **kawargs arguments/values to format string for

    Returns:
        str: string formatted appropriately for use as command line option. Returns no arguments provided.

    Raises:
        ValueError if user requested argument conflicts with one of the specified reserved arguments.

    """

    arguments = []
    reserved_arguments = set(reserved_arguments)

    for key, value in kwargs.iteritems():
        normalized_key = key.strip('-')

        # Replace characters for formatting
        for char, new_char in replace_chars.iteritems():
            normalized_key = normalized_key.replace(char, new_char)

        # Validate user inputs to make sure no blatant conflicts
        if normalized_key in reserved_arguments:
            raise ValueError('Specified option conflicts with reserved argument: %s. \
                             Reserved arguments are: %s' % (normalized_key, ','.join(reserved_arguments)))

        # Correctly prefix arguments
        if len(key) > 1:
            prefix = long_prefix
        else:
            prefix = short_prefix

        argument = '%s%s' % (prefix, normalized_key)
        option_value = kwargs.get(key) if kwargs.get(key) is not None else ''
        arguments.append('%s%s%s' % (argument, sep, option_value))

    return ' '.join(arguments)

class Sam(object):
    '''
    the sam alignment format
    '''
    def __init__(self, line_in):
        list_split = re.split('\t', line_in)
        self.line = line_in
        self.query = list_split[0]
        self.ref = list_split[2]

def ReadSam(file_in, type_receptor):
    '''
    read sam file -> [(f1, f2),]
    type_receptor: IG/TR
    '''
    i = 0
    list_re = []
    list_tmp = []
    with open(file_in, 'r') as in_sam:
        for line in in_sam:
            if not line.startswith('@'):
                i += 1
                ob = Sam(line.strip())
                list_tmp.append(ob)
                if i == 2:
                    if re.search(type_receptor, list_tmp[0].ref) and \
                       list_tmp[0].ref == list_tmp[1].ref:
                        list_re.append(list_tmp[0])
                    list_tmp = []
                    i = 0
    return list_re

