const parser = require("@asyncapi/parser");
var fs = require("fs");
var path = require("path");
var Ajv = require("ajv");
var betterAjvErrors = require("better-ajv-errors");
var os = require("os");

var BUFFER = bufferFile("./json/asyncapi.json");
var json_data = BUFFER.toString();
var json_lines = json_data.split(os.EOL);
var json_obj = require("./json/asyncapi.json")

var hasExcape = /~/;
var escapeMatcher = /~[01]/g;

function escapeReplacer(m) {
  switch (m) {
    case "~1":
      return "/";
    case "~0":
      return "~";
  }
  throw new Error("Invalid tilde escape: " + m);
}

function untilde(str) {
  if (!hasExcape.test(str)) return str;
  return str.replace(escapeMatcher, escapeReplacer);
}
function bufferFile(relPath) {
  return fs.readFileSync(path.join(__dirname, relPath));
}

function compilePointer(pointer) {
  if (typeof pointer === "string") {
    pointer = pointer.split("/");
    if (pointer[0] === "") return pointer;
    throw new Error("Invalid JSON pointer.");
  } else if (Array.isArray(pointer)) {
    return pointer;
  }

  throw new Error("Invalid JSON pointer.");
}

function get(obj, pointer) {
  if (typeof obj !== "object") throw new Error("Invalid input object.");
  pointer = compilePointer(pointer);
  var len = pointer.length;
  if (len === 1) return obj;

  for (var p = 1; p < len; ) {
    key = untilde(pointer[p++]);
    console.log(key);
    obj = obj[key];
    //console.log(JSON.stringify(obj));
    if (len === p) return obj;
    if (typeof obj !== "object")
      return " Err @ " + key + ":" + typeof obj + ":" + JSON.stringify(obj);
  }
}

const doc = parser.parse(json_data).catch((ex) => {
  //console.log( ex.toJS() );
  //console.log( JSON.stringify( ex.validationErrors, null, 2 ) );

  ex.validationErrors.forEach(function (err) {
    console.log("Error : ", err.title);
    console.log("  Loc : ", err.location.jsonPointer);
    //console.log("  Val : ", get(json_obj, "/channels"));
    console.log("  Val : ", get(json_obj, err.location.jsonPointer));
    //console.log( err );
  });
  process.exit(1);
});
