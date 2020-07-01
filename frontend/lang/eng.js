export default (context) => {
  const locale = {
    welcome: 'Welcome'
  }

  return new Promise(function (resolve) {
    resolve(locale)
  });
}
