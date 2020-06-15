const parser = require( '@asyncapi/parser' );
var fs = require( 'fs' );
var path = require( 'path' );
var Ajv = require( 'ajv' );
var betterAjvErrors = require( 'better-ajv-errors' );
var os = require( 'os' );


var BUFFER = bufferFile( './json/asyncapi.json' );
var json_data = BUFFER.toString()
var json_lines = json_data.split( os.EOL );

function bufferFile( relPath ) {
    return fs.readFileSync( path.join( __dirname, relPath ) );
}

const doc = parser.parse( json_data ).catch( ( ex ) => {
    // console.log( ex.toJS() );
    // console.log( JSON.stringify( ex.validationErrors, null, 2 ) );

    var err = ex.validationErrors[ 0 ]
    var start = err.location.startLine - 1
    var end = err.location.endLine - 1
    var x1 = err.location.startColumn
    var x2 = err.location.endColumn

    console.log( "Error : ", err.title )
    console.log( "  Line: ", start + 1, "to", end + 1 )
    console.log( "-".repeat( 79 ) )


    for ( var line = 0; line < json_lines.length; line++ ) {
        if ( ( line >= start - 5 ) && ( line <= start + 5 ) ) {
            if ( ( line >= start ) && ( line <= start ) ) {
                console.log( line, "-->" + json_lines[ line ] );
                console.log( line, "   ", " ".repeat( x1 - 1 ), "^".repeat( x2 - x1 ) );
            } else {
                console.log( line, "   " + json_lines[ line ] );
            }
        }
    }
    process.exit( 1 )
} );
