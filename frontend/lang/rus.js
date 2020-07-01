export default (context) => {
  const locale = {
    welcome: 'Добро пожаловать'
  }

  return new Promise(function (resolve) {
    resolve(locale)
  });
}
