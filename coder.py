""" Huffman coder """

import operator
import struct

from priority_queue import PriorityQueue
from tree_node import TreeNode


def prepare_frame(in_file, frame_len):
    """ Initialized frame with chars from file """

    success = True
    frame = ''
    while len(frame) < frame_len:
        char = in_file.read(1)
        if not char:
            success = False
            break
        else:
            frame += char
    return success, frame


def shift_frame(in_file, frame):
    """ Shifts frame with one char """

    success = True
    char = in_file.read(1)
    if not char:
        success = False
    else:
        frame = frame[1:] + char

    return success, frame

def update_frame(in_file, frame, frame_len):
    """ Updates frame so it matches the desired length """

    success = True
    while len(frame) < frame_len:
        char = in_file.read(1)
        if not char:
            success = False
            break
        else:
            frame += char
    return success, frame

def update_dict(code_dict, frame):
    """ Updates dictionary word counters """

    count = 0
    for i in xrange(len(frame)):
        word = frame[i:]
        if word in code_dict:
            code_dict[word] += 1
        else:
            code_dict[word] = 1
        count += 1
    return count

def process_tree(queue):
    """ Creates Huffman tree from priority queue """

    root = None
    while not queue.empty():
        first = queue.pop()
        if queue.empty():
            root = first
            break
        second = queue.pop()

        new_elem = TreeNode('?', first.probability + second.probability)

        new_elem.left = first
        new_elem.right = second

        queue.push(new_elem.probability, new_elem)

    return root

def initial_update(code_dict, frame):
    """ Updates code dictionary with all permutations of frame """

    count = 0
    for i in xrange(len(frame)):
        for j in xrange(i, len(frame)):
            word = frame[i:j+1]
            if word in code_dict:
                code_dict[word] += 1
            else:
                code_dict[word] = 1
            count += 1
    return count

def make_dict(in_file, di_file, frame_len):
    """ Creates codes dictionary from input file """

    code_dict = {}

    signs_len = 0

    success, frame = prepare_frame(in_file, frame_len)
    if success:
        signs_len += initial_update(code_dict, frame)

    while success:
        success, frame = shift_frame(in_file, frame)
        if success:
            signs_len += update_dict(code_dict, frame)

    print 'done dict'

    sorted_dict = sorted(code_dict.items(), key=operator.itemgetter(1))

    print 'sorted'

    tree_node_list = [TreeNode(x, k / float(signs_len)) for x, k in sorted_dict]

    print 'made nodes'

    queue = PriorityQueue()

    for item in tree_node_list:
        queue.push(item.probability, item)

    root = process_tree(queue)

    print 'got tree'

    root.set_code('')

    print 'made code'

    for item in tree_node_list:
        di_file.write(item.code + '|' + item.sign.encode('base64', 'strict'))

    print 'wrote file'

def read_dict(di_file):
    """ Recreates dict from file in sign -> code manner """

    code_dict = {}
    for word in di_file:
        parts = word.split('|')
        sign = parts[len(parts) - 1]
        code = parts[0]
        code_dict[sign[:-1]] = code
    return code_dict

def read_decode_dict(di_file):
    """ Recreates dict from file in code -> sign manner """

    code_dict = {}
    for word in di_file:
        parts = word.split('|')
        sign = parts[len(parts) - 1]
        code = parts[0]
        code_dict[code] = sign[:-1]
    return code_dict

def write_binary(out_file, code):
    """ Writes binary representation of code to file """

    binary = struct.pack('<ib', int(code, 2), len(code))
    out_file.write(binary)

def read_binary(in_file):
    """ Reads binary representation of code from file """

    binary = in_file.read(5)
    if not binary:
        return (True, '')
    else:
        code, leng = struct.unpack('<ib', binary)
        code2b = format(code, 'b')
        if len(code2b) < leng:
            for _ in range(leng - len(code2b)):
                code2b = '0' + code2b
        return (False, code2b)

def code_frame(out_file, code_dict, frame):
    """ Encodes frame based on dictionary """

    frame_len = len(frame)
    while frame_len != 0:
        frame_part = frame[:frame_len].encode('base64', 'strict').replace('\n', '')
        if frame_part in code_dict:
            write_binary(out_file, code_dict[frame_part])
            return frame[frame_len:]
        frame_len -= 1
    raise ValueError('Cannot match any code to frame ' + frame + '.')

def encode(in_file, di_file, out_file, frame_len):
    """ Encodes the input file based on dictionary """

    code_dict = read_dict(di_file)

    success, frame = update_frame(in_file, '', frame_len)

    while success:
        frame = code_frame(out_file, code_dict, frame)

        success, frame = update_frame(in_file, frame, frame_len)

    if frame != '':
        code_frame(out_file, code_dict, frame)

def decode(in_file, di_file, out_file):
    """ Decodes file based on dictionary """

    code_dict = read_decode_dict(di_file)

    code_part = ''
    eof = False

    while not eof:
        eof, code_part = read_binary(in_file)
        print code_part
        if not eof:
            out_file.write(code_dict[code_part].decode('base64', 'strict'))
