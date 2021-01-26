const bitcore = require('bitcore-lib')

function throwError(msg) {
  throw new Error(msg)
}

async function createTransaction(privKey, pubKey, spendables, payables, fee, isTestnet) {
    Array.isArray(spendables) || throwError("Invalid spendables format")
    Array.isArray(payables) || throwError("Invalid payables format")
    bitcore.PrivateKey.isValid(privKey) || throwError("Invalid private key")
    bitcore.PublicKey.isValid(pubKey) || throwError("Invalid public key")

    let network = isTestnet === true ? bitcore.Networks.testnet : bitcore.Networks.livenet

    const cosig1Priv = new bitcore.PrivateKey(privKey, network)
    const cosig2Pub = new bitcore.PublicKey(pubKey, {network: network})
    const pubKeys = [cosig1Priv.publicKey, cosig2Pub]
    const threshold = 2
    const address = new bitcore.Address(pubKeys, threshold);

    let utxos = spendables.map(i => {
        return {
            txId: i.tx_hash_hex,
            outputIndex: i.tx_out_index,
            address: address.toString(),
            script: i.script_hex,
            satoshis: i.coin_value,
        }
    })
    let transaction = new bitcore.Transaction(null)
        .from(utxos, pubKeys, threshold)
        .to(payables[0][0], payables[0][1])
        .change(address.toString())
        .fee(fee)
        .sign(cosig1Priv, 1)

    return {
        rawTransactionData: JSON.stringify(transaction),
        rawSignatureData: JSON.stringify(transaction.getSignatures(cosig1Priv)),
    }
}

exports.postMultisig = async (req, res, next) => {
  let {cosig1Priv, cosig2Pub, spendables, payables, fee, testnet} = req.body
  if (!cosig1Priv || !cosig2Pub || !spendables || !payables || !fee || !testnet) {
    return res.status(400).send({"success": false})
  }
  createTransaction(cosig1Priv, cosig2Pub, spendables, payables, fee, testnet)
      .then(data => res.send(data))
      .catch(() => res.status(500).send({"success": false}))
}
