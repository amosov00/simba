import {PORT, SENTRY_DSN, COMMIT} from "./config";

const Sentry = require('@sentry/node');
const express = require('express');

const multisigController = require("./controllers/api/multisig")

const app = express();

Sentry.init({dsn: SENTRY_DSN, release: COMMIT});

app.set('port', PORT);

app.use(Sentry.Handlers.requestHandler());
app.use(Sentry.Handlers.errorHandler());
app.use(express.json());


app.post("/api/multisig", multisigController.postMultisig)


app.listen(app.get('port'), () => {
  console.log(' App is running at http://localhost:%d in %s mode', app.get('port'), app.get('env'));
  console.log(' Press CTRL-C to stop\n');
});

module.exports = app;