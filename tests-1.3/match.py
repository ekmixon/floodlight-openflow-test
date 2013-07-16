# Distributed under the OpenFlow Software License (see LICENSE)
# Copyright (c) 2010 The Board of Trustees of The Leland Stanford Junior University
# Copyright (c) 2012, 2013 Big Switch Networks, Inc.
"""
Flow match test cases

These tests check the behavior of each match field. The only action used is a
single output.
"""

import logging

from oftest import config
import oftest.base_tests as base_tests
import ofp

from oftest.testutils import *

class MatchTest(base_tests.SimpleDataPlane):
    """
    Base class for match tests
    """

    def verify_match(self, match, matching, nonmatching):
        """
        Verify matching behavior

        Checks that all the packets in 'matching' match 'match', and that
        the packets in 'nonmatching' do not.

        'match' is a LOXI match object. 'matching' and 'nonmatching' are
        dicts mapping from string names (used in log messages) to string
        packet data.
        """
        ports = sorted(config["port_map"].keys())
        in_port = ports[0]
        out_port = ports[1]

        logging.info("Running match test for %s", match.show())

        delete_all_flows(self.controller)

        logging.info("Inserting flow sending matching packets to port %d", out_port)
        request = ofp.message.flow_add(
                table_id=0,
                match=match,
                instructions=[
                    ofp.instruction.apply_actions(
                        actions=[
                            ofp.action.output(
                                port=out_port,
                                max_len=ofp.OFPCML_NO_BUFFER)])],
                buffer_id=ofp.OFP_NO_BUFFER,
                priority=1000)
        self.controller.message_send(request)

        logging.info("Inserting match-all flow sending packets to controller")
        request = ofp.message.flow_add(
            table_id=0,
            instructions=[
                ofp.instruction.apply_actions(
                    actions=[
                        ofp.action.output(
                            port=ofp.OFPP_CONTROLLER,
                            max_len=ofp.OFPCML_NO_BUFFER)])],
            buffer_id=ofp.OFP_NO_BUFFER,
            priority=1)
        self.controller.message_send(request)

        do_barrier(self.controller)

        for name, pkt in matching.items():
            logging.info("Sending matching packet %s, expecting output to port %d", repr(name), out_port)
            pktstr = str(pkt)
            self.dataplane.send(in_port, pktstr)
            receive_pkt_verify(self, [out_port], pktstr, in_port)

        for name, pkt in nonmatching.items():
            logging.info("Sending non-matching packet %s, expecting packet-in", repr(name))
            pktstr = str(pkt)
            self.dataplane.send(in_port, pktstr)
            verify_packet_in(self, pktstr, in_port, ofp.OFPR_ACTION)

class VlanExact(MatchTest):
    """
    Match on VLAN VID and PCP
    """
    def runTest(self):
        match = ofp.match([
            ofp.oxm.vlan_vid(ofp.OFPVID_PRESENT|2),
            ofp.oxm.vlan_pcp(3),
        ])

        matching = {
            "vid=2 pcp=3": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=2, vlan_pcp=3),
        }

        nonmatching = {
            "vid=4 pcp=2": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=4, vlan_pcp=2),
            "vid=4 pcp=3": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=4, vlan_pcp=2),
            "vid=2 pcp=2": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=4, vlan_pcp=2),
            "vid=0 pcp=3": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=4, vlan_pcp=2),
            "vid=2 pcp=0": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=4, vlan_pcp=2),
            "no vlan tag": simple_tcp_packet(),
        }

        self.verify_match(match, matching, nonmatching)

class VlanVID(MatchTest):
    """
    Match on VLAN VID
    """
    def runTest(self):
        match = ofp.match([
            ofp.oxm.vlan_vid(ofp.OFPVID_PRESENT|2),
        ])

        matching = {
            "vid=2 pcp=3": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=2, vlan_pcp=3),
            "vid=2 pcp=7": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=2, vlan_pcp=7),
        }

        nonmatching = {
            "vid=4 pcp=2": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=4, vlan_pcp=2),
            "no vlan tag": simple_tcp_packet(),
        }

        self.verify_match(match, matching, nonmatching)

class VlanVIDMasked(MatchTest):
    """
    Match on VLAN VID (masked)
    """
    def runTest(self):
        match = ofp.match([
            ofp.oxm.vlan_vid_masked(ofp.OFPVID_PRESENT|3, ofp.OFPVID_PRESENT|3),
        ])

        matching = {
            "vid=3 pcp=2": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=3, vlan_pcp=2),
            "vid=7 pcp=2": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=7, vlan_pcp=2),
            "vid=11 pcp=2": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=11, vlan_pcp=2),
        }

        nonmatching = {
            "vid=0 pcp=2": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=0, vlan_pcp=2),
            "vid=1 pcp=2": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=1, vlan_pcp=2),
            "vid=2 pcp=2": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=2, vlan_pcp=2),
            "vid=4 pcp=2": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=4, vlan_pcp=2),
            "no vlan tag": simple_tcp_packet(),
        }

        self.verify_match(match, matching, nonmatching)

class VlanPCP(MatchTest):
    """
    Match on VLAN PCP (VID matched)
    """
    def runTest(self):
        match = ofp.match([
            ofp.oxm.vlan_vid(ofp.OFPVID_PRESENT|2),
            ofp.oxm.vlan_pcp(3),
        ])

        matching = {
            "vid=2 pcp=3": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=2, vlan_pcp=3),
        }

        nonmatching = {
            "vid=2 pcp=4": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=2, vlan_pcp=4),
            "no vlan tag": simple_tcp_packet(),
        }

        self.verify_match(match, matching, nonmatching)

@nonstandard
class VlanPCPMasked(MatchTest):
    """
    Match on VLAN PCP (masked, VID matched)
    """
    def runTest(self):
        match = ofp.match([
            ofp.oxm.vlan_vid(ofp.OFPVID_PRESENT|2),
            ofp.oxm.vlan_pcp_masked(3, 3),
        ])

        matching = {
            "vid=2 pcp=3": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=2, vlan_pcp=3),
            "vid=2 pcp=7": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=2, vlan_pcp=7),
        }

        nonmatching = {
            "vid=2 pcp=1": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=2, vlan_pcp=1),
            "vid=2 pcp=2": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=2, vlan_pcp=2),
            "vid=2 pcp=4": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=2, vlan_pcp=4),
            "vid=2 pcp=5": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=2, vlan_pcp=5),
            "vid=2 pcp=6": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=2, vlan_pcp=6),
            "no vlan tag": simple_tcp_packet(),
        }

        self.verify_match(match, matching, nonmatching)

class VlanPCPAnyVID(MatchTest):
    """
    Match on VLAN PCP (VID present)
    """
    def runTest(self):
        match = ofp.match([
            ofp.oxm.vlan_vid_masked(ofp.OFPVID_PRESENT, ofp.OFPVID_PRESENT),
            ofp.oxm.vlan_pcp(3),
        ])

        matching = {
            "vid=2 pcp=3": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=2, vlan_pcp=3),
            "vid=0 pcp=3": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=0, vlan_pcp=3),
        }

        nonmatching = {
            "vid=2 pcp=4": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=2, vlan_pcp=4),
            "no vlan tag": simple_tcp_packet(),
        }

        self.verify_match(match, matching, nonmatching)

class VlanPresent(MatchTest):
    """
    Match on any VLAN tag (but must be present)
    """
    def runTest(self):
        match = ofp.match([
            ofp.oxm.vlan_vid_masked(ofp.OFPVID_PRESENT, ofp.OFPVID_PRESENT),
        ])

        matching = {
            "vid=2 pcp=3": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=2, vlan_pcp=3),
            "vid=0 pcp=7": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=0, vlan_pcp=7),
            "vid=2 pcp=0": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=2, vlan_pcp=0),
        }

        nonmatching = {
            "no vlan tag": simple_tcp_packet()
        }

        self.verify_match(match, matching, nonmatching)

class VlanAbsent(MatchTest):
    """
    Match on absent VLAN tag
    """
    def runTest(self):
        match = ofp.match([
            ofp.oxm.vlan_vid(ofp.OFPVID_NONE),
        ])

        matching = {
            "no vlan tag": simple_tcp_packet()
        }

        nonmatching = {
            "vid=2 pcp=3": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=2, vlan_pcp=3),
            "vid=0 pcp=7": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=0, vlan_pcp=7),
            "vid=2 pcp=0": simple_tcp_packet(dl_vlan_enable=True, vlan_vid=2, vlan_pcp=0),
        }

        self.verify_match(match, matching, nonmatching)
