const Sentry = require('@sentry/node');
const express = require('express');

const multisigController = require("./controllers/api/multisig")

const app = express();

Sentry.init({dsn: process.env.SENTRY_DSN_NODEJS, release: process.env.COMMIT});

app.set('port', process.env.PORT || 8080);

app.use(Sentry.Handlers.requestHandler());
app.use(Sentry.Handlers.errorHandler());
app.use(express.json());


app.post("/api/multisig", multisigController.postMultisig)


app.listen(app.get('port'), () => {
  console.log(' App is running at http://localhost:%d in %s mode', app.get('port'), app.get('env'));
  console.log(' Press CTRL-C to stop\n');
});

module.exports = app;