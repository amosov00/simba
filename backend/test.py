# import blockcypher
# from pprint import pp
#
# from pywallet import wallet
#
# API_KEY = "5aa6c893b8714281ba720891eaea1c57"
# PUB_KEY = "047b2f4756b620153120f47b8c630000e76a1ab99f8258b18e44947b8ed0d0dafdc2b202a41657c82e564980bbdefe180e8253b06d9821abf0c1cd56595a59d8c6"
# PRIV_KEY = "1395c31d2f947982d4cfb10c214b1ecc567730e96b0709abf361bf7268366df7"

# a1 = blockcypher.get_wallet_addresses(
#     "test1",
#     API_KEY,
#     True,
#     coin_symbol="btc-testnet"
# )
# pp(a1)

# a1 = blockcypher.simple_spend(
#     from_privkey=PRIV_KEY,
#     to_address="mgcEs8CPgX1uJjjyLRbv4vLVuabevKe9LE",
#     to_satoshis=110000000,
#     api_key=API_KEY,
#     coin_symbol="btc-testnet",
# )
# a1 = blockcypher.simple_spend_p2sh()
# pp(a1)
#
# sigh_trans = blockcypher.make_tx_signatures(
#     ["0c6254e52d19ad8f59eb740d4359aae3ea1f0cf25864d3b16b4484656e94bd06", "21615004adb74df83171a4179f2a6b3120e0d7d58198b927f5a66c1e117eb173"],
#     ["1395c31d2f947982d4cfb10c214b1ecc567730e96b0709abf361bf7268366df7", "1395c31d2f947982d4cfb10c214b1ecc567730e96b0709abf361bf7268366df7"],
#     ["047b2f4756b620153120f47b8c630000e76a1ab99f8258b18e44947b8ed0d0dafdc2b202a41657c82e564980bbdefe180e8253b06d9821abf0c1cd56595a59d8c6", "047b2f4756b620153120f47b8c630000e76a1ab99f8258b18e44947b8ed0d0dafdc2b202a41657c82e564980bbdefe180e8253b06d9821abf0c1cd56595a59d8c6"]
# )
#
#
# pp(sigh_trans)

