export const statusToColor = (status) => {
    switch (status) {
        case "created":
            return "#0065a9"
        case "waiting":
        case "processing":
        case "paid":
            return "#e2a500"
        case "completed":
            return "#00a90c"
        case "cancelled":
            return "#b51100"
        default:
            return "#000000"
    }
}
