# Copyright (c) 2008 The Board of Trustees of The Leland Stanford Junior University
# Copyright (c) 2011, 2012 Open Networking Foundation
# Copyright (c) 2012, 2013 Big Switch Networks, Inc.
# See the file LICENSE.pyloxi which should have been included in the source distribution

# Automatically generated by LOXI from template module.py
# Do not modify

import struct
import loxi
from . import util
import loxi.generic_util

import sys
ofp = sys.modules['loxi.of13']

class action(loxi.OFObject):
    subtypes = {}


    def __init__(self, type=None):
        self.type = type if type != None else 0
        return

    def pack(self):
        packed = [struct.pack("!H", self.type)]
        packed.extend((struct.pack("!H", 0), '\x00' * 4))
        length = sum(len(x) for x in packed)
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        subtype, = reader.peek('!H', 0)
        if subclass := action.subtypes.get(subtype):
            return subclass.unpack(reader)

        obj = action()
        obj.type = reader.read("!H")[0]
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        reader.skip(4)
        return obj

    def __eq__(self, other):
        return False if type(self) != type(other) else self.type == other.type

    def pretty_print(self, q):
        q.text("action {")
        with q.group():
            with q.indent(2):
                q.breakable()
            q.breakable()
        q.text('}')


class experimenter(action):
    subtypes = {}

    type = 65535

    def __init__(self, experimenter=None, data=None):
        self.experimenter = experimenter if experimenter != None else 0
        self.data = data if data != None else ''
        return

    def pack(self):
        packed = [struct.pack("!H", self.type)]
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append(struct.pack("!L", self.experimenter))
        packed.append(self.data)
        length = sum(len(x) for x in packed)
        packed.append(loxi.generic_util.pad_to(8, length))
        length += len(packed[-1])
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        subtype, = reader.peek('!L', 4)
        if subclass := experimenter.subtypes.get(subtype):
            return subclass.unpack(reader)

        obj = experimenter()
        _type = reader.read("!H")[0]
        assert(_type == 65535)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        obj.experimenter = reader.read("!L")[0]
        obj.data = str(reader.read_all())
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        if self.experimenter != other.experimenter: return False
        return self.data == other.data

    def pretty_print(self, q):
        q.text("experimenter {")
        with q.group():
            with q.indent(2):
                q.breakable()
                q.text("data = ");
                q.pp(self.data)
            q.breakable()
        q.text('}')

action.subtypes[65535] = experimenter

class bsn(experimenter):
    subtypes = {}

    type = 65535
    experimenter = 6035143

    def __init__(self, subtype=None):
        self.subtype = subtype if subtype != None else 0
        return

    def pack(self):
        packed = [struct.pack("!H", self.type)]
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append(struct.pack("!L", self.experimenter))
        packed.extend((struct.pack("!L", self.subtype), '\x00' * 4))
        length = sum(len(x) for x in packed)
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        subtype, = reader.peek('!L', 8)
        if subclass := bsn.subtypes.get(subtype):
            return subclass.unpack(reader)

        obj = bsn()
        _type = reader.read("!H")[0]
        assert(_type == 65535)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        _experimenter = reader.read("!L")[0]
        assert(_experimenter == 6035143)
        obj.subtype = reader.read("!L")[0]
        reader.skip(4)
        return obj

    def __eq__(self, other):
        return False if type(self) != type(other) else self.subtype == other.subtype

    def pretty_print(self, q):
        q.text("bsn {")
        with q.group():
            with q.indent(2):
                q.breakable()
            q.breakable()
        q.text('}')

experimenter.subtypes[6035143] = bsn

class bsn_checksum(bsn):
    type = 65535
    experimenter = 6035143
    subtype = 4

    def __init__(self, checksum=None):
        self.checksum = checksum if checksum != None else 0
        return

    def pack(self):
        packed = [struct.pack("!H", self.type)]
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append(struct.pack("!L", self.experimenter))
        packed.append(struct.pack("!L", self.subtype))
        packed.append(util.pack_checksum_128(self.checksum))
        length = sum(len(x) for x in packed)
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = bsn_checksum()
        _type = reader.read("!H")[0]
        assert(_type == 65535)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        _experimenter = reader.read("!L")[0]
        assert(_experimenter == 6035143)
        _subtype = reader.read("!L")[0]
        assert(_subtype == 4)
        obj.checksum = util.unpack_checksum_128(reader)
        return obj

    def __eq__(self, other):
        return False if type(self) != type(other) else self.checksum == other.checksum

    def pretty_print(self, q):
        q.text("bsn_checksum {")
        with q.group():
            with q.indent(2):
                q.breakable()
                q.text("checksum = ");
                q.pp(self.checksum)
            q.breakable()
        q.text('}')

bsn.subtypes[4] = bsn_checksum

class bsn_gentable(bsn):
    type = 65535
    experimenter = 6035143
    subtype = 5

    def __init__(self, table_id=None, key=None):
        self.table_id = table_id if table_id != None else 0
        self.key = key if key != None else []
        return

    def pack(self):
        packed = [struct.pack("!H", self.type)]
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append(struct.pack("!L", self.experimenter))
        packed.append(struct.pack("!L", self.subtype))
        packed.append(struct.pack("!L", self.table_id))
        packed.append(loxi.generic_util.pack_list(self.key))
        length = sum(len(x) for x in packed)
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = bsn_gentable()
        _type = reader.read("!H")[0]
        assert(_type == 65535)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        _experimenter = reader.read("!L")[0]
        assert(_experimenter == 6035143)
        _subtype = reader.read("!L")[0]
        assert(_subtype == 5)
        obj.table_id = reader.read("!L")[0]
        obj.key = loxi.generic_util.unpack_list(reader, ofp.bsn_tlv.bsn_tlv.unpack)
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        return False if self.table_id != other.table_id else self.key == other.key

    def pretty_print(self, q):
        q.text("bsn_gentable {")
        with q.group():
            with q.indent(2):
                q.breakable()
                q.text("table_id = ");
                q.text("%#x" % self.table_id)
                q.text(","); q.breakable()
                q.text("key = ");
                q.pp(self.key)
            q.breakable()
        q.text('}')

bsn.subtypes[5] = bsn_gentable

class bsn_mirror(bsn):
    type = 65535
    experimenter = 6035143
    subtype = 1

    def __init__(self, dest_port=None, vlan_tag=None, copy_stage=None):
        self.dest_port = dest_port if dest_port != None else 0
        self.vlan_tag = vlan_tag if vlan_tag != None else 0
        self.copy_stage = copy_stage if copy_stage != None else 0
        return

    def pack(self):
        packed = [struct.pack("!H", self.type)]
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append(struct.pack("!L", self.experimenter))
        packed.append(struct.pack("!L", self.subtype))
        packed.append(struct.pack("!L", self.dest_port))
        packed.append(struct.pack("!L", self.vlan_tag))
        packed.extend((struct.pack("!B", self.copy_stage), '\x00' * 3))
        length = sum(len(x) for x in packed)
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = bsn_mirror()
        _type = reader.read("!H")[0]
        assert(_type == 65535)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        _experimenter = reader.read("!L")[0]
        assert(_experimenter == 6035143)
        _subtype = reader.read("!L")[0]
        assert(_subtype == 1)
        obj.dest_port = reader.read("!L")[0]
        obj.vlan_tag = reader.read("!L")[0]
        obj.copy_stage = reader.read("!B")[0]
        reader.skip(3)
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        if self.dest_port != other.dest_port: return False
        if self.vlan_tag != other.vlan_tag: return False
        return self.copy_stage == other.copy_stage

    def pretty_print(self, q):
        q.text("bsn_mirror {")
        with q.group():
            with q.indent(2):
                q.breakable()
                q.text("dest_port = ");
                q.text("%#x" % self.dest_port)
                q.text(","); q.breakable()
                q.text("vlan_tag = ");
                q.text("%#x" % self.vlan_tag)
                q.text(","); q.breakable()
                q.text("copy_stage = ");
                q.text("%#x" % self.copy_stage)
            q.breakable()
        q.text('}')

bsn.subtypes[1] = bsn_mirror

class bsn_set_tunnel_dst(bsn):
    type = 65535
    experimenter = 6035143
    subtype = 2

    def __init__(self, dst=None):
        self.dst = dst if dst != None else 0
        return

    def pack(self):
        packed = [struct.pack("!H", self.type)]
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append(struct.pack("!L", self.experimenter))
        packed.append(struct.pack("!L", self.subtype))
        packed.append(struct.pack("!L", self.dst))
        length = sum(len(x) for x in packed)
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = bsn_set_tunnel_dst()
        _type = reader.read("!H")[0]
        assert(_type == 65535)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        _experimenter = reader.read("!L")[0]
        assert(_experimenter == 6035143)
        _subtype = reader.read("!L")[0]
        assert(_subtype == 2)
        obj.dst = reader.read("!L")[0]
        return obj

    def __eq__(self, other):
        return False if type(self) != type(other) else self.dst == other.dst

    def pretty_print(self, q):
        q.text("bsn_set_tunnel_dst {")
        with q.group():
            with q.indent(2):
                q.breakable()
                q.text("dst = ");
                q.text("%#x" % self.dst)
            q.breakable()
        q.text('}')

bsn.subtypes[2] = bsn_set_tunnel_dst

class copy_ttl_in(action):
    type = 12

    def __init__(self):
        return

    def pack(self):
        packed = [struct.pack("!H", self.type)]
        packed.extend((struct.pack("!H", 0), '\x00' * 4))
        length = sum(len(x) for x in packed)
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = copy_ttl_in()
        _type = reader.read("!H")[0]
        assert(_type == 12)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        reader.skip(4)
        return obj

    def __eq__(self, other):
        return type(self) == type(other)

    def pretty_print(self, q):
        q.text("copy_ttl_in {")
        with q.group():
            with q.indent(2):
                q.breakable()
            q.breakable()
        q.text('}')

action.subtypes[12] = copy_ttl_in

class copy_ttl_out(action):
    type = 11

    def __init__(self):
        return

    def pack(self):
        packed = [struct.pack("!H", self.type)]
        packed.extend((struct.pack("!H", 0), '\x00' * 4))
        length = sum(len(x) for x in packed)
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = copy_ttl_out()
        _type = reader.read("!H")[0]
        assert(_type == 11)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        reader.skip(4)
        return obj

    def __eq__(self, other):
        return type(self) == type(other)

    def pretty_print(self, q):
        q.text("copy_ttl_out {")
        with q.group():
            with q.indent(2):
                q.breakable()
            q.breakable()
        q.text('}')

action.subtypes[11] = copy_ttl_out

class dec_mpls_ttl(action):
    type = 16

    def __init__(self):
        return

    def pack(self):
        packed = [struct.pack("!H", self.type)]
        packed.extend((struct.pack("!H", 0), '\x00' * 4))
        length = sum(len(x) for x in packed)
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = dec_mpls_ttl()
        _type = reader.read("!H")[0]
        assert(_type == 16)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        reader.skip(4)
        return obj

    def __eq__(self, other):
        return type(self) == type(other)

    def pretty_print(self, q):
        q.text("dec_mpls_ttl {")
        with q.group():
            with q.indent(2):
                q.breakable()
            q.breakable()
        q.text('}')

action.subtypes[16] = dec_mpls_ttl

class dec_nw_ttl(action):
    type = 24

    def __init__(self):
        return

    def pack(self):
        packed = [struct.pack("!H", self.type)]
        packed.extend((struct.pack("!H", 0), '\x00' * 4))
        length = sum(len(x) for x in packed)
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = dec_nw_ttl()
        _type = reader.read("!H")[0]
        assert(_type == 24)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        reader.skip(4)
        return obj

    def __eq__(self, other):
        return type(self) == type(other)

    def pretty_print(self, q):
        q.text("dec_nw_ttl {")
        with q.group():
            with q.indent(2):
                q.breakable()
            q.breakable()
        q.text('}')

action.subtypes[24] = dec_nw_ttl

class group(action):
    type = 22

    def __init__(self, group_id=None):
        self.group_id = group_id if group_id != None else 0
        return

    def pack(self):
        packed = [struct.pack("!H", self.type)]
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append(struct.pack("!L", self.group_id))
        length = sum(len(x) for x in packed)
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = group()
        _type = reader.read("!H")[0]
        assert(_type == 22)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        obj.group_id = reader.read("!L")[0]
        return obj

    def __eq__(self, other):
        return False if type(self) != type(other) else self.group_id == other.group_id

    def pretty_print(self, q):
        q.text("group {")
        with q.group():
            with q.indent(2):
                q.breakable()
                q.text("group_id = ");
                q.text("%#x" % self.group_id)
            q.breakable()
        q.text('}')

action.subtypes[22] = group

class nicira(experimenter):
    subtypes = {}

    type = 65535
    experimenter = 8992

    def __init__(self, subtype=None):
        self.subtype = subtype if subtype != None else 0
        return

    def pack(self):
        packed = [struct.pack("!H", self.type)]
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append(struct.pack("!L", self.experimenter))
        packed.extend((struct.pack("!H", self.subtype), '\x00' * 2, '\x00' * 4))
        length = sum(len(x) for x in packed)
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        subtype, = reader.peek('!H', 8)
        if subclass := nicira.subtypes.get(subtype):
            return subclass.unpack(reader)

        obj = nicira()
        _type = reader.read("!H")[0]
        assert(_type == 65535)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        _experimenter = reader.read("!L")[0]
        assert(_experimenter == 8992)
        obj.subtype = reader.read("!H")[0]
        reader.skip(2)
        reader.skip(4)
        return obj

    def __eq__(self, other):
        return False if type(self) != type(other) else self.subtype == other.subtype

    def pretty_print(self, q):
        q.text("nicira {")
        with q.group():
            with q.indent(2):
                q.breakable()
            q.breakable()
        q.text('}')

experimenter.subtypes[8992] = nicira

class nicira_dec_ttl(nicira):
    type = 65535
    experimenter = 8992
    subtype = 18

    def __init__(self):
        return

    def pack(self):
        packed = [struct.pack("!H", self.type)]
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append(struct.pack("!L", self.experimenter))
        packed.extend((struct.pack("!H", self.subtype), '\x00' * 2, '\x00' * 4))
        length = sum(len(x) for x in packed)
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = nicira_dec_ttl()
        _type = reader.read("!H")[0]
        assert(_type == 65535)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        _experimenter = reader.read("!L")[0]
        assert(_experimenter == 8992)
        _subtype = reader.read("!H")[0]
        assert(_subtype == 18)
        reader.skip(2)
        reader.skip(4)
        return obj

    def __eq__(self, other):
        return type(self) == type(other)

    def pretty_print(self, q):
        q.text("nicira_dec_ttl {")
        with q.group():
            with q.indent(2):
                q.breakable()
            q.breakable()
        q.text('}')

nicira.subtypes[18] = nicira_dec_ttl

class output(action):
    type = 0

    def __init__(self, port=None, max_len=None):
        self.port = port if port != None else 0
        self.max_len = max_len if max_len != None else 0
        return

    def pack(self):
        packed = [struct.pack("!H", self.type)]
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append(util.pack_port_no(self.port))
        packed.extend((struct.pack("!H", self.max_len), '\x00' * 6))
        length = sum(len(x) for x in packed)
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = output()
        _type = reader.read("!H")[0]
        assert(_type == 0)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        obj.port = util.unpack_port_no(reader)
        obj.max_len = reader.read("!H")[0]
        reader.skip(6)
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        return False if self.port != other.port else self.max_len == other.max_len

    def pretty_print(self, q):
        q.text("output {")
        with q.group():
            with q.indent(2):
                q.breakable()
                q.text("port = ");
                q.text(util.pretty_port(self.port))
                q.text(","); q.breakable()
                q.text("max_len = ");
                q.text("%#x" % self.max_len)
            q.breakable()
        q.text('}')

action.subtypes[0] = output

class pop_mpls(action):
    type = 20

    def __init__(self, ethertype=None):
        self.ethertype = ethertype if ethertype != None else 0
        return

    def pack(self):
        packed = [struct.pack("!H", self.type)]
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.extend((struct.pack("!H", self.ethertype), '\x00' * 2))
        length = sum(len(x) for x in packed)
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = pop_mpls()
        _type = reader.read("!H")[0]
        assert(_type == 20)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        obj.ethertype = reader.read("!H")[0]
        reader.skip(2)
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        return self.ethertype == other.ethertype

    def pretty_print(self, q):
        q.text("pop_mpls {")
        with q.group():
            with q.indent(2):
                q.breakable()
                q.text("ethertype = ");
                q.text("%#x" % self.ethertype)
            q.breakable()
        q.text('}')

action.subtypes[20] = pop_mpls

class pop_pbb(action):
    type = 27

    def __init__(self):
        return

    def pack(self):
        packed = [struct.pack("!H", self.type)]
        packed.extend((struct.pack("!H", 0), '\x00' * 4))
        length = sum(len(x) for x in packed)
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = pop_pbb()
        _type = reader.read("!H")[0]
        assert(_type == 27)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        reader.skip(4)
        return obj

    def __eq__(self, other):
        return type(self) == type(other)

    def pretty_print(self, q):
        q.text("pop_pbb {")
        with q.group():
            with q.indent(2):
                q.breakable()
            q.breakable()
        q.text('}')

action.subtypes[27] = pop_pbb

class pop_vlan(action):
    type = 18

    def __init__(self):
        return

    def pack(self):
        packed = [struct.pack("!H", self.type)]
        packed.extend((struct.pack("!H", 0), '\x00' * 4))
        length = sum(len(x) for x in packed)
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = pop_vlan()
        _type = reader.read("!H")[0]
        assert(_type == 18)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        reader.skip(4)
        return obj

    def __eq__(self, other):
        return type(self) == type(other)

    def pretty_print(self, q):
        q.text("pop_vlan {")
        with q.group():
            with q.indent(2):
                q.breakable()
            q.breakable()
        q.text('}')

action.subtypes[18] = pop_vlan

class push_mpls(action):
    type = 19

    def __init__(self, ethertype=None):
        self.ethertype = ethertype if ethertype != None else 0
        return

    def pack(self):
        packed = [struct.pack("!H", self.type)]
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.extend((struct.pack("!H", self.ethertype), '\x00' * 2))
        length = sum(len(x) for x in packed)
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = push_mpls()
        _type = reader.read("!H")[0]
        assert(_type == 19)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        obj.ethertype = reader.read("!H")[0]
        reader.skip(2)
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        return self.ethertype == other.ethertype

    def pretty_print(self, q):
        q.text("push_mpls {")
        with q.group():
            with q.indent(2):
                q.breakable()
                q.text("ethertype = ");
                q.text("%#x" % self.ethertype)
            q.breakable()
        q.text('}')

action.subtypes[19] = push_mpls

class push_pbb(action):
    type = 26

    def __init__(self, ethertype=None):
        self.ethertype = ethertype if ethertype != None else 0
        return

    def pack(self):
        packed = [struct.pack("!H", self.type)]
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.extend((struct.pack("!H", self.ethertype), '\x00' * 2))
        length = sum(len(x) for x in packed)
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = push_pbb()
        _type = reader.read("!H")[0]
        assert(_type == 26)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        obj.ethertype = reader.read("!H")[0]
        reader.skip(2)
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        return self.ethertype == other.ethertype

    def pretty_print(self, q):
        q.text("push_pbb {")
        with q.group():
            with q.indent(2):
                q.breakable()
                q.text("ethertype = ");
                q.text("%#x" % self.ethertype)
            q.breakable()
        q.text('}')

action.subtypes[26] = push_pbb

class push_vlan(action):
    type = 17

    def __init__(self, ethertype=None):
        self.ethertype = ethertype if ethertype != None else 0
        return

    def pack(self):
        packed = [struct.pack("!H", self.type)]
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.extend((struct.pack("!H", self.ethertype), '\x00' * 2))
        length = sum(len(x) for x in packed)
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = push_vlan()
        _type = reader.read("!H")[0]
        assert(_type == 17)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        obj.ethertype = reader.read("!H")[0]
        reader.skip(2)
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        return self.ethertype == other.ethertype

    def pretty_print(self, q):
        q.text("push_vlan {")
        with q.group():
            with q.indent(2):
                q.breakable()
                q.text("ethertype = ");
                q.text("%#x" % self.ethertype)
            q.breakable()
        q.text('}')

action.subtypes[17] = push_vlan

class set_field(action):
    type = 25

    def __init__(self, field=None):
        self.field = field if field != None else None
        return

    def pack(self):
        packed = [struct.pack("!H", self.type)]
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append(self.field.pack())
        length = sum(len(x) for x in packed)
        packed.append(loxi.generic_util.pad_to(8, length))
        length += len(packed[-1])
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = set_field()
        _type = reader.read("!H")[0]
        assert(_type == 25)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        obj.field = ofp.oxm.oxm.unpack(reader)
        return obj

    def __eq__(self, other):
        return False if type(self) != type(other) else self.field == other.field

    def pretty_print(self, q):
        q.text("set_field {")
        with q.group():
            with q.indent(2):
                q.breakable()
                q.text("field = ");
                q.pp(self.field)
            q.breakable()
        q.text('}')

action.subtypes[25] = set_field

class set_mpls_ttl(action):
    type = 15

    def __init__(self, mpls_ttl=None):
        self.mpls_ttl = mpls_ttl if mpls_ttl != None else 0
        return

    def pack(self):
        packed = [struct.pack("!H", self.type)]
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.extend((struct.pack("!B", self.mpls_ttl), '\x00' * 3))
        length = sum(len(x) for x in packed)
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = set_mpls_ttl()
        _type = reader.read("!H")[0]
        assert(_type == 15)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        obj.mpls_ttl = reader.read("!B")[0]
        reader.skip(3)
        return obj

    def __eq__(self, other):
        return False if type(self) != type(other) else self.mpls_ttl == other.mpls_ttl

    def pretty_print(self, q):
        q.text("set_mpls_ttl {")
        with q.group():
            with q.indent(2):
                q.breakable()
                q.text("mpls_ttl = ");
                q.text("%#x" % self.mpls_ttl)
            q.breakable()
        q.text('}')

action.subtypes[15] = set_mpls_ttl

class set_nw_ttl(action):
    type = 23

    def __init__(self, nw_ttl=None):
        self.nw_ttl = nw_ttl if nw_ttl != None else 0
        return

    def pack(self):
        packed = [struct.pack("!H", self.type)]
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.extend((struct.pack("!B", self.nw_ttl), '\x00' * 3))
        length = sum(len(x) for x in packed)
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = set_nw_ttl()
        _type = reader.read("!H")[0]
        assert(_type == 23)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        obj.nw_ttl = reader.read("!B")[0]
        reader.skip(3)
        return obj

    def __eq__(self, other):
        return False if type(self) != type(other) else self.nw_ttl == other.nw_ttl

    def pretty_print(self, q):
        q.text("set_nw_ttl {")
        with q.group():
            with q.indent(2):
                q.breakable()
                q.text("nw_ttl = ");
                q.text("%#x" % self.nw_ttl)
            q.breakable()
        q.text('}')

action.subtypes[23] = set_nw_ttl

class set_queue(action):
    type = 21

    def __init__(self, queue_id=None):
        self.queue_id = queue_id if queue_id != None else 0
        return

    def pack(self):
        packed = [struct.pack("!H", self.type)]
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append(struct.pack("!L", self.queue_id))
        length = sum(len(x) for x in packed)
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = set_queue()
        _type = reader.read("!H")[0]
        assert(_type == 21)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        obj.queue_id = reader.read("!L")[0]
        return obj

    def __eq__(self, other):
        return False if type(self) != type(other) else self.queue_id == other.queue_id

    def pretty_print(self, q):
        q.text("set_queue {")
        with q.group():
            with q.indent(2):
                q.breakable()
                q.text("queue_id = ");
                q.text("%#x" % self.queue_id)
            q.breakable()
        q.text('}')

action.subtypes[21] = set_queue


