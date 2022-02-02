#! /usr/bin/python3
from pyln.client import Plugin
import runes

plugin = Plugin()
def getChannel(peerid, chanid):
    peer = plugin.rpc.listpeers(peerid)
    assert peer, "cannot find peer"

    chan = peer["channels"]
    assert chan["channel_id"]==chanid, "cannot find channel"

    return {peer, chan}

@plugin.method("spark-listpays")
def spark_listpays():
    plugin.log("listpeers")
    return plugin.rpc.listpeers()

@plugin.method("spark-listpeers")
def spark_listpeers():
    """
    If this returns (a dict), that's the JSON "result" returned.  If
    it raises an exception, that causes a JSON "error" return (raising
    pyln.client.RpcException allows finer control over the return).
    """
    plugin.log("listpeers")
    return plugin.rpc.listpeers()

@plugin.method("spark-getinfo")
def spark_getinfo():
    plugin.log("getinfo")
    return plugin.rpc.getinfo()

@plugin.method("spark-offer")
def spark_offer(amount, discription):
    plugin.log("offer")
    return plugin.rpc.offer(amount, discription)

@plugin.method("spark-listfunds")
def spark_listfunds():
    plugin.log("listfunds")
    return plugin.rpc.listfunds()

@plugin.method("spark-invoice")
def spark_invoice(amt, label, disc):
    plugin.log("invoice")
    return plugin.rpc.invoice(amt, label, disc)

@plugin.method("spark-newaddr")
def spark_invoice():
    plugin.log("newaddr")
    return plugin.rpc.newaddr()

@plugin.method("spark-getlog")
def spark_invoice():
    plugin.log("getlog")
    return plugin.rpc.getlog()

@plugin.method("spark-listconfigs")
def spark_listconfigs():
    plugin.log("listconfigs")
    return plugin.rpc.listconfigs()

@plugin.method("spark-listinvoices")
def spark_listconfigs():
    plugin.log("listinvoices")
    temp = plugin.rpc.listinvoices()["invoices"]
    res = []
    for i in temp:
        if i["status"]=="paid":
            res.append(i)
    return res


@plugin.method("spark-decodecheck")
def spark_decodecheck(paystr):
    plugin.log("decodecheck")
    s = plugin.rpc.decode(paystr)
    if(s["type"]=="bolt12 offer"):
        assert "recurrence" in s.keys(), "Offers with recurrence are unsupported"
        assert s["quantity_min"] == None or s["msatoshi"] or s["amount"], 'Offers with quantity but no payment amount are unsupported'
        assert not s["send_invoice"] or s["msatoshi"], "send_invoice offers with no amount are unsupported"
        assert not s["send_invoice"] or s["min_quantity"] == None, 'send_invoice offers with quantity are unsupported'
    return s

@plugin.method("spark-connectfund")
def spark_connectfund(peeruri, satoshi, feerate):
        peerid = peeruri.split('@')[0]
        plugin.rpc.connect(peerid)
        res = plugin.rpc.fundchannel(peerid, satoshi, feerate)
        assert (res and res["channel_id"]), "cannot open channel"
        return getChannel(peerid, res["channel_id"])

plugin.method("spark-close")
def spark_close(peerid, chainid, force, timeout):
        res = plugin.rpc.close(peerid, timeout)
        assert res and res["txid"], "Cannot close channel"

        peer,chan = getChannel(peerid, res["channel_id"])
        return {peer, chan, res}

@plugin.init()
def init(options, configuration, plugin):
    plugin.log("Plugin helloworld.py initialized")
    # This can also return {'disabled': <reason>} to self-disable,
	# but normally it returns None.

plugin.run()