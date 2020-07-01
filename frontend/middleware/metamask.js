export default function() {
  if (window.ethereum !== undefined) {
    window.ethereum.enable();
  }
}
