export const InvoiceStatus = {
  CREATED: "created",
  WAITING: "waiting",  // Waiting transaction from user
  PROCESSING: "processing",  // Waiting to generate SIMBA or send BTC
  PAID: "paid",  // Paid but waiting for tx confirmation
  COMPLETED: "completed",  // success end
  CANCELLED: "cancelled",  // invoice closed
  SUSPENDED: "suspended",  // KYC and verification issues
}

export const InvoiceType = {
  BUY: 1,
  SELL: 2,
}


export const statusToColor = (status) => {
  switch (status) {
    case InvoiceStatus.CREATED:
      return '#0065a9'
    case InvoiceStatus.WAITING:
    case InvoiceStatus.PROCESSING:
    case InvoiceStatus.PAID:
      return '#e2a500'
    case InvoiceStatus.COMPLETED:
      return '#00a90c'
    case InvoiceStatus.SUSPENDED:
      return '#b51100'
    case InvoiceStatus.CANCELLED:
    default:
      return '#000000'
  }
}
