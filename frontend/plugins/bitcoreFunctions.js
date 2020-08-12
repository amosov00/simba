import * as bitcore from "bitcore-lib"


function throwError(msg) {
  throw new Error(msg)
}


function createTransaction(privKey, pubKey, spendables, payables, fee) {
  Array.isArray(spendables) || throwError("Invalid spendables format")
  Array.isArray(payables) || throwError("Invalid payables format")
  bitcore.PrivateKey.isValid(privKey) || throwError("Invalid private key")
  bitcore.PublicKey.isValid(pubKey) || throwError("Invalid public key")

  const cosig1Priv = new bitcore.PrivateKey(privKey)
  const cosig2Pub = new bitcore.PublicKey(pubKey, {network: bitcore.Networks.testnet})
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

  let transaction = new bitcore.Transaction()
    .from(utxos, pubKeys, threshold)
    .change(address.toString())
    .fee(fee)
    .sign(cosig1Priv)

  payables.map(i => {
    let [address, amount] = i
    transaction.to(address, amount)
  })

  return {
    rawTransactionData: JSON.stringify(transaction),
    rawSignatureData: JSON.stringify(transaction.getSignatures(cosig1Priv)),
  }
}

export {createTransaction}
