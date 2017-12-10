var express = require("express")
app = express();
app.get('/', function (req, res) {
  return res.send("hello")
})
app.listen(80);
console.log("web app is listen on port 80")